from sqlalchemy import create_engine, text
engine = create_engine("mysql+pymysql://ukeptbsx_chat_bot:UkzkUpjzThj4cL4mS22V@103.97.126.29:3306/ukeptbsx_chat_bot?charset=utf8mb4")

with engine.connect() as conn:
    result = conn.execute(text("SELECT * FROM statement LIMIT 1;"))
    row = result.fetchone()
    print(row)