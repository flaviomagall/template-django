# core/tests/test_models.py

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username='testuser', password='password')
    assert user.username == 'testuser'
    assert user.is_active
    assert not user.is_staff
    assert not user.is_superuser

@pytest.mark.django_db
def test_create_superuser():
    admin_user = User.objects.create_superuser(username='admin', password='password')
    assert admin_user.username == 'admin'
    assert admin_user.is_active
    assert admin_user.is_staff
    assert admin_user.is_superuser
