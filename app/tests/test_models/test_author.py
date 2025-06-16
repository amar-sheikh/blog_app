import pytest
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
from app.models import Author, Comment, Tag

@pytest.mark.django_db
class TestAuthorQuerySet:

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

    @pytest.fixture(autouse=True)
    def author_without_published_article(self, user2):
        author = Author.objects.create(
            user=user2,
            bio='Author 2 bio'
        )
        author.articles.create(
            title='Unpublished article title',
            content='Unpublished article content',
            is_published=False
        )
        return author

    @pytest.fixture(autouse=True)
    def author_with_published_article(self, user):
        author = Author.objects.create(
            user=user,
            bio='Author 1 bio'
        )
        author.articles.create(
            title='Published article title',
            content='Published article content',
            is_published=True,
            published_at=timezone.now() - timedelta(days=8)
        )
        return author

    class TestActiceSince:

        @pytest.fixture
        def user3(self, django_user_model):
            return django_user_model.objects.create(
                username='User3',
                email='user3@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture(autouse=True)
        def author_with_published_article_published_after_datetime(self, user3):
            author = Author.objects.create(
                user=user3,
                bio='Author 3 bio'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=6)
            )
            return author

        def test_returns_authors_with_published_articles_published_after_datetime(self, author_with_published_article_published_after_datetime):
            date_time = timezone.now() - timedelta(days=7)
            assert Author.objects.count() == 3
            assert Author.objects.active_since(date_time).count() == 1
            assert list(Author.objects.active_since(date_time)) == [author_with_published_article_published_after_datetime]

    class TestWithArticles:

        @pytest.fixture
        def user3(self, django_user_model):
            return django_user_model.objects.create(
                username='User3',
                email='user3@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture(autouse=True)
        def author_without_article(self, user3):
            return Author.objects.create(
                user=user3,
                bio='Author 3 bio'
            )

        def test_returns_authors_having_articles(self, author_without_published_article, author_with_published_article):
            assert Author.objects.count() == 3
            assert Author.objects.with_articles().count() == 2
            assert list(Author.objects.with_articles()) == [author_with_published_article, author_without_published_article]

        def test_with_article_titles_returns_authors_having_articles_with_those_title(self, author_with_published_article):
            assert Author.objects.count() == 3
            assert Author.objects.with_articles(['Published article title']).count() == 1
            assert list(Author.objects.with_articles(['Published article title'])) == [author_with_published_article]

    class TestWithPublishedArticles:
        def test_returns_authors_with_published_articles(self, author_with_published_article):
            assert Author.objects.count() == 2
            assert Author.objects.with_published_articles().count() == 1
            assert list(Author.objects.with_published_articles()) == [author_with_published_article]

    class TestWithUnPublishedArticles:
        def test_returns_authors_with_published_articles(self, author_without_published_article):
            assert Author.objects.count() == 2
            assert Author.objects.with_un_published_articles().count() == 1
            assert list(Author.objects.with_un_published_articles()) == [author_without_published_article]

    class TestWithTaggedArticles:

        @pytest.fixture
        def tag1(self):
            return Tag.objects.create(name='Tag1')

        @pytest.fixture
        def tag2(self):
            return Tag.objects.create(name='Tag2')

        @pytest.fixture
        def user3(self, django_user_model):
            return django_user_model.objects.create(
                username='User3',
                email='user3@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture(autouse=True)
        def author_with_tags_1(self, user3, tag1, tag2):
            author = Author.objects.create(
                user=user3,
                bio='Author 3 bio'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            author.articles.last().tags.set([tag1, tag2])
            return author

        @pytest.fixture
        def user4(self, django_user_model):
            return django_user_model.objects.create(
                username='User4',
                email='user4@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture(autouse=True)
        def author_with_tags_2(self, user4, tag1):
            author = Author.objects.create(
                user=user4,
                bio='Author 4 bio'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            author.articles.last().tags.set([tag1])
            return author

        def test_returns_authors_having_articles_with_tags(self, author_with_tags_1, author_with_tags_2):
            assert Author.objects.count() == 4
            assert Author.objects.with_tagged_articles().count() == 2
            assert list(Author.objects.with_tagged_articles()) == [author_with_tags_1, author_with_tags_2]

        def test_with_tag_names_returns_authors_having_articles_with_those_tags(self, author_with_tags_1):
            assert Author.objects.count() == 4
            assert Author.objects.with_tagged_articles(['Tag2']).count() == 1
            assert list(Author.objects.with_tagged_articles(['Tag2'])) == [author_with_tags_1]

    class TestTopActiveAuthors:

        @pytest.fixture
        def tag1(self):
            return Tag.objects.create(name='Tag1')

        @pytest.fixture
        def tag2(self):
            return Tag.objects.create(name='Tag2')

        @pytest.fixture
        def user3(self, django_user_model):
            return django_user_model.objects.create(
                username='User3',
                email='user3@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture
        def user4(self, django_user_model):
            return django_user_model.objects.create(
                username='User4',
                email='user4@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture
        def user5(self, django_user_model):
            return django_user_model.objects.create(
                username='User5',
                email='user5@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture
        def user6(self, django_user_model):
            return django_user_model.objects.create(
                username='User6',
                email='user6@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture(autouse=True)
        def author_with_tags_without_comment(self, user3, tag1):
            author = Author.objects.create(
                user=user3,
                bio='Author 3 bio'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            author.articles.last().tags.set([tag1])
            return author

        @pytest.fixture(autouse=True)
        def author_with_tags_with_4_approved_comments(self, user4, user, tag1, tag2):
            author = Author.objects.create(
                user=user4,
                bio='Author 4 bio'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            author.articles.last().tags.set([tag1, tag2])
            author.articles.last().comments.set(
                [
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 2, content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 3, content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 4, content', is_approved=True)
                ]
            )
            return author

        @pytest.fixture(autouse=True)
        def author_with_tags_with_5_approved_comments(self, user5, user, tag1, tag2):
            author = Author.objects.create(
                user=user5,
                bio='Author 5 bio'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            author.articles.last().tags.set([tag1, tag2])
            author.articles.last().comments.set(
                [
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 2 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 3 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 4 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 5 content', is_approved=True)
                ]
            )
            return author

        @pytest.fixture(autouse=True)
        def author_with_tags_with_6_approved_comments(self, user6, user, tag1, tag2):
            author = Author.objects.create(
                user=user6,
                bio='Author 6 bio'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            author.articles.last().tags.set([tag1, tag2])
            author.articles.last().comments.set(
                [
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 2 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 3 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 4 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 5 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user, content='Comment 5 content', is_approved=True)
                ]
            )
            return author

        def test_returns_top_active_authors(self, author_with_tags_with_5_approved_comments, author_with_tags_with_6_approved_comments):
            date_time=timezone.now() - timedelta(days=9)
            assert Author.objects.count() == 6
            assert Author.objects.top_active_authors(date_time).count() == 2
            assert list(Author.objects.top_active_authors(date_time)) == [
                author_with_tags_with_6_approved_comments,
                author_with_tags_with_5_approved_comments
            ]

        def test_with_invalid_comment_count_raises_error(self):
            date_time=timezone.now() - timedelta(days=9)
            with pytest.raises(ValueError) as exception_info:
                assert Author.objects.top_active_authors(date_time, min_comments=3)

            assert str(exception_info.value) == "count can't be less than 5"

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
