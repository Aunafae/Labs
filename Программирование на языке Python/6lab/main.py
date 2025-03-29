# Разработать клиент-серверное приложение (чат).
# Клиенты должны последовательно отправлять сообщения.

# Требования к клиенту:
# - отправка на сервер введенного пользователем сообщения
# - получение сообщений, отправленных другими клиентами
# - удобный графический интерфейс

# Требования к серверу:
# - организация чата между клиентами (до 3 клиентов), а именно отправка всем клиентам полученных сервером сообщений
# - полученные сообщения перед отправкой клиентам необходимо преобразовывать к верхнему регистру


import socket
import threading
import tkinter as tk

active = True
def listening_thread():
    client.settimeout(2)
    message = ""
    while active:
        try:
            while len(message) < 1024:
                message += client.recv(1024).decode()
        except:
            continue
        msg = ""
        for i in range(len(message)):
            if message[i] == '\0':
                break
            msg += message[i]
        output_text.configure(state='normal')
        output_text.insert(tk.END, "Server: " + msg + '\n')
        output_text.configure(state='disabled')
        message = ""

def on_send():
    request = input_entry.get("1.0",'end-1c')
    if request:
        for i in range(len(request)+1, 1024+1):
            request += '\0'
        client.send(request.encode())
        input_entry.delete('1.0', tk.END)

# основное окно
def on_close():
    global active
    client.close()
    root.destroy()
    active = False

root = tk.Tk()
root.title("ЛАБ6")
root.geometry("1150x700")
root.config(bg='#8662ad')
root.protocol("WM_DELETE_WINDOW", on_close)

font_size = 16
text_color = '#323843'

def char_limit(event):
    count = len(input_entry.get('1.0', 'end-1c'))
    if count >= 1000 and event.keysym not in {'BackSpace', 'Delete'}:
        return 'break'

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 3333))

# Поле вывода
output_text = tk.Text(root, height=16, fg=text_color, state='disabled', wrap=tk.WORD, borderwidth=2, relief='solid', font=('Arial', font_size))
output_text.pack(pady=(30, 10), padx=30, fill=tk.BOTH, expand=True)

# Контейнер для ввода
entry_frame = tk.Frame(root, bg='#8662ad')
entry_frame.pack(pady=(10, 30), padx=30, fill=tk.BOTH)
# Многострочное поле ввода
input_entry = tk.Text(entry_frame, height=4, fg=text_color, borderwidth=2, relief='solid', font=('Arial', font_size))
input_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
input_entry.bind('<KeyPress>', char_limit)
input_entry.bind('<KeyRelease>', char_limit)
# Кнопка "Отправить"
send_button = tk.Button(entry_frame, height=4, background='#CBE857', text="Отправить", command=on_send, fg='black', borderwidth=2, relief='solid', font=('Arial', font_size))
send_button.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(5, 0))

thread = threading.Thread(target=listening_thread)
thread.start()
root.mainloop()
thread.join()