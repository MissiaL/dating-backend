from http import HTTPStatus

from app.db_models import Action
from main import app
from tests.factories import ActionFactory, UserFactory


class TestActions:
    data = {
    }

    def test_create_action_like(self, client):
        first_user = UserFactory.create()
        second_user = UserFactory.create()

        self.data.update({'user':first_user.id, 'like_to_user':second_user.id, 'dislike_to_user':None})

        url = app.url_path_for('create_action')
        response = client.post(url, json=self.data)
        assert response.status_code == HTTPStatus.CREATED

        action = Action.get()
        assert action.user.id

    def test_get_actions(self, client):
        ActionFactory.create_batch(size=3)

        url = app.url_path_for('get_actions')
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

        assert response.json()['data']

    def test_update_action(self, client):
        action = ActionFactory.create()
        user = UserFactory.create()
        url = app.url_path_for('update_action', action_id=action.id)
        response = client.patch(url, json={'like_to_user':user.id, 'user':action.user.id})

        assert response.status_code == HTTPStatus.OK
        assert response.json()['data']['like_to_user']['id'] == user.id

    def test_delete_action(self, client):
        action = ActionFactory.create()
        url = app.url_path_for('delete_action', action_id=action.id)
        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert list(Action.select()) == []