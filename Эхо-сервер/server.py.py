#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import socket
import hashlib

def get_user(ip):
    """Получить имя пользователя, связанное с заданным IP-адресом, из списка пользователей."""
    with open("Users_IP.txt", "r") as my_file:
        for line in my_file:
            ip_name = line.split()
            if ip == ip_name[0]:
                return ip_name[1]
    return ''

def write_logs(log_message):
    """Записать сообщения журнала в файл журнала."""
    with open("Users_logs.txt", "a") as log_file:
        log_file.write(f'{log_message}\n')

def get_pass(ip):
    """Получить хешированный пароль, связанный с заданным IP-адресом, из списка пользователей."""
    with open("Users_IP.txt", "r") as my_file:
        for line in my_file:
            ip_name = line.split()
            if ip == ip_name[0]:
                return ip_name[2]
    return ''

def send_socket(conn, message):
    """Отправить сообщение через сокет с фиксированным заголовком, указывающим длину сообщения."""
    bytes_message = message.encode()
    if len(bytes_message) == 0:
        return False
    len_msg = len(bytes_message)
    send_bytes = [len_msg // 256, len_msg % 256] + list(bytes_message)
    conn.send(bytearray(send_bytes))
    return True

def recv_socket(conn):
    """Принять сообщение из сокета, прочитав фиксированный заголовок, а затем сообщение."""
    data = conn.recv(1024)
    if not data:
        return None
    length = data[0] * 256 + data[1]
    return bytearray(data[2:]).decode() if length > 0 else ''

# Запрос на ввод номера порта и создание сокета
print('Введите номер порта:')
port = int(input())
address = ('localhost', port)

sock = socket.socket()

# Привязка сокета к заданному порту или поиск свободного порта
try:
    sock.bind(address)
except OSError:
    for any_port in range(1024, 65536):
        try:
            address = ('localhost', any_port)
            sock.bind(address)
            break
        except OSError:
            pass

# Логирование запуска сервера
write_logs(f'Сервер запущен, {address}')
print(f"Соединение установлено, порт: {address[1]}")

# Ожидание подключения клиентов
sock.listen()
write_logs(f'Ожидание подключения на порту {address[1]}')

is_disconnect = True
while True:
    if is_disconnect:
        conn, addr = sock.accept()
        is_disconnect = False
        write_logs(f'Клиент подключился {addr}')
        no_name_for_new_user = False
        no_pass_for_new_user = False
        is_auth = False
        ip_srv = addr[0]
        usr = get_user(ip_srv)

        # Идентификация нового пользователя или запрос аутентификации
        if usr == '':
            no_name_for_new_user = True
            no_pass_for_new_user = True
            send_socket(conn, "Введите имя")
        else:
            send_socket(conn, f"Привет, {usr}! Введите пароль:")
            is_auth = True

    message = recv_socket(conn)
    if message is None:
        conn.close()
        write_logs(f'Клиент отключился {addr[0]}')
        is_disconnect = True
        continue

    # Регистрация нового пользователя
    if no_name_for_new_user and no_pass_for_new_user:
        name_new_user = message
        no_name_for_new_user = False
        send_socket(conn, "Введите пароль")
        continue

    # Запись нового пользователя и его пароля в файл
    if not no_name_for_new_user and no_pass_for_new_user:
        pass_new_user = hashlib.sha224(message.encode()).hexdigest()
        with open("list_ip.txt", "a") as my_file:
            my_file.write(f"{addr[0]} {name_new_user} {pass_new_user}\n")
        send_socket(conn, "Регистрация прошла успешно")
        no_pass_for_new_user = False
        continue

    # Аутентификация пользователя
    if is_auth:
        if get_pass(ip_srv) == hashlib.sha224(message.encode()).hexdigest():
            send_socket(conn, f"Привет, {usr}! Аутентификация прошла успешно!")
            is_auth = False
        else:
            send_socket(conn, f"Привет, {usr}! Ошибка аутентификации! Введите пароль:")
        continue

    # Обмен сообщениями с клиентом
    print(f'Получены данные {message} от клиента {usr}')
    try:
        if message == "выход":
            continue
    except ConnectionResetError:
        print("Выход из системы")

    send_socket(conn, message)
    print(f'Отправлены данные {message} клиенту {usr}')
    open('Users_logs.txt', 'w').close()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




