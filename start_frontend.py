import http.server
import socketserver
import os

PORT = 8080
DIRECTORY = "frontend"

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

os.chdir(os.path.dirname(os.path.abspath(__file__)))

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print("=" * 60)
    print(f"🌐 Frontend server running at http://localhost:{PORT}")
    print("=" * 60)
    print(f"📊 Open http://localhost:{PORT}/index.html in your browser")
    print(f"📈 Dashboard: http://localhost:{PORT}/dashboard.html")
    print("=" * 60)
    httpd.serve_forever()
