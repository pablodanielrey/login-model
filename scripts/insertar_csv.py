
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
        #for lastname, name, dni, passw, student_number, email in csv_data:
        for dni, name, lastname, passw, student_number, email in csv_data:
            name = name.strip().capitalize()
            lastname = lastname.strip().capitalize()
            dni = dni.strip().upper()
            student_number = student_number.strip().lower()
            email = email.strip().lower()
            if 'Nombre' in name:
                continue
            students.append(Student(name=name, lastname=lastname, dni=dni, number=student_number, passw=passw, email=email))
    return students

def generate_users(students, results_file, dry_run = True):
    from login.model import obtener_session as open_login_session
    from users.model import open_session as open_users_session
    from users.model.entities.User import User, IdentityNumber, IdentityNumberTypes, Mail, MailTypes
    from login.model.entities.Login import UserCredentials
    from sqlalchemy import select
    from sqlalchemy import or_, and_

    with open(results_file,'w') as results:
        with open_users_session(echo=False) as session:
            with open_login_session(echo=False) as login_session:

                for student in students:

                    agregar_persona = True
                    agregar_legajo = True
                    print(f"testeando : {student.dni} {student.name} {student.lastname}")
                    stmt = select(IdentityNumber.user_id).filter(IdentityNumber.number==student.dni)
                    user_id = session.execute(stmt).first()
                    print(user_id)
                    # stmt = select(User.id).all()
                    if  user_id is not None:
                        user_id = user_id[0]
                        print(f'YA EXISTE ESE DNI {user_id}')
                        results.write(f"{student.dni};{student.name};{student.lastname};{student.number};{student.email};YA EXISTE DNI\n")
                        agregar_persona = False

                        print(f"testeando : {student.number} {student.name} {student.lastname}")
                        stmt = select(IdentityNumber.user_id).filter(and_(IdentityNumber.user_id==user_id, IdentityNumber.number==student.number))
                        aux_id = session.execute(stmt).first()
                        # stmt = select(User.id).all()
                        if  aux_id is not None:
                            print(f'YA EXISTE ESE LEGAJO {user_id}')
                            results.write(f"{student.dni};{student.name};{student.lastname};{student.number};{student.email};YA EXISTE LEGAJO\n")
                            agregar_legajo = False


                    agregar_credenciales = True
                    stmt = select(UserCredentials.id).filter_by(username=student.dni)
                    lid = login_session.execute(stmt).first()
                    if lid is not None:
                        print(f'LOGIN YA EXISTE {user_id} {student.dni}')
                        results.write(f"{student.dni};{student.name};{student.lastname};{student.number};{student.email};YA EXISTE LAS CREDENCIALES\n")
                        agregar_credenciales = False

                    if agregar_persona:

                        print(f"agrego al alumno debido a que no existe {student.dni} {student.name} {student.lastname} {student.email} ")


                        """ agrego la persona debido a que no existe """
                        user_id = str(uuid.uuid4())
                        email_id = str(uuid.uuid4())
                        id_id = str(uuid.uuid4())
                        
                        user = User(id=user_id, firstname=student.name, lastname=student.lastname)
                        session.add(user)

                        email = Mail(id=email_id, user_id=user_id, type=MailTypes.ALTERNATIVE, confirmed=datetime.datetime.now(), email=student.email)
                        session.add(email)

                        idn = IdentityNumber(id=id_id, user_id=user_id, number=student.dni, type=IdentityNumberTypes.DNI)
                        session.add(idn)
                    
                    if agregar_legajo:
                        student_id = str(uuid.uuid4())
                        print(f"agrego el legajo debido a que no existe {student.number} {student.dni} {student.name} {student.lastname} {student.email} ")
                        idns = IdentityNumber(id=student_id, user_id=user_id, number=student.number, type=IdentityNumberTypes.STUDENT)
                        session.add(idns)
    
                    if not dry_run:
                        print('hago commit')
                        session.commit()

                    if agregar_credenciales:
                        login_id = str(uuid.uuid4())
                        print(f"agrego las credenciales {student.dni} {student.name} {student.lastname} {student.email} ")
                        credentials = UserCredentials(id=login_id, user_id=user_id, username=student.dni, credentials=student.passw, temporal=False)
                        login_session.add(credentials)
                        if not dry_run:
                            print('hago commit')
                            login_session.commit()            

                    results.write(f"{student.dni};{student.name};{student.lastname};{student.number};{student.email};AGREGADO\n")

        return results

if __name__ == '__main__':
    csv_file = sys.argv[1]
    results_csv = sys.argv[2]
    dry_run = True if len(sys.argv) <= 3 else bool(int(sys.argv[3]))
    data = read_csv(csv_file)
    if dry_run:
        print('EJECUTANDO EN MODO DRYRUN')
    generate_users(data, results_csv, dry_run)

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