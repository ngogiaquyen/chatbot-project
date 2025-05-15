from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import find_best_answer

@csrf_exempt
def chatbot_api(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print(data)
        user_question = data.get("content", "")
        answer_data = data
        answer_data["content"] = find_best_answer(user_question)["answer"]

        # Hoán đổi sender và receiver ID nếu cần
        receiver_id = data.get("receiver_id")
        sender_id = data.get("sender_id")

        # Bạn có thể thêm vào answer_data nếu muốn phản hồi cả sender/receiver
        answer_data["receiver_id"] = sender_id
        answer_data["sender_id"] = receiver_id

        print(answer_data)
        return JsonResponse(answer_data)
