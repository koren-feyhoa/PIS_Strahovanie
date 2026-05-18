import pytest
from datetime import date, datetime
from domain.entities.ClientEntity import ClientEntity
from domain.entities.ApplicationEntity import ApplicationEntity
from domain.entities.ContractEntity import ContractEntity
from domain.entities.ProfileEntity import ProfileEntity


# ------------------------------------------------------------
# Тесты для ClientEntity
# ------------------------------------------------------------
class TestClientEntity:
    def test_create_valid_client(self):
        client = ClientEntity.create(
            fullname="Иванов Иван Иванович",
            phone="+79231234567",
            email="ivan@example.com",
            password="hash123"
        )
        assert client.fullname == "Иванов Иван Иванович"
        assert client.phone == "+79231234567"
        assert client.email == "ivan@example.com"
        assert client.password == "hash123"
        # id не задан, должен быть None
        assert client.id is None

    def test_empty_fullname_raises_error(self):
        with pytest.raises(ValueError, match="ФИО не может быть пустым"):
            ClientEntity.create(fullname="", phone="+79231234567", email="test@test.ru", password="123")

    def test_invalid_email_raises_error(self):
        with pytest.raises(ValueError, match="Некорректный email"):
            ClientEntity.create(fullname="Test", phone="+79231234567", email="invalid", password="123")

    def test_invalid_phone_format_raises_error(self):
        with pytest.raises(ValueError, match="Неверный формат номера телефона"):
            ClientEntity.create(fullname="Test", phone="not a phone", email="test@test.ru", password="123")

    def test_invalid_phone_number_raises_error(self):
        with pytest.raises(ValueError, match="Введите корректный номер телефона"):
            # Номер с неверной длиной или несуществующий код страны
            ClientEntity.create(fullname="Test", phone="+123", email="test@test.ru", password="123")

# ------------------------------------------------------------
# Тесты для ApplicationEntity
# ------------------------------------------------------------
class TestApplicationEntity:
    def test_create_valid_application(self):
        app = ApplicationEntity.create(
            client_id=1,
            agent_id=2,
            insurance_type="ОСАГО",
            profile_id=5,
            status_application="Новая"
        )
        assert app.client_id == 1
        assert app.agent_id == 2
        assert app.insurance_type == "ОСАГО"
        assert app.profile_id == 5
        assert app.status_application == "Новая"
        assert app.calculate_price is None  # не передавали
        assert isinstance(app.data_create, datetime)

    def test_create_default_status(self):
        app = ApplicationEntity.create(
            client_id=1, agent_id=1, insurance_type="Клещ", profile_id=1
        )
        assert app.status_application == "Заявка в обработке"

    def test_empty_insurance_type_raises_error(self):
        with pytest.raises(ValueError, match="Тип страхования обязателен"):
            ApplicationEntity.create(
                client_id=1, agent_id=1, insurance_type="", profile_id=1
            )

    def test_invalid_insurance_type_raises_error(self):
        with pytest.raises(ValueError, match="Тип документа должен быть из списка"):
            ApplicationEntity.create(
                client_id=1, agent_id=1, insurance_type="Медицина", profile_id=1
            )

    def test_negative_price_raises_error(self):
        # Цена не передаётся в create, но может быть установлена позже
        app = ApplicationEntity.create(
            client_id=1, agent_id=1, insurance_type="ОСАГО", profile_id=1
        )
        with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
            app.calculate_price = -100
            app.__post_init__()  # повторно вызываем валидацию (обычно не нужно, но для теста)
        # Проверка при прямом создании через конструктор
        with pytest.raises(ValueError, match="Цена не может быть отрицательной"):
            ApplicationEntity(
                id=None,
                client_id=1,
                agent_id=1,
                insurance_type="ОСАГО",
                data_create=datetime.now(),
                profile_id=1,
                status_application="new",
                calculate_price=-50
            )

# ------------------------------------------------------------
# Тесты для ContractEntity
# ------------------------------------------------------------
class TestContractEntity:
    def test_create_valid_contract(self):
        start = date(2025, 1, 1)
        end = date(2025, 12, 31)
        contract = ContractEntity.create(
            client_id=1,
            application_id=10,
            agent_id=2,
            contract_number="CONT-001",
            start_date=start,
            end_date=end,
            file_name="doc.pdf",
            file_path="/files/1",
            file_time=datetime(2025, 1, 1, 12, 0),
            status="Активен"
        )
        assert contract.client_id == 1
        assert contract.application_id == 10
        assert contract.contract_number == "CONT-001"
        assert contract.start_date == start
        assert contract.end_date == end
        assert contract.file_name == "doc.pdf"
        assert contract.file_path == "/files/1"
        assert contract.file_time == datetime(2025, 1, 1, 12, 0)
        assert contract.status_contract == "Активен"

    def test_create_with_default_status(self):
        contract = ContractEntity.create(
            client_id=1, application_id=1, agent_id=1,
            contract_number="C-001",
            start_date=date(2025,1,1), end_date=date(2025,12,31),
            file_name="f.txt", file_path="/tmp", file_time=datetime.now()
        )
        assert contract.status_contract == "Посмотреть"

    def test_start_date_after_end_date_raises_error(self):
        with pytest.raises(ValueError, match="Дата начала должна быть раньше даты окончания"):
            ContractEntity.create(
                client_id=1, application_id=1, agent_id=1,
                contract_number="C-001",
                start_date=date(2025,12,31), end_date=date(2025,1,1),
                file_name="f.txt", file_path="/tmp", file_time=datetime.now()
            )

    def test_empty_contract_number_raises_error(self):
        with pytest.raises(ValueError, match="Номер договора не может быть пустым"):
            ContractEntity.create(
                client_id=1, application_id=1, agent_id=1,
                contract_number="   ",
                start_date=date(2025,1,1), end_date=date(2025,12,31),
                file_name="f.txt", file_path="/tmp", file_time=datetime.now()
            )

    def test_missing_file_fields_raises_error(self):
        with pytest.raises(ValueError, match="Файл не загружен"):
            ContractEntity.create(
                client_id=1, application_id=1, agent_id=1,
                contract_number="C-001",
                start_date=date(2025,1,1), end_date=date(2025,12,31),
                file_name=None, file_path="/tmp", file_time=datetime.now()
            )
        with pytest.raises(ValueError, match="Файл не загружен"):
            ContractEntity.create(
                client_id=1, application_id=1, agent_id=1,
                contract_number="C-001",
                start_date=date(2025,1,1), end_date=date(2025,12,31),
                file_name="f.txt", file_path=None, file_time=datetime.now()
            )
        with pytest.raises(ValueError, match="Файл не загружен"):
            ContractEntity.create(
                client_id=1, application_id=1, agent_id=1,
                contract_number="C-001",
                start_date=date(2025,1,1), end_date=date(2025,12,31),
                file_name="f.txt", file_path="/tmp", file_time=None
            )

# ------------------------------------------------------------
# Тесты для ProfileEntity
# ------------------------------------------------------------
class TestProfileEntity:
    def test_create_valid_profile(self):
        info = {"series": "1234", "number": "567890"}
        profile = ProfileEntity.create(
            client_id=1,
            type_document="Паспорт РФ",
            info=info
        )
        assert profile.client_id == 1
        assert profile.type_document == "Паспорт РФ"
        assert profile.info == info

    def test_empty_type_document_raises_error(self):
        with pytest.raises(ValueError, match="Тип документа не указан"):
            ProfileEntity.create(client_id=1, type_document="", info={"a": 1})

    def test_invalid_type_document_raises_error(self):
        with pytest.raises(ValueError, match="Тип документа должен быть из списка"):
            ProfileEntity.create(client_id=1, type_document="Справка", info={"a": 1})

    def test_empty_info_raises_error(self):
        with pytest.raises(ValueError, match="Заполните все поля"):
            ProfileEntity.create(client_id=1, type_document="Паспорт РФ", info={})

# ------------------------------------------------------------
# Параметризованные тесты для ClientEntity
# ------------------------------------------------------------
import pytest

class TestClientEntityExtended:
    @pytest.mark.parametrize("fullname, phone, email, password", [
        ("Петров Пётр Петрович", "+79123456789", "petrov@mail.ru", "hash456"),
        ("Анна", "+375291234567", "anna@gmail.com", "qwerty"),  # белорусский номер
        ("John Doe", "+447911123456", "john@example.com", "pass"),  # британский
    ])
    def test_create_multiple_valid_clients(self, fullname, phone, email, password):
        client = ClientEntity.create(fullname, phone, email, password)
        assert client.fullname == fullname
        assert client.phone == phone
        assert client.email == email
        assert client.password == password

    @pytest.mark.parametrize("invalid_phone", [
        "12345",
        "+000",
        "8-800-555-35-35",
        "abc",
        "+791234567890",  # слишком длинный
        "+71234567890",   # несуществующий код
    ])
    def test_invalid_phone_variants_raise_error(self, invalid_phone):
        with pytest.raises(ValueError, match="корректный номер|формат номера"):
            ClientEntity.create("Имя", invalid_phone, "test@test.ru", "123")

    @pytest.mark.parametrize("invalid_email", [
        "missing_at",
        "user@domain",
        "@domain.com",
        "user@.com",
        "user@domain.c",
    ])
    def test_invalid_email_variants_raise_error(self, invalid_email):
        with pytest.raises(ValueError, match="Некорректный email"):
            ClientEntity.create("Имя", "+79231234567", invalid_email, "123")


# ------------------------------------------------------------
# Дополнительные тесты для ApplicationEntity
# ------------------------------------------------------------
class TestApplicationEntityExtended:
    @pytest.mark.parametrize("insurance_type", ["Клещ", "Животное", "ОСАГО", "ВетПаспорт"])
    def test_valid_insurance_types(self, insurance_type):
        app = ApplicationEntity.create(
            client_id=1, agent_id=1, insurance_type=insurance_type, profile_id=1
        )
        assert app.insurance_type == insurance_type

    def test_calculate_price_default_is_none(self):
        app = ApplicationEntity.create(1, 1, "ОСАГО", 1)
        assert app.calculate_price is None

    def test_status_application_default(self):
        app = ApplicationEntity.create(1, 1, "ОСАГО", 1)
        assert app.status_application == "Заявка в обработке"

    def test_create_with_custom_status(self):
        app = ApplicationEntity.create(1, 1, "ОСАГО", 1, status_application="Одобрена")
        assert app.status_application == "Одобрена"

    def test_data_create_is_auto_set(self):
        before = datetime.now()
        app = ApplicationEntity.create(1, 1, "ОСАГО", 1)
        after = datetime.now()
        assert before <= app.data_create <= after


# ------------------------------------------------------------
# Дополнительные тесты для ContractEntity (включая метод update_status_by_date)
# ------------------------------------------------------------
class TestContractEntityExtended:
    def test_contract_number_with_spaces_only_raises(self):
        with pytest.raises(ValueError, match="Номер договора не может быть пустым"):
            ContractEntity.create(
                client_id=1, application_id=1, agent_id=1,
                contract_number="   ",
                start_date=date.today(), end_date=date.today(),
                file_name="f.txt", file_path="/tmp", file_time=datetime.now()
            )








# ------------------------------------------------------------
# Дополнительные тесты для ProfileEntity
# ------------------------------------------------------------
class TestProfileEntityExtended:
    @pytest.mark.parametrize("doc_type", ["Паспорт РФ", "Водительские права", "Машина", "ВетПаспорт"])
    def test_valid_document_types(self, doc_type):
        profile = ProfileEntity.create(1, doc_type, {"key": "value"})
        assert profile.type_document == doc_type

    def test_info_dict_can_contain_nested_data(self):
        info = {
            "series": "1234",
            "number": "567890",
            "issue_date": "2020-01-01",
            "issued_by": "MVD"
        }
        profile = ProfileEntity.create(1, "Паспорт РФ", info)
        assert profile.info == info

    def test_info_is_stored_as_dict(self):
        info = {"a": 1, "b": [2, 3]}
        profile = ProfileEntity.create(1, "Водительские права", info)
        assert isinstance(profile.info, dict)
        assert profile.info["b"][1] == 3