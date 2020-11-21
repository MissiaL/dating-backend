from http import HTTPStatus

import pytest

from app.db_models import Photo
from main import app
from tests.factories import PhotoFactory, UserFactory



class TestPhotos:

    def test_create_photo(self, client, image):
        user = UserFactory.create()
        url = app.url_path_for('create_photo')
        multipart_form_data = {
            'image': ('image.jpg', image),
            'user': (None, str(user.id)),
            'is_main': (None, 'false')
        }
        response = client.post(url, files=multipart_form_data)
        assert response.status_code == HTTPStatus.CREATED

        photo = Photo.get()
        assert photo.id

    def test_get_photos(self, client):
        PhotoFactory.create_batch(size=3)

        url = app.url_path_for('get_photos')
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

        assert response.json()['data']

    def test_delete_photo(self, client):
        photo = PhotoFactory.create()
        url = app.url_path_for('delete_photo', photo_id=photo.id)
        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert list(Photo.select()) == []