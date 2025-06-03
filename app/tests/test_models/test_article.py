import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from app.models import Article, Author

@pytest.mark.django_db
class TestArticle:

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
    
    @pytest.fixture
    def author(self, user):
        return Author.objects.create(
            user=user,
            bio='Author bio'
        )

    def test_creation_with_valid_data(self, user, author):
        assert Article.objects.count() == 0

        article = Article.objects.create(
            author=author,
            title='Article title',
            content='Article content',
        )
        article.full_clean()
        assert Article.objects.count() == 1
        assert (
            article.author.id,
            article.title,
            article.content
        ) == (
            author.id,
            'Article title',
            'Article content'
        )

    def test_creation_without_author(self):
        with pytest.raises(IntegrityError) as exception_info:
            article = Article.objects.create(
                title='Article title',
                content='Article content',
            )
            article.full_clean()

        assert str(exception_info.value) == 'NOT NULL constraint failed: app_article.author_id'

    def test_creation_without_data(self, author):
        with pytest.raises(ValidationError) as exception_info:
            article = Article.objects.create(
                author=author,
            )
            article.full_clean()

        for field in ['title', 'content']:
            assert 'This field cannot be blank.' in exception_info.value.message_dict[field]

    def test_creation_with_invalid_title(self, author):
        with pytest.raises(ValidationError) as exception_info:
            article = Article.objects.create(
                author=author,
                title='A'*256,
                content='Article content'
            )
            article.full_clean()

        assert 'Ensure this value has at most 255 characters (it has 256).' in exception_info.value.message_dict['title']
