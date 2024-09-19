# -*- coding: utf-8 -*-
# Подключаем объект приложения Flask из __init__.py
from carapp import app #,db
# Подключаем библиотеку для "рендеринга" html-шаблонов из папки templates
from flask import render_template, make_response, request, Response, jsonify, json, session, redirect, url_for
from . import dbservice
import functools



navmenu = [
    {
        'name': 'General',
        'addr': '/index'
    },
    {
        'name': 'NEW CARS',
        'addr': '/new-cars'
    },
    {
        'name': 'PRE-OWNED CARS',
        'addr': '#'
    },
    {
        'name': 'FINANCE',
        'addr': '#'
    },
    {
        'name': 'LEASE VS BUY',
        'addr': '#'
    },
    {
        'name': 'CONTACT US',
        'addr': '/contact'
    },
]

# Функция-декоратор для проверки авторизации пользователя
def login_required(route_func):
    @functools.wraps(route_func)
    def decorated_route(*args, **kwargs):
        # Если не установлен параметр сессии user или значение cookie 'AuthToken' не равно логину пользователя
        if not session.get('user') or request.cookies.get('AuthToken') != session.get('user'):
            # перенаправляем на страницу регистрации
            return redirect(url_for('register'))
        return route_func(*args, **kwargs)
    return decorated_route

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='GENERAL', navmenu=navmenu)


@app.route('/new-cars')
@login_required
def new_cars():
    return render_template('new-cars.html', title='NEW CARS', navmenu=navmenu)

@app.route('/contact')
def contact():
    return render_template('contact.html', title='CONTACT', navmenu=navmenu)


# Страница авторизации
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Если POST-запрос
    if request.method == 'POST':
        # если нажата кнопка "Зарегистрировать", переадресуем на страницу регистрации
        if request.form.get('regBtn') == 'true':
            return redirect(url_for('register'))
        # иначе запускаем авторизацию по данным формы
        else:
            return dbservice.login_user(request.form)
    else:
        return render_template('login.html', title='Login', navmenu=navmenu)


# Страница регистрации
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Если POST-запрос, регистрируем нового пользователя
    if request.method == 'POST':
        return dbservice.register_user(request.form)
    else:
        return render_template('register.html', title='Registration', navmenu=navmenu)




#Получаем все записи contactrequests из БД
@app.route('/api/contactrequest', methods=['GET'])
def get_contact_req_all():
    response = dbservice.get_contact_req_all()
    return json_response(response)

@app.route('/api/contactrequest/<int:id>', methods=['GET'])
# Получаем запись по id
def get_contact_req_by_id(id):
    response = dbservice.get_contact_req_by_id(id)
    return json_response(response)

@app.route('/api/contactrequest/author/<string:firstname>', methods=['GET'])
# Получаем запись по имени пользователя
def get_contact_req_by_author(firstname):
    if not firstname:
        # то возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
        # Иначе отправляем json-ответ
    else:
        response = dbservice.get_contact_req_by_author(firstname)
    return json_response(response)



# Обработка POST-запроса для демонстрации AJAX
@app.route('/api/contactrequest', methods=['POST'])
def create_contact_req():
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в этом объекте нет, например, обязательного поля 'firstname'
    if not request.json or not 'name' in request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе отправляем json-ответ
    else:
        msg = request.json['name'] + ",  your request has been received !";
        response = dbservice.create_contact_req(request.json)
        # return json_response(response)
        return json_response({ 'message': msg })


@app.route('/api/contactrequest/<int:id>', methods=['PUT'])
# Обработка запроса на обновление записи в БД
def update_contact_req_by_id(id):
    # Если в запросе нет данных или неверный заголовок запроса (т.е. нет 'application/json'),
    # или в данных нет обязательного поля 'reqtext'
    if not request.json or not 'reqtext' in request.json:
        # возвращаем стандартный код 400 HTTP-протокола (неверный запрос)
        return bad_request()
    # Иначе обновляем запись в БД и отправляем json-ответ
    else:
        response = dbservice.update_contact_req_by_id(id, request.json)
        return json_response(response)


@app.route('/api/contactrequest/<int:id>', methods=['DELETE'])
# Обработка запроса на удаление записи в БД по id
def delete_contact_req_by_id(id):
    response = dbservice.delete_contact_req_by_id(id)
    return json_response(response)




# Возврат html-страницы с кодом 404 (Не найдено)
@app.route('/notfound')
def not_found_html():
    return render_template('404.html', title='404', err={ 'error': 'Not found', 'code': 404 })

# Формирование json-ответа. Если в метод передается только data (dict-объект), то по-умолчанию устанавливаем код возврата code = 200
# В Flask есть встроенный метод jsonify(dict), который также реализует данный метод (см. пример метода not_found())
def json_response(data, code=200):
    return Response(status=code, mimetype="application/json", response=json.dumps(data))

# Пример формирования json-ответа с использованием встроенного метода jsonify()
# Обработка ошибки 404 протокола HTTP (Данные/страница не найдены)
def not_found():
    return make_response(jsonify({'error': 'Not found'}), 404)

# Обработка ошибки 400 протокола HTTP (Неверный запрос)
def bad_request():
    return make_response(jsonify({'error': 'Bad request'}), 400)
