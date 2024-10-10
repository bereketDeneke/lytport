from database import Database

db = Database()

#todo: we create all our database here

#todo: public figures info table

#todo: post table

#todo: comments


db.create_table('user', {'name':"VARCHAR(100) NOT NULL", 'followers':"INT"})
db.insert('user', ['name', 'followers'], ['John Doe', 30])
db.update('user', ['name'], ['Jane Doe'], 'id', 1)
db.delete('user', 'id', 1)

rows = db.select('user', ['name', 'followers'])
for row in rows:
    print(row)
db.close()
