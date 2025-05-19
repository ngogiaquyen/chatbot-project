from django.db import models
from pymongo import MongoClient

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Create your models here.

# Kết nối MongoDB
client = MongoClient("mongodb+srv://ngogiaquyendhtn223:qz5rZCHVYNjookUm@chat.ycokswf.mongodb.net/")
db = client["chat_message"]
qa_collection = db["faq"]

def find_best_answer(user_question):
    qa_pairs = list(qa_collection.find({}, {"_id": 0}))  # lấy hết
    questions = [q["question"] for q in qa_pairs]

    vectorizer = TfidfVectorizer().fit_transform(questions + [user_question])
    vectors = vectorizer.toarray()

    cosine_similarities = cosine_similarity([vectors[-1]], vectors[:-1])
    best_match_index = np.argmax(cosine_similarities)

    if cosine_similarities[0][best_match_index] > 0.5:  # ngưỡng tin cậy
        return qa_pairs[best_match_index]
    else:
        return {"answer": "Hệ thống chưa thể phản hồi tự động tin nhắn này. NGQ sẽ sớm liên hệ lại với bạn. Bạn có thể để lại địa chỉ Gmail để tiện liên lạc.", "related_articles": []}

