
import datetime
import csv
from unicodedata import name
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
            if 'Nombre' in name:
                continue
            students.append(Student(name=name, lastname=lastname, dni=dni, number=student_number, passw=passw, email=email))
    return students

def generate_users(students, results_file):
    from login.model import obtener_session as open_login_session
    from users.model import open_session as open_users_session
    from users.model.entities.User import User, IdentityNumber, IdentityNumberTypes, Mail, MailTypes
    from login.model.entities.Login import UserCredentials
    from sqlalchemy import select
    from sqlalchemy import or_

    with open(results_file,'w') as results:
        with open_users_session() as session:
            for student in students:
                print(f"testeando : {student.dni} {student.name} {student.lastname}")
                stmt = select(IdentityNumber.user_id).filter(or_(IdentityNumber.number==student.dni, IdentityNumber.number==student.number))
                user_id = session.execute(stmt).first()
                # stmt = select(User.id).all()
                if  user_id is None:
                    print(f'No existe {student.dni} {student.name} {student.lastname}')
                    results.write(f"{student.dni};{student.name};{student.lastname};{student.number};{student.email};NO EXISTE\n")
                    continue

                user_id = user_id[0]
                emid = session.execute(select(Mail.id).filter_by(email=student.email, user_id=user_id)).first()
                if emid is not None:
                    print('ya tiene el correo')
                    continue
                email_id = str(uuid.uuid4())
                email = Mail(id=email_id, user_id=user_id, type=MailTypes.ALTERNATIVE, confirmed=datetime.datetime.now(), email=student.email)
                session.add(email)
                session.commit()

                results.write(f"{student.dni};{student.name};{student.lastname};{student.number};{student.email};AGREGADO\n")

        return results

if __name__ == '__main__':
    csv_file = sys.argv[1]
    results_csv = sys.argv[2]
    data = read_csv(csv_file)
    generate_users(data, results_csv)

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