from api import PetFriends
from settings import valid_email, valid_password
from datatest import TestFunc
import pytest

pf = PetFriends()
tf = TestFunc()

def test_get_api_key_for_valid_user(email = valid_email, password = valid_password):
    '''Проверяем возможность получения ключа аутентификации с корректными данными'''
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result

@pytest.mark.xfail
@pytest.mark.parametrize("email", [
                            valid_email
                            , ''
                            , tf.generate_string(255)
                            , tf.generate_string(1000)
                            , tf.russian_chars()
                            , tf.russian_chars().upper()
                            , tf.chinese_chars()
                            , tf.special_chars()
                            , 123
                        ],
                        ids =
                        [
                            'valid'
                            , 'empty'
                            , '255 symbols'
                            , 'more than 1000 symbols'
                            , 'russian'
                            , 'RUSSIAN'
                            , 'chinese'
                            , 'specials'
                            , 'digit'
                        ])
@pytest.mark.parametrize("password",
                         [
                             ''
                             , tf.generate_string(255)
                             , tf.generate_string(1000)
                             , tf.russian_chars()
                             , tf.russian_chars().upper()
                             , tf.chinese_chars()
                             , tf.special_chars()
                             , 123
                         ],
                         ids=
                         [
                             'empty'
                             , '255 symbols'
                             , 'more than 1000 symbols'
                             , 'russian'
                             , 'RUSSIAN'
                             , 'chinese'
                             , 'specials'
                             , 'digit'
                         ])
def test_get_api_key_for_nonvalid_user(email, password):
    '''Проверяем возможность получения ключа аутентификации с неверным паролем'''

    pytest.status, result = pf.get_api_key(email, password)

    # Проверяем статус ответа
    assert pytest.status == 403
    assert 'key' not in result








