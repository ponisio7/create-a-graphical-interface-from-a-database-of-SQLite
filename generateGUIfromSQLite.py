from tkinter import ttk
from tkinter import *
#import os.path as path
import sqlite3
import re


saveIn = "db" #yet no
db_name = "database.db"
stringpy=""    
table_names= []
column_list = [] 
information_from_the_database = {}    

def readDB(databese_name):
    #database name
    #databese_name="database.db"

    #write the address of the database
    connection = sqlite3.connect(databese_name)        
    crsr = connection.cursor()

    #table names
    crsr.execute("SELECT name FROM sqlite_master WHERE type='table';")
    result = crsr.fetchall()
    table_names= []
    for nameTable in result:
        table_names.append(str(nameTable[0]))

    #names of columns and count of rows in each table
    columns_and_rows_with_their_tables={}
    columns1={}
    rows1={}
    for nameTable in table_names:
        if (re.match('sqlite_sequence', nameTable, re.IGNORECASE)==None):
            cursor = connection.execute('select * from {}'.format(nameTable))
            names = [description[0] for description in cursor.description]
            count = cursor.execute('select count(*) from {}'.format(nameTable))
            count = count.fetchone()
            columns1[nameTable]=names
            rows1[nameTable]=count[0]
            columns_and_rows_with_their_tables[nameTable]={'rows':rows1[nameTable],'columns':columns1[nameTable]}
    #print("43",columns_and_rows_with_their_tables)
    connection.close()

        #return the names of the columns, number of rows for each table within the database
        #example
        #{'product': {'rows': 4, 'columns': ['id', 'name', 'price']}, 'anto': {'rows': 2, 'columns': ['id', 'nombre', 'precio']}}
        #print(columns_and_rows_with_their_tables)
    return columns_and_rows_with_their_tables

information_from_the_database = readDB(db_name)
for x in information_from_the_database:
    table_names.append(x)
            #print(str(len(table_names)))



class Product:
    for thetables in table_names:
        global stringpy
        stringpy=""
        count_=0
        print("64",(column_list))

        
        try:
            for val in column_list:
                column_list.remove(val)
                print("remove1",val)
        except expression as identifier:
            for val in column_list:
                column_list.remove(val)
                print("remove2",val)
        try:
            for val in column_list:
                column_list.remove(val)
                print("remove1",val)
        except expression as identifier:
            for val in column_list:
                column_list.remove(val)
                print("remove2",val)
        try:
            for val in column_list:
                column_list.remove(val)
                print("remove1",val)
        except expression as identifier:
            for val in column_list:
                column_list.remove(val)
                print("remove2",val)

        for a in (information_from_the_database.get(thetables).get('columns')):
            column_list.append(a)
        
        stringpy+= "from tkinter import ttk\nfrom tkinter import *\nimport sqlite3\n"
        stringpy+="\nclass "+thetables+":\n\n    # connection dir property\n    db_name = \'"+ '{}'.format(db_name)+"\' \n\n"
        stringpy+="    def __init__(self, window):\n        # Initializations\n        self.wind = window\n        "
        stringpy+="##'.format(thetables)\n        self.wind.title(\'" + '{}'.format(thetables)+"\') \n\n        "
        stringpy+="# Creating a Frame Container\n        ##'.format(thetables)\n        "
        stringpy+="frame = LabelFrame(self.wind, text = \'Register new "+ '{}'.format(thetables)+"\')\n        "
        stringpy+="frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)\n\n        ## Input\n        "
        count_row =0
        count_=0
        for x in column_list:
            if (count_!=0):
                count_column=0
                count_row=count_row+1
                    #Label(frame, text = 'Name: ').grid(row = 1, column = 0)
                stringpy+="Label(frame, text = \'"+'{}'.format(x)+ ": \').grid(row = "+ '{}'.format(str(count_row)) + ", column = " + '{}'.format(str(count_column)) +")\n        "
                    #self.name = Entry(frame)
                stringpy+="self."+'{}'.format(x)+" = Entry(frame)\n        "
                if(count_row == 1):
                    stringpy+="self."+'{}'.format(x)+".focus()\n        "
                count_column = count_column+1
                stringpy+="self."+'{}'.format(x)+".grid(row = "+ '{}'.format(str(count_row)) + ", column = " + '{}'.format(str(count_column)) +")\n\n        "
            count_+=1   
        count_row=count_row+1
        stringpy+="# Button Add\n        ttk.Button(frame, text = 'Save "+ '{}'.format(thetables)+"\'"
        stringpy+=", command = self.add_"+ '{}'.format(thetables)+").grid(row = " + '{}'.format(str(count_row)) + ", columnspan = 2, sticky = W + E)"
        stringpy+="\n\n        # Output Messages \n        self.message = Label(text = '', fg = 'red')\n        "
        stringpy+="self.message.grid(row = " +'{}'.format(str(count_row)) +", column = 0, columnspan = 2, sticky = W + E)\n\n        # Creating a Frame Container\n        "
        stringpy+="container = LabelFrame(self.wind, text = 'Table of " + '{}'.format(thetables)+"\')\n        container.grid(row = "
        count_row=count_row+1
        stringpy+='{}'.format(str(count_row)) +", column = 0, columnspan = 3)\n\n        # Table\n        self.tree = ttk.Treeview(height = 10, columns = ["
        count_=0
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+="\'"+name_+"\',"
            else:
                if(count_== len(column_list)-1):
                    stringpy+="\'"+name_+"\'])\n        self.tree.heading(\'#0\', text = \'"+'{}'.format(str(column_list[0]))+"\', anchor = CENTER)\n        "
            count_+=1
        count_=0
        for name_ in column_list:
            if (count_!=0):
                stringpy+="self.tree.heading(\'#"+'{}'.format(str(count_))+"\', text = \'"+name_+ "\', anchor = CENTER)\n        "
            count_+=1
        stringpy+="\n        #scroll\n        vsb = ttk.Scrollbar(orient=\"vertical\", command=self.tree.yview)\n        "
        stringpy+="hsb = ttk.Scrollbar(orient=\"horizontal\",command=self.tree.xview)\n        self.tree.configure(yscrollcommand=vsb.set,xscrollcommand=hsb.set)"
        stringpy+="\n        self.tree.grid(column=0, row=0, sticky=\'nsew\', in_=container)\n        "
        stringpy+="vsb.grid(column=1, row=0, sticky=\'ns\', in_=container)\n        "
        stringpy+="hsb.grid(column=0, row=1, sticky=\'ew\', in_=container)\n\n        # Buttons\n        "
        count_row=count_row+1
        stringpy+="ttk.Button(text = 'DELETE', command = self.delete_"+ '{}'.format(thetables)+").grid(row = "+'{}'.format(str(count_row))+", column = 0, sticky = W+E, columnspan = 1)"
        stringpy+="\n        ttk.Button(text = 'EDIT', command = self.edit_"+ '{}'.format(thetables)+").grid(row = "+'{}'.format(str(count_row))+", column = 1, sticky = W+E,  columnspan = 2)"
        stringpy+="\n\n        # Filling the Rows\n        self.get_"+ '{}'.format(thetables)+"s()\n\n    "
        stringpy+="# Function to Execute Database Querys\n    def run_query(self, query, parameters = ()):\n        with sqlite3.connect(self.db_name) as conn:"
        stringpy+="\n            cursor = conn.cursor()\n            result = cursor.execute(query, parameters)\n            conn.commit()"
        stringpy+="\n        return result\n\n    # Get "+ '{}'.format(thetables)+" from Database\n    def get_"+ '{}'.format(thetables)+"s(self):"
        stringpy+="\n        # cleaning Table\n        records = self.tree.get_children()\n        for element in records:\n            self.tree.delete(element)"
        stringpy+="\n        # getting data\n        query = \'SELECT * FROM " + '{}'.format(thetables)+ " ORDER BY " + '{}'.format(column_list[0])
        stringpy+=" DESC\'\n        db_rows = self.run_query(query)\n        # filling data\n        for row in db_rows:\n            self.tree.insert('',0,  text = row[0], values = ("
        count_=0
        for number in range(len(column_list)-1):
            count_+=1
            if(count_!= len(column_list)-1):
                stringpy+="row["+str(count_ )+"],"
            else:
                stringpy+="row["+str(count_ )+ "]))\n\n    "
        stringpy+="# User Input Validation\n    def validation(self):\n        return "
        count_=0
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+="len(self."+name_+".get()) != 0 and "
            else:
                if(count_== len(column_list)-1):
                    stringpy+="len(self."+name_+".get()) != 0\n\n    "
            count_+=1
        count_=0
        stringpy+="def add_"+ '{}'.format(thetables)+"(self):\n        if self.validation():\n            query = \'INSERT INTO "+ '{}'.format(thetables)+" VALUES(NULL, "
        for number in range(len(column_list)-1):
            count_+=1
            if(count_!= len(column_list)-1):
                stringpy+="?, "
            else:
                stringpy+="?)\'"+ "\n            parameters =  ("
        count_=0
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+="self."+name_+".get(), "
            else:
                if(count_== len(column_list)-1):
                    stringpy+="self."+name_+".get())\n            self.run_query(query, parameters)\n            self.message[\'text\'] = \'"
            count_+=1
        stringpy+='{}'.format(thetables)+" {} added Successfully'.format(self."+ '{}'.format(column_list[1])+".get())\n            "
        count_=0
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+="self."+name_+".delete(0, END)\n            "
            else:
                if(count_== len(column_list)-1):
                    stringpy+="self."+name_+".delete(0, END)\n        else:\n            self.message['text'] = \'"
            count_+=1
        count_=0
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+=name_+" and "
            else:
                if(count_== len(column_list)-1):
                    stringpy+= name_+ " is Required\'\n        self.get_"+'{}'.format(thetables)+"s()\n\n    def delete_"+ '{}'.format(thetables)+"(self):"
            count_+=1
        stringpy+="\n        self.message[\'text\'] = \'\'\n        try:\n            self.tree.item(self.tree.selection())['text']\n        except IndexError as e:"
        stringpy+="\n            self.message[\'text¸'] = \'Please select a Record in the Grid\'\n            return\n        self.message[\'text\'] = \'\'\n        "
        stringpy+="##\n        name = self.tree.item(self.tree.selection())[\'text\']\n        query = \'DELETE FROM "+ '{}'.format(thetables)
        stringpy+=" WHERE " + '{}'.format(column_list[0])+" = ?\'\n        self.run_query(query, (name, ))\n        self.message[\'text\'] = \'Record {} deleted Successfully\'.format(name)"
        stringpy+="\n        self.get_"+ '{}'.format(thetables)+"s()"
        
        stringpy+="\n\n    def edit_"+ '{}'.format(thetables)+"(self):\n        self.message[\'text\'] = \'\'\n        try:\n            "
        stringpy+="self.tree.item(self.tree.selection())['values'][0]\n        except IndexError as e:\n            self.message[\'text\'] = \'Please, select Record in the Grid\'"
        stringpy+="\n            return\n        "
        count_=0
        for name_ in column_list:
            if (count_!=0 ):
                stringpy+="old_"+name_ + " = self.tree.item(self.tree.selection())['values']["+str(count_-1)+"]\n        "
            count_+=1
        stringpy+="self.edit_wind = Toplevel()\n        self.edit_wind.title = \'Edit "+ '{}'.format(thetables)+"\'\n        "
        count_=0
        rows=1
        for name_ in column_list:
            if (count_!=0 ):
                
                stringpy+="# Old "+name_ + "\n        Label(self.edit_wind, text = \'Old "+name_ + ":\').grid(row = "+str(rows-1)+", column = 1)\n        "
                stringpy+="Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_"+name_ +"), state = 'readonly').grid(row = "
                stringpy+=str(rows-1)+", column = 2)\n        "
                rows+=1
                stringpy+="# New "+name_ + "\n        Label(self.edit_wind, text = \'New "+name_ + ":\').grid(row = "+str(rows-1)+", column = 1)\n        "
                stringpy+="new_"+name_ + " = Entry(self.edit_wind)\n        new_"+name_ + ".grid(row = "+str(rows-1)+", column = 2)\n        "
                rows+=1
            count_+=1
        stringpy+="\n        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records("
        count_=0
        rows+=1
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+="new_"+name_+".get(), old_"+name_+", "
            else:
                if(count_== len(column_list)-1):
                    stringpy+="new_"+name_+".get(), old_"+name_+")).grid(row = "+str(rows-2)+", column = 2, sticky = W)\n        self.edit_wind.mainloop()"
            count_+=1
        stringpy+="\n\n    def edit_records(self, "
        count_=0
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+="new_"+name_+", old_"+name_+", "
            else:
                if(count_== len(column_list)-1):
                    stringpy+="new_"+name_+", old_"+name_+"):\n        query = 'UPDATE " + '{}'.format(thetables) + " SET "
            count_+=1
        count_=0
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+= name_+" = ?, "
            else:
                if(count_== len(column_list)-1):
                    stringpy+= name_+" = ? WHERE "
            count_+=1
        count_=0
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+= name_+" = ? AND "
            else:
                if(count_== len(column_list)-1):
                    stringpy+= name_+" = ?\'\n        parameters = ("
            count_+=1
        count_=0
        #parameters = (new_first_name,  new_last_name, new_email, new_phone, old_first_name, old_last_name, old_email, old_phone)
            #stringpy+="new_"+name_+", old_"+name_+", "
        for name_ in column_list:
            if (count_!=0):
                stringpy+="new_"+name_+", "
            count_+=1
        count_=0
            #stringpy+="new_"+name_+", old_"+name_+", "
        for name_ in column_list:
            if (count_!=0 and count_<len(column_list)-1):
                stringpy+="old_"+name_+", "
            else:
                if(count_== len(column_list)-1):
                    stringpy+="old_"+name_+")\n        self.run_query(query, parameters)\n        self.edit_wind.destroy()\n        "
            count_+=1
        count_=0
        stringpy+="self.message[\'text\'] = \'Record {} updated successfylly\'.format(old_"+'{}'.format(column_list[1])+")\n        self.get_"+ '{}'.format(thetables)+"s()"
        stringpy+="\n\nif __name__ == '__main__':\n    window = Tk()\n    application = "+thetables+"(window)\n    window.mainloop()"
            #print(stringpy)

        file = open(saveIn+thetables+".py", 'w')
        file.write(stringpy)
        print("stringpy")
        file.close()
    
