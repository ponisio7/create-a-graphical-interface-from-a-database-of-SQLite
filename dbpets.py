from tkinter import ttk
from tkinter import *
import sqlite3

class pets:

    # connection dir property
    db_name = 'database.db' 

    def __init__(self, window):
        # Initializations
        self.wind = window
        ##'.format(thetables)
        self.wind.title('pets') 

        # Creating a Frame Container
        ##'.format(thetables)
        frame = LabelFrame(self.wind, text = 'Register new pets')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        ## Input
        Label(frame, text = 'pet_name: ').grid(row = 1, column = 0)
        self.pet_name = Entry(frame)
        self.pet_name.focus()
        self.pet_name.grid(row = 1, column = 1)

        Label(frame, text = 'breed: ').grid(row = 2, column = 0)
        self.breed = Entry(frame)
        self.breed.grid(row = 2, column = 1)

        Label(frame, text = 'kind_of_animal: ').grid(row = 3, column = 0)
        self.kind_of_animal = Entry(frame)
        self.kind_of_animal.grid(row = 3, column = 1)

        Label(frame, text = 'id_owner: ').grid(row = 4, column = 0)

        cb = ttk.Combobox(frame, values=("1", "2", "3", "4", "5"))
        cb.set("1")
        cb.grid( row=4, column=1)

        ttk.Button(frame, text = 'Record new owner').grid(row = 4, column=2, columnspan = 2, sticky = W + E)

        # Button Add
        ttk.Button(frame, text = 'Save pets', command = self.add_pets).grid(row = 5, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 5, column = 0, columnspan = 2, sticky = W + E)

        # Creating a Frame Container
        container = LabelFrame(self.wind, text = 'Table of pets')
        container.grid(row = 6, column = 0, columnspan = 3)

        # Table
        self.tree = ttk.Treeview(height = 10, columns = ['pet_name','breed','kind_of_animal','id_owner'])
        self.tree.heading('#0', text = 'id_pet', anchor = CENTER)
        self.tree.heading('#1', text = 'pet_name', anchor = CENTER)
        self.tree.heading('#2', text = 'breed', anchor = CENTER)
        self.tree.heading('#3', text = 'kind_of_animal', anchor = CENTER)
        self.tree.heading('#4', text = 'id_owner', anchor = CENTER)
        
        #scroll
        vsb = ttk.Scrollbar(orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)

        # Buttons
        ttk.Button(text = 'DELETE', command = self.delete_pets).grid(row = 7, column = 0, sticky = W+E, columnspan = 1)
        ttk.Button(text = 'EDIT', command = self.edit_pets).grid(row = 7, column = 1, sticky = W+E,  columnspan = 2)

        # Filling the Rows
        self.get_petss()

    # Function to Execute Database Querys
    def run_query(self, query, parameters = ()):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            result = cursor.execute(query, parameters)
            conn.commit()
        return result

    # Get pets from Database
    def get_petss(self):
        # cleaning Table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)
        # getting data
        query = 'SELECT * FROM pets ORDER BY id_pet DESC'
        db_rows = self.run_query(query)
        # filling data
        for row in db_rows:
            self.tree.insert('',0,  text = row[0], values = (row[1],row[2],row[3],row[4]))

    # User Input Validation
    def validation(self):
        return len(self.pet_name.get()) != 0 and len(self.breed.get()) != 0 and len(self.kind_of_animal.get()) != 0 and len(self.id_owner.get()) != 0

    def add_pets(self):
        if self.validation():
            query = 'INSERT INTO pets VALUES(NULL, ?, ?, ?, ?)'
            parameters =  (self.pet_name.get(), self.breed.get(), self.kind_of_animal.get(), self.id_owner.get())
            self.run_query(query, parameters)
            self.message['text'] = 'pets {} added Successfully'.format(self.pet_name.get())
            self.pet_name.delete(0, END)
            self.breed.delete(0, END)
            self.kind_of_animal.delete(0, END)
            self.id_owner.delete(0, END)
        else:
            self.message['text'] = 'pet_name and breed and kind_of_animal and id_owner is Required'
        self.get_petss()

    def delete_pets(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['text']
        except IndexError as e:
            self.message['text¸'] = 'Please select a Record in the Grid'
            return
        self.message['text'] = ''
        ##
        name = self.tree.item(self.tree.selection())['text']
        query = 'DELETE FROM pets WHERE id_pet = ?'
        self.run_query(query, (name, ))
        self.message['text'] = 'Record {} deleted Successfully'.format(name)
        self.get_petss()

    def edit_pets(self):
        self.message['text'] = ''
        try:
            self.tree.item(self.tree.selection())['values'][0]
        except IndexError as e:
            self.message['text'] = 'Please, select Record in the Grid'
            return
        old_pet_name = self.tree.item(self.tree.selection())['values'][0]
        old_breed = self.tree.item(self.tree.selection())['values'][1]
        old_kind_of_animal = self.tree.item(self.tree.selection())['values'][2]
        old_id_owner = self.tree.item(self.tree.selection())['values'][3]
        self.edit_wind = Toplevel()
        self.edit_wind.title = 'Edit pets'
        # Old pet_name
        Label(self.edit_wind, text = 'Old pet_name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_pet_name), state = 'readonly').grid(row = 0, column = 2)
        # New pet_name
        Label(self.edit_wind, text = 'New pet_name:').grid(row = 1, column = 1)
        new_pet_name = Entry(self.edit_wind)
        new_pet_name.grid(row = 1, column = 2)
        # Old breed
        Label(self.edit_wind, text = 'Old breed:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_breed), state = 'readonly').grid(row = 2, column = 2)
        # New breed
        Label(self.edit_wind, text = 'New breed:').grid(row = 3, column = 1)
        new_breed = Entry(self.edit_wind)
        new_breed.grid(row = 3, column = 2)
        # Old kind_of_animal
        Label(self.edit_wind, text = 'Old kind_of_animal:').grid(row = 4, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_kind_of_animal), state = 'readonly').grid(row = 4, column = 2)
        # New kind_of_animal
        Label(self.edit_wind, text = 'New kind_of_animal:').grid(row = 5, column = 1)
        new_kind_of_animal = Entry(self.edit_wind)
        new_kind_of_animal.grid(row = 5, column = 2)
        # Old id_owner
        Label(self.edit_wind, text = 'Old id_owner:').grid(row = 6, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_id_owner), state = 'readonly').grid(row = 6, column = 2)
        # New id_owner
        Label(self.edit_wind, text = 'New id_owner:').grid(row = 7, column = 1)
        new_id_owner = Entry(self.edit_wind)
        new_id_owner.grid(row = 7, column = 2)
        
        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(new_pet_name.get(), old_pet_name, new_breed.get(), old_breed, new_kind_of_animal.get(), old_kind_of_animal, new_id_owner.get(), old_id_owner)).grid(row = 8, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def edit_records(self, new_pet_name, old_pet_name, new_breed, old_breed, new_kind_of_animal, old_kind_of_animal, new_id_owner, old_id_owner):
        query = 'UPDATE pets SET pet_name = ?, breed = ?, kind_of_animal = ?, id_owner = ? WHERE pet_name = ? AND breed = ? AND kind_of_animal = ? AND id_owner = ?'
        parameters = (new_pet_name, new_breed, new_kind_of_animal, new_id_owner, old_pet_name, old_breed, old_kind_of_animal, old_id_owner)
        self.run_query(query, parameters)
        self.edit_wind.destroy()
        self.message['text'] = 'Record {} updated successfylly'.format(old_pet_name)
        self.get_petss()

if __name__ == '__main__':
    window = Tk()
    application = pets(window)
    window.mainloop()