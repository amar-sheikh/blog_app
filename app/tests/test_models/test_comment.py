import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from app.models import Article, Author, Comment

@pytest.mark.django_db
class TestComment:

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

    @pytest.fixture
    def article(self, author):
        return Article.objects.create(
            author=author,
            title='Article title',
            content='Article content',
        )

    def test_creation_with_valid_data(self, user, article):
        assert Comment.objects.count() == 0

        comment = Comment.objects.create(
            user=user,
            article=article,
            content='Comment content',
            is_approved=True
        )
        comment.full_clean()
        assert Comment.objects.count() == 1
        assert (
            comment.content,
            comment.is_approved
        ) == (
            'Comment content',
            True
        )

    def test_creation_without_user(self, article):
        with pytest.raises(IntegrityError) as exception_info:
            comment = Comment.objects.create(
                article=article,
                content='Comment content',
                is_approved=True
            )
            comment.full_clean()

        assert str(exception_info.value) == 'NOT NULL constraint failed: app_comment.user_id'

    def test_creation_without_article(self, user):
        with pytest.raises(IntegrityError) as exception_info:
            comment = Comment.objects.create(
                user=user,
                content='Comment content',
                is_approved=True
            )
            comment.full_clean()

        assert str(exception_info.value) == 'NOT NULL constraint failed: app_comment.article_id'

    def test_creation_without_content(self, user, article):
        with pytest.raises(ValidationError) as exception_info:
            comment = Comment.objects.create(
                user=user,
                article=article
            )
            comment.full_clean()

        # is_approved does not raise error
        assert 'This field cannot be blank.' in exception_info.value.message_dict['content']
