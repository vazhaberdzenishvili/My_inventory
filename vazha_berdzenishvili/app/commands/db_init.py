from flask_script import Command
from app.models import db
from app.models.user import UserModel,Role


class InitDbCommand(Command):
    def run(self):
        init_db()


def init_db():
    db.drop_all()
    db.create_all()
    populate_db()


def populate_db():
    # for users in user_data:
    #     users = UserModel(**users)
    admin_role = find_or_create_role("Admin")

    find_or_create_user(
        firstname="nick",
        lastname="smth",
        username="smth1234",
        email="smth@mail.ru",
        password="pass1234",
        role=admin_role,
    )

    find_or_create_user(
        firstname="user1",
        lastname="user1",
        username="user0001",
        email="user@mail.ru",
        password="user1234",
    )
    db.session.commit()


def find_or_create_role(name):
    role = Role.query.filter_by(name=name).first()
    if not role:
        role = Role(name)
        db.session.add(role)
    return role


def find_or_create_user(firstname, lastname, username, password, email, role=None):
    user = UserModel.query.filter_by(email=email).first()
    if not user:
        user = UserModel(firstname=firstname,
                         lastname=lastname,
                         username=username,
                         password=password,
                         email=email)
        if role:
            user.roles.append(role)
            print(user.roles)

        db.session.add(user)

    return user
