from http import HTTPStatus

import pytest

from app.db_models import Photo
from main import app
from tests.factories import PhotoFactory

@pytest.mark.skip()
class TestPhotos:
    data = {
        'is_main': True,
        'password': 'password',
        'firstname': 'bob',
        'lastname': 'marley',
        'age': 25,
        'gender': 'female',
        'height': 170,
        'is_smoke': False,
        'hobbies': 2,
    }

    def test_create_photo(self, client):
        url = app.url_path_for('create_photo')
        response = client.post(url, json=self.data)
        assert response.status_code == HTTPStatus.CREATED

        photo = Photo.get()
        assert photo.email == self.data['email']

    def test_get_photos(self, client):
        PhotoFactory.create_batch(size=3)

        url = app.url_path_for('get_photos')
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

        assert response.json()['data']

    def test_update_photo(self, client):
        photo = PhotoFactory.create()
        url = app.url_path_for('update_photo', photo_id=photo.id)
        response = client.patch(url, json={'firstname':'aaaa'})

        assert response.status_code == HTTPStatus.OK

    def test_delete_photo(self, client):
        photo = PhotoFactory.create()
        url = app.url_path_for('delete_photo', photo_id=photo.id)
        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert list(Photo.select()) == []