from tkinter import ttk
from tkinter import *
import sqlite3
import os
from PIL import Image, ImageTk

class stock:

    # connection dir property
    db_name = 'Store.sqlite3' 

    def __init__(self, window):
        # Initializations
        self.wind = window
        ##'.format(thetables)
        self.wind.title('stock') 

        # Creating a Frame Container
        ##'.format(thetables)
        frame = LabelFrame(self.wind, text = 'Register new stock')
        frame.grid(row = 0, column = 0, columnspan = 4, pady = 10, sticky = 'ew')

        #focus
        frame.bind("<FocusIn>", self.on_focus_in)
        frame.bind("<FocusOut>", self.on_focus_out)

        ## Input :)
        Label(frame, text = 'product: ').grid(row = 1, column = 0)
        self.product = Entry(frame)
        self.product.focus()
        self.product.grid(row = 1, column = 1)

        Label(frame, text = 'description: ').grid(row = 2, column = 0)
        self.description = Entry(frame)
        self.description.grid(row = 2, column = 1)

        Label(frame, text = 'price: ').grid(row = 3, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 3, column = 1)

        Label(frame, text = 'in_stock: ').grid(row = 4, column = 0)
        self.in_stock = Entry(frame)
        self.in_stock.grid(row = 4, column = 1)

        # Button Add
        ttk.Button(frame, text = 'Save stock', command = self.add_stock).grid(row = 5, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 5, column = 0, columnspan = 2, sticky = W + E)

        # Creating a Frame Container
        container = LabelFrame(self.wind, text = 'Table of stock')
        container.grid(row = 6, column = 0, columnspan = 3)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = ['product','description','price','in_stock'])
        self.tree.heading('#0', text = 'id_stock', anchor = CENTER)
        self.tree.heading('#1', text = 'product', anchor = CENTER)
        self.tree.heading('#2', text = 'description', anchor = CENTER)
        self.tree.heading('#3', text = 'price', anchor = CENTER)
        self.tree.heading('#4', text = 'in_stock', anchor = CENTER)
        
        #scroll
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)

        # Buttons
        ttk.Button(text = 'DELETE', command = self.delete_stock).grid(row = 7, column = 0, sticky = W+E, columnspan = 1)
        ttk.Button(text = 'EDIT', command = self.edit_stock).grid(row = 7, column = 1, sticky = W+E,  columnspan = 2)

        # Filling the Rows
        self.get_stocks()



    def on_focus_out(self, event):
        #print("I DON'T have focus")
        pass

    def on_focus_in(self, event):
        #print("I have focus")
        pass

# Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get stock from Database
    def get_stocks(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM stock ORDER BY id_stock DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('',0,  text = row[0], values = (row[1],row[2],row[3],row[4]))

    # User Input Validation
    def validation(self):
        return len(self.product.get()) != 0 and len(self.description.get()) != 0 and len(self.price.get()) != 0 and len(self.in_stock.get()) != 0

    def add_stock(self):
        if self.validation():
            query = 'INSERT INTO stock VALUES(NULL, ?, ?, ?, ?)'
            parameters =  (self.product.get(), self.description.get(), self.price.get(), self.in_stock.get())
            self.run_query(query, parameters)
            self.message['text'] = 'stock {} added Successfully'.format(self.product.get())
            self.product.delete(0, END)
            self.description.delete(0, END)
            self.price.delete(0, END)
            self.in_stock.delete(0, END)
        else:
            self.message['text'] = 'product and description and price and in_stock is Required'
        self.get_stocks()

    def delete_stock(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text¸'] = 'Please select a Record in the Grid'
            return
        self.message['text'] = ''
        ##
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM stock WHERE id_stock = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_stocks()

    def edit_stock(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record in the Grid'
            return
        old_product = self.tree.item(self.tree.selection())['values'][0]
        old_description = self.tree.item(self.tree.selection())['values'][1]
        old_price = self.tree.item(self.tree.selection())['values'][2]
        old_in_stock = self.tree.item(self.tree.selection())['values'][3]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit stock'
        # Old product
        Label(self.edit_wind, text = 'Old product:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_product), state = 'readonly').grid(row = 0, column = 2)
        # New product
        Label(self.edit_wind, text = 'New product:').grid(row = 1, column = 1)
        new_product = Entry(self.edit_wind)
        new_product.grid(row = 1, column = 2)
        # Old description
        Label(self.edit_wind, text = 'Old description:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_description), state = 'readonly').grid(row = 2, column = 2)
        # New description
        Label(self.edit_wind, text = 'New description:').grid(row = 3, column = 1)
        new_description = Entry(self.edit_wind)
        new_description.grid(row = 3, column = 2)
        # Old price
        Label(self.edit_wind, text = 'Old price:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 4, column = 2)
        # New price
        Label(self.edit_wind, text = 'New price:').grid(row = 5, column = 1)
        new_price = Entry(self.edit_wind)
        new_price.grid(row = 5, column = 2)
        # Old in_stock
        Label(self.edit_wind, text = 'Old in_stock:').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_in_stock), state = 'readonly').grid(row = 6, column = 2)
        # New in_stock
        Label(self.edit_wind, text = 'New in_stock:').grid(row = 7, column = 1)
        new_in_stock = Entry(self.edit_wind)
        new_in_stock.grid(row = 7, column = 2)
        
        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_product.get(), old_product, new_description.get(), old_description, new_price.get(), old_price, new_in_stock.get(), old_in_stock)).grid(row = 8, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_product, old_product, new_description, old_description, new_price, old_price, new_in_stock, old_in_stock):
        query = 'UPDATE stock SET product = ?, description = ?, price = ?, in_stock = ? WHERE product = ? AND description = ? AND price = ? AND in_stock = ?'
        parameters = (new_product, new_description, new_price, new_in_stock, old_product, old_description, old_price, old_in_stock)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(old_product)
        self.get_stocks()

if __name__ == '__main__':
    window = Tk()
    application = stock(window)
    window.mainloop()