import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
import mysql

mydb = mysql.connector.connect(host="localhost",
                               user="root",
                               password="12345678",
                               database="bus_depot")


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = mydb
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='purple', bd=10)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        btn_open_dialog = tk.Button(toolbar, text="Add",
                                    command=self.open_dialog, bg='purple', height=2, width=10, foreground='white',
                                    font=('calibri', 14),
                                    bd=0,
                                    compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)
        btn_edit_dialog = tk.Button(toolbar, text="Edit",
                                    command=self.open_update_dialog, bg='purple', height=2, width=10, foreground='white',
                                    font=('calibri', 14), bd=0,
                                    compound=tk.TOP)
        btn_edit_dialog.pack(side=tk.LEFT)

        btn_delete_dialog = tk.Button(toolbar, text="Delete",
                                      command=self.delete_records, bg='purple', height=2, width=10, foreground='white',
                                      font=('calibri', 14),
                                      bd=0,
                                      compound=tk.TOP)
        btn_delete_dialog.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, column=("id", "title", "car_number", "brand", "passenger_seats"), height=10,
                                 show='headings')
        self.tree.column("id", width=50, anchor=tk.CENTER)
        self.tree.column("title", width=300, anchor=tk.CENTER)
        self.tree.column("car_number", width=100, anchor=tk.CENTER)
        self.tree.column("brand", width=100, anchor=tk.CENTER)
        self.tree.column("passenger_seats", width=100, anchor=tk.CENTER)

        self.tree.heading("id", text='id')
        self.tree.heading("title", text='Title')
        self.tree.heading("car_number", text='Car_number')
        self.tree.heading("brand", text='Brand')
        self.tree.heading("passenger_seats", text='Passenger seats')

        self.tree.pack()

    def records(self, title, car_number, brand, passenger_seats):
        self.db.insert_data(title, car_number, brand, passenger_seats)
        self.view_records()

    def update_records(self, title, car_number, brand, passenger_seats):
        self.db.c.execute(
            '''UPDATE `bus` SET `title` = %s, `car_number` = %s, `brand` = %s, `passenger_seats` = %s WHERE (`id` = %s);''',
            (title, car_number, brand, passenger_seats, self.tree.set(
                self.tree.selection()[0], '#1')))
        self.view_records()

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM `bus` WHERE (`id` = %s);''', (self.tree.set(selection_item, '#1'),))
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM bus;''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def error(self):
        return messagebox.showinfo('Error')

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title("Add")
        self.geometry('400x220+400+300')
        self.resizable(False, False)

        label_title = tk.Label(self, text='title')
        label_title.place(x=50, y=50)
        label_car_number = tk.Label(self, text='car_number')
        label_car_number.place(x=50, y=75)
        label_brand = tk.Label(self, text='brand')
        label_brand.place(x=50, y=100)
        label_passenger_seats = tk.Label(self, text='passenger_seats')
        label_passenger_seats.place(x=50, y=125)

        self.entry_title = ttk.Entry(self)
        self.entry_title.place(x=200, y=50)

        self.entry_car_number = ttk.Entry(self)
        self.entry_car_number.place(x=200, y=75)

        self.entry_brand = ttk.Entry(self)
        self.entry_brand.place(x=200, y=100)

        self.entry_passenger_seats = ttk.Entry(self)
        self.entry_passenger_seats.place(x=200, y=125)

        btn_cancel = ttk.Button(self, text='Cancel', command=self.destroy)
        btn_cancel.place(x=300, y=185)

        self.btn_ok = ttk.Button(self, text='Add')
        self.btn_ok.place(x=220, y=185)
        self.btn_ok.bind('<Button-1>',
                         lambda event: self.view.records(self.entry_title.get(), self.entry_car_number.get(),
                                                         self.entry_brand.get(), self.entry_passenger_seats.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = mydb

    def init_edit(self):
        self.title('Edit')
        btn_edit = ttk.Button(self, text='Edit')
        btn_edit.place(x=220, y=185)
        btn_edit.bind('<Button-1>',
                      lambda event: self.view.update_records(self.entry_title.get(), self.entry_car_number.get(),
                                                             self.entry_brand.get(), self.entry_passenger_seats.get()))

        self.grab_set()
        self.focus_set()


class DB:
    def __init__(self):
        self.db = mydb
        self.c = self.db.cursor()

    def insert_data(self, title, car_number, brand, passenger_seats):
        self.c.execute(
            '''INSERT INTO `bus`(`title`, `car_number`, `brand`, `passenger_seats`) VALUES (%s, %s, %s, %s);''',
            (title, car_number, brand, passenger_seats))
        self.db.commit()


if __name__ == "__main__":
    root = tk.Tk()
    mydb = DB()
    app = Main(root)
    app.pack()
    root.title("Bus depot")
    root.geometry('650x450+300+200')
    root.resizable(False, False)
    root.mainloop()
