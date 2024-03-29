from testing.testcases import TestCase
from utils.redis_client import RedisClient


class UtilsTests(TestCase):

    def setUp(self):
        self.clear_cache()

    def test_redis_client(self):
        conn = RedisClient.get_connection()
        conn.lpush('redis_key', 1)
        conn.lpush('redis_key', 2)
        # 取0到-1（倒数第一个数）闭区间  lpush是往左放，所以是 2，1 ，以字节形式的字符串储存
        cached_list = conn.lrange('redis_key', 0, -1)
        self.assertEqual(cached_list, [b'2', b'1'])

        RedisClient.clear()
        cached_list = conn.lrange('redis_key', 0, -1)
        self.assertEqual(cached_list, [])
