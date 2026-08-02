import os
import sys
import uvicorn

# Ensure project root is in sys.path
root_dir = os.path.dirname(os.path.abspath(__file__))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from app.main import app

if __name__ == "__main__":
    port_str = os.environ.get("X_ZOHO_CATALYST_LISTEN_PORT") or os.environ.get("PORT") or "9000"
    try:
        port = int(port_str)
    except ValueError:
        port = 9000

    print(f"Starting CrimeSphere AI AppSail server on 0.0.0.0:{port}...", flush=True)
    uvicorn.run(app, host="0.0.0.0", port=port)
