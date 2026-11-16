import json
from http.server import BaseHTTPRequestHandler, HTTPServer


class CounterService(HTTPServer):
    def __init__(self, server_address):
        super().__init__(server_address, CounterHandler)
        self.counter = 0


class CounterHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/counter":
            self.send_error(404)
            return
        self.send_counter()

    def do_POST(self):
        if self.path != "/counter/increment":
            self.send_error(404)
            return
        self.server.counter += 1
        self.send_counter()

    def send_counter(self):
        body = json.dumps({"counter": self.server.counter}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    with CounterService(("127.0.0.1", 8000)) as server:
        server.serve_forever()
