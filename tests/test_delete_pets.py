from api import PetFriends
from conftest import ket_api_key
from datatest import TestFunc
import pytest

tf = TestFunc()
kak = ket_api_key
pf = PetFriends()

def test_delete_pet_with_valid_data():
    '''Проверяем возможность удаления своего питомца'''

    _, my_pets = pf.get_list_of_pets(pytest.key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(pytest.key, "Суперкот", "кот", "3", "images/photo_2022-10-11_12-34-21.jpg")
        _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    pytest.status, _ = pf.delete_pet_petid(pytest.key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(pytest.key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert pytest.status == 200
    assert pet_id not in my_pets.values()

@pytest.mark.fail
def test_delete_pet_another_user():
    '''Проверяем возможность удаления питомца другого пользователя'''

    _, all_pets = pf.get_list_of_pets(pytest.key, '')

    # Берём id первого питомца из общего списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][0]['id']
    pytest.status, _ = pf.delete_pet_petid(pytest.key, pet_id)

    # Ещё раз запрашиваем список всех питомцев
    _, all_pets = pf.get_list_of_pets(pytest.key, '')

    # Проверяем что статус ответа равен 403 и в списке питомцев есть id питомца, которого пытались удалить
    assert pytest.status == 403 #в настоящее время тест отрабатывает неверно - это баг, питомец удаляется, статус код 200
    assert pet_id in all_pets.values() #в настоящее время тест отрабатывает неверно - это баг, питомец удаляется, его id нет в списке всех питомцев