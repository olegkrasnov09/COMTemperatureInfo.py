from tkinter import *
from tkinter import ttk
import serial

root = Tk()
root.title("Термодатчик")
root.geometry("300x220")
root.resizable(False, False)
root.config(bg="#494949")
root.iconbitmap('free-icon-temperatures-3988334.ico')

t_info = StringVar()
com_entry = StringVar()
error = StringVar()

curr_com = ""
t_info.set("")
ser = 0


def connect():
    global ser
    read_com()
    try:
        ser = serial.Serial(f'COM{curr_com}', 9600)
        errorlbl.config(fg="yellow")
        error.set("Подключение...")
    except:
        errorlbl.config(fg="red")
        error.set("Ошибка подключения")
    show_temp()


def show_temp():
    data = float(ser.readline().decode('utf-8').strip())
    if data > 30 and data < 40:
        text.config(fg="#ddce00")  # желтый
        errorlbl.config(fg="limegreen")
        error.set("")
    elif data > 40:
        text.config(fg="#df0000")  # красный
        errorlbl.config(fg="red")
        error.set("Высокая температура!")
    else:
        text.config(fg="#40c901")  # зеленый
        errorlbl.config(fg="limegreen")
        error.set("")
    t_info.set(f"{str(data)}°C")
    text.after(500, show_temp)


def read_com():
    global curr_com
    try:
        with open("com.txt", "r") as com:
            curr_com = com.read()
            com_entry.set(curr_com)
            errorlbl.config(fg="limegreen")
            error.set(f"Прочитано COM{curr_com}")
    except FileNotFoundError:
        errorlbl.config(fg="red")
        error.set("COM-порт не задан")


def write_com():
    with open("com.txt", "w") as com:
        com.write(com_entry.get())
        errorlbl.config(fg="limegreen")
        error.set(f"COM{com_entry.get()} сохранен")


f1 = Frame(bg="#494949")
f1.pack()
text_t = Label(f1, text="t:", bg="#494949", font=('Century Gothic', 32, "bold"), fg="white")
text_t.grid(row=0, column=0)
text = Label(f1, textvariable=t_info, font=("Century Gothic", 32, "bold"), bg="#494949")
text.grid(row=0, column=1, columnspan=3, pady=20)

text_com = Label(f1, text="COM:", bg="#494949", font=('Century Gothic', 16), fg="white")
text_com.grid(row=1, column=0)
comEntry = ttk.Entry(f1, font=('Century Gothic', 16), width=6, textvariable=com_entry)
comEntry.grid(row=1, column=1, stick='we', padx=10)

writeButton = Button(f1, width=12, text="Сохранить", font=('Century Gothic', 10), bg='#98a700', fg='white',
                     activebackground='#c7c7c7', activeforeground='#98a700', command=write_com)
writeButton.grid(row=1, column=3, stick="we")
connectButton = Button(f1, width=14, text="Подключение", font=('Century Gothic', 10), bg='#00759c', fg='white',
                       activebackground='#c7c7c7', activeforeground='#00759c', command=connect)
connectButton.grid(row=2, column=0, stick="we", columnspan=4, pady=10)

authorlbl = Label(f1, text="Developed by Krasnov Oleg", bg='#494949', fg='gray')
authorlbl.grid(row=4, column=0, stick="we", columnspan=4)

errorlbl = Label(f1, textvariable=error, bg='#494949', fg='red')
errorlbl.grid(row=3, column=0, stick="we", columnspan=4)

read_com()

root.mainloop()
