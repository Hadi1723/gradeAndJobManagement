import sqlite3

#establishing connection to database
conn = sqlite3.connect('usersList.db')

#creating a cursor
cur = conn.cursor()

#create a table using a cursor
cur.execute("""CREATE TABLE customers (
    whole_name text,
    passWords text,
    fileGrade text,
    fileJobs text,
    dateUpdated date
)""")

#actually executing above command using the connection
conn.commit()

#close connection (similar to what is done in files)
conn.close()
