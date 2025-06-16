import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

@pytest.mark.django_db
class TestUser:

    @pytest.fixture
    def user(self, django_user_model):
        return django_user_model.objects.create(
            username='User1',
            email='user1@xyz.com',
            password='password123',
            first_name='abc',
            last_name='123',
            gender='m'
        )

    def test_creation_with_valid_data(self, user):
        user.full_clean()
        assert user.username == 'User1'

    def test_creation_duplicate_username(self, user, django_user_model):
        with pytest.raises(IntegrityError) as exception_info:
            django_user_model.objects.create(
                username='User1',
                email='user2@xyz.com',
                password='password123',
            )

        assert str(exception_info.value) == 'UNIQUE constraint failed: app_user.username'

    def test_creation_username_having_invalid_character(self, user, django_user_model):
        with pytest.raises(ValidationError) as exception_info:
            user2 = django_user_model.objects.create(
                username='User 1',
                email='user2@xyz.com',
                password='password123',
            )
            user2.full_clean()

        assert 'Enter a valid username. This value may contain only letters, numbers, and @/./+/-/_ characters.' in exception_info.value.message_dict['username']

    def test_creation_without_attributes(self, django_user_model):
        with pytest.raises(ValidationError) as exception_info:
            user2 = django_user_model.objects.create()
            user2.full_clean()

        for field in ['username', 'password', 'gender']:
            assert 'This field cannot be blank.' in exception_info.value.message_dict[field]
    
    def test_creation_with_invalid_gender(self, django_user_model):
        with pytest.raises(ValidationError) as exception_info:
            user = django_user_model.objects.create(
                username='User1',
                email='user2@xyz.com',
                password='password123',
                gender='a'
            )
            user.full_clean()

        assert "Value 'a' is not a valid choice." in exception_info.value.message_dict['gender']
