from tkinter import ttk
from tkinter import *
import sqlite3
import os
from PIL import Image, ImageTk

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
        frame.grid(row = 0, column = 0, columnspan = 4, pady = 10, sticky = 'ew')

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
        ttk.Button(frame, text = 'Record new stock', command = self.open_record_new_stock).grid(row = 2, column=3)
        # find-148857_640.png
        buttonImage = Image.open('find-148857_640.png')
        buttonImage = buttonImage.resize((15, 15), Image.ANTIALIAS)
        buttonPhoto = ImageTk.PhotoImage(buttonImage)
        self.btn_id_stock = ttk.Button(frame, image=buttonPhoto , command = self.find_records_in_stock)
        self.btn_id_stock.grid(column= 2, row= 2)
        # assign image to other object
        self.btn_id_stock.image = buttonPhoto
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

    def find_records_in_stock(self):
        self.message['text'] = ''
        self.edit_wind = Toplevel()
        self.edit_wind.title = "Find records in stock"
        #
        Label(self.edit_wind, text="type the word you want to search in one or more boxes", justify = LEFT).grid(row = 1 , column = 0)


        Label(self.edit_wind, text = "product").grid(row = 2, column = 0, sticky = W)
        product = Entry(self.edit_wind)
        product.grid(row = 2, column = 1)
        Label(self.edit_wind, text = "description").grid(row = 3, column = 0, sticky = W)
        description = Entry(self.edit_wind)
        description.grid(row = 3, column = 1)
        Label(self.edit_wind, text = "price").grid(row = 4, column = 0, sticky = W)
        price = Entry(self.edit_wind)
        price.grid(row = 4, column = 1)
        Label(self.edit_wind, text = "in_stock").grid(row = 5, column = 0, sticky = W)
        in_stock = Entry(self.edit_wind)
        in_stock.grid(row = 5, column = 1)
        Label(self.edit_wind, text = "").grid(row = 6, column = 0, sticky = W)

        Button(self.edit_wind, text = 'Search match', command = lambda: self.search_match_stock(product.get(), description.get(), price.get(), in_stock.get())).grid(row = 6, column = 2, sticky = W)
        self.edit_wind.mainloop()

    def search_match_stock(self,product, description, price, in_stock):
        #print("102",product)
        column_list=['product', 'description', 'price', 'in_stock']
        search =["", "", "", ""]
        search[0] = product
        search[1] = description
        search[2] = price
        search[3] = in_stock
        stringt="SELECT * FROM stock WHERE "
        #print("114",str(len(stringt)))
        count_=0
        sum_=0
        for t in range(len(search)):
            var=str(search[t])
            if (len(var)>0):
                sum_+=1
                #print("120",sum_)
        while(count_<len(search)):
            var=str(search[count_])
            #print("suma",sum_)
            if (len(var)>0):
                if(sum_==1):
                    stringt+= str(column_list[count_]) + " = '"+ str(search[count_]) +"'"
                    break
                if(count_!=sum_-1):
                    stringt+= str(column_list[count_]) + " = '"+ str(search[count_]) + "' AND "
                else:
                    stringt+= str(column_list[count_]) + " = '"+ str(search[count_])  +"'"
                    break
            count_+=1
        list_text = stringt.split(' ')
        if (len(str(list_text[-1]))==0):
            if(len(stringt)==26):
                stringt='SELECT * FROM stock'
            else:
                stringt=stringt[:-len(' AND')]

        # getting data
        query = stringt.replace("\"","")
        db_rows = self.run_query(query)
        # filling data list
        list_=[]
        for row in list_:
            list_.remove(row)
        count_=1
        for row in db_rows:
            list_.append(row)
  
        if(len(list_)==0):
            #print("159",list_)
            self.edit_wind = Toplevel()
            Label(self.edit_wind, text = "**********************************").grid(row = 1, column = 0, sticky = W)
            Label(self.edit_wind, text = "************** no match***********").grid(row = 2, column = 0, sticky = W)
            Label(self.edit_wind, text = "**********************************").grid(row = 3, column = 0, sticky = W)
            return
 
        else:
            self.edit_wind = Toplevel()
            #print("168",list_)
            for row in list_:
                #print("170",row)
                Label(self.edit_wind, text = row).grid(row = count_, column = 0, sticky = W)
                count_+=1
            return

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