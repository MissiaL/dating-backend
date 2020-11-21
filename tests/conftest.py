import pathlib

from pytest import fixture
from starlette.testclient import TestClient

from app.database import db, BaseModel
from main import app
from app import db_models

@fixture
def client():
    client = TestClient(app)
    return client


@fixture(autouse=True, scope="session")
def test_db():
    db.connect()
    tables = [db_models.User, db_models.Message, db_models.Photo, db_models.Cost, db_models.Action]
    db.drop_tables(tables)
    db.create_tables(tables)
    yield db
    db.drop_tables(tables)
    db.close()

@fixture(autouse=True)
def transaction(test_db):
    test_db.create_tables(BaseModel.__subclasses__())
    yield
    test_db.drop_tables(BaseModel.__subclasses__())

@fixture()
def image():
    p = pathlib.Path(__file__).parent.absolute() / 'photo.jpg'
    return p.open('rb')