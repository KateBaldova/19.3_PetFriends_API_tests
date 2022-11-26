from api import PetFriends
from settings import valid_email, valid_password
import os

pf = PetFriends()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    '''Проверяем возможность получения ключа аутентификации с корректными данными'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

def test_get_api_key_for_nonvalid_user(email = valid_email, password = '123456'):
    '''Проверяем возможность получения ключа аутентификации с неверным паролем'''
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result

def test_get_all_pets_with_valid_key(filter=''):
    '''Проверяем возможность получения списка всех питомцев'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0

def test_get_my_pets_with_valid_key(filter='my_pets'):
    '''Проверяем возможность применения фильтра "my_pets"'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    status, result = pf.get_list_of_pets(auth_key, filter)
    print(result)
    assert status == 200
    assert len(all_pets['pets']) > len(result['pets'])

def test_add_new_pet_with_valid_data(name = 'Ася', animal_type = 'русская голубая', age = '13', pet_photo = 'images/photo_2022-10-10_12-09-21.jpg'):
    '''Проверяем возможность добавления питомца'''
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_delete_pet_with_valid_data():
    '''Проверяем возможность удаления своего питомца'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, 'my_pets')

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/photo_2022-10-11_12-34-21.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

        # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet_petid(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()

def test_delete_pet_another_user():
    '''Проверяем возможность удаления питомца другого пользователя'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Берём id первого питомца из общего списка и отправляем запрос на удаление
    pet_id = all_pets['pets'][0]['id']
    status, _ = pf.delete_pet_petid(auth_key, pet_id)

    # Ещё раз запрашиваем список всех питомцев
    _, all_pets = pf.get_list_of_pets(auth_key, '')

    # Проверяем что статус ответа равен 403 и в списке питомцев есть id питомца, которого пытались удалить
    assert status == 403 #в настоящее время тест отрабатывает неверно - это баг, питомец удаляется, статус код 200
    assert pet_id in all_pets.values() #в настоящее время тест отрабатывает неверно - это баг, питомец удаляется, его id нет в списке всех питомцев

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

def test_create_pet_simple(name='Мурка', animal_type='дворовая', age='5'):
    '''Проверяем возможность создания питомца без загрузки фото'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name

def test_create_pet_simple_no_photo(name='Кыш', animal_type='собака', age='3'):
    '''Проверяем, что поле "фото" карточки питомца пустое при создании питомца методом create_pet_simple'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 200
    assert result['pet_photo'] == ''

def test_create_pet_simple_empty_data(name='', animal_type='', age=''):
    '''Проверяем возможность создания питомца с пустыми данными'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    assert status == 400 #данные некорректны, должен быть статус код 400. Сейчас он 200, питомец создаётся - баг
    assert result['id'] == 0

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








