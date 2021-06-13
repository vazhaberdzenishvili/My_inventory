from app import create_app
from flask_script import Manager, Server
from flask_migrate import MigrateCommand
from .db_init import InitDbCommand

manager = Manager(create_app())
manager.add_command('database', MigrateCommand)
manager.add_command('db_init', InitDbCommand)
manager.add_command('runserver', Server(port=5000))
