import os
import sys
import traceback
from http.server import HTTPServer, BaseHTTPRequestHandler

# Ensure project root & vendor directory are in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

vendor_dir = os.path.join(root_dir, "vendor")
if os.path.exists(vendor_dir) and vendor_dir not in sys.path:
    sys.path.insert(0, vendor_dir)

startup_error = None
app_imported = False

try:
    print("Importing app.main...", flush=True)
    from app.main import app
    app_imported = True
    print("Successfully imported app.main!", flush=True)
except Exception as e:
    startup_error = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
    print(f"CRITICAL ERROR importing app.main:\n{startup_error}", flush=True)

if app_imported and startup_error is None:
    import uvicorn
    port = int(os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT") or os.environ.get("PORT") or "9000")
    print(f"Starting CrimeSphere AI Uvicorn on 0.0.0.0:{port}...", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)
else:
    class ErrorHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(500)
            self.send_header('Content-Type', 'text/plain')
            self.end_headers()
            err_msg = f"Startup Exception:\n{startup_error}"
            self.wfile.write(err_msg.encode('utf-8'))

    port = int(os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT") or os.environ.get("PORT") or "9000")
    print(f"Serving error diagnostic on port {port}...", flush=True)
    server = HTTPServer(('0.0.0.0', port), ErrorHandler)
    server.serve_forever()
