# 테스트 케이스 만들기
from django.test import TestCase


class TestView(TestCase):

    def test_add_view(self) -> None:
        result = self.client.get('/api/add', {'a': 46, 'b': 4861}) # urls에 만들었던 add 호출
        self.assertEqual(result.status_code, 200)                  # 응답값 제대로 오는지 확인
        self.assertEqual(result.json(), {'result': 4907})          # 결과 검증poetry add isort==5.10.1
