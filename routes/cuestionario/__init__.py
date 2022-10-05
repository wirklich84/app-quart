from quart import Blueprint, render_template, session, request, redirect, url_for
from quart_auth import login_required

cuestionario_route = Blueprint('cuestionario', __name__, url_prefix='/cuestionario', template_folder='templates')

@cuestionario_route.route('/', methods=['GET', 'POST'])
@login_required
async def index():
    return await render_template('cuestionario/index.html')

@cuestionario_route.route('/fotalecimiento', methods=['GET', 'POST'])
@login_required
async def fortalecimiento():

    if request.method == 'GET':
        if session["fortalecimiento_info"]:
            take_info = session["fortalecimiento_info"]
            print(take_info)
            if take_info == 1:
                redirect(url_for('cuestionario.fortalecimiento_examen'))
        redirect(url_for('cuestionario.fortalecimiento_examen'))
    return await render_template('cuestionario/fortalecimiento.html')

@cuestionario_route.route('/fotalecimiento/examen', methods=['GET', 'POST'])
@login_required
async def fortalecimiento_examen():

    if request.method == 'GET':
        session["fortalecimiento_info"] = 1
        print(session["fortalecimiento_info"])
    return await render_template('cuestionario/fortalecimiento_examen.html')
