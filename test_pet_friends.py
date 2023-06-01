from api import PetFriends
from settings import valid_email, valid_password, invalid_email, invalid_password
import os

pf = PetFriends()

def test_add_new_pet_simple_with_valid_data(name='Lola', animal_type='shark', age='4'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 200
    assert result['name'] == name


def test_add_photo_valid_pet(pet_photo='images/cat.jpg'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    if len(my_pets['pets'])>0:
        status,result = pf.add_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert result['pet_photo'] == my_pets['pets'][0]['pet_photo']
    else:
        raise Exception("There is no my pets")


def test_get_api_key_for_invalid_user(email=invalid_email, password=invalid_password):

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_add_new_pet_simple_with_invalid_data(name='Lola', animal_type='shark',
                                             age='jjghhjfdkjsehfhbcer000gidjsehrfnvv!!!bfcnvjgrjvvjfjfjhd'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
    assert result['name'] == name

def test_add_new_pet_simple_with_missed_data(name='', animal_type='shark',
                                             age='2'):

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_simple(auth_key, name, animal_type, age)

    assert status == 400
    assert result['name'] == name


def test_wrong_update_self_pet_info(name='@#%#%@!', animal_type='', age=0):

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][-1]['id'], name, animal_type, age)

        assert status == 400
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_get_all_pets_with_invalid_key(filter=''):

    _, auth_key = pf.get_api_key(invalid_email, invalid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    assert status == 403


def test_add_new_pet_with_valid_data_with_invalid_photo(name='Tom', animal_type='dog',
                                     age='1', pet_photo='images/test_photo'):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['name'] == name


def test_delete_pet_with_invalid_key():

    _, auth_key = pf.get_api_key(valid_email, invalid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet_with_photo(auth_key, "Sam", "cat", "3", "images/cat.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 403

def test_add_new_pet_with_missed_data(name='', animal_type='',
                                     age='', pet_photo=''):

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_new_pet_with_photo(auth_key, name, animal_type, age, pet_photo)

    assert status == 400
    assert result['name'] == name

