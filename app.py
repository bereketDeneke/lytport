from database import Database

db = Database()

#todo: we intitialize our tables here
db.create_table('user', {'name':"VARCHAR(100) NOT NULL", 'followers':"INT"})
db.insert('user', ['name', 'followers'], ['John Doe', 30])
db.update('user', ['name'], ['Jane Doe'], 'id', 1)
db.delete('user', 'id', 1)

rows = db.select('user', ['name', 'followers'])
for row in rows:
    print(row)
db.close()
