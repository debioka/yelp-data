# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:22:46 2017

@author: david
"""

import json
from parsing_funs import file_path

with open(file_path['user'], encoding='utf8') as file:
    users = []
    for line in file:
        users.append(json.loads(line))
        
def friend_in_users(friend_id):
   return( friend_id in [user['user_id'] for user in users])

#%%

with open(file_path['business']) as file:
    businesses = []
    for line in file:
        users.append(json.loads(line))
    