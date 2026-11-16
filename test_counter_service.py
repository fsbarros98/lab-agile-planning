import json
import threading
import unittest
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from counter_service import CounterService


class CounterServiceTests(unittest.TestCase):
    def setUp(self):
        self.server = CounterService(("127.0.0.1", 0))
        self.thread = threading.Thread(target=self.server.serve_forever)
        self.thread.start()
        self.url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.thread.join()
        self.server.server_close()

    def request(self, path, method="GET"):
        with urlopen(Request(self.url + path, method=method)) as response:
            return json.load(response)

    def test_initial_value_and_two_increments(self):
        self.assertEqual(self.request("/counter"), {"counter": 0})
        self.assertEqual(self.request("/counter/increment", "POST"), {"counter": 1})
        self.assertEqual(self.request("/counter/increment", "POST"), {"counter": 2})
        self.assertEqual(self.request("/counter"), {"counter": 2})
        self.assertEqual(self.request("/counter"), {"counter": 2})

    def test_unknown_paths_do_not_change_counter(self):
        for method in ("GET", "POST"):
            with self.subTest(method=method):
                with self.assertRaises(HTTPError) as error:
                    self.request("/unknown", method)
                self.assertEqual(error.exception.code, 404)
        self.assertEqual(self.request("/counter"), {"counter": 0})


if __name__ == "__main__":
    unittest.main()
