from app.models import Article, Author, Comment
from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
import pytest
from unittest.mock import patch
from urllib.parse import urlencode
from app.views import CommentListView

class TestCommentView:

    class TestCommentListView:

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

        @pytest.fixture
        def approved_comment_of_user(self, user, published_article):
            return Comment.objects.create(
                user=user,
                article=published_article,
                content='Approved comment content of user 1',
                is_approved=True
            )

        @pytest.fixture
        def approved_comment_of_user2(self, user2, published_article):
            return Comment.objects.create(
                user=user2,
                article=published_article,
                content='Approved comment content of user 2',
                is_approved=True
            )

        @pytest.fixture
        def non_approved_comment_of_user(self, user, published_article):
            return Comment.objects.create(
                user=user,
                article=published_article,
                content='Non approved comment content of user 1',
                is_approved=False
            )

        @pytest.fixture
        def non_approved_comment_of_user2(self, user2, published_article):
            return Comment.objects.create(
                user=user2,
                article=published_article,
                content='Non approved comment content of user 2',
                is_approved=False
            )

        def test_without_filter(
                self,
                client,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
            response = client.get(reverse('comments'))

            assert response.status_code == 200
            assert approved_comment_of_user.content.encode() in response.content
            assert approved_comment_of_user2.content.encode() in response.content
            assert non_approved_comment_of_user.content.encode() in response.content
            assert non_approved_comment_of_user2.content.encode() in response.content

        def test_with_approved_all_filter(
                self,
                client,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
            response = client.get(reverse('comments') + '?' + urlencode({'approved': 'all'}))

            assert response.status_code == 200
            assert approved_comment_of_user.content.encode() in response.content
            assert approved_comment_of_user2.content.encode() in response.content
            assert non_approved_comment_of_user.content.encode() in response.content
            assert non_approved_comment_of_user2.content.encode() in response.content


        def test_with_approved_filter(
                self,
                client,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
            response = client.get(reverse('comments') + '?' + urlencode({'approved': 'True'}))

            assert response.status_code == 200
            assert approved_comment_of_user.content.encode() in response.content
            assert approved_comment_of_user2.content.encode() in response.content

            assert non_approved_comment_of_user.content.encode() not in response.content
            assert non_approved_comment_of_user2.content.encode() not in response.content

        def test_with_non_approved_filter(
                self,
                client,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
            response = client.get(reverse('comments') + '?' + urlencode({'approved': 'False'}))

            assert response.status_code == 200
            assert non_approved_comment_of_user.content.encode() in response.content
            assert non_approved_comment_of_user2.content.encode() in response.content

            assert approved_comment_of_user.content.encode() not in response.content
            assert approved_comment_of_user2.content.encode() not in response.content

        def test_with_user_id_filter(
                self,
                client,
                user2,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
            response = client.get(reverse('comments') + '?' + urlencode({'user_id': user2.id}))

            assert response.status_code == 200
            assert approved_comment_of_user2.content.encode() in response.content
            assert non_approved_comment_of_user2.content.encode() in response.content

            assert approved_comment_of_user.content.encode() not in response.content
            assert non_approved_comment_of_user.content.encode() not in response.content

        def test_with_user_id_and_approved_filter(
                self,
                client,
                user2,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
            response = client.get(reverse('comments') + '?' + urlencode({'user_id': user2.id, 'approved': 'True'}))

            assert response.status_code == 200
            assert approved_comment_of_user2.content.encode() in response.content

            assert approved_comment_of_user.content.encode() not in response.content
            assert non_approved_comment_of_user.content.encode() not in response.content
            assert non_approved_comment_of_user2.content.encode() not in response.content

        def test_with_user_id_and_non_approved_filter(
                self,
                client,
                user2,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
            response = client.get(reverse('comments') + '?' + urlencode({'user_id': user2.id, 'approved': 'False'}))

            assert response.status_code == 200
            assert non_approved_comment_of_user2.content.encode() in response.content

            assert approved_comment_of_user2.content.encode() not in response.content
            assert approved_comment_of_user.content.encode() not in response.content
            assert non_approved_comment_of_user.content.encode() not in response.content

        @patch.object(CommentListView, 'paginate_by', 3)
        class TestPagination:

            def test_page1(
                self,
                client,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
                response = client.get(reverse('comments') + '?' + urlencode({'page': 1}))

                assert response.status_code == 200
                assert approved_comment_of_user.content.encode() in response.content
                assert approved_comment_of_user2.content.encode() in response.content
                assert non_approved_comment_of_user.content.encode() in response.content

                assert non_approved_comment_of_user2.content.encode() not in response.content

            def test_page2(
                self,
                client,
                approved_comment_of_user,
                approved_comment_of_user2,
                non_approved_comment_of_user,
                non_approved_comment_of_user2
            ):
                response = client.get(reverse('comments') + '?' + urlencode({'page': 2}))

                assert response.status_code == 200
                assert non_approved_comment_of_user2.content.encode() in response.content

                assert approved_comment_of_user.content.encode() not in response.content
                assert approved_comment_of_user2.content.encode() not in response.content
                assert non_approved_comment_of_user.content.encode()  not in response.content
