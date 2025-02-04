from codenames import app

from fastapi.testclient import TestClient


def test_create_room():
    client = TestClient(app)
    words = ["Admin" for _ in range(25)]
    colors = ["red"] * 25

    response = client.post("/room", json={"words": words, "colors": colors})
    assert response.status_code == 201
    response.json()

    room_id = response.json()["id"]
    token = response.json()["token"]
    auth_header = {"Authorization": f"Bearer {token}"}
    room_response = client.get(f"/room/{room_id}", headers=auth_header)
    assert room_response.status_code == 200
    room_data = room_response.json()
    assert room_data["words"] == words
    assert room_data["colors"] == colors

    delete_response = client.delete(
        f"/room/{room_id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert delete_response.status_code == 200

    second_room_response = client.get(f"/room/{room_id}", headers=auth_header)
    assert second_room_response.status_code == 404
