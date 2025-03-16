import bcrypt
import uuid
import MySQLdb


db=MySQLdb.connect(host="localhost",user="lucas",password="lucas1234",database="development")
c = db.cursor()

password = 'admin1234'
password_hashed = bcrypt.generate_password_hash(password).decode('utf-8')

user_id = str(uuid.uuid4())

user_table = f"""
INSERT INTO User(id, first_name, last_name, email, password, is_admin)
VALUES ('{user_id}', 'Admin', 'HBnB', 'admin@hbnb.io', '{password_hashed}', 'True');
"""

amenity_table = f"""
INSERT INTO Amenity(id, name) 
VALUES ('{str(uuid.uuid4())}', 'Wifi'), 
       ('{str(uuid.uuid4())}', 'Swimming Pool'), 
       ('{str(uuid.uuid4())}', 'Air Conditioning');
"""

c.execute(user_table)
c.executemany(amenity_table)

db.commit()

c.close()
db.close()