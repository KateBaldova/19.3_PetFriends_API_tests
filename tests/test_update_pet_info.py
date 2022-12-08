from api import PetFriends, generate_string
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_successful_update_self_pet_info(name='Ася', animal_type='русская голубая', age=13):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_update_pet_info_of_another_user(name='Рубикон', animal_type='корги', age=3):
    """Проверяем возможность обновления информации о питомце другого юзера"""

    # Получаем ключ auth_key и список всех питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    old_name = all_pets['pets'][0]['name']

    status, result = pf.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)
    _, all_pets_new = pf.get_list_of_pets(auth_key, "")

    #Проверяем что статус ответа = 500 и имя питомца не соответствует заданному
    assert all_pets['pets'][0]['name'] == old_name
    assert name not in all_pets_new.values()
    assert status == 500 #в данный момент статус код = 200, хотя изменения данных чужого питомца не происходит. Баг?