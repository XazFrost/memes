import requests

base_url = 'http://localhost:8000'
add_meme_url = f'{base_url}/add_meme'
get_memes_url = f'{base_url}/memes'
get_meme_by_id_url = f'{base_url}/get_meme_by_id'
delete_meme_url = f'{base_url}/delete_meme'

new_meme = {
    "id": 99,
    "name": "Distracted Boyfriend",
    "description": "A meme showing a man looking at another woman while his girlfriend is displeased.",
    "image_url": "https://example.com/distracted-boyfriend.jpg"
}


def test_1_add_meme():
    response = requests.post(add_meme_url, json=new_meme)
    assert response.status_code == 200
    assert response.json()['name'] == new_meme['name']


def test_2_get_memes():
    response = requests.get(get_memes_url)
    assert response.status_code == 200
    assert len(response.json()) > 0


def test_3_get_meme_by_id():
    response = requests.get(f"{get_meme_by_id_url}/99")
    assert response.status_code == 200
    assert response.json()['id'] == 99


def test_4_delete_meme():
    delete_response = requests.delete(f"{delete_meme_url}/99")
    assert delete_response.status_code == 200

    response = requests.get(f"{get_meme_by_id_url}/99")
    assert response.status_code == 404
