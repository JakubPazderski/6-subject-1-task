from select import select
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
   """ create a database connection to the SQLite database
       specified by db_file
   :param db_file: database file
   :return: Connection object or None
   """
   conn = None
   try:
       conn = sqlite3.connect(db_file)
       return conn
   except Error as e:
       print(e)

   return conn

def update(conn, contacts, last_name, **kwargs):
   """
   update the last name 
   :param conn:
   :param table: table name
   :param last_name: last_name
   :return:
   """
   parameters = [f"{k} = ?" for k in kwargs]
   parameters = ", ".join(parameters)
   values = tuple(v for v in kwargs.values())
   values += (last_name, )

   sql = f''' UPDATE {contacts}
             SET {parameters}
             WHERE last_name = ?'''
   try:
       cur = conn.cursor()
       cur.execute(sql, values)
       conn.commit()
       print("OK")
   except sqlite3.OperationalError as e:
       print(e)

def delete_where(conn, contacts, **kwargs):
   """
   Delete one row with given attribute
   :param conn:  Connection to the SQLite database
   :param contacts: contacts
   :param kwargs: dict of attributes and values
   :return:
   """
   qs = []
   values = tuple()
   for k, v in kwargs.items():
       qs.append(f"{k}=?")
       values += (v,)
   q = " AND ".join(qs)

   sql = f'DELETE FROM {contacts} WHERE {q}'
   cur = conn.cursor()
   cur.execute(sql, values)
   conn.commit()
   print("Deleted")

def execute_sql(conn, sql):
   """ Execute sql
   :param conn: Connection object
   :param sql: a SQL script
   :return:
   """
   try:
       c = conn.cursor()
       c.execute(sql)
   except Error as e:
       print(e)

if __name__ == '__main__':
   create_connection("database.db")

create_contacts_sql="""
--contacts table
CREATE TABLE IF NOT EXISTS contacts(
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone TEXT NOT NULL UNIQUE
    );
    """
db_file = "database.db"

conn=create_connection(db_file)
if conn is not None:
    execute_sql(conn, create_contacts_sql)
    conn.close()

def add_contact(conn, contact):
   """
   Create a new contact into the contacts table
   :param conn:
   :param contact:
   :return: id
   """
   sql='''INSERT OR REPLACE INTO contacts(first_name, last_name, email, phone) VALUES(?,?,?,?)'''
   cur=conn.cursor()
   cur.execute(sql, contact)
   conn.commit()
   return cur.lastrowid

conn=create_connection("database.db")
contact=("Jakub","Pazderski","jak.pazderski@gmail.com,","573313216")
cont_id=add_contact(conn,contact)
add_contact(conn,contact)
contact=("Bogdan","Kowalski","b.kow@wp.pl","764896320")
add_contact(conn,contact)
contact=("Adam","Nowak","adam.n@o2.pl","856342890")
add_contact(conn,contact)
contact=("Andrzej","Janda","janda89@gmail.com","554786901")
add_contact(conn,contact)
contact=("Tymon","Kałużny","tym.kalu@interia.pl","857420709")
add_contact(conn,contact)

def select_by_name(conn,first_name):
    """
    Select contact by first_name
    :param conn: the Connection object
    :param first_name:
    :return:
   """
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts WHERE first_name=?", (first_name,))
    rows = cur.fetchall()
    conn.commit()
    return rows


