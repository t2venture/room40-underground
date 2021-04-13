import os
import unittest

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from app.main.model import user, activity, assessment, company_activity, company_assessment, company, deal_event, deal_investor, deal_note, deal, event_participant, event, note, user_company, user_company, vote
from app.main import create_app, db
from app import blueprint
from app.main.model import blacklist

app = create_app(os.getenv('BOILERPLATE_ENV') or 'dev')
app.register_blueprint(blueprint)

app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def run():
    app.run()

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

#TODO: Change all mapping tables "Save" service method to only take in data and pass in a dictionary with current params. Just like user_company_serivce
#TODO: Search functionality