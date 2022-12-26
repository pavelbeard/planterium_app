import json
import unittest

from fastapi.testclient import TestClient

from main import app


class TestAPI(unittest.TestCase):
    client = TestClient(app)
    headers = {"Content-Type": "application/json"}

    def test_main(self):
        response = self.client.get('/api/main')
        assert response.status_code == 200
        assert response.json() == {'1': '1'}

    def test_get_plants(self):
        response = self.client.get('/get_plants/1')
        assert response.status_code == 200
        assert response.json() == {'plant_id': 1}

    def test_post_customer(self):
        data = {"first_name": "pavel", "last_name": "borodin"}
        response = self.client.post('/app/post_customer', json=data)
        assert response.status_code == 200
        assert response.json() == {"load": "done"}

    def test_post_plant(self):
        data = [
            {"plant_image": "http://localhost:8002/images/pexels-kek-roseclay-912413.jpg",
             "plant_name": "цветок kek", "plant_text": "отличный цветок kek!", "with_transplant": True,
             "amount": 2},
            {"plant_image": "http://localhost:8002/images/pexels-islam-roseclay-912413.jpg",
             "plant_name": "цветок islam", "plant_text": "отличный цветок islam!", "with_transplant": False,
             "amount": 10},
        ]

        response = self.client.post('/app/post_plant', content=json.dumps(data), headers=self.headers)
        assert response.status_code == 200
        assert response.json() == {'load_plant': 'done'}

    def test_get_plant(self):
        response = self.client.get('/app/get_plant/1')
        assert response.status_code == 200

    def test_add_admin(self):
        data = {"user_id": 1131}
        response = self.client.post("/api/create_admin", headers=self.headers, content=json.dumps(data))
        assert response.status_code == 200

    def test_get_admins(self):
        response = self.client.get("/api/get_admins", headers=self.headers)
        assert type(response.json()) == list
        assert response.status_code == 200

    # TODO: разобраться с миграциями
    # TODO: написать тесты для остальных endpoints