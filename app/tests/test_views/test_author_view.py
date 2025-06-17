from app.models import Article, Author, Comment, Tag
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
import pytest
from unittest.mock import patch
from urllib.parse import urlencode
from app.views import AuthorListView

class TestAuthorView:

    class TestAuthorListView:

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
        def author_without_article(self, user):
            return Author.objects.create(
                user=user,
                bio='Author without article bio'
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
        def author_without_published_article(self, user2, tag1):
            author = Author.objects.create(
                user=user2,
                bio='Author without published article bio'
            )
            author.articles.create(
                title='Unpublished article title',
                content='Unpublished article content',
                is_published=False
            )
            author.articles.last().tags.set([tag1])
            return author

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
        def author_with_published_before_datetime_article(self, user3, tag2):
            author = Author.objects.create(
                user=user3,
                bio='Author with published article published before datetime bio without comments'
            )
            author.articles.create(
                title='Published article before datetime title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=8)
            )
            author.articles.last().tags.set([tag2])
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

        @pytest.fixture
        def author_with_published_after_datetime_article(self, user4, tag2):
            author = Author.objects.create(
                user=user4,
                bio='Author with published article published after datetime bio without comments'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=6)
            )
            author.articles.last().tags.set([tag2])
            return author

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
        def author_with_4_approved_comments_article(self, user5, user2, tag2):
            author = Author.objects.create(
                user=user5,
                bio='Author with published article published after datetime bio with 4 approved comments'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=5)
            )
            author.articles.last().tags.set([tag2])
            author.articles.last().comments.set(
                [
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 2, content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 3, content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 4, content', is_approved=True)
                ]
            )
            return author

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

        @pytest.fixture
        def author_with_5_approved_comments_article(self, user6, user2, tag2):
            author = Author.objects.create(
                user=user6,
                bio='Author with published article published after datetime bio with 5 approved comments'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=6)
            )
            author.articles.last().tags.set([tag2])
            author.articles.last().comments.set(
                [
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 2 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 3 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 4 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 5 content', is_approved=True)
                ]
            )
            return author

        @pytest.fixture
        def user7(self, django_user_model):
            return django_user_model.objects.create(
                username='User7',
                email='user7@xyz.com',
                password='password123',
                first_name='abc',
                last_name='123',
                gender='m'
            )

        @pytest.fixture
        def author_with_6_approved_comments_article(self, user7, user2, tag2):
            author = Author.objects.create(
                user=user7,
                bio='Author with published article published after datetime bio with 6 approved comments'
            )
            author.articles.create(
                title='Published article title',
                content='Published article content',
                is_published=True,
                published_at=timezone.now() - timedelta(days=6)
            )
            author.articles.last().tags.set([tag2])
            author.articles.last().comments.set(
                [
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 1 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 2 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 3 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 4 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 5 content', is_approved=True),
                    Comment.objects.create(article=author.articles.last(), user=user2, content='Comment 6 content', is_approved=True)
                ]
            )
            return author

        def test_without_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors'))

            assert response.status_code == 200
            assert author_without_article.bio.encode() in response.content
            assert author_without_published_article.bio.encode() in response.content
            assert author_with_published_before_datetime_article.bio.encode() in response.content
            assert author_with_published_after_datetime_article.bio.encode() in response.content
            assert author_with_4_approved_comments_article.bio.encode() in response.content
            assert author_with_5_approved_comments_article.bio.encode() in response.content
            assert author_with_6_approved_comments_article.bio.encode() in response.content

        def test_with_published_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({ 'published': 'True' }))

            assert response.status_code == 200
            assert author_with_published_before_datetime_article.bio.encode() in response.content
            assert author_with_published_after_datetime_article.bio.encode() in response.content
            assert author_with_4_approved_comments_article.bio.encode() in response.content
            assert author_with_5_approved_comments_article.bio.encode() in response.content
            assert author_with_6_approved_comments_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content
            assert author_without_published_article.bio.encode() not in response.content

        def test_with_non_published_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({ 'published': 'False' }))

            assert response.status_code == 200
            assert author_without_published_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content
            assert author_with_published_before_datetime_article.bio.encode() not in response.content
            assert author_with_published_after_datetime_article.bio.encode() not in response.content
            assert author_with_4_approved_comments_article.bio.encode() not in response.content
            assert author_with_5_approved_comments_article.bio.encode() not in response.content
            assert author_with_6_approved_comments_article.bio.encode() not in response.content

        def test_with_articles_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({ 'with_articles': '1' }))

            assert response.status_code == 200
            assert author_without_published_article.bio.encode() in response.content
            assert author_with_published_before_datetime_article.bio.encode() in response.content
            assert author_with_published_after_datetime_article.bio.encode() in response.content
            assert author_with_4_approved_comments_article.bio.encode() in response.content
            assert author_with_5_approved_comments_article.bio.encode() in response.content
            assert author_with_6_approved_comments_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content

        def test_with_articles_of_specific_titles_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({
                'with_articles': '1',
                'article_titles[]':[
                    'Unpublished article title',
                    'Published article before datetime title',
                ]
            }, doseq=True))

            assert response.status_code == 200
            assert author_without_published_article.bio.encode() in response.content
            assert author_with_published_before_datetime_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content
            assert author_with_published_after_datetime_article.bio.encode() not in response.content
            assert author_with_4_approved_comments_article.bio.encode() not in response.content
            assert author_with_5_approved_comments_article.bio.encode() not in response.content
            assert author_with_6_approved_comments_article.bio.encode() not in response.content

        def test_with_tagged_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({ 'tagged': '1' }))

            assert response.status_code == 200
            assert author_without_published_article.bio.encode() in response.content
            assert author_with_published_before_datetime_article.bio.encode() in response.content
            assert author_with_published_after_datetime_article.bio.encode() in response.content
            assert author_with_4_approved_comments_article.bio.encode() in response.content
            assert author_with_5_approved_comments_article.bio.encode() in response.content
            assert author_with_6_approved_comments_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content

        def test_with_articles_of_specific_tag_names_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({
                'tagged': '1',
                'tag_names[]':['Tag1']
            }, doseq=True))

            assert response.status_code == 200
            assert author_without_published_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content
            assert author_with_published_before_datetime_article.bio.encode() not in response.content
            assert author_with_published_after_datetime_article.bio.encode() not in response.content
            assert author_with_4_approved_comments_article.bio.encode() not in response.content
            assert author_with_5_approved_comments_article.bio.encode() not in response.content
            assert author_with_6_approved_comments_article.bio.encode() not in response.content

        def test_with_date_time_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({ 'date_time': timezone.now() - timedelta(days=7) }))

            assert response.status_code == 200
            assert author_with_published_after_datetime_article.bio.encode() in response.content
            assert author_with_4_approved_comments_article.bio.encode() in response.content
            assert author_with_5_approved_comments_article.bio.encode() in response.content
            assert author_with_6_approved_comments_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content
            assert author_without_published_article.bio.encode() not in response.content
            assert author_with_published_before_datetime_article.bio.encode() not in response.content

        def test_with_top_active_authors_filter(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({ 'top_active_authors': '1' }))

            assert response.status_code == 200
            assert author_with_5_approved_comments_article.bio.encode() in response.content
            assert author_with_6_approved_comments_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content
            assert author_without_published_article.bio.encode() not in response.content
            assert author_with_published_before_datetime_article.bio.encode() not in response.content
            assert author_with_published_after_datetime_article.bio.encode() not in response.content
            assert author_with_4_approved_comments_article.bio.encode() not in response.content

        def test_with_more_than_one_filters(
                self,
                client,
                author_without_article,
                author_without_published_article,
                author_with_published_before_datetime_article,
                author_with_published_after_datetime_article,
                author_with_4_approved_comments_article,
                author_with_5_approved_comments_article,
                author_with_6_approved_comments_article
            ):
            response = client.get(reverse('authors') + '?' + urlencode({ 'published': 'True', 'date_time': timezone.now() - timedelta(days=6) }))

            assert response.status_code == 200
            # have articles published under last 6 days only
            assert author_with_4_approved_comments_article.bio.encode() in response.content

            assert author_without_article.bio.encode() not in response.content
            assert author_without_published_article.bio.encode() not in response.content
            assert author_with_published_before_datetime_article.bio.encode() not in response.content
            assert author_with_published_after_datetime_article.bio.encode() not in response.content
            assert author_with_5_approved_comments_article.bio.encode() not in response.content
            assert author_with_6_approved_comments_article.bio.encode() not in response.content

        @patch.object(AuthorListView, 'paginate_by', 3)
        class TestPagination:
            def test_with_page1(
                    self,
                    client,
                    author_without_article,
                    author_without_published_article,
                    author_with_published_before_datetime_article,
                    author_with_published_after_datetime_article,
                    author_with_4_approved_comments_article,
                    author_with_5_approved_comments_article,
                    author_with_6_approved_comments_article
                ):
                response = client.get(reverse('authors') + '?' + urlencode({ 'page': '1' }))

                assert response.status_code == 200
                assert author_without_article.bio.encode() in response.content
                assert author_without_published_article.bio.encode() in response.content
                assert author_with_published_before_datetime_article.bio.encode() in response.content

                assert author_with_published_after_datetime_article.bio.encode() not in response.content
                assert author_with_4_approved_comments_article.bio.encode() not in response.content
                assert author_with_5_approved_comments_article.bio.encode() not in response.content
                assert author_with_6_approved_comments_article.bio.encode() not in response.content

            def test_with_page2(
                    self,
                    client,
                    author_without_article,
                    author_without_published_article,
                    author_with_published_before_datetime_article,
                    author_with_published_after_datetime_article,
                    author_with_4_approved_comments_article,
                    author_with_5_approved_comments_article,
                    author_with_6_approved_comments_article
                ):
                response = client.get(reverse('authors') + '?' + urlencode({ 'page': '2' }))

                assert response.status_code == 200
                assert author_with_published_after_datetime_article.bio.encode() in response.content
                assert author_with_4_approved_comments_article.bio.encode() in response.content
                assert author_with_5_approved_comments_article.bio.encode() in response.content

                assert author_without_article.bio.encode() not in response.content
                assert author_without_published_article.bio.encode() not in response.content
                assert author_with_published_before_datetime_article.bio.encode() not in response.content
                assert author_with_6_approved_comments_article.bio.encode() not in response.content

            def test_with_page3(
                    self,
                    client,
                    author_without_article,
                    author_without_published_article,
                    author_with_published_before_datetime_article,
                    author_with_published_after_datetime_article,
                    author_with_4_approved_comments_article,
                    author_with_5_approved_comments_article,
                    author_with_6_approved_comments_article
                ):
                response = client.get(reverse('authors') + '?' + urlencode({ 'page': '3' }))

                assert response.status_code == 200
                assert author_with_6_approved_comments_article.bio.encode() in response.content

                assert author_without_article.bio.encode() not in response.content
                assert author_without_published_article.bio.encode() not in response.content
                assert author_with_published_before_datetime_article.bio.encode() not in response.content
                assert author_with_published_after_datetime_article.bio.encode() not in response.content
                assert author_with_4_approved_comments_article.bio.encode() not in response.content
                assert author_with_5_approved_comments_article.bio.encode() not in response.content

            def test_with_page2_and_published_filter(
                    self,
                    client,
                    author_without_article,
                    author_without_published_article,
                    author_with_published_before_datetime_article,
                    author_with_published_after_datetime_article,
                    author_with_4_approved_comments_article,
                    author_with_5_approved_comments_article,
                    author_with_6_approved_comments_article
                ):
                response = client.get(reverse('authors') + '?' + urlencode({ 'page': '2', 'published': 'True' }))

                assert response.status_code == 200
                assert author_with_5_approved_comments_article.bio.encode() in response.content
                assert author_with_6_approved_comments_article.bio.encode() in response.content

                assert author_without_article.bio.encode() not in response.content
                assert author_without_published_article.bio.encode() not in response.content
                assert author_with_published_before_datetime_article.bio.encode() not in response.content
                assert author_with_published_after_datetime_article.bio.encode() not in response.content
                assert author_with_4_approved_comments_article.bio.encode() not in response.content
