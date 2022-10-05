from quart import Quart, redirect, url_for
from config.database import iniciar_db
from models.user import User, UserData
from quart_auth import AuthManager

from routes.user import user_route
from routes.cuestionario import cuestionario_route

app = Quart(__name__)

AuthManager(app)

app.secret_key="chupas"

@app.before_serving
async def start_database():
    await iniciar_db()


@app.get('/')
async def index():
    return redirect(url_for('user.user_login'))


app.register_blueprint(user_route)
app.register_blueprint(cuestionario_route)
