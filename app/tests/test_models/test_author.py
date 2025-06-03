import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from app.models import Author

@pytest.mark.django_db
class TestAuthor:

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
        assert Author.objects.count() == 0

        author = Author.objects.create(
            user=user,
            bio='Author bio'
        )
        author.full_clean()
        assert Author.objects.count() == 1
        assert (
            author.user.id,
            author.bio
        ) == (
            user.id,
            'Author bio'
        )
    
    def test_creation_without_user(self):
        with pytest.raises(IntegrityError) as exception_info:
            author = Author.objects.create(
                bio='Author bio'
            )
            author.full_clean()

        assert str(exception_info.value) == 'NOT NULL constraint failed: app_author.user_id'

    def test_creation_with_invalid_data(self, user):
        with pytest.raises(ValidationError) as exception_info:
            author = Author.objects.create(
                user=user,
                bio='A' * 256
            )
            author.full_clean()

        assert 'Ensure this value has at most 255 characters (it has 256).' in exception_info.value.message_dict['bio']
