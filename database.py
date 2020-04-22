from tkinter import ttk
from tkinter import *
import sqlite3

class pet_owner:

    # connection dir property
    db_name = 'database.db' 

    def __init__(self, window):
        # Initializations
        self.wind = window
        ##'.format(table_names[0])
        self.wind.title('pet_owner') 

        # Creating a Frame Container
        ##'.format(table_names[0])
        frame = LabelFrame(self.wind, text = 'Register new pet_owner')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        ## Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.Name = Entry(frame)
        self.Name.focus()
        self.Name.grid(row = 1, column = 1)

        Label(frame, text = 'Lasta: ').grid(row = 2, column = 0)
        self.Lasta = Entry(frame)
        self.Lasta.grid(row = 2, column = 1)

        Label(frame, text = 'address: ').grid(row = 3, column = 0)
        self.address = Entry(frame)
        self.address.grid(row = 3, column = 1)

        Label(frame, text = 'phone: ').grid(row = 4, column = 0)
        self.phone = Entry(frame)
        self.phone.grid(row = 4, column = 1)

        Label(frame, text = 'email: ').grid(row = 5, column = 0)
        self.email = Entry(frame)
        self.email.grid(row = 5, column = 1)

        # Button Add
        ttk.Button(frame, text = 'Save pet_owner', command = self.add_pet_owner).grid(row = 6, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 6, column = 0, columnspan = 2, sticky = W + E)

        # Creating a Frame Container
        container = LabelFrame(self.wind, text = 'Table of pet_owner')
        container.grid(row = 7, column = 0, columnspan = 3)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = ['Name','Lasta','address','phone','email'])
        self.tree.heading('#0', text = 'id_owner', anchor = CENTER)
        self.tree.heading('#1', text = 'Name', anchor = CENTER)
        self.tree.heading('#2', text = 'Lasta', anchor = CENTER)
        self.tree.heading('#3', text = 'address', anchor = CENTER)
        self.tree.heading('#4', text = 'phone', anchor = CENTER)
        self.tree.heading('#5', text = 'email', anchor = CENTER)
        
        #scroll
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)

        # Buttons
        ttk.Button(text = 'DELETE', command = self.delete_pet_owner).grid(row = 8, column = 0, sticky = W+E, columnspan = 1)
        ttk.Button(text = 'EDIT', command = self.edit_pet_owner).grid(row = 8, column = 1, sticky = W+E,  columnspan = 2)

        # Filling the Rows
        self.get_pet_owners()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get pet_owner from Database
    def get_pet_owners(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM pet_owner ORDER BY id_owner DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('',0,  text = row[0], values = (row[1],row[2],row[3],row[4],row[5]))

    # User Input Validation
    def validation(self):
        return len(self.Name.get()) != 0 and len(self.Lasta.get()) != 0 and len(self.address.get()) != 0 and len(self.phone.get()) != 0 and len(self.email.get()) != 0

    def add_pet_owner(self):
        if self.validation():
            query = 'INSERT INTO pet_owner VALUES(NULL, ?, ?, ?, ?, ?)'
            parameters =  (self.Name.get(), self.Lasta.get(), self.address.get(), self.phone.get(), self.email.get())
            self.run_query(query, parameters)
            self.message['text'] = 'pet_owner {} added Successfully'.format(self.Name.get())
            self.Name.delete(0, END)
            self.Lasta.delete(0, END)
            self.address.delete(0, END)
            self.phone.delete(0, END)
            self.email.delete(0, END)
        else:
            self.message['text'] = 'Name and Lasta and address and phone and email is Required'
        self.get_pet_owners()

    def delete_pet_owner(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text¸'] = 'Please select a Record in the Grid'
            return
        self.message['text'] = ''
        ##
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM pet_owner WHERE id_owner = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_pet_owners()

    def edit_pet_owner(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record in the Grid'
            return
        old_Name = self.tree.item(self.tree.selection())['values'][0]
        old_Lasta = self.tree.item(self.tree.selection())['values'][1]
        old_address = self.tree.item(self.tree.selection())['values'][2]
        old_phone = self.tree.item(self.tree.selection())['values'][3]
        old_email = self.tree.item(self.tree.selection())['values'][4]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit pet_owner'
        # Old Name
        Label(self.edit_wind, text = 'Old Name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_Name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New Name:').grid(row = 1, column = 1)
        new_Name = Entry(self.edit_wind)
        new_Name.grid(row = 1, column = 2)
        # Old Lasta
        Label(self.edit_wind, text = 'Old Lasta:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_Lasta), state = 'readonly').grid(row = 2, column = 2)
        # New Lasta
        Label(self.edit_wind, text = 'New Lasta:').grid(row = 3, column = 1)
        new_Lasta = Entry(self.edit_wind)
        new_Lasta.grid(row = 3, column = 2)
        # Old address
        Label(self.edit_wind, text = 'Old address:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_address), state = 'readonly').grid(row = 4, column = 2)
        # New address
        Label(self.edit_wind, text = 'New address:').grid(row = 5, column = 1)
        new_address = Entry(self.edit_wind)
        new_address.grid(row = 5, column = 2)
        # Old phone
        Label(self.edit_wind, text = 'Old phone:').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_phone), state = 'readonly').grid(row = 6, column = 2)
        # New phone
        Label(self.edit_wind, text = 'New phone:').grid(row = 7, column = 1)
        new_phone = Entry(self.edit_wind)
        new_phone.grid(row = 7, column = 2)
        # Old email
        Label(self.edit_wind, text = 'Old email:').grid(row = 8, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_email), state = 'readonly').grid(row = 8, column = 2)
        # New email
        Label(self.edit_wind, text = 'New email:').grid(row = 9, column = 1)
        new_email = Entry(self.edit_wind)
        new_email.grid(row = 9, column = 2)
        
        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_Name.get(), old_Name, new_Lasta.get(), old_Lasta, new_address.get(), old_address, new_phone.get(), old_phone, new_email.get(), old_email)).grid(row = 10, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_Name, old_Name, new_Lasta, old_Lasta, new_address, old_address, new_phone, old_phone, new_email, old_email):
        query = 'UPDATE pet_owner SET Name = ?, Lasta = ?, address = ?, phone = ?, email = ? WHERE Name = ? AND Lasta = ? AND address = ? AND phone = ? AND email = ?'
        parameters = (new_Name, new_Lasta, new_address, new_phone, new_email, old_Name, old_Lasta, old_address, old_phone, old_email)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(old_Name)
        self.get_pet_owners()

if __name__ == '__main__':
    window = Tk()
    application = pet_owner(window)
    window.mainloop()