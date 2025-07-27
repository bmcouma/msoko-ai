from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .utils.prompt_loader import get_msoko_response

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_input = data.get("message", "").strip()

            if not user_input:
                return JsonResponse({"error": "No message provided"}, status=400)

            ai_reply = get_msoko_response(user_input)
            return JsonResponse({"response": ai_reply})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"message": "Msoko AI is ready."})
