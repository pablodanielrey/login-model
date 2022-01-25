
import uuid

data = [('2729455','prueba_nombre','prueba_apellido','prueba_email@gmail.com')]

for dni, name, lastname, email in data:
    user_id = str(uuid.uuid4())
    email_id = str(uuid.uuid4())
    id_id = str(uuid.uuid4())
    login_id = str(uuid.uuid4())
    print(f"insert into users (id, lastname, firstname) values ('{user_id}', '{name}', '{lastname}');")
    print(f"insert into identity_numbers (id, number, user_id) values ('{id_id}', '{dni}', '{user_id}');")
    print(f"insert into mails (id, email, type, confirmed, user_id) values ('{email_id}', '{email}', 'ALTERNATIVE', now(), '{user_id}');")
    print("\n\n")
    print(f"insert into user_credentials (id, created, user_id, temporal, username, credentials) values ('{login_id}', now(), '{user_id}', false, '{dni}', '{dni}');")