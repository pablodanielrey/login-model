
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
            with open_login_session(echo=False) as login_session:

                for student in students:
                    print(f"testeando : {student.dni} {student.name} {student.lastname}")
                    stmt = select(IdentityNumber.user_id).filter(or_(IdentityNumber.number==student.dni, IdentityNumber.number==student.number))
                    user_id = session.execute(stmt).first()
                    # stmt = select(User.id).all()
                    if  user_id is not None:
                        print(f'YA EXISTE {user_id}')
                        results.write(f"{student.dni};{student.name};{student.lastname};{student.number};{student.email};YA EXISTE\n")
                        continue

                    stmt = select(UserCredentials.id).filter_by(username=student.dni)
                    lid = login_session.execute(stmt).first()
                    if lid is not None:
                        print(f'LOGIN YA EXISTE {user_id} {student.dni}')
                        results.write(f"{student.dni};{student.name};{student.lastname};{student.number};{student.email};YA EXISTE\n")
                        continue                    


                    """ agrego la persona debido a que no existe """
                    user_id = str(uuid.uuid4())
                    email_id = str(uuid.uuid4())
                    id_id = str(uuid.uuid4())
                    student_id = str(uuid.uuid4())
                    login_id = str(uuid.uuid4())

                    user = User(id=user_id, firstname=student.name, lastname=student.lastname)
                    session.add(user)

                    email = Mail(email=email_id, type=MailTypes.ALTERNATIVE, confirmed=datetime.datetime.now())
                    session.add(email)

                    idn = IdentityNumber(id=id_id, user_id=user_id, number=student.dni, type=IdentityNumberTypes.DNI)
                    idns = IdentityNumber(id=student_id, user_id=user_id, number=student.number, type=IdentityNumberTypes.STUDENT)
                    session.add(idn)
                    session.add(idns)
                    session.commit()

                    credentials = UserCredentials(id=login_id, user_id=user_id, username=student.dni, credentials=student.passw, temporal=False)
                    login_session.add(credentials)
                    login_session.commit()            

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