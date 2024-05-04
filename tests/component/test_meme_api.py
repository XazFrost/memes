import requests

# URL сервиса
base_url = 'http://localhost:8001'
popular_memes_url = f'{base_url}/get_popular_memes'
create_meme_url = f'{base_url}/create_meme'


def test_get_popular_memes():
    response = requests.get(popular_memes_url)
    assert response.status_code == 200
    assert len(response.json()) > 0
