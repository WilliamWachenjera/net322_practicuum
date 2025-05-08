# HTTP Server (ThreadPool)
from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
import json
import time

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Simulate CPU-bound work
        data = {str(i): i*i for i in range(1000)}
        
        # Simulate I/O-bound work
        time.sleep(0.1)
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        response = {
            'path': self.path,
            'data': data,
            'status': 'success'
        }
        self.wfile.write(json.dumps(response).encode())

def run_server():
    server = HTTPServer(('localhost', 8081), SimpleHTTPRequestHandler)
    print("ThreadPool HTTP Server running at http://localhost:8081")
    with ThreadPoolExecutor(max_workers=10) as executor:
        while True:
            executor.submit(server.handle_request)

if __name__ == '__main__':
    run_server()