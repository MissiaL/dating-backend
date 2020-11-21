import click
import uvicorn

from app import db_models
from app.database import db


@click.group()
def cli() -> None:
    pass

def create_db():
    db.connect()
    db.create_tables([db_models.User, db_models.Cost, db_models.Action, db_models.Photo, db_models.Message])
    db.close()
    click.secho("\nCreate DB tables!", fg='green')

@cli.command()
def generate() -> None:
    """
    Generates some initial records in database
    """
    from tests.factories import UserFactory, ActionFactory, MessageFactory, CostFactory
    db.connect()
    db.create_tables([db_models.User, db_models.Cost, db_models.Action, db_models.Photo, db_models.Message])

    # will generate the whole database by chain of subfactories
    UserFactory.create_batch(size=5)
    ActionFactory.create_batch(size=5)
    MessageFactory.create_batch(size=5)
    CostFactory.create_batch(size=5)
    click.secho("\nGeneration done!", fg='green')
    db.close()


@cli.command()
def runserver() -> None:
    """
    Runs application server
    """
    from app.settings import settings
    from main import app

    create_db()

    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        debug=settings.debug,
        access_log=False,
        timeout_keep_alive=10,
    )
