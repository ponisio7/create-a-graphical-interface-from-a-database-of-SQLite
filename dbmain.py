from tkinter import ttk
from tkinter import *
import sqlite3
import os

class car:

    # connection dir property
    db_name = 'Store.sqlite3' 

    def __init__(self, window):
        # Initializations
        self.wind = window
        ##'.format(thetables)
        self.wind.title('car') 

        # Creating a Frame Container
        ##'.format(thetables)
        frame = LabelFrame(self.wind, text = 'Register new car')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20, sticky = 'ew')

        #focus
        frame.bind("<FocusIn>", self.on_focus_in)
        frame.bind("<FocusOut>", self.on_focus_out)

        ## Input :)
        Label(frame, text = 'Name_client: ').grid(row = 1, column = 0)
        self.Name_client = Entry(frame)
        self.Name_client.focus()
        self.Name_client.grid(row = 1, column = 1)

        Label(frame, text = 'id_stock: ').grid(row = 2, column = 0)
        self.id_stock = ttk.Combobox(frame,postcommand = self.updtcblist)
        self.id_stock.grid(row = 2, column = 1)

        # Button Add
        ttk.Button(frame, text = 'Record new stock', command = self.open_record_new_stock).grid(row = 2, column=2, columnspan = 2, sticky = W + E)
        ttk.Button(frame, text = 'Save car', command = self.add_car).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Creating a Frame Container
        container = LabelFrame(self.wind, text = 'Table of car')
        container.grid(row = 4, column = 0, columnspan = 3)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = ['Name_client','id_stock'])
        self.tree.heading('#0', text = 'id_car', anchor = CENTER)
        self.tree.heading('#1', text = 'Name_client', anchor = CENTER)
        self.tree.heading('#2', text = 'id_stock', anchor = CENTER)
        
        #scroll
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)

        # Buttons
        ttk.Button(text = 'DELETE', command = self.delete_car).grid(row = 5, column = 0, sticky = W+E, columnspan = 1)
        ttk.Button(text = 'EDIT', command = self.edit_car).grid(row = 5, column = 1, sticky = W+E,  columnspan = 2)

        # Filling the Rows
        self.get_cars()

    def on_focus_out(self, event):
        #print("I DON'T have focus")
        pass

    def on_focus_in(self, event):
        #print("I have focus")
        self.updtcblist()


    def open_record_new_stock(self):
        os.system ("python3 dbstock.py")

    def updtcblist(self):
        ## change clients
        list_=self.get_stocks_listed()
        self.id_stock['values'] = list_

    def get_stocks_listed(self):
        # getting data
        query = 'SELECT * FROM stock ORDER BY id_stock ASC'
        db_rows = self.run_query(query)
        # filling data list
        list_=[]
        for row in db_rows:
            text_=str(row[0])+":"+str(row[1])+"  "+str(row[3])
            list_.append(text_)
        return list_

# Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get car from Database
    def get_cars(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM car ORDER BY id_car DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('',0,  text = row[0], values = (row[1],row[2]))

    # User Input Validation
    def validation(self):
        return len(self.Name_client.get()) != 0 and len(self.id_stock.get()) != 0

    def add_car(self):
        if self.validation():
            query = 'INSERT INTO car VALUES(NULL, ?, ?)'
            parameters =  (self.Name_client.get(), (self.id_stock.get().split(':'))[0])
            self.run_query(query, parameters)
            self.message['text'] = 'car {} added Successfully'.format(self.Name_client.get())
            self.Name_client.delete(0, END)
            self.id_stock.delete(0, END)
        else:
            self.message['text'] = 'Name_client and id_stock is Required'
        self.get_cars()

    def delete_car(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text¸'] = 'Please select a Record in the Grid'
            return
        self.message['text'] = ''
        ##
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM car WHERE id_car = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_cars()

    def edit_car(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record in the Grid'
            return
        old_Name_client = self.tree.item(self.tree.selection())['values'][0]
        old_id_stock = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit car'
        # Old Name_client
        Label(self.edit_wind, text = 'Old Name_client:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_Name_client), state = 'readonly').grid(row = 0, column = 2)
        # New Name_client
        Label(self.edit_wind, text = 'New Name_client:').grid(row = 1, column = 1)
        new_Name_client = Entry(self.edit_wind)
        new_Name_client.grid(row = 1, column = 2)
        # Old id_stock
        Label(self.edit_wind, text = 'Old id_stock:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_id_stock), state = 'readonly').grid(row = 2, column = 2)
        # New id_stock
        Label(self.edit_wind, text = 'New id_stock:').grid(row = 3, column = 1)
        new_id_stock = Entry(self.edit_wind)
        new_id_stock.grid(row = 3, column = 2)
        
        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_Name_client.get(), old_Name_client, new_id_stock.get(), old_id_stock)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_Name_client, old_Name_client, new_id_stock, old_id_stock):
        query = 'UPDATE car SET Name_client = ?, id_stock = ? WHERE Name_client = ? AND id_stock = ?'
        parameters = (new_Name_client, new_id_stock, old_Name_client, old_id_stock)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(old_Name_client)
        self.get_cars()

if __name__ == '__main__':
    window = Tk()
    application = car(window)
    window.mainloop()