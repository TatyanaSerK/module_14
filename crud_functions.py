
# initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
# Эта таблица должна содержать следующие поля:
# id - целое число, первичный ключ
# title(название продукта) - текст (не пустой)
# description(описание) - тест
# price(цена) - целое число (не пустой)


import sqlite3

def initiate_db():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INTEGER NOT NULL
    )
    ''')
    # for i in range (1,5): #
    #     cursor.execute("INSERT INTO Products (title, description, price) VALUES (?,?,?)",
    #                    (f"Продукт{i}", f"описание {i}", f"{100*i}"))
    connection.commit()
    connection.close()

# get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.
def get_all_products():
    connection = sqlite3.connect("Products.db")
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM Products ")
    products = cursor.fetchall()
    return products
