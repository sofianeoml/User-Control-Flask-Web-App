from flask import *
import pymongo
import re
import hashlib
import time
import secrets


# Replace with your MongoDB connection string
client = pymongo.MongoClient("mongodb://localhost:27017/") 

# Access a database (create it if it doesn't exist)
db = client["user-control"]
counter_collection = db["counters"]   
users = db["users"]  
sessions = db['sessions']

username_regex = r'^[a-z_]\w*$'
name_regex = r'^[a-zA-Z]{1,25}$'
password_regex = r'^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/]).{8,}$'
