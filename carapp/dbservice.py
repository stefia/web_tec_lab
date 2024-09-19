# for CRUD operations

from carapp import db
from datetime import datetime
from sqlalchemy import text
from flask import session, make_response, redirect, url_for, jsonify
import bcrypt

def get_all_requests():
    try:
        result = []  # создаем пустой список
        # Получаем итерируемый объект, где содержатся все строки таблицы contactrequests
        stmt = text("SELECT * FROM sqlite_sequence")
        rows = db.session.execute(stmt).fetchall()
        # Каждую строку конвертируем в словарь
        for row in rows:
            row_dict = dict(row._mapping.items())
            result.append(row_dict)
        # Возвращаем словарь с ключом 'contactrequests', где значение - это список словарей с информацией
        return {'sqlite_sequence': result}
    except Exception as e:
        # Обработка ошибок
        return {'error': str(e)}




# Получаем запрос с фильтром по id
def get_contact_req_by_id(id):
    stmt = text(f"SELECT * FROM contactrequests WHERE id = {id}")
    result = db.session.execute(stmt).fetchone()
    if result:
        return dict(result._asdict())
    else:
        return None

# Получаем список всех запросов.
def get_contact_req_all():
    try:
        result = []  # создаем пустой список
        # Получаем итерируемый объект, где содержатся все строки таблицы contactrequests
        stmt = text("SELECT * FROM contactrequests")
        rows = db.session.execute(stmt).fetchall()
        # Каждую строку конвертируем в словарь
        for row in rows:
            row_dict = dict(row._mapping.items())
            result.append(row_dict)
        # Возвращаем словарь с ключом 'contactrequests', где значение - это список словарей с информацией
        return {'contactrequests': result}
    except Exception as e:
        # Обработка ошибок
        return {'error': str(e)}



# Получаем все запросы по имени автора
def get_contact_req_by_author(name):
    result = []
    stmt = text(f"SELECT * FROM contactrequests WHERE name = '{name}'")
    rows = db.session.execute(stmt).fetchall()
    for row in rows:
        row_dict = dict(row._mapping.items())
        result.append(row_dict)
        # result.append(dict(row))
    return {'contactrequests': result}





# Создать новый запрос
def create_contact_req(json_data):
    try:
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")     # текущая дата и время

        # Используйте text() для объявления текстового SQL-выражения
        stmt = text("INSERT INTO contactrequests (name, email, reqtext, createdAt, updatedAt) "
                    "VALUES (:name, :email, :reqtext, :createdAt, :updatedAt)")

        # Выполните SQL-выражение с использованием параметров
        db.session.execute(stmt, {
            'name': json_data['name'],
            'email': json_data['email'],
            'reqtext': json_data['reqtext'],
            'createdAt': cur_time,
            'updatedAt': cur_time
        })

        # Подтвердите изменения в БД
        db.session.commit()

        # Возвращаем результат
        return {'message': "Order request created"}

    except Exception as e:
        # Откатываем изменения в БД
        db.session.rollback()
        # Возвращаем dict с ключом 'error' и текстом ошибки
        return {'message': str(e)}





# Удалить запрос по id в таблице
def delete_contact_req_by_id(id):
    try:
        # DELETE запрос в БД
        stmt = text(f"DELETE FROM contactrequests WHERE id = {id}")
        db.session.execute(stmt)
        db.session.commit()
        return {'message': "Order request deleted"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}

# Обновить email запроса по id в таблице
def update_contact_email_by_id(id, json_data):
    try:
        cur_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # текущая дата и время
        # UPDATE запрос в БД
        stmt = text(f"UPDATE contactrequests SET email = '{json_data['email']}', "f"updatedAt = '{cur_time}' WHERE id = {id}")
        db.session.execute(stmt)
        db.session.commit()
        return {'message': "Order request updated"}
    except Exception as e:
        db.session.rollback()
        return {'message': str(e)}
    




# Поиск аккаунта пользователя в БД
def login_user(form_data):
    # Получаем логин и пароль из данных формы
    username = form_data.get('login')
    password = form_data.get('password')
    if username == '':
        return redirect(url_for('login'))
    # Ищем пользователя в БД
    result = db.session.execute(text(f"SELECT * FROM logins WHERE username = '{username}'")).fetchone()
    # если пользователь не найден переадресуем на страницу /login
    if result is None:
        return redirect(url_for('login'))
    # print(result)
    # user = dict(result)
    user = {
        'id': result[0],
        'username': result[1],
        'password': result[2]
    }
    # если пароль не прошел проверку, переадресуем на страницу /login
    if not bcrypt.checkpw(password.encode('utf-8'), user.get('password').encode('utf-8')):
        return redirect(url_for('login'))
    # иначе регистрируем сессию пользователя (записываем логин пользователя в параметр user) и высылаем cookie "AuthToken"
    else:
        response = redirect('/')
        session['user'] = user['username']
        session['userId'] = user['id']
        response.set_cookie('AuthToken', user['username'])
        return response

# Создание пользовательского аккаунта
def register_user(form_data):
    # Получаем данные пользователя из формы
    username = form_data.get('login')
    password = form_data.get('password')
    # Проверяем полученные данные на наличие обязательных полей
    if username == '' or password == '':
        return make_response(jsonify({'message': 'The data entered are not correct!'}), 400)
    # Создаем хеш пароля с солью
    salt = bcrypt.gensalt()
    print(password)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    try:
        stmt = text(f"INSERT INTO logins "
                           f"(username, password) "
                           f"VALUES ("
                           f"'{username}', "
                           f"'{hashed}'"
                           ")")
        db.session.execute(stmt)
        # Подтверждение изменений в БД
        db.session.commit()
        # Переадресуем на страницу авторизации
        return redirect(url_for('login'))
        # если возникла ошибка запроса в БД
    except Exception as e:
        # откатываем изменения в БД
        db.session.rollback()
        # возвращаем response с ошибкой сервера
        return make_response(jsonify({'message': str(e)}), 500)

