import hypercorn
from app import app

if __name__ == "__main__":
    app.run(port=5050, host="0.0.0.0")