from api import PetFriends
from conftest import ket_api_key
from datatest import TestFunc
import pytest

tf = TestFunc()
kak = ket_api_key
pf = PetFriends()

def test_add_photo_to_pet_valid_data(pet_photo = 'images/photo_2022-10-11_12-34-21.jpg'):
    '''Проверяем возможность добавления фото в карточку своего питомца'''

    pf.create_pet_simple(pytest.key, "Локи", "кошка", "15")
    _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    pytest.status, result = pf.add_photo_to_pet(pytest.key, pet_id, pet_photo)

    # Проверяем что статус ответа = 200 и id питомца соответствует заданному
    assert pytest.status == 200
    assert result['id'] == pet_id

@pytest.mark.xfail
def test_add_photo_to_pet_nonvalid_data(pet_photo = 'images/image_inc.pdf'):
    '''Проверяем возможность загрузки файла недопустимого формата'''

    pf.create_pet_simple(pytest.key, "Люксио", "попугай", "2")
    _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    pytest.status = pf.add_photo_to_pet(pytest.key, pet_id, pet_photo)

    # Проверяем что статус ответа = 400, так как формат данных отличен от допустимых (pdf)
    assert pytest.status == 400 #в настоящее время выполнение запроса приводит к ошибке 500. Баг?

def test_add_photo_to_pet_of_another_user(pet_photo = 'images/photo_2022-10-10_12-09-21.jpg'):
    '''Проверяем возможность добавления фото в карточку чужого питомца'''

    _, all_pets = pf.get_list_of_pets(pytest.key, "")
    pet_id = all_pets['pets'][0]['id']

    pytest.status, result = pf.add_photo_to_pet(pytest.key, pet_id, pet_photo)

    # Проверяем что статус ответа = 500
    assert pytest.status == 500
