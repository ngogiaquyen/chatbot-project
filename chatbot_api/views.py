from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pymongo import MongoClient

# Tạo chatbot

chatbot = ChatBot(
    "BotVN",
    logic_adapters=["chatterbot.logic.BestMatch"],
    database_uri="mysql+pymysql://ukeptbsx_chat_bot:UkzkUpjzThj4cL4mS22V@103.97.126.29:3306/ukeptbsx_chat_bot?charset=utf8mb4"
)

trainer = ListTrainer(chatbot)

# Kết nối MongoDB
client = MongoClient("mongodb+srv://ngogiaquyendhtn223:qz5rZCHVYNjookUm@chat.ycokswf.mongodb.net/")
db = client["chat_message"]
collection = db["faq"]

# Truy xuất dữ liệu và huấn luyện
def train_from_db():
    faq_data = collection.find()
    for item in faq_data:
        question = item.get('question')
        answer = item.get('answer')
        if question and answer:
            trainer.train([question.strip(), answer.strip()])
            collection.update_one({"_id": item["_id"]}, {"$set": {"trained": True}})

# Gọi huấn luyện (chỉ cần gọi một lần khi ứng dụng bắt đầu)
train_from_db()

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
