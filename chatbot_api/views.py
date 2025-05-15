from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import find_best_answer

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_question = data.get("message", "")

        answer_data = find_best_answer(user_question)

        return JsonResponse(answer_data)
