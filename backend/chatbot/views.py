import json

from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, get_object_or_404
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChatThread, ChatMessage, UserPreference, BusinessProfile, BusinessGoal, BusinessDocument
from .serializers import (
    ChatMessageSerializer,
    ChatThreadSerializer,
    UserPreferenceSerializer,
    BusinessProfileSerializer,
    BusinessGoalSerializer,
    BusinessDocumentSerializer,
)
from .utils.agent import default_agent

def home_view(request):
    """
    Serves the main professional chat interface.
    """
    return render(request, "index.html")

@csrf_exempt
def chat_stream_view(request):
    """
    Streaming chat endpoint for Msoko AI (SSE) with persistent threading.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Only POST allowed"}, status=405)

    try:
        data = json.loads(request.body)
        user_input = data.get("message", "").strip()
        thread_id = data.get("thread_id")
        image_data = data.get("image") # Base64 data:image/...;base64,...
        
        # Determine current thread
        thread = None
        history = []
        if thread_id:
            try:
                thread = ChatThread.objects.get(id=thread_id)
                past_msgs = thread.messages.all().order_by('-created_at')[:10]
                for m in reversed(past_msgs):
                    history.append({"role": "user" if m.role == "user" else "assistant", "content": m.content})
            except ChatThread.DoesNotExist:
                pass
        
        if not thread:
            thread = ChatThread.objects.create(title=user_input[:50] or "Product Analysis")

        # Save user message
        ChatMessage.objects.create(thread=thread, role="user", content=user_input, media_url=image_data or "")
        
        def event_stream():
            full_reply = []
            yield f"data: {json.dumps({'thread_id': thread.id})}\n\n"
            
            context = {"user_id": request.user.id, "user_name": request.user.username} if request.user.is_authenticated else {}
            if image_data: context["is_multimodal"] = True
            
            uid = request.user.id if request.user.is_authenticated else None
            for chunk in get_msoko_streaming_response(user_input, history=history, user_id=uid, image_data=image_data, context=context):
                full_reply.append(chunk)
                yield f"data: {json.dumps({'text': chunk})}\n\n"
            
            # Save AI message after streaming finished
            if full_reply:
                ChatMessage.objects.create(thread=thread, role="ai", content="".join(full_reply))
                thread.save() # Update updated_at
                
            yield "data: [DONE]\n\n"

        return StreamingHttpResponse(event_stream(), content_type="text/event-stream")

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
from .serializers import (
    ChatMessageSerializer,
    ChatThreadSerializer,
    UserPreferenceSerializer,
    BusinessProfileSerializer,
    BusinessGoalSerializer,
    BusinessDocumentSerializer,
)
from .utils.agent import get_msoko_response, get_msoko_streaming_response


@csrf_exempt
@require_http_methods(["GET", "POST"])
def chat_view(request):
    """
    Legacy chat endpoint for Msoko AI (single-shot, no threading).
    GET: readiness message
    POST: user message -> AI response
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "").strip()

            if not user_input:
                return JsonResponse({"error": "No message provided"}, status=400)

            # Limit message length to prevent abuse
            if len(user_input) > 2000:
                return JsonResponse(
                    {"error": "Message too long. Maximum 2000 characters."}, status=400
                )

            uid = request.user.id if request.user.is_authenticated else None
            ai_reply = get_msoko_response(user_input, user_id=uid)
            return JsonResponse({"response": ai_reply})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
        except Exception as e:  # pragma: no cover - fallback
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Msoko AI is ready.", "status": "online"})


class ThreadListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.query_params.get("q")
        threads = ChatThread.objects.filter(user=request.user)
        if query:
            threads = threads.filter(title__icontains=query)
        threads = threads.order_by("-updated_at")
        serializer = ChatThreadSerializer(threads, many=True)
        return Response(serializer.data)

    def post(self, request):
        title = request.data.get("title") or "New chat"
        user = request.user if request.user.is_authenticated else None
        thread = ChatThread.objects.create(user=user, title=title)
        serializer = ChatThreadSerializer(thread)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ThreadDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, thread_id):
        thread = get_object_or_4_0_4(ChatThread, id=thread_id, user=request.user)
        title = request.data.get("title")
        if title:
            thread.title = title[:255]
            thread.save(update_fields=["title", "updated_at"])
        serializer = ChatThreadSerializer(thread)
        return Response(serializer.data)

    def delete(self, request, thread_id):
        try:
            thread = ChatThread.objects.get(id=thread_id, user=request.user)
        except ChatThread.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        thread.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MessageListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, thread_id):
        try:
            if request.user.is_authenticated:
                thread = ChatThread.objects.get(id=thread_id, user=request.user)
            else:
                thread = ChatThread.objects.get(id=thread_id)
        except ChatThread.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        messages = thread.messages.all()
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)

    def post(self, request, thread_id):
        try:
            thread = ChatThread.objects.get(id=thread_id, user=request.user)
        except ChatThread.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        content = (request.data.get("message") or "").strip()
        if not content:
            return Response({"error": "No message provided"}, status=400)
        if len(content) > 2000:
            return Response(
                {"error": "Message too long. Maximum 2000 characters."}, status=400
            )

        # Store user message
        user_msg = ChatMessage.objects.create(
            thread=thread, role="user", content=content
        )

        # Get AI reply
        ai_reply = get_msoko_response(content, user_id=request.user.id)
        ai_msg = ChatMessage.objects.create(
            thread=thread, role="ai", content=ai_reply or ""
        )

        thread.save(update_fields=["updated_at"])

        return Response(
            {
                "user": ChatMessageSerializer(user_msg).data,
                "ai": ChatMessageSerializer(ai_msg).data,
            },
            status=status.HTTP_201_CREATED,
        )


class PreferenceView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        prefs, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(prefs)
        return Response(serializer.data)

    def patch(self, request):
        prefs, _ = UserPreference.objects.get_or_create(user=request.user)
        serializer = UserPreferenceSerializer(prefs, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        first_name = request.data.get("first_name", "").strip()
        last_name = request.data.get("last_name", "").strip()
        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not email or not password or not first_name:
            return Response({"error": "Missing required fields (First Name, Email, Password)"}, status=status.HTTP_400_BAD_REQUEST)

        if password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({"error": "Password must be at least 8 characters"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=email).exists() or User.objects.filter(email=email).exists():
            return Response({"error": "A user with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        # Use email as username for industrial standard consistency
        user = User.objects.create_user(
            username=email, 
            email=email, 
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        # Create initial profile with name
        BusinessProfile.objects.create(user=user, business_name=f"{first_name}'s Venture")
        
        login(request, user)
        return Response({
            "message": "Account created successfully", 
            "user": {
                "first_name": user.first_name,
                "email": user.email
            }
        })


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        password = request.data.get("password")
        
        # Authenticate using email as username
        user = authenticate(username=email, password=password)
        if user:
            login(request, user)
            return Response({
                "message": "Logged in", 
                "user": {
                    "first_name": user.first_name,
                    "email": user.email
                }
            })
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logged out"})


class SessionView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                "authenticated": True, 
                "user": {
                    "first_name": request.user.first_name,
                    "email": request.user.email
                }
            })
        return Response({"authenticated": False})


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email", "").strip().lower()
        if not email:
            return Response({"error": "Email is required"}, status=400)
        
        # Simulating email sending for industrial demo
        user_exists = User.objects.filter(email=email).exists()
        return Response({
            "message": "If an account exists with this email, you will receive a reset link shortly."
        })


class BusinessProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile, _ = BusinessProfile.objects.get_or_create(user=request.user)
        serializer = BusinessProfileSerializer(profile)
        return Response(serializer.data)

    def patch(self, request):
        profile, _ = BusinessProfile.objects.get_or_create(user=request.user)
        serializer = BusinessProfileSerializer(profile, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        threads_count = ChatThread.objects.filter(user=user).count()
        messages_count = ChatMessage.objects.filter(thread__user=user).count()
        
        profile, _ = BusinessProfile.objects.get_or_create(user=user)
        goals = BusinessGoal.objects.filter(user=user, is_completed=False)
        
        goal_data = []
        for g in goals:
            progress = (g.current_value / g.target_value * 100) if g.target_value > 0 else 0
            goal_data.append({
                "title": g.title,
                "progress": round(min(progress, 100), 1)
            })

        data = {
            "business_name": profile.business_name or "My Business",
            "stats": {
                "consultations": threads_count,
                "total_messages": messages_count,
                "revenue_target": profile.monthly_revenue_target,
            },
            "goals": goal_data,
            "recent_insights": [
                f"Msoko AI Suggests: You have {len(goals)} active goals. Keep pushing!",
                "Trending: Demand for specialized digital skills is rising globally.",
                "Strategy: Position your skills as solutions, not just services."
            ]
        }
        return Response(data)


class GoalListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        goals = BusinessGoal.objects.filter(user=request.user)
        serializer = BusinessGoalSerializer(goals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BusinessGoalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MemoryClearView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # GDPR-style privacy control: Delete profile and goals
        BusinessProfile.objects.filter(user=request.user).delete()
        BusinessGoal.objects.filter(user=request.user).delete()
        BusinessDocument.objects.filter(user=request.user).delete()
        return Response({"message": "Memory cleared successfully."})


from rest_framework.parsers import MultiPartParser, FormParser

class DocumentListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        docs = BusinessDocument.objects.filter(user=request.user)
        serializer = BusinessDocumentSerializer(docs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BusinessDocumentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        # TODO: Trigger AI analysis of the document content
        return Response(serializer.data, status=status.HTTP_201_CREATED)
