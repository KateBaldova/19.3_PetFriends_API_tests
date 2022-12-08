from api import PetFriends
import os
from conftest import ket_api_key
from datatest import TestFunc
import pytest

tf = TestFunc()
kak = ket_api_key
pf = PetFriends()

def test_add_new_pet_with_valid_data(name = 'Ася', animal_type = 'русская голубая', age = '13', pet_photo = 'images/photo_2022-10-10_12-09-21.jpg'):
    '''Проверяем возможность добавления питомца'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    pytest.status, result = pf.add_new_pet(pytest.key, name, animal_type, age, pet_photo)
    assert pytest.status == 200
    assert result['name'] == name

def test_create_pet_simple(name='Мурка', animal_type='дворовая', age='5'):
    '''Проверяем возможность создания питомца без загрузки фото'''

    pytest.status, result = pf.create_pet_simple(pytest.key, name, animal_type, age)
    assert pytest.status == 200
    assert result['name'] == name

def test_create_pet_simple_no_photo(name='Кыш', animal_type='собака', age='3'):
    '''Проверяем, что поле "фото" карточки питомца пустое при создании питомца методом create_pet_simple'''

    pytest.status, result = pf.create_pet_simple(pytest.key, name, animal_type, age)
    assert pytest.status == 200
    assert result['pet_photo'] == ''

def test_create_pet_simple_empty_data(name='', animal_type='', age=''):
    '''Проверяем возможность создания питомца с пустыми данными'''

    pytest.status, result = pf.create_pet_simple(pytest.key, name, animal_type, age)
    assert pytest.status == 400 #данные некорректны, должен быть статус код 400. Сейчас он 200, питомец создаётся - баг
    assert result['id'] == 0