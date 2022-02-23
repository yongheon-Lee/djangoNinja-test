from django.db import IntegrityError
from django.test import TestCase

from tabom.models.article import Article
from tabom.models.like import Like
from tabom.models.user import User
from tabom.services.like_service import do_like, undo_like


class TestLikeService(TestCase):
    def test_a_user_can_like_an_article(self) -> None:
        # Given: 데이터가 주어졌을 때(user와 article)
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When: 해당 기능이 실행됐을 때(해당 id의 user가 해당 id의 article에 좋아요를 눌렀을 때)
        like = do_like(user.id, article.id)  # like 객체 생성

        # Then: 다음 검증을 수행한다(test코드 실행)
        self.assertIsNotNone(like.id)  # like 객체의 id는 None이 아니다 = db에 들어갔다(pk가 발급됐다)
        self.assertEqual(user.id, like.user_id)  # user id가 like의 user id와 같다
        self.assertEqual(article.id, like.article_id)  # article id가 like의 article id와 같다

    def test_a_user_can_like_an_article_only_once(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # Except
        do_like(user.id, article.id)
        with self.assertRaises(IntegrityError):
            do_like(user.id, article.id)

    def test_it_should_raise_exception_when_like_an_user_does_not_exist(self) -> None:
        # Given
        invalid_user_id = 9988
        article = Article.objects.create(title="test_title")

        # Expect
        with self.assertRaises(IntegrityError):
            do_like(invalid_user_id, article.id)

    def test_it_should_raise_exception_when_like_an_article_does_not_exist(self) -> None:
        # Given
        user = User.objects.create(name="test")
        invalid_article_id = 9988

        # Expect
        with self.assertRaises(IntegrityError):
            do_like(user.id, invalid_article_id)

    def test_like_should_increase(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")

        # When
        do_like(user.id, article.id)

        # Then
        article = Article.objects.get(id=article.id)
        self.assertEqual(1, article.like_set.count())

    def test_a_user_can_undo_like(self) -> None:
        # Given
        user = User.objects.create(name="test")
        article = Article.objects.create(title="test_title")
        like = do_like(user.id, article.id)

        # When
        undo_like(user.id, article.id)

        # Then
        with self.assertRaises(Like.DoesNotExist):
            Like.objects.filter(id=like.id).get()
