import sqlite3
connect = sqlite3.connect('database2.db', check_same_thread=False)
cursor = connect.cursor()
users = cursor.execute('CREATE TABLE IF NOT EXISTS "users"("id" Integer NOT NULL, "login" TEXT NOT NULL, primary key("id" AUTOINCREMENT));')
categories = cursor.execute('CREATE TABLE IF NOT EXISTS "categories"("id" Integer NOT NULL, "name" TEXT NOT NULL, primary key("id" AUTOINCREMENT));')
sub = cursor.execute('CREATE TABLE IF NOT EXISTS "subscrabies" ("id_user" Integer NOT NULL, "id_categories" Integer NOT NULL, FOREIGN KEY("id_user") REFERENCES "users" ("id"), FOREIGN KEY("id_categories") REFERENCES "categories" ("id"));')
connect.commit()
# регистрация пользователя
def registr(login, connect):
    cursor = connect.cursor()
    return cursor.execute('INSERT INTO users (login) VALUES (?);', (login,))
# авторизация пользователя
def auto(login, connect):
    cursor = connect.cursor()
    return cursor.execute('SELECT * FROM "users" WHERE login = ? ', (login, )).fetchone()
#добавление категории
def addcategory(name, connect):
    cursor = connect.cursor()
    return cursor.execute('INSERT INTO categories (name) VALUES (?);', (name,))
# удаление категории
def delit(name, connect):
    cursor = connect.cursor()
    return cursor.execute('DELETE FROM "categories" WHERE name = ?', (name, ))
#отписка
def unsubcat(user, category, connect):
    cursor = connect.cursor()
    return cursor.execute('DELETE FROM "subscrabies" WHERE id_user = ? AND id_categories = ?', (user, category))
#подписка
def subcat(user, category, connect):
    cursor = connect.cursor()
    print(222222)
    return cursor.execute('INSERT INTO "subscrabies" (id_user, id_categories) VALUES (?, ?);', (user, category))
# посмотреть подписки
def seecub(user, connect):
    cursor = connect.cursor()
    return cursor.execute('SELECT subscrabies.id_categories, categories.name FROM "subscrabies" INNER JOIN categories ON id_categories = categories.id WHERE id_user = ?', (user,)).fetchall()
# поиск категории по имени
def findcat(name, connect):
    cursor = connect.cursor()
    return cursor.execute('SELECT * FROM "categories" WHERE name = ?', (name,)).fetchone()
def finduser(login, connect):
    cursor = connect.cursor()
    return cursor.execute('SELECT * FROM "users" WHERE login = ?', (login,)).fetchone()
# поиск категории у пользователя
def findcatus(user_id, category, connect):
    cursor = connect.cursor()
    return cursor.execute('SELECT * FROM "subscrabies" WHERE id_user = ? AND id_categories = ?', (user_id, category)).fetchone()
# вывод категорий
def catg(connect):
    cursor = connect.cursor()
    return cursor.execute('SELECT id, name FROM "categories"').fetchall()
def catser(connect):
    cursor = connect.cursor()
    return cursor.execute('SELECT COUNT(*) FROM "categories"').fetchall()
cat = ["business", "entertainment", "general", "health", "science", "sports", "technology"]

def delete(connect):
    cursor = connect.cursor()
    return cursor.execute('DELETE FROM "categories" ').fetchall()
def dob(connect):
    if(len(catser(connect)) < 1):
        for i in range(len(cat)):
            addcategory(cat[i], connect)
            connect.commit()
    else:
        return 'категории добавлены'
# connect.commit()
