"""
Simple web server to display MinIO images in browser.
Run with: python view_minio_images.py
Then open: http://localhost:8080
"""
from http.server import HTTPServer, SimpleHTTPRequestHandler
from minio_utils import MinioStorage
import webbrowser

PORT = 8080

def generate_html():
    """Generate HTML page with all images from MinIO"""
    storage = MinioStorage()
    objects = storage.list_objects_with_urls(expires_hours=2)
    
    # Filter only jpg/png images
    images = [obj for obj in objects if obj['name'].lower().endswith(('.jpg', '.jpeg', '.png'))]
    
    html = """<!DOCTYPE html>
<html>
<head>
    <title>MinIO Image Viewer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
            color: #fff;
            min-height: 100vh;
            padding: 20px;
        }
        h1 { 
            text-align: center; 
            margin-bottom: 30px;
            font-size: 2rem;
            background: linear-gradient(90deg, #00d2ff, #3a7bd5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .stats {
            text-align: center;
            margin-bottom: 20px;
            color: #888;
        }
        .grid { 
            display: grid; 
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); 
            gap: 20px; 
            max-width: 1400px;
            margin: 0 auto;
        }
        .card { 
            background: rgba(255,255,255,0.05);
            border-radius: 12px;
            overflow: hidden;
            transition: transform 0.3s, box-shadow 0.3s;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 40px rgba(0,210,255,0.2);
        }
        .card img { 
            width: 100%; 
            height: 200px; 
            object-fit: cover;
            cursor: pointer;
        }
        .card-info { 
            padding: 15px; 
        }
        .card-info h3 { 
            font-size: 0.85rem; 
            word-break: break-all;
            color: #00d2ff;
            margin-bottom: 8px;
        }
        .card-info p { 
            font-size: 0.75rem; 
            color: #888; 
        }
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.9);
            z-index: 1000;
            justify-content: center;
            align-items: center;
        }
        .modal img {
            max-width: 90%;
            max-height: 90%;
            object-fit: contain;
        }
        .modal.active { display: flex; }
        .close-btn {
            position: absolute;
            top: 20px; right: 30px;
            font-size: 40px;
            color: #fff;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>🖼️ MinIO Image Viewer</h1>
    <p class="stats">Found """ + str(len(images)) + """ images in bucket: yolo-detections</p>
    <div class="grid">
"""
    
    for img in images[-50:]:  # Show latest 50 images
        html += f"""
        <div class="card">
            <img src="{img['url']}" alt="{img['name']}" onclick="openModal(this.src)">
            <div class="card-info">
                <h3>{img['name']}</h3>
                <p>Size: {img['size'] / 1024:.1f} KB | {img['last_modified'].strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
        </div>
"""
    
    html += """
    </div>
    <div class="modal" id="modal" onclick="closeModal()">
        <span class="close-btn">&times;</span>
        <img id="modal-img" src="">
    </div>
    <script>
        function openModal(src) {
            document.getElementById('modal-img').src = src;
            document.getElementById('modal').classList.add('active');
        }
        function closeModal() {
            document.getElementById('modal').classList.remove('active');
        }
        document.onkeydown = function(e) {
            if (e.key === 'Escape') closeModal();
        }
    </script>
</body>
</html>"""
    return html

class ImageHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(generate_html().encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == '__main__':
    print(f"Starting MinIO Image Viewer at http://localhost:{PORT}")
    print("Press Ctrl+C to stop")
    webbrowser.open(f'http://localhost:{PORT}')
    HTTPServer(('', PORT), ImageHandler).serve_forever()
