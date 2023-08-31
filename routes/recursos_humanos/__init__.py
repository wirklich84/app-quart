from quart import Blueprint, render_template, session, request, redirect, url_for, flash, Response, make_response, jsonify
from quart_auth import login_required, current_user
from models.user import User, UserAdminView
from models.cuestionario import FortalecimientoSegudadInfo, LineamientoSeguridadInfo, UserData, Cuestionarios
import pdfkit
from datetime import datetime

capacitacion_360_route = Blueprint('recursos_humanos', __name__, url_prefix='/recursos_humanos', template_folder='templates')

@capacitacion_360_route.route('/', methods=['GET', 'POST'])
@login_required
async def index():

    return await render_template('recursos_humanos/index.html')


@capacitacion_360_route.route('/capacitacion_360', methods=['GET', 'POST'])
@login_required
async def capacitacion_360():

    return await render_template('recursos_humanos/capacitacion_360.html')

