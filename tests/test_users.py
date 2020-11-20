from http import HTTPStatus

from app.db_models import User
from main import app
from tests.factories import UserFactory


class TestUsers:
    data = {
        'email': 'some@gmail.com',
        'password': 'password',
        'firstname': 'bob',
        'lastname': 'marley',
        'age': 25,
        'gender': 'female',
        'height': 170,
        'is_smoke': False,
        'hobbies': 2,
    }

    def test_create_user(self, client):
        url = app.url_path_for('create_user')
        response = client.post(url, json=self.data)
        assert response.status_code == HTTPStatus.CREATED

        user = User.get()
        assert user.email == self.data['email']

    def test_get_users(self, client):
        UserFactory.create_batch(size=3)

        url = app.url_path_for('get_users')
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

        assert response.json()['data']

    def test_update_user(self, client):
        user = UserFactory.create()
        url = app.url_path_for('update_user', user_id=user.id)
        response = client.patch(url, json={'firstname':'aaaa'})

        assert response.status_code == HTTPStatus.OK

    def test_delete_user(self, client):
        user = UserFactory.create()
        url = app.url_path_for('delete_user', user_id=user.id)
        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert list(User.select()) == []