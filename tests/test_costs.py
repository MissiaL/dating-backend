from http import HTTPStatus

import pytest

from app.db_models import Cost
from main import app
from tests.factories import CostFactory, UserFactory

class TestCosts:
    data = {
        'name': 'молоко',
        'price': 3000
    }

    def test_create_cost(self, client):
        user = UserFactory.create()

        self.data.update({'user': user.id})

        url = app.url_path_for('create_cost')
        response = client.post(url, json=self.data)
        assert response.status_code == HTTPStatus.CREATED

        cost = Cost.get()
        assert cost.user.id

    def test_get_costs(self, client):
        CostFactory.create_batch(size=3)

        url = app.url_path_for('get_costs')
        response = client.get(url)

        assert response.status_code == HTTPStatus.OK

        assert response.json()['data']

    def test_update_cost(self, client):
        cost = CostFactory.create()
        url = app.url_path_for('update_cost', cost_id=cost.id)
        response = client.patch(url, json={'name': 'хлеб', 'user': cost.user.id})

        assert response.status_code == HTTPStatus.OK
        assert response.json()['data']['name'] == 'хлеб'

    def test_delete_cost(self, client):
        cost = CostFactory.create()
        url = app.url_path_for('delete_cost', cost_id=cost.id)
        response = client.delete(url)

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert list(Cost.select()) == []
