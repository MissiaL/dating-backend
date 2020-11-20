from http import HTTPStatus

from app.db_models import Message
from main import app
from tests.factories import MessageFactory, UserFactory


class TestMessages:
    data = {
        'text': 'bob',
    }

    def test_create_message(self, client):
        first_user = UserFactory.create()
        second_user = UserFactory.create()
        self.data.update({'user':first_user.id, 'to_user':second_user.id})

        url = app.url_path_for('create_message')
        response = client.post(url, json=self.data)
        assert response.status_code == HTTPStatus.CREATED

        message = Message.get()
        assert message.text == self.data['text']

    def test_get_messages(self, client):
        MessageFactory.create_batch(size=3)

        url = app.url_path_for('get_messages')
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

        assert response.json()['data']

    def test_update_message(self, client):
        message = MessageFactory.create()
        message2 = MessageFactory.create()
        url = app.url_path_for('update_message', message_id=message2.id)
        response = client.patch(url, json={'text':'aaaa', 'user':message2.user.id})

        assert response.status_code == HTTPStatus.OK
        assert response.json()['data']['text'] == 'aaaa'

    def test_delete_message(self, client):
        message = MessageFactory.create()
        url = app.url_path_for('delete_message', message_id=message.id)
        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert list(Message.select()) == []