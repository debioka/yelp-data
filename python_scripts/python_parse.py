# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 18:22:46 2017

@author: david
"""

import json
from parsing_funs import file_path, folder


def load_file(file_name):
    """Returns the contents of the file as a dictionary"""
    with open(file_path[file_name], encoding='utf8') as file:
        data = []
        for line in file:
            data.append(json.loads(line))
    return data


def friend_in_users(friend_id, users):
    """Is the friend_id in the list of user ids?"""
    return friend_id in [user['user_id'] for user in users]


def friends_in_users(users):
    """Are all friends of all users in the list of user ids?"""
    return all([all([friend_in_users(friend_id, users) for friend_id in user['friends']]) for user in users])


def write_attributes(write_file, businesses):
    """Writes all unique attributes to file"""
    attributes = []
    for business in businesses:
        if 'attributes' in business:
            if type(business['attributes']) != None:
                for attribute in business['attributes']:
                    if attribute not in attributes:
                        attributes.append(attribute)
    with open(write_file, 'w') as f:
        f.write(attributes)