from flask.cli import FlaskGroup
from flask_migrate import MigrateCommand

from app import create_app

app = create_app()
cli = FlaskGroup(create_app=create_app)
cli.add_command('db', MigrateCommand)


if __name__ == '__main__':
    cli()
