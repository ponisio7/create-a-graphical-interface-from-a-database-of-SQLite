from tkinter import ttk
from tkinter import *
import sqlite3
import os
from PIL import Image, ImageTk

class product_to_buy:

    # connection dir property
    db_name = 'buy.db' 

    def __init__(self, window):
        # Initializations
        self.wind = window
        ##'.format(thetables)
        self.wind.title('product_to_buy') 

        # Creating a Frame Container
        ##'.format(thetables)
        frame = LabelFrame(self.wind, text = 'Register new product_to_buy')
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

        # Button Add
        ttk.Button(frame, text = 'Save product_to_buy', command = self.add_product_to_buy).grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Creating a Frame Container
        container = LabelFrame(self.wind, text = 'Table of product_to_buy')
        container.grid(row = 4, column = 0, columnspan = 3)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = ['product','description'])
        self.tree.heading('#0', text = 'id_product_to_buy', anchor = CENTER)
        self.tree.heading('#1', text = 'product', anchor = CENTER)
        self.tree.heading('#2', text = 'description', anchor = CENTER)
        
        #scroll
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)

        # Buttons
        ttk.Button(text = 'DELETE', command = self.delete_product_to_buy).grid(row = 5, column = 0, sticky = W+E, columnspan = 1)
        ttk.Button(text = 'EDIT', command = self.edit_product_to_buy).grid(row = 5, column = 1, sticky = W+E,  columnspan = 2)

        # Filling the Rows
        self.get_product_to_buys()



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

    # Get product_to_buy from Database
    def get_product_to_buys(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM product_to_buy ORDER BY id_product_to_buy DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('',0,  text = row[0], values = (row[1],row[2]))

    # User Input Validation
    def validation(self):
        return len(self.product.get()) != 0 and len(self.description.get()) != 0

    def add_product_to_buy(self):
        if self.validation():
            query = 'INSERT INTO product_to_buy VALUES(NULL, ?, ?)'
            parameters =  (self.product.get(), self.description.get())
            self.run_query(query, parameters)
            self.message['text'] = 'product_to_buy {} added Successfully'.format(self.product.get())
            self.product.delete(0, END)
            self.description.delete(0, END)
        else:
            self.message['text'] = 'product and description is Required'
        self.get_product_to_buys()

    def delete_product_to_buy(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text¸'] = 'Please select a Record in the Grid'
            return
        self.message['text'] = ''
        ##
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM product_to_buy WHERE id_product_to_buy = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_product_to_buys()

    def edit_product_to_buy(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record in the Grid'
            return
        old_product = self.tree.item(self.tree.selection())['values'][0]
        old_description = self.tree.item(self.tree.selection())['values'][1]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit product_to_buy'
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
        
        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_product.get(), old_product, new_description.get(), old_description)).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_product, old_product, new_description, old_description):
        query = 'UPDATE product_to_buy SET product = ?, description = ? WHERE product = ? AND description = ?'
        parameters = (new_product, new_description, old_product, old_description)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(old_product)
        self.get_product_to_buys()

if __name__ == '__main__':
    window = Tk()
    application = product_to_buy(window)
    window.mainloop()