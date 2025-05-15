import pymysql

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
