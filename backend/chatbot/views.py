from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .utils.prompt_loader import get_msoko_response

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        user_input = request.POST.get("message", "").strip()
        if not user_input:
            return JsonResponse({"error": "No message provided"}, status=400)

        ai_reply = get_msoko_response(user_input)
        return JsonResponse({"response": ai_reply})

    return JsonResponse({"message": "Msoko AI is ready."})
