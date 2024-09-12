from flask import Flask
from data import db_session
from data.users import User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    db_session.global_init("db/mars_explorer.db")
    db_sess = db_session.create_session()
    # app.run()
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "email@email.ru"
    user.hashed_password = "scrypt:32768:8:1$CTuzOyzAT5i45DAn$f1f77531847f" \
                           "8e790ef12886f8a580e3573596aac2ff68f18a19f01b1ee383" \
                           "681db4459345f6f79f14852c735d89b52a3848d5d139d54afbb76cb70f3f3abe88"
    db_sess.add(user)

    user = User()
    user.surname = "Alex1"
    user.name = "Nic1"
    user.age = 31
    user.position = "sailor1"
    user.speciality = "engineer1"
    user.address = "module_1"
    user.email = "email1@email.ru"
    user.hashed_password = "scrypt:32768:8:1$CTuzOyzAT5i45DAn$f1f77531847f" \
                           "8e790ef12886f8a580e3573596aac2ff68f18a19f01b1ee383" \
                           "681db4459345f6f79f14852c735d89b52a3848d5d139d54afbb76cb70f3f3abe88"
    db_sess.add(user)

    user = User()
    user.surname = "Alex2"
    user.name = "Nic2"
    user.age = 32
    user.position = "sailor2"
    user.speciality = "engineer2"
    user.address = "module_2"
    user.email = "email2@email.ru"
    user.hashed_password = "scrypt:32768:8:1$CTuzOyzAT5i45DAn$f1f77531847f" \
                           "8e790ef12886f8a580e3573596aac2ff68f18a19f01b1ee383" \
                           "681db4459345f6f79f14852c735d89b52a3848d5d139d54afbb76cb70f3f3abe88"
    db_sess.add(user)

    user = User()
    user.surname = "Alex3"
    user.name = "Nic3"
    user.age = 33
    user.position = "sailor3"
    user.speciality = "engineer3"
    user.address = "module_3"
    user.email = "email3@email.ru"
    user.hashed_password = "scrypt:32768:8:1$CTuzOyzAT5i45DAn$f1f77531847f" \
                           "8e790ef12886f8a580e3573596aac2ff68f18a19f01b1ee383" \
                           "681db4459345f6f79f14852c735d89b52a3848d5d139d54afbb76cb70f3f3abe88"
    db_sess.add(user)

    db_sess.commit()


if __name__ == '__main__':
    main()
