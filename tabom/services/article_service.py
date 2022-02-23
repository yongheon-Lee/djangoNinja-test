# from django.core.paginator import Page, Paginator
from django.db.models import Prefetch, QuerySet

from tabom.models.article import Article
from tabom.models.like import Like


def get_an_article(user_id: int, article_id: int) -> Article:
    return Article.objects.prefetch_related(
        Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes")
    ).get(id=article_id)


# QuerySet[Article]: Article을 member로 갖고 있는 QuerySet
def get_article_list(user_id: int, offset: int, limit: int) -> QuerySet[Article]:
    return (
        Article.objects.order_by("-id")
        .prefetch_related("like_set")
        .prefetch_related(Prefetch("like_set", queryset=Like.objects.filter(user_id=user_id), to_attr="my_likes"))[
            offset : offset + limit
        ]
    )
    # -컬럼명: 내림차순 정렬, [offset:offset+limit]: 범위 슬라이싱
    # prefetch: 미리 가져오겠다!
    # Prefetch 객체를 사용(like_set을 가져오는데, user id에 해당하는 like의 쿼리셋을 들고오고, my_likes라는 필드 할당)


# paginator 사용
# def get_article_page(page: int, limit: int) -> Page[Article]:
#     return Paginator(Article.objects.order_by('-id'), limit).page(page)
