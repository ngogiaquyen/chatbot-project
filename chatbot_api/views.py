from chatterbot import ChatBot
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
import pymysql

def test_sql():
    try:
        conn = pymysql.connect(
            host='103.97.126.29',
            user='ukeptbsx_chat_bot',
            password='UkzkUpjzThj4cL4mS22V',
            database='ukeptbsx_chat_bot',
            port=3306,
            connect_timeout=5,
        )

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM statement LIMIT 1;")
            row = cursor.fetchone()
            print(row)

    except Exception as e:
        print("Lỗi khi kết nối hoặc truy vấn:", e)

    finally:
        if conn:
            conn.close()

test_sql()

chatbot = None

@csrf_exempt
def chatbot_api(request):
    global chatbot
    if chatbot is None:
        chatbot = ChatBot(
            "BotVN",
            logic_adapters=["chatterbot.logic.BestMatch"],
            read_only=True,
            database_uri="mysql+pymysql://ukeptbsx_chat_bot:UkzkUpjzThj4cL4mS22V@103.97.126.29:3306/ukeptbsx_chat_bot?charset=utf8mb4"
        )

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            if user_message:
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
