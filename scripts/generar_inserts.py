
import csv
import uuid
from dataclasses import dataclass
import sys
from dotenv import load_dotenv
load_dotenv()

@dataclass
class Student:
    name: str
    lastname: str
    dni: str
    passw: str
    number: str
    email: str

def read_csv(csv_file):
    students = []
    with open(csv_file,'r') as csv_file_descriptor:
        csv_data =  csv.reader(csv_file_descriptor, delimiter=',')
        for lastname, name, dni, passw, student_number, email in csv_data:
            name = name.strip().capitalize()
            lastname = lastname.strip().capitalize()
            dni = dni.strip().upper()
            student_number = student_number.strip().lower()
            email = email.strip().lower()
            students.append(Student(name=name, lastname=lastname, dni=dni, number=student_number, passw=passw, email=email))
    return students

def generate_users(students):
    from login.model import obtener_session as open_login_session
    from users.model import open_session as open_users_session
    from users.model.entities.User import User, IdentityNumber
    from sqlalchemy import select

    results = []
    with open_users_session() as session:
        for student in students:
            print(f"testeando : {student.dni} {student.name} {student.lastname}")
            stmt = select(IdentityNumber.user_id).filter_by(number=student.dni)
            user_id = session.execute(stmt).first()
            # stmt = select(User.id).all()
            if  user_id is not None:
                print(f'YA EXISTE {user_id}')
                results.append({
                    'dni': student.dni,
                    'nombre': student.name,
                    'apellido': student.lastname,
                    'legajo': student.number,
                    'status': 'YA EXISTE'
                })
                continue
    
    return results

if __name__ == '__main__':
    csv_file = sys.argv[1]
    data = read_csv(csv_file)
    results = generate_users(data)
    print(results)

"""
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
"""