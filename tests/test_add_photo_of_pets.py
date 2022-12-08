from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_add_photo_to_pet_valid_data(pet_photo = 'images/photo_2022-10-11_12-34-21.jpg'):
    '''Проверяем возможность добавления фото в карточку своего питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.create_pet_simple(auth_key, "Лори", "кошка", "11")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 200 и id питомца соответствует заданному
    assert status == 200
    assert result['id'] == pet_id

def test_add_photo_to_pet_nonvalid_data(pet_photo = 'images/image_inc.pdf'):
    '''Проверяем возможность загрузки файла недопустимого формата'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pf.create_pet_simple(auth_key, "Люксио", "попугай", "2")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']

    status = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 400, так как формат данных отличен от допустимых (pdf)
    assert status == 400 #в настоящее время выполнение запроса приводит к ошибке 500. Баг?

def test_add_photo_to_pet_of_another_user(pet_photo = 'images/photo_2022-10-10_12-09-21.jpg'):
    '''Проверяем возможность добавления фото в карточку чужого питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, all_pets = pf.get_list_of_pets(auth_key, "")
    pet_id = all_pets['pets'][0]['id']

    status, result = pf.add_photo_to_pet(auth_key, pet_id, pet_photo)

    # Проверяем что статус ответа = 500
    assert status == 500
