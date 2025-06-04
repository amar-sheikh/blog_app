from app.models import Article, Author, Tag, Comment
import copy
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
import pytest

@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create(
        username='User1',
        email='user1@xyz.com',
        password='password123',
        first_name='abc',
        last_name='123',
        gender='m'
    )

@pytest.fixture
def author(user):
    return Author.objects.create(
        user=user,
        bio='Author bio'
    )

@pytest.mark.django_db
class TestArticleQuerySet:

    @pytest.fixture
    def published_article(self, author):
        return Article.objects.create(
            author=author,
            title='Published article title',
            content='Published article content',
            is_published=True,
            published_at=timezone.now() - timedelta(days=8)
        )

    @pytest.fixture
    def un_published_article(self, author):
        return Article.objects.create(
            author=author,
            title='Unpublished article title',
            content='Unpublished article content',
            is_published=False
        )

    class TestPublished:
        def test_returns_published_articles(self, published_article, un_published_article):
            assert Article.objects.count() == 2
            assert Article.objects.published().count() == 1
            assert list(Article.objects.published()) == [published_article]

    class TestRecent:

        @pytest.fixture(autouse=True)
        def un_published_article(self, un_published_article):
            return un_published_article

        @pytest.fixture(autouse=True)
        def non_recent_article(self, published_article):
            return published_article

        @pytest.fixture(autouse=True)
        def recent_article(self, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=6)
            new_article.save()
            return new_article

        def test_returns_recent_articles(self, recent_article):
            assert Article.objects.count() == 3
            assert Article.objects.recent().count() == 1
            assert list(Article.objects.recent()) == [recent_article]

    class TestTagged:

        @pytest.fixture
        def tag1(self):
            return Tag.objects.create(name='Tag 1')

        @pytest.fixture
        def tag2(self):
            return Tag.objects.create(name='Tag 2')

        @pytest.fixture(autouse=True)
        def non_tagged_article(self, un_published_article):
            return un_published_article

        @pytest.fixture(autouse=True)
        def tagged_article1(self, tag1, published_article):
            published_article.tags.add(tag1)
            published_article.save()
            return published_article

        @pytest.fixture(autouse=True)
        def tagged_article2(self, tag2, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.save()
            new_article.tags.add(tag2)
            new_article.save()
            return new_article

        def test_without_tag_names_returns_all_tagged_articles(self, tagged_article1, tagged_article2):
            assert Article.objects.count() == 3
            assert Article.objects.tagged().count() == 2
            assert list(Article.objects.tagged()) == [tagged_article1, tagged_article2]

        def test_with_tag_names_returns_all_tagged_articles_matching_tag_names(self, tagged_article1):
            assert Article.objects.count() == 3
            assert Article.objects.tagged(['Tag 1']).count() == 1
            assert list(Article.objects.tagged(['Tag 1'])) == [tagged_article1]

    class TestWithApprovedComments:

        @pytest.fixture(autouse=True)
        def un_published_article(self, un_published_article):
            return un_published_article

        @pytest.fixture(autouse=True)
        def published_article_without_comment(self, published_article):
            return published_article

        @pytest.fixture(autouse=True)
        def published_article_without_approved_comment(self, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.save()
            new_article.comments.create(
                user=user,
                content='Comment content',
                is_approved=False
            )
            return new_article

        @pytest.fixture(autouse=True)
        def published_article_with_one_approved_comment(self, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.save()
            new_article.comments.create(
                user=user,
                content='Comment content',
                is_approved=True
            )
            return new_article

        @pytest.fixture(autouse=True)
        def published_article_with_two_approved_comment(self, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.save()
            new_article.comments.create(
                user=user,
                content='Comment 1 content',
                is_approved=True
            )
            new_article.comments.create(
                user=user,
                content='Comment 2 content',
                is_approved=True
            )
            return new_article

        def test_returns_published_articles_with_approved_comment(
                self,
                published_article_with_one_approved_comment,
                published_article_with_two_approved_comment,
            ):
            assert Article.objects.count() == 5
            assert Article.objects.with_approved_comments().count() == 2
            assert list(Article.objects.with_approved_comments()) == [
                published_article_with_one_approved_comment,
                published_article_with_two_approved_comment
            ]

        def test_returns_published_articles_with_2_approved_comment(
                self,
                published_article_with_two_approved_comment,
            ):
            assert Article.objects.count() == 5
            assert Article.objects.with_approved_comments(2).count() == 1
            assert list(Article.objects.with_approved_comments(2)) == [
                published_article_with_two_approved_comment
            ]

        def test_raises_error_with_invalid_count(self):
            with pytest.raises(ValueError) as exception_info:
                assert Article.objects.with_approved_comments(0)

            assert str(exception_info.value) == "count can't be less than 1"

    class TestSearch:

        def test_returns_matching_results(self, published_article, un_published_article):
            assert Article.objects.count() == 2
            assert Article.objects.search('un').count() == 1
            assert list(Article.objects.search('un')) == [un_published_article]

    class TestByAuthor:

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
        def author2(self, user2):
            return Author.objects.create(
                user=user2,
                bio='Author2 bio'
            )

        @pytest.fixture(autouse=True)
        def article_by_author1(self, un_published_article):
            return un_published_article

        @pytest.fixture(autouse=True)
        def article_by_author2(self, published_article, author2):
            new_article = copy.copy(published_article)
            new_article.author=author2
            new_article.save()
            return new_article

        def test_returns_matching_author_name(self, article_by_author1):
            assert Article.objects.count() == 2
            assert Article.objects.by_author('user1').count() == 1
            assert list(Article.objects.by_author('user1')) == [article_by_author1]

    class TestHotArticles:

        @pytest.fixture
        def tag(self):
            return Tag.objects.create(name='Tag')

        @pytest.fixture(autouse=True)
        def un_published_article(self, un_published_article):
            return un_published_article

        @pytest.fixture(autouse=True)
        def non_recent_article(self, published_article):
            return published_article

        @pytest.fixture(autouse=True)
        def recent_untagged_article(self, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=6)
            new_article.save()
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_uncommented_article(self, tag, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=6)
            new_article.save()
            new_article.tags.set([tag])
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_non_proved_commented_article(self, tag, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=6)
            new_article.save()
            new_article.tags.set([tag])
            new_article.comments.create(
                user=user,
                content='Comment content',
                is_approved=False
            )
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_proved_commented_article(self, tag, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=6)
            new_article.save()
            new_article.tags.set([tag])
            new_article.comments.create(
                user=user,
                content='Comment content',
                is_approved=True
            )
            return new_article

        def test_returns_resent_tagged_approved_commented_articles(
            self,
            recent_tagged_proved_commented_article
            ):
            assert Article.objects.count() == 6
            assert Article.objects.hot_articles().count() == 1
            assert list(Article.objects.hot_articles()) == [
                recent_tagged_proved_commented_article
            ]

        def test_with_no_recent_article_returns_empty_result(self):
            assert Article.objects.count() == 6
            assert Article.objects.hot_articles(days=4).count() == 0
            assert list(Article.objects.hot_articles(days=4)) == []

        def test_with_no_matching_tagged_article_returns_empty_result(self):
            assert Article.objects.count() == 6
            assert Article.objects.hot_articles(tag_names=['non matching tag']).count() == 0
            assert list(Article.objects.hot_articles(tag_names=['non matching tag'])) == []

    class TestTrending:

        @pytest.fixture
        def tag(self):
            return Tag.objects.create(name='Tag')

        @pytest.fixture(autouse=True)
        def un_published_article(self, un_published_article):
            return un_published_article

        @pytest.fixture(autouse=True)
        def non_recent_article(self, published_article):
            return published_article

        @pytest.fixture(autouse=True)
        def recent_untagged_article(self, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=2)
            new_article.save()
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_uncommented_article(self, tag, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=2)
            new_article.save()
            new_article.tags.set([tag])
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_non_proved_commented_article(self, tag, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=2)
            new_article.save()
            new_article.tags.set([tag])
            new_article.comments.create(
                user=user,
                content='Comment content',
                is_approved=False
            )
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_4_proved_commented_article(self, tag, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=2)
            new_article.save()
            new_article.tags.set([tag])
            new_article.comments.set(
                [
                    Comment.objects.create(article=new_article, user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 2, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 3, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 4, content', is_approved=True)
                ]
            )
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_5_proved_commented_article(self, tag, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=2)
            new_article.save()
            new_article.tags.set([tag])
            new_article.comments.set(
                [
                    Comment.objects.create(article=new_article, user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 2, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 3, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 4, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 5, content', is_approved=True)
                ]
            )
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_6_proved_commented_article_published_first(self, tag, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=2)
            new_article.save()
            new_article.tags.set([tag])
            new_article.comments.set(
                [
                    Comment.objects.create(article=new_article, user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 2, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 3, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 4, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 5, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 5, content', is_approved=True)
                ]
            )
            return new_article

        @pytest.fixture(autouse=True)
        def recent_tagged_6_proved_commented_article_published_later(self, tag, user, published_article):
            new_article = copy.copy(published_article)
            new_article.pk = None
            new_article.published_at = timezone.now() - timedelta(days=1)
            new_article.save()
            new_article.tags.set([tag])
            new_article.comments.set(
                [
                    Comment.objects.create(article=new_article, user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 2, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 3, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 4, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 5, content', is_approved=True),
                    Comment.objects.create(article=new_article, user=user, content='Comment 5, content', is_approved=True)
                ]
            )
            return new_article

        def test_returns_trending_articles(
            self,
            recent_tagged_5_proved_commented_article,
            recent_tagged_6_proved_commented_article_published_first,
            recent_tagged_6_proved_commented_article_published_later
            ):
            assert Article.objects.count() == 9
            assert Article.objects.trending().count() == 3
            assert list(Article.objects.trending()) == [
                recent_tagged_6_proved_commented_article_published_later,
                recent_tagged_6_proved_commented_article_published_first,
                recent_tagged_5_proved_commented_article
            ]

        def test_with_matching_article_returns_empty_result(self):
            assert Article.objects.count() == 9
            assert Article.objects.trending(tag_names=['un matched tag']).count() == 0
            assert list(Article.objects.trending(tag_names=['un matched tag'])) == []

        def test_raise_error_with_invalid_min_count(self):
            with pytest.raises(ValueError) as exception_info:
                assert Article.objects.trending(min_comments=3)

            assert str(exception_info.value) == "count can't be less than 5"

@pytest.mark.django_db
class TestArticle:

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
