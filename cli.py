import click
import uvicorn


@click.group()
def cli() -> None:
    pass

#
# @cli.command()
# def generate() -> None:
#     """
#     Generates some initial records in database
#     """
#     from tests.factories import StudentAnswerFactory
#
#     # will generate the whole database by chain of subfactories
#     StudentAnswerFactory.create_batch(size=5)
#     click.secho("\nGeneration done!", fg='green')
#

@cli.command()
def runserver() -> None:
    """
    Runs application server
    """
    from app.settings import settings
    from main import app

    uvicorn.run(
        app,
        host=settings.app_host,
        port=settings.app_port,
        debug=settings.debug,
        access_log=False,
        timeout_keep_alive=10,
    )
