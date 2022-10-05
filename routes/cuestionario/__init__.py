from quart import Blueprint
from quart_auth import login_required

cuestionario_route = Blueprint('/cuestionario', __name__, url_prefix='/cuestionario', template_folder='templates')

@cuestionario_route.route('/', methods=['GET', 'POST'])
@login_required
async def index():
    return {"hola" : "hola"}