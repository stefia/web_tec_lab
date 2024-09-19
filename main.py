# Подключаем приложение Flask из пакета appiphnoe
from carapp import app

"""

    Этот файл запускает приложение

"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8888)