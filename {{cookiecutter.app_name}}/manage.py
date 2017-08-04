#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
from flask_script import Manager, Shell, Server
from flask_migrate import MigrateCommand

from {{ cookiecutter.app_name }}.app import create_app
import {{ cookiecutter.app_name }}.models as models
from {{ cookiecutter.app_name }}.database import db
try:
    import {{ cookiecutter.app_name }}.settings_local as settings
except ImportError:
    import {{ cookiecutter.app_name }}.settings as settings

env = os.environ.get('env', 'Local')

config_object = getattr(settings, env)
app = create_app(config_object=config_object)

manager = Manager(app)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': app, 'db': db, 'models': models}


@manager.command
def test():
    import subprocess
    command = 'nosetests --cover-erase --with-xunit --with-coverage --cover-package={{ cookiecutter.app_name }}'.split(' ')
    return subprocess.call(command)

manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    sys.stdout.flush()
    manager.run()
