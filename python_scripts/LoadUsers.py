
# coding: utf-8

# In[ ]:

import json
import sqlite3


# In[ ]:

db_name = 'yelp'
file_dir = '/Users/david/Documents/Big Data/Yelp/yelp_academic_dataset_user.json'
insert_script_template = 'INSERT INTO {} ({}) VALUES (?{});'  # template for insert command
table_scripts = {}  # dictionary of create table scripts for each table
ignored_keys = {}   # dictionary of keys ignored by each table
string_values = {}  # dictionary of values that need to be converted to strings to input into table

# In[ ]:

# connect to database
connection = sqlite3.connect(db_name)
cursor = connection.cursor()


# In[ ]:

# user table constants
table_name = 'users'
table_scripts[table_name] = (   "CREATE TABLE users ("                     # create table command for sqlite
                                "user_id char(22) NOT NULL PRIMARY KEY, "  # char(22) since id is fixed-length str
                                "name varchar(32) NOT NULL, "              # longest name in file is 32 characters
                                "review_count int(10) NOT NULL, "
                                "yelping_since date NOT NULL, "
                                "useful int(10) NOT NULL, "
                                "funny int(10) NOT NULL, "
                                "cool int(10) NOT NULL, "
                                "fans int(10) NOT NULL, "
                                "average_stars FLOAT(3,2), "
                                "compliment_hot int(5) NOT NULL, "
                                "compliment_more int(5) NOT NULL, "
                                "compliment_profile int(5) NOT NULL, "
                                "compliment_cute int(5) NOT NULL, "
                                "compliment_list int(5) NOT NULL, "
                                "compliment_note int(5) NOT NULL, "
                                "compliment_plain int(5) NOT NULL, "
                                "compliment_cool int(5) NOT NULL, "
                                "compliment_funny int(5) NOT NULL, "
                                "compliment_writer int(5) NOT NULL, "
                                "compliment_photos int(5) NOT NULL, "
                                "type varchar(20))")
ignored_keys[table_name] = ['friends', 'elite']
string_values = ['user_id', 'name', 'type', 'yelping_since']


# In[ ]:

try:
    cursor.execute(table_scripts[table_name])
except sqlite3.Error as error:
    print('An error occurred when making table:', error)


# In[ ]:

with open(file_dir, 'r', encoding="utf8") as file:  # encoding specified since I was running into errors when I didn't
    columns = [key for key in json.loads(file.readline()) if key not in ignored_keys[table_name]]  # used column names
    file.seek(0)  # returns to beginning of file
    for line in file:
        user = json.loads(line)
        data = []
        for key in user:
            if key not in ignored_keys[table_name]:
                if key in string_values:
                    data.append('"{}"'.format(str(user[key])))  # adds double quotes to the value so that
                else:                                           # it's recognized as a string
                    data.append(user[key])
        cursor.execute(insert_script_template.format(table_name, ','.join(columns), ', ?' * (len(columns)-1)), data)
    connection.commit()
