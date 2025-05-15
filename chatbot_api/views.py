from chatterbot import ChatBot
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

# Tạo chatbot - KHÔNG train, chỉ sử dụng dữ liệu đã có
chatbot = ChatBot(
    "BotVN",
    logic_adapters=["chatterbot.logic.BestMatch"],
    read_only=True,  # RẤT QUAN TRỌNG: Ngăn không cho tự học lại
    database_uri="mysql+pymysql://ukeptbsx_chat_bot:UkzkUpjzThj4cL4mS22V@103.97.126.29:3306/ukeptbsx_chat_bot?charset=utf8mb4"
)

# Xử lý API
@csrf_exempt
def chatbot_api(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            if user_message:
                # Lấy phản hồi từ chatbot
                bot_response = chatbot.get_response(user_message)
                return JsonResponse({'response': str(bot_response)})
            else:
                return JsonResponse({'error': 'No message provided'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format'}, status=400)

@csrf_exempt
def test_api(request):
    if request.method == 'GET':
        return JsonResponse({'success': 'get thanh cong'}, status=200)
