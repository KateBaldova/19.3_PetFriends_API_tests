import pytest
from api import PetFriends
from conftest import ket_api_key
from datatest import TestFunc

pf = PetFriends()
tf = TestFunc()
kak = ket_api_key

@pytest.mark.parametrize("filter",
                        [
                            tf.generate_string(255)
                            , tf.generate_string(1000)
                            , tf.russian_chars()
                            , tf.russian_chars().upper()
                            , tf.chinese_chars()
                            , tf.special_chars()
                            , 123
                        ],
                        ids =
                        [
                            '255 symbols'
                            , 'more than 1000 symbols'
                            , 'russian'
                            , 'RUSSIAN'
                            , 'chinese'
                            , 'specials'
                            , 'digit'
                        ])
def test_get_all_pets_with_negative_filter(filter):
   pytest.status, result = pf.get_list_of_pets(pytest.key, filter)

   # Проверяем статус ответа
   assert pytest.status == 400


@pytest.mark.parametrize("filter",
                        ['', 'my_pets'],
                        ids=['empty string', 'only my pets'])
def test_get_all_pets_with_valid_key(filter):
   pytest.status, result = pf.get_list_of_pets(pytest.key, filter)

   # Проверяем статус ответа
   assert pytest.status == 200
   assert len(result['pets']) > 0