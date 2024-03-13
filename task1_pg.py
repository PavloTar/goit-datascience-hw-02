from faker import Faker
import psycopg2
import random

fake = Faker()

# connection
conn = psycopg2.connect(
    dbname='db_goit',
    user='postgres',
    password='passpostgres',
    host='127.0.0.1'
)

cur = conn.cursor()

# users
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s)", (fullname, email))

# tasks
for _ in range(20):
    title = fake.sentence(nb_words=6)
    description = fake.text(max_nb_chars=200)
    status_id = random.randint(1, 3)  
    user_id = random.randint(1, 10) 
    cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)", (title, description, status_id, user_id))

conn.commit()


# Check sql script:

cur.execute("SELECT * FROM tasks WHERE user_id = 1;")
print(cur.fetchall())

cur.execute("SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = 'new');")
print(cur.fetchall())

cur.execute("UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = 'in progress') WHERE id = 1;")
conn.commit()

cur.execute("SELECT * FROM users WHERE id NOT IN (SELECT user_id FROM tasks);")
rows = cur.fetchall()
print('\n'.join(map(str, rows)))

cur.execute("INSERT INTO tasks (title, description, status_id, user_id) VALUES ('New task', 'description of new task', 1, 1);")
conn.commit()

cur.execute("SELECT * FROM tasks WHERE status_id != (SELECT id FROM status WHERE name = 'completed');")
rows = cur.fetchall()
print('\n'.join(map(str, rows)))

cur.execute("DELETE FROM tasks WHERE id = 1;")
conn.commit()

cur.execute("SELECT * FROM users WHERE email LIKE '%example.com';")
rows = cur.fetchall()
print('\n'.join(map(str, rows)))

cur.execute("UPDATE users SET fullname = 'New name' WHERE id = 1;")
conn.commit()

cur.execute("SELECT status_id, COUNT(*) FROM tasks GROUP BY status_id;")
rows = cur.fetchall()
print('\n'.join(map(str, rows)))

cur.execute("SELECT t.* FROM tasks t JOIN users u ON t.user_id = u.id WHERE u.email LIKE '%@example.com';")
rows = cur.fetchall()
print('\n'.join(map(str, rows)))

cur.execute("SELECT * FROM tasks WHERE description IS NULL OR description = '';")
rows = cur.fetchall()
print('\n'.join(map(str, rows)))

cur.execute("SELECT u.*, t.* FROM users u INNER JOIN tasks t ON u.id = t.user_id WHERE t.status_id = (SELECT id FROM status WHERE name = 'in progress');")
rows = cur.fetchall()
print('\n'.join(map(str, rows)))

cur.execute("SELECT u.id, u.fullname, COUNT(t.id) FROM users u LEFT JOIN tasks t ON u.id = t.user_id GROUP BY u.id;")
rows = cur.fetchall()
print('\n'.join(map(str, rows)))


cur.close()
conn.close()