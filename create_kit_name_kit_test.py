import sender_stand_request
import data


def get_new_user_token():
    # хотим переиспользовать одного пользователя для всех тестов
    # поэтому сохраняем токен в словарь session_data и не создаем
    # нового пользователя (для нового токена) без необходимости
    if data.session_data["user_token"] is None:
        new_user_response = sender_stand_request.post_new_user(data.user_body)
        data.session_data["user_token"] = new_user_response.json()["authToken"]

    return data.session_data["user_token"]


def positive_assert(kit_body):
    # Позитивная проверка:
    # Код ответа от API = 201
    # В теле ответа поле "name" совпадает с полем "name" в запросе
    new_kit_reponse = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    assert new_kit_reponse.status_code == 201
    assert new_kit_reponse.json()["name"] == kit_body["name"]


def negative_assert(kit_body):
    # Негативная проверка:
    # Код ответа от API = 400
    new_kit_reponse = sender_stand_request.post_new_client_kit(kit_body, get_new_user_token())

    assert new_kit_reponse.status_code == 400


def get_kit_body(kit_name):
    # Создаем копию тела запроса по умочанию
    # Меняем "name" в словаре на переданное значение
    body = data.kit_body.copy()
    body["name"] = kit_name
    return body


# Тест 1. Успешное создание набора
# Параметр name состоит из 1 символа
def test_create_kit_1_char_in_name_get_success_response():
    positive_assert(get_kit_body("a"))


# Тест 2. Успешное создание набора
# Параметр name состоит из 511 символов
def test_create_kit_511_chars_in_name_get_success_response():
    positive_assert(
        get_kit_body(
            "Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdAbcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabC"
        )
    )


# Тест 3. Ошибка
# Параметр name состоит из пустой строки
def test_create_kit_empty_name_get_error_response():
    negative_assert(get_kit_body(""))


# Тест 4. Ошибка
# Параметр name состоит из 512 символов
def test_create_kit_512_chars_in_name_get_success_response():
    negative_assert(
        get_kit_body(
            "Abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdAbcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcdabcd"
            "abcdabcdabcdabcdabcdabcdabcdabcdabcD"
        )
    )


# Тест 5. Успешное создание набора
# Параметр name состоит из английских букв
def test_create_kit_english_letter_in_name_get_success_response():
    positive_assert(get_kit_body("QWErty"))


# Тест 6. Успешное создание набора
# Параметр name состоит из русских букв
def test_create_kit_russian_letter_in_name_get_success_response():
    positive_assert(get_kit_body("Мария"))


# Тест 7. Успешное создание набора
# Параметр name состоит из строки спецсимволов
def test_create_kit_has_special_symbol_in_name_get_success_response():
    positive_assert(get_kit_body('"№%@",'))


# Тест 8. Успешное создание набора
# Параметр name состоит из слов с пробелами
def test_create_kit_has_space_in_name_get_success_response():
    positive_assert(get_kit_body("Человек и КО"))


# Тест 9. Успешное создание набора
# Параметр name состоит из цифр
def test_create_kit_has_number_in_name_get_success_response():
    positive_assert(get_kit_body("123"))


# Тест 10. Ошибка
# Параметр name не передан
def test_create_kit_no_name_get_error_response():
    # get_kit_body гарантированно создает копию словаря kit_body
    body = get_kit_body("")
    body.pop("name")
    negative_assert(body)


# Тест 12. Ошибка
# Тип параметра name: число
def test_create_kit_number_type_name_get_error_response():
    negative_assert(get_kit_body(123))
