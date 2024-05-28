import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox as ms
import mysql.connector
import mysql

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="12345678",
                               database="de_user1")


class main:
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.password = StringVar()
        self.n_username = StringVar()
        self.n_password = StringVar()
        self.widgets()

    def login(self):
        c = mydb.cursor()

        find_user = "SELECT * FROM user WHERE name = %s and password = %s;"
        c.execute(find_user, [(self.username.get()), (self.password.get())])
        result = c.fetchall()
        if result:
            self.logf.pack_forget()
            self.head['text'] = self.username.get() + '\n добрый день'
            self.head['pady'] = 150

        else:
            ms.showerror('Уведомление', 'Данный пользователь не найден')

    def new_user(self):
        c = mydb.cursor()

        find_user = "SELECT name FROM user WHERE name = %s;"
        c.execute(find_user, [(self.n_username.get())])
        if c.fetchall():
            ms.showerror('Уведомление', 'Имя пользователя занято, попробуйте другое.')

        else:
            ms.showinfo('Успех', 'Пользователь создан')
            self.log()
        insert = "INSERT INTO user(name, password) VALUES(%s, %s);"
        c.execute(insert, [(self.n_username.get()), (self.n_password.get())])
        mydb.commit()

    def log(self):
        self.username.set('')
        self.password.set('')
        self.crf.pack_forget()
        self.head['text'] = 'Авторизация'
        self.logf.pack()

    def cr(self):
        self.n_username.set('')
        self.n_password.set('')
        self.logf.pack_forget()
        self.head['text'] = 'Создать пользователя'
        self.crf.pack()

    def widgets(self):
        self.head = Label(self.master, text='Авторизация', font=('', 35), pady=10)
        self.head.pack()
        self.logf = Frame(self.master, padx=10, pady=10)
        Label(self.logf, text='Логин:', font=('', 15), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.logf, text='Пароль:', font=('', 15), pady=5, padx=5).grid(sticky=W)
        Entry(self.logf, textvariable=self.password, bd=5, font=('', 15)).grid(row=1, column=1)
        Button(self.logf, text='Войти', bd=3, font=('', 15), padx=5, pady=5, command=self.login).grid()
        Button(self.logf, text='Создать пользователя', bd=3, font=('', 15), padx=5, pady=5, command=self.cr).grid(row=2,
                                                                                                                  column=1)
        self.logf.pack()

        self.crf = Frame(self.master, padx=10, pady=10)
        Label(self.crf, text='Логин:', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_username, bd=5, font=('', 15)).grid(row=0, column=1)
        Label(self.crf, text='Пароль:', font=('', 20), pady=5, padx=5).grid(sticky=W)
        Entry(self.crf, textvariable=self.n_password, bd=5, font=('', 15), show='*').grid(row=1, column=1)
        Button(self.crf, text='Создать пользователя', bd=3, font=('', 15), padx=5, pady=5, command=self.new_user).grid()
        Button(self.crf, text='Назад', bd=3, font=('', 15), padx=5, pady=5, command=self.log).grid(
            row=2,
            column=1)


if __name__ == '__main__':
    root = Tk()
    root.title('Авторизация')
    main(root)
    root.mainloop()