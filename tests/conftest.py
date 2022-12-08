import pytest
from api import PetFriends
from settings import valid_email, valid_password

pf = PetFriends()

@pytest.fixture(autouse=True)
def ket_api_key():
   """ Проверяем, что запрос api-ключа возвращает статус 200 и в результате содержится слово key"""

   # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
   status, pytest.key = pf.get_api_key(valid_email, valid_password)

   # Сверяем полученные данные с нашими ожиданиями
   assert status == 200
   assert 'key' in pytest.key

   yield

   # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
   # assert pytest.status == 200