import pytest
import copy
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
from app.models import Article, Author, Comment

class TestCommentQuerySet:

    @pytest.fixture
    def author_user(self, django_user_model):
        return django_user_model.objects.create(
            username='Author',
            email='author@xyz.com',
            password='password123',
            gender='f'
        )

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
    def user2(self, django_user_model):
        return django_user_model.objects.create(
            username='User2',
            email='user2@xyz.com',
            password='password123',
            first_name='abc',
            last_name='123',
            gender='m'
        )

    @pytest.fixture
    def author(self, author_user):
        return Author.objects.create(
            user=author_user,
            bio='Author bio'
        )

    @pytest.fixture
    def published_article(self, author):
        return Article.objects.create(
            author=author,
            title='Published article 1 title',
            content='Published article 1 content',
            is_published=True,
            published_at=timezone.now() - timedelta(days=8)
        )

    @pytest.fixture(autouse=True)
    def approved_comment_of_user(self, user, published_article):
        return Comment.objects.create(
            user=user,
            article=published_article,
            content='Comment content',
            is_approved=True
        )

    @pytest.fixture(autouse=True)
    def approved_comment_of_user2(self, user2, published_article):
        return Comment.objects.create(
            user=user2,
            article=published_article,
            content='Comment content',
            is_approved=True
        )

    @pytest.fixture(autouse=True)
    def non_approved_comment_of_user(self, user, published_article):
        return Comment.objects.create(
            user=user,
            article=published_article,
            content='Comment content',
            is_approved=False
        )

    @pytest.fixture(autouse=True)
    def non_approved_comment_of_user2(self, user2, published_article):
        return Comment.objects.create(
            user=user2,
            article=published_article,
            content='Comment content',
            is_approved=False
        )

    class TestApproved:
        def test_returns_approved_comment(self, approved_comment_of_user, approved_comment_of_user2):
            assert Comment.objects.count() == 4
            assert Comment.objects.approved().count() == 2
            assert list(Comment.objects.approved()) == [
                approved_comment_of_user,
                approved_comment_of_user2
            ]

    class TestNonApproved:
        def test_returns_non_approved_comment(self, non_approved_comment_of_user, non_approved_comment_of_user2):
            assert Comment.objects.count() == 4
            assert Comment.objects.non_approved().count() == 2
            assert list(Comment.objects.non_approved()) == [
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ]

    class TestbyUser:
        def test_returns_comments_of_user(self, user, approved_comment_of_user, non_approved_comment_of_user):
            assert Comment.objects.count() == 4
            assert Comment.objects.by_user(user.id).count() == 2
            assert list(Comment.objects.by_user(user.id)) == [
                approved_comment_of_user,
                non_approved_comment_of_user
            ]

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
