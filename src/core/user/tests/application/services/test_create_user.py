import pytest
from src.core.user.application.service.create_user import CreateUser
from src.core.user.domain.dto.user_dto import InputCreateUser
from src.core.user.domain.exceptions.user_exceptions import (
    InvalidUserError,
    UserAlreadyExistError,
)
from src.core.user.infra.in_memory_user import InMemoryUserRepository

STATUS_CONFLICT = 409


@pytest.fixture
def repository():
    return InMemoryUserRepository()


class TestCreateUser:
    def test_create_user(self, repository: InMemoryUserRepository):
        request = InputCreateUser(email="test@hotmail.com", password="12345678")
        service = CreateUser(repository)
        response = service.execute(input=request)

        assert response.email == request.email
        assert response.id is not None

    def test_raise_exception_when_no_email(self, repository: InMemoryUserRepository):
        request = InputCreateUser(email="", password="12345678")
        service = CreateUser(repository)
        with pytest.raises(InvalidUserError) as excinfo:
            service.execute(input=request)
        assert str(excinfo.value) == "Invalid user"

    def test_raise_exception_when_user_already_exist(
        self,
        repository: InMemoryUserRepository,
    ):
        request = InputCreateUser(email="teste@hotmail.com", password="12345678")
        service = CreateUser(repository)
        service.execute(input=request)

        with pytest.raises(UserAlreadyExistError) as excinfo:
            service.execute(input=request)

        assert str(excinfo.value) == "User already exists"
        assert excinfo.value.status_code == STATUS_CONFLICT
