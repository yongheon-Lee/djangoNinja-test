# from django.db import connection
from django.test import TestCase

from tabom.models.article import Article
from tabom.models.user import User
from tabom.services.article_service import get_an_article, get_article_list
from tabom.services.like_service import do_like

# from django.test.utils import CaptureQueriesContext


class TestArticleService(TestCase):
    def test_you_can_get_an_article_by_id(self) -> None:
        # Given
        title = "test_title"
        article = Article.objects.create(title=title)

        # When
        result_article = get_an_article(article.id)

        # Then
        self.assertEqual(article.id, result_article.id)
        self.assertEqual(title, result_article.title)

    def test_it_should_raise_exception_when_article_does_not_exist(self) -> None:
        # Given
        invalid_article_id = 9988

        # Except
        with self.assertRaises(Article.DoesNotExist):
            get_an_article(invalid_article_id)

    def test_get_article_list_should_prefetch_like(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        articles = [Article.objects.create(title=f"{i}") for i in range(1, 21)]
        do_like(user.id, articles[-1].id)  # 가장 최신 article에 좋아요

        # When
        # with CaptureQueriesContext(connection) as ctx:
        with self.assertNumQueries(3):  # 정해진 횟수에 맞게 쿼리가 발생하는지 검증
            result_articles = get_article_list(user.id, 0, 10)
            result_counts = [a.like_set.count() for a in result_articles]  # 좋아요 개수 리스트 생성 가능

            # Then
            self.assertEqual(len(result_articles), 10)  # 불러온 글이 10개인지 검증
            self.assertEqual(1, result_counts[0])  # 최신 글 전체 like가 1인지 검증
            self.assertEqual(  # 내림차순으로 정렬됐는지 검증
                [a.id for a in reversed(articles[10:21])], [a.id for a in result_articles]
            )

    def test_get_article_list_should_contain_my_like_when_like_exists(self) -> None:
        # Given
        user = User.objects.create(name="test_user")
        article1 = Article.objects.create(title="article1")
        like = do_like(user.id, article1.id)  # article1에 like 표시
        Article.objects.create(title="article2")

        # When
        articles = get_article_list(user.id, 0, 10)  # 모든 article을 요청한 id와 연결된 article을 0번째부터 10개 들고옴

        # Then
        self.assertEqual(like.id, articles[1].my_likes[0].id)  # like한 id와 articles에 to_attr로 할당한 my_likes 필드에서
        # article1에 내 like의 id가 같은지 검증
        self.assertEqual(0, len(articles[0].my_likes))  # 1번째 article의 내 like가 0과 같은지 검증
