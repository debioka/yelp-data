# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 03:39:23 2017

@author: david
"""
import json
import mysql.connector

folder = '/Users/david/Documents/Big Data/Yelp/{}'
file_extension = 'yelp_academic_dataset_{}.json'
file_path = {}
for name in ['business','checkin','review','tip','user']:
    file_path[name] = folder.format(file_extension.format(name))

# creates type dict where each key corrseponds to the dictionary with keys
# type, options, and if type was a list, list type.     
def set_type_dict(file_name):
    with open(file_path[file_name], 'r') as file:
        line = file.readline()
        print(line)
        obj = json.loads(line)
        type_dict = {}
        for key in obj:
            print('\n\n{} : {}'.format(key, obj[key]))
            item_type = input("Item type. Leave blank to not include: ")
            if (item_type != ''):
                if (item_type == 'list'):
                    list_type = input("List type: ")
                    item_options = input("Other item options. Leave blank "
                                         "to not include: ")                
                    type_dict[key] = {'type' : item_type,
                                     'options' : item_options,
                                     'list type' : list_type}
                else:
                    item_options = input("Other item options. Leave blank "
                                         "to not include: ")                
                    type_dict[key] = {'type' : item_type,
                                     'options' : item_options}
    return(type_dict)

          
# finds the largest data type size
def max_size(path, type_dict):
    size_dict = {}
    for key in type_dict:
        size_dict[key] = 0
    with open(path, 'r') as file:
        for line in file:
            size_dict = data_size(json.loads(line), type_dict, size_dict)
    return(size_dict)

def data_size(data, data_type, max_size):
    if (data_type['type'] == 'varchar'):
        return(max([len(data), max_size]))
    if (data_type['type'] == 'int'):
        return(max([data, max_size]))
    if (data_type['type'] == 'line'):
        for item in data:
            max_size = data_size(item, data_type['list type'], max_size)
        return(max_size)
    
def load_file(file_name, type_dict, table_name):
    
    cnx = mysql.connector.connect(user='david', password='Pw',
                              host='localhost')
    cursor = cnx.cursor()
    cursor.execute('USE yelp')
    insert_template = 'INSERT INTO {table} ({keys}) VALUES ({values});'
    
    with open(file_path[file_name]) as file:
        for line in file:
            obj = json.loads(line)
            data = {}
            for key in type_dict:
                if (type_dict[key]['type'] != 'int'):
                    data[key] = '"{}"'.format(str(obj[key]))
                else:
                    data[key] = str(obj[key])
                
            cursor.execute(insert_template.format(
                    table  = table_name,
                    keys   = ", ".join(type_dict.keys()),
                    values = ", ".join(data.values())))
    cnx.conector.close()


def make_table(file_name, type_dict, table_name, options=''):
    cnx = mysql.connector.connect(
            user     = 'david', 
            password = 'Pw', 
            host     = 'localhost')
    cursor = cnx.cursor()
    cursor.execute('USE yelp')
    columns_list = []
    for key in type_dict:
        columns_list.append('"{col_name}"" {col_type}{col_details}'.format(
                col_name = key,
                col_type = type_dict[key]['type'],
                details  = type_dict[key]['options'])
         
    cursor.execute('CREATE TABLE {table} ({columns}{col_options});' .format(
            table       = table_name,
            columns     = ', '.join(columns_list),
            col_options = options))