from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from transformers import pipeline
import json

# Kết nối MongoDB
client = MongoClient("mongodb+srv://ngogiaquyendhtn223:qz5rZCHVYNjookUm@chat.ycokswf.mongodb.net/")
db = client["chat_message"]
collection = db["faq"]  # Chúng ta giả định rằng câu hỏi và câu trả lời được lưu trong collection "faq"

# Load mô hình Transformers
chatbot = pipeline("text-generation", model="distilgpt2")

def get_faq_from_db():
    # Truy vấn từ MongoDB để lấy danh sách câu hỏi và câu trả lời
    faq_data = collection.find()  # Giả định rằng mỗi tài liệu chứa 'question' và 'answer'
    faq = {}
    for item in faq_data:
        faq[item['question']] = item['answer']
    return faq

@csrf_exempt
def chat_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_msg = data.get("message", "")

        # Lấy bộ câu hỏi và câu trả lời từ MongoDB
        FAQ = get_faq_from_db()

        # Kiểm tra câu hỏi có trong bộ câu hỏi phổ biến không
        reply = "Sory i can't reply this question"
        if user_msg in FAQ:
            reply = FAQ[user_msg]
        # else:
        #     # Dự đoán phản hồi từ mô hình GPT-2 nếu câu hỏi không có trong FAQ
        #     reply = chatbot(user_msg, max_length=50, do_sample=True)[0]["generated_text"]

        # Lưu vào MongoDB
        collection = db["chat_message"]
        collection.insert_one({
            "user": user_msg,
            "bot": reply
        })

        return JsonResponse({"reply": reply})
    else:
        return JsonResponse({"error": "Invalid method"}, status=405)
