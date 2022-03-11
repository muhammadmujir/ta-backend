# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 09:39:16 2022

@author: Admin

https://www.digitalocean.com/community/tutorials/how-to-use-a-postgresql-database-in-a-flask-application

"""

import os
import psycopg2

conn = psycopg2.connect(
        host="127.0.0.1",
        database="ta_crowd_counting",
        user="postgres",
        password="root")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS books;')
cur.execute('CREATE TABLE books (id serial PRIMARY KEY,'
                                 'title varchar (150) NOT NULL,'
                                 'author varchar (50) NOT NULL,'
                                 'pages_num integer NOT NULL,'
                                 'review text,'
                                 'date_added date DEFAULT CURRENT_TIMESTAMP);'
                                 )

# Execute a command: this creates a new table
cur.execute('DROP TABLE IF EXISTS users;')
cur.execute('CREATE TABLE users (id serial PRIMARY KEY,'
                                 'name varchar (150) NOT NULL,'
                                 'age varchar (120) NOT NULL,'
                                 'address varchar (150) NOT NULL,'
                                 'password varchar (150) NOT NULL);'
                                 )

# Insert data into the table

cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('A Tale of Two Cities',
             'Charles Dickens',
             489,
             'A great classic!')
            )


cur.execute('INSERT INTO books (title, author, pages_num, review)'
            'VALUES (%s, %s, %s, %s)',
            ('Anna Karenina',
             'Leo Tolstoy',
             864,
             'Another great classic!')
            )

cur.execute('INSERT INTO users (name, age, address, password)'
            'VALUES (%s, %s, %s, %s)',
            ('Mujir',
             '19 Tahun',
             'Pasuruan',
             'passwordkuuuu')
            )

conn.commit()

cur.close()
conn.close()