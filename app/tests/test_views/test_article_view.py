from app.models import Article, Author, Comment, Tag
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
import pytest
from unittest.mock import patch
from urllib.parse import urlencode
from app.views import ArticleListView

class TestArticleView:

    class TestArticleListView:

        @pytest.fixture
        def tag1(self):
            return Tag.objects.create(name='Tag1')

        @pytest.fixture
        def tag2(self):
            return Tag.objects.create(name='Tag2')

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
                bio='Author 1 bio'
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
        def author2(self, user2):
            return Author.objects.create(
                user=user2,
                bio='Author 2 bio'
            )

        @pytest.fixture
        def un_published_article(self, author):
            return Article.objects.create(
                author=author,
                title='Unpublished article title',
                content='Unpublished article content',
                is_published=False
            )

        @pytest.fixture
        def non_recent_published_article(self, author):
            return Article.objects.create(
                author=author,
                title='Non recent published article title without tag and comment',
                content='Non recent published article content without tag and comment',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )

        @pytest.fixture
        def non_recent_published_article_with_tags_and_non_approved_comments(self, author, user, tag1):
            article = Article.objects.create(
                author=author,
                title='Non recent published article title with tags and non approved comments',
                content='Non recent published article content with tags and approved comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            article.tags.add(tag1)
            article.comments.create(
                user=user,
                content='Comment content',
                is_approved=False
            )
            return article

        @pytest.fixture
        def non_recent_published_article_with_tags_and_1_approved_comments(self, author, user, tag1):
            article = Article.objects.create(
                author=author,
                title='Non recent published article title with tags and one appproved comments',
                content='Non recent published article content with tags and one approved comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            article.tags.add(tag1)
            article.comments.create(
                user=user,
                content='Comment content',
                is_approved=True
            )
            return article

        @pytest.fixture
        def non_recent_published_article_with_tags_and_2_approved_comments(self, author2, user, tag1):
            article = Article.objects.create(
                author=author2,
                title='Non recent published article title with tags and two appproved comments',
                content='Non recent published article content with tags and two approved comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            article.tags.add(tag1)
            article.comments.create(
                user=user,
                content='Comment 1 content',
                is_approved=True
            )
            article.comments.create(
                user=user,
                content='Comment 2 content',
                is_approved=True
            )
            return article

        @pytest.fixture
        def recent_published_article(self, author):
            return Article.objects.create(
                author=author,
                title='Recent published article title without tag and comment',
                content='Recent published article content without tag and comment',
                is_published=True,
                published_at=timezone.now() - timedelta(days=6)
            )

        @pytest.fixture
        def recent_published_article_with_tags_and_non_approved_comments(self, author, user, tag2):
            article = Article.objects.create(
                author=author,
                title='Recent published article title with tags and comments',
                content='Recent published article content with tags and comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=6)
            )
            article.tags.add(tag2)
            article.comments.create(
                user=user,
                content='Comment content',
                is_approved=False
            )
            return article

        @pytest.fixture
        def recent_published_article_with_tags_and_1_approved_comments(self, author, user, tag1):
            article = Article.objects.create(
                author=author,
                title='Recent published article title with tags and one appproved comments',
                content='Recent published article content with tags and one approved comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=6)
            )
            article.tags.add(tag1)
            article.comments.create(
                user=user,
                content='Comment content',
                is_approved=True
            )
            return article

        @pytest.fixture
        def recent_published_article_with_tags_and_4_approved_comments(self, author2, user, tag1):
            article = Article.objects.create(
                author=author2,
                title='Recent published article title with tags and four appproved comments',
                content='Recent published article content with tags and four approved comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=6)
            )
            article.tags.add(tag1)
            article.comments.set(
                [
                    Comment.objects.create(article=article, user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 2 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 3 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 4 content', is_approved=True)
                ]
            )
            return article

        @pytest.fixture
        def recent_published_article_with_tags_and_5_approved_comments(self, author2, user, tag1):
            article = Article.objects.create(
                author=author2,
                title='Recent published article title with tags and five appproved comments',
                content='Recent published article content with tags and five approved comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=2)
            )
            article.tags.add(tag1)
            article.comments.set(
                [
                    Comment.objects.create(article=article, user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 2 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 3 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 4 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 5 content', is_approved=True)
                ]
            )
            return article

        @pytest.fixture
        def recent_published_article_with_tags_and_6_approved_comments_published_before(self, author2, user, tag1):
            article = Article.objects.create(
                author=author2,
                title='Recent published before article title with tags and six appproved comments',
                content='Recent published before article content with tags and six approved comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=2)
            )
            article.tags.add(tag1)
            article.comments.set(
                [
                    Comment.objects.create(article=article, user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 2 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 3 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 4 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 5 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 6 content', is_approved=True)
                ]
            )
            return article

        @pytest.fixture
        def recent_published_article_with_tags_and_6_approved_comments_published_later(self, author2, user, tag1):
            article = Article.objects.create(
                author=author2,
                title='Recent published after article title with tags and six appproved comments',
                content='Recent published after article content with tags and six approved comments',
                is_published=True,
                published_at=timezone.now() - timedelta(days=1)
            )
            article.tags.add(tag1)
            article.comments.set(
                [
                    Comment.objects.create(article=article, user=user, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 2 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 3 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 4 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 5 content', is_approved=True),
                    Comment.objects.create(article=article, user=user, content='Comment 6 content', is_approved=True)
                ]
            )
            return article

        def test_without_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles'))

            assert response.status_code == 200
            assert un_published_article.title.encode() in response.content
            assert non_recent_published_article.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content
            assert recent_published_article.title.encode() in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

        def test_with_search_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({ 'search': 'non' }))

            assert response.status_code == 200
            assert non_recent_published_article.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() not in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() not in response.content

        def test_with_author_names_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({
                'author_names[]': ['User2']
            }, doseq=True))

            assert response.status_code == 200
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content

        def test_with_tagged_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({'tagged': '1' }))

            assert response.status_code == 200
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content

        def test_with_tagged_of_specific_tag_names_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({
                'tagged': '1',
                'tag_names[]': ['Tag1']
            }, doseq=True))

            assert response.status_code == 200
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content

        def test_with_approved_comment_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({'with_approved_comment': '1' }))

            assert response.status_code == 200
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content

        def test_with_approved_commen_of_specific_count_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({
                'with_approved_comment': '1',
                'comments_count': 2
            }, doseq=True))

            assert response.status_code == 200
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content

        def test_with_published_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({ 'published': 'True' }))

            assert response.status_code == 200
            assert non_recent_published_article.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content
            assert recent_published_article.title.encode() in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content

        def test_with_non_published_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({ 'published': 'False' }))

            assert response.status_code == 200
            assert un_published_article.title.encode() in response.content

            assert non_recent_published_article.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() not in response.content
            assert recent_published_article.title.encode()  not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() not in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() not in response.content

        def test_with_date_time_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({ 'days': 7 }))

            assert response.status_code == 200
            assert recent_published_article.title.encode() in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() not in response.content

        def test_with_special_hot_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({ 'special': 'hot' }))

            assert response.status_code == 200
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content

        def test_with_special_trending_filter(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({ 'special': 'trending' }))

            assert response.status_code == 200
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() not in response.content

        def test_with_mutiple_filters(
                self,
                client,
                un_published_article,
                non_recent_published_article,
                non_recent_published_article_with_tags_and_non_approved_comments,
                non_recent_published_article_with_tags_and_1_approved_comments,
                non_recent_published_article_with_tags_and_2_approved_comments,
                recent_published_article,
                recent_published_article_with_tags_and_non_approved_comments,
                recent_published_article_with_tags_and_1_approved_comments,
                recent_published_article_with_tags_and_4_approved_comments,
                recent_published_article_with_tags_and_5_approved_comments,
                recent_published_article_with_tags_and_6_approved_comments_published_before,
                recent_published_article_with_tags_and_6_approved_comments_published_later
            ):
            response = client.get(reverse('articles') + '?' + urlencode({
                'author_names[]': ['User2'],
                'search': 'six'
            }, doseq=True))

            assert response.status_code == 200
            assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
            assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

            assert un_published_article.title.encode() not in response.content
            assert non_recent_published_article.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert recent_published_article.title.encode() not in response.content
            assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
            assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_4_approved_comments.title.encode() not in response.content
            assert recent_published_article_with_tags_and_5_approved_comments.title.encode() not in response.content

        @patch.object(ArticleListView, 'paginate_by', 5)
        class TestPagination:
            def test_with_page1(
                    self,
                    client,
                    un_published_article,
                    non_recent_published_article,
                    non_recent_published_article_with_tags_and_non_approved_comments,
                    non_recent_published_article_with_tags_and_1_approved_comments,
                    non_recent_published_article_with_tags_and_2_approved_comments,
                    recent_published_article,
                    recent_published_article_with_tags_and_non_approved_comments,
                    recent_published_article_with_tags_and_1_approved_comments,
                    recent_published_article_with_tags_and_4_approved_comments,
                    recent_published_article_with_tags_and_5_approved_comments,
                    recent_published_article_with_tags_and_6_approved_comments_published_before,
                    recent_published_article_with_tags_and_6_approved_comments_published_later
                ):
                response = client.get(reverse('articles') + '?' + urlencode({'page': '1'}))

                assert response.status_code == 200
                assert un_published_article.title.encode() in response.content
                assert non_recent_published_article.title.encode() in response.content
                assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
                assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
                assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() in response.content

                assert recent_published_article.title.encode() not in response.content
                assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_4_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_5_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() not in response.content
                assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() not in response.content

            def test_with_page2(
                    self,
                    client,
                    un_published_article,
                    non_recent_published_article,
                    non_recent_published_article_with_tags_and_non_approved_comments,
                    non_recent_published_article_with_tags_and_1_approved_comments,
                    non_recent_published_article_with_tags_and_2_approved_comments,
                    recent_published_article,
                    recent_published_article_with_tags_and_non_approved_comments,
                    recent_published_article_with_tags_and_1_approved_comments,
                    recent_published_article_with_tags_and_4_approved_comments,
                    recent_published_article_with_tags_and_5_approved_comments,
                    recent_published_article_with_tags_and_6_approved_comments_published_before,
                    recent_published_article_with_tags_and_6_approved_comments_published_later
                ):
                response = client.get(reverse('articles') + '?' + urlencode({'page': '2'}))

                assert response.status_code == 200
                assert recent_published_article.title.encode() in response.content
                assert recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
                assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content
                assert recent_published_article_with_tags_and_4_approved_comments.title.encode() in response.content
                assert recent_published_article_with_tags_and_5_approved_comments.title.encode() in response.content

                assert un_published_article.title.encode() not in response.content
                assert non_recent_published_article.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() not in response.content
                assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() not in response.content

            def test_with_page3(
                    self,
                    client,
                    un_published_article,
                    non_recent_published_article,
                    non_recent_published_article_with_tags_and_non_approved_comments,
                    non_recent_published_article_with_tags_and_1_approved_comments,
                    non_recent_published_article_with_tags_and_2_approved_comments,
                    recent_published_article,
                    recent_published_article_with_tags_and_non_approved_comments,
                    recent_published_article_with_tags_and_1_approved_comments,
                    recent_published_article_with_tags_and_4_approved_comments,
                    recent_published_article_with_tags_and_5_approved_comments,
                    recent_published_article_with_tags_and_6_approved_comments_published_before,
                    recent_published_article_with_tags_and_6_approved_comments_published_later
                ):
                response = client.get(reverse('articles') + '?' + urlencode({'page': '3'}))

                assert response.status_code == 200
                assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() in response.content
                assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() in response.content

                assert un_published_article.title.encode() not in response.content
                assert non_recent_published_article.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() not in response.content
                assert recent_published_article.title.encode() not in response.content
                assert recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_4_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_5_approved_comments.title.encode() not in response.content

            def test_with_filter_and_page2(
                    self,
                    client,
                    un_published_article,
                    non_recent_published_article,
                    non_recent_published_article_with_tags_and_non_approved_comments,
                    non_recent_published_article_with_tags_and_1_approved_comments,
                    non_recent_published_article_with_tags_and_2_approved_comments,
                    recent_published_article,
                    recent_published_article_with_tags_and_non_approved_comments,
                    recent_published_article_with_tags_and_1_approved_comments,
                    recent_published_article_with_tags_and_4_approved_comments,
                    recent_published_article_with_tags_and_5_approved_comments,
                    recent_published_article_with_tags_and_6_approved_comments_published_before,
                    recent_published_article_with_tags_and_6_approved_comments_published_later
                ):
                response = client.get(reverse('articles') + '?' + urlencode({
                    'page': '2',
                    'author_names[]': ['User1']
                }, doseq=True))

                assert response.status_code == 200
                assert recent_published_article_with_tags_and_non_approved_comments.title.encode() in response.content
                assert recent_published_article_with_tags_and_1_approved_comments.title.encode() in response.content

                assert un_published_article.title.encode() not in response.content
                assert non_recent_published_article.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_non_approved_comments.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_1_approved_comments.title.encode() not in response.content
                assert non_recent_published_article_with_tags_and_2_approved_comments.title.encode() not in response.content
                assert recent_published_article.title.encode() not in response.content
                assert recent_published_article_with_tags_and_4_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_5_approved_comments.title.encode() not in response.content
                assert recent_published_article_with_tags_and_6_approved_comments_published_before.title.encode() not in response.content
                assert recent_published_article_with_tags_and_6_approved_comments_published_later.title.encode() not in response.content
