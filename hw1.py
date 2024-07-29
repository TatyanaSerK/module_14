import sqlite3

connection = sqlite3.connect("not_telegram.db")
cursor = connection.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

cursor.execute("CREATE INDEX IF NOT EXISTS idx_email ON Users (email)")
#Заполните её 10 записями User1, example1@gmail.com, 10, 1000
for i in range (1,11): #
    cursor.execute("INSERT INTO Users (username, email, age, balance) VALUES (?,?,?,?)",
                   (f"User{i}", f"example{i}@gmail.com", f"{10*i}", "1000"))



# Обновите balance у каждой 2ой записи начиная с 1ой на 500:
for i in range(1,11):
    if i % 2 != 0:
        cursor.execute("UPDATE Users SET balance = ? WHERE id = ?",
                       ('500', f"{i}"))

#Удалите каждую 3ую запись в таблице начиная с 1ой:
i=1
while i<11:
    cursor.execute("DELETE FROM Users WHERE id = ?", (f'{i}',))
    i += 3

# Сделайте выборку всех записей,где возраст не равен 60 и выведите их в консоль:
# Имя: <username> | Почта: <email> | Возраст: <age> | Баланс: <balance>
cursor.execute("SELECT username, email, age, balance FROM Users WHERE age != 60  ")
users = cursor.fetchall()
for user in users:
    print(f'Имя: {user[0]} | Почта: {user[1]} | Возраст: {user[2]} | Баланс: {user[3]}')

connection.commit()
connection.close()

