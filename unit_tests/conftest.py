import pytest

from rest_framework.test import APIClient

from tasks.enum import TaskStatus
from tasks.models import Task
from tasks.repository import TaskRepository
from tasks.service import TaskService
from users.models import User
from users.repository import UserRepository
from users.service import UserService


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def task_repository():
    return TaskRepository()


@pytest.fixture
def task_service(task_repository):
    return TaskService(task_repository=task_repository)


@pytest.fixture
def user_service(user_repository):
    return UserService(user_repository=user_repository)


@pytest.fixture
def test_user(db):
    """
    Create and return a test user.
    """
    user = User.objects.create_user(
        name="Test",
        email="testuser@example.com",
        password="password123",
    )
    return user


@pytest.fixture
def another_user(db):
    """
    Fixture to create a secondary user for testing unauthorized access.
    """
    return User.objects.create_user(
        email="another_user@example.com",
        name="Another User",
        password="password123"
    )


@pytest.fixture
def authenticated_client(api_client, test_user):
    """
    Authenticate the API client using the test user.
    """
    api_client.force_authenticate(user=test_user)
    return api_client


@pytest.fixture
def sample_task(test_user):
    """
    Create a sample task for the test user.
    """
    return Task.objects.create(
        owner=test_user,
        title="Sample Task",
        description="This is a sample task",
        status=TaskStatus.CREATED.value
    )
