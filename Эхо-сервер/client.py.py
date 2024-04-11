#!/usr/bin/env python
# coding: utf-8

# In[1]:


import socket

def send_socket(conn, message):
    """Отправляет сообщение по сокету с заголовком фиксированной длины, указывающим длину сообщения."""
    message_bytes = message.encode()  

    if len(message_bytes) == 0:  # Проверяет, что сообщение не пустое
        return False

    message_length = len(message_bytes)  # Получает длину сообщения в байтах
    # Создает массив байт для отправки с заголовком длины сообщения
    send_bytes = [message_length // 256, message_length % 256] + list(message_bytes)
    conn.send(bytearray(send_bytes))  # Отправляет сообщение по сокету
    return True

def receive_socket(conn):
    """Получает сообщение из сокета, читая заголовок фиксированной длины, а затем само сообщение."""
    data = conn.recv(1024)  # Получает данные из сокета

    if not data:  # Проверяет, что данные получены
        return None

    length = data[0] * 256 + data[1]  # Получает длину сообщения из заголовка
    # Возвращает раскодированное сообщение, если длина больше 0, иначе возвращает пустую строку
    return bytearray(data[2:]).decode() if length > 0 else ''

def main():
    print('Введите номер порта:')
    port = int(input())  # Запрашивает номер порта у пользователя

    print('Введите имя хоста (Нажмите Enter для localhost):')
    host = input() or 'localhost'  # Запрашивает имя хоста у пользователя, по умолчанию используется localhost

    address = (host, port)  # Формирует кортеж с адресом сервера
    sock = socket.socket()  # Создает новый сокет

    try:
        sock.connect(address)  # Подключается к серверу по заданному адресу
    except Exception as e:
        print(f"Ошибка подключения к {host}:{port}: {e}")  # Выводит сообщение об ошибке и завершает программу
        exit(1)

    print('Подключено к серверу:', address)  # Выводит сообщение об успешном подключении

    data_received = receive_socket(sock)  # Получает данные от сервера
    print(data_received)  # Выводит полученные данные

    while True:
        message = ""  # Инициализирует переменную для хранения сообщения
        input_line = ""  # Инициализирует переменную для хранения ввода пользователя
        while True:
            input_line = input()  # Запрашивает ввод пользователя
            if input_line == "send":  # Проверяет, если пользователь ввел "send", то завершает ввод сообщения
                message = message.rstrip('\n')  # Удаляет лишние переносы строк из сообщения
                break
            message += input_line + "\n"  # Добавляет ввод пользователя в сообщение с новой строки

        if send_socket(sock, message):  # Отправляет сообщение на сервер
            data_received = receive_socket(sock)  # Получает ответ от сервера
            print(f'Отправлено: {message}\nПолучено: {data_received}')  # Выводит отправленное сообщение и полученный ответ
        else:
            print("Не удалось отправить данные. Повторите ввод.")  # Выводит сообщение об ошибке при отправке

        if message.lower() == 'exit':  # Проверяет, если пользователь ввел 'exit', то завершает программу
            break

    sock.close()  # Закрывает соединение с сервером
    print('Соединение закрыто:', address)  # Выводит сообщение о закрытии соединения

if __name__ == "__main__":
    main()  # Вызывает функцию main(), если скрипт запущен напрямую


# In[ ]:




