import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_cors import CORS, cross_origin

from app.main.model import user, property, property_model, portfolio, property_portfolio, document, team, user_team, team_portfolio
from app.main import create_app, db
from app import blueprint
from app.main.model import blacklist
from app.main.util.janitor import clean_database
from app.main.util.data_uploader import upload_data, clear_data

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
# Eliminate CORS issue.
CORS(app)
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run(host='192.168.1.26')

@manager.command
def populate_db():
    upload_data()

@manager.command
def clear_db(): 
    clear_data()

@manager.command
def run_janitor():
    clean_database()

@manager.command
def test():
    """Runs the unit tests."""
    tests = unittest.TestLoader().discover('app/test', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

if __name__ == '__main__':
    manager.run()
