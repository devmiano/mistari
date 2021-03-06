from app import create_app, db
from flask_script import Manager, Server
from flask_migrate import Migrate, MigrateCommand
from app.models import *

# app = create_app('development')
app = create_app('production')


manager = Manager(app)
migrate = Migrate(app, db)
'''function to import and execute the application with the specified server'''
manager.add_command('server', Server)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.shell
def make_shell_context():
    return dict(app=app, db=db, User=User, Pitch=Pitch, Category=Category, Comment=Comment, Upvote=Upvote, Downvote=Downvote)


if __name__ == '__main__':
    manager.run()
