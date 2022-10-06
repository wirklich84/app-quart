from urllib import response
from quart import Blueprint, render_template, session, request, redirect, url_for, flash, Response
from quart_auth import login_required, current_user
from models.cuestionario import FortalecimientoSegudadInfo
import pdfkit

cuestionario_route = Blueprint('cuestionario', __name__, url_prefix='/cuestionario', template_folder='templates')

@cuestionario_route.route('/', methods=['GET', 'POST'])
@login_required
async def index():
    return await render_template('cuestionario/index.html')

@cuestionario_route.route('/fotalecimiento', methods=['GET', 'POST'])
@login_required
async def fortalecimiento():
    
    if "fortalecimiento_info" in session:
        take_info = session["fortalecimiento_info"]       
        
        if take_info == 1:
            return redirect(url_for('cuestionario.fortalecimiento_examen'))    
    

    return await render_template('cuestionario/fortalecimiento.html')

@cuestionario_route.route('/fotalecimiento/examen', methods=['GET', 'POST'])
@login_required
async def fortalecimiento_examen():
    pregunta_1 : str = ""
    pregunta_2 : str = ""
    pregunta_3 : str = ""
    pregunta_4 : str = ""
    pregunta_5 : str = ""  




    if request.method == 'GET':
        session["fortalecimiento_info"] = 1
        print(current_user.auth_id)
        
    if  request.method == 'POST':
        form: dict = await request.form
        
        pregunta_1 = form.get("pregunta_1", "")
        pregunta_2 = form.get("pregunta_2", "")
        pregunta_3 = form.get("pregunta_3", "")
        pregunta_4 = form.get("pregunta_4", "")
        pregunta_5 = form.get("pregunta_5", "")
        
        if not pregunta_1 or not pregunta_2 or not pregunta_3 or not pregunta_4 or not pregunta_5:
            await flash("Falta algun campo por llenar", category="error")
            print("esta alguno vacio")
        else:
            encuesta = FortalecimientoSegudadInfo(usuario_id=current_user.auth_id, pregunta_1=pregunta_1, pregunta_2=pregunta_2, pregunta_3=pregunta_3, pregunta_4=pregunta_4, pregunta_5=pregunta_5)
            
            await encuesta.create()

            session.pop('fortalecimiento_info', None)

            return redirect(url_for('cuestionario.index'))
        
        
        
    return await render_template('cuestionario/fortalecimiento_examen.html')


@cuestionario_route.route('/pdf/<id>', methods=['GET','POST'])
async def pdf(id):
    
    cuestionario = FortalecimientoSegudadInfo.get(id)

    out = await render_template('cuestionario/fotalecimiento_pdf.html', cuestionario=cuestionario)

    
    # PDF options
    options = {
        "page-size": "LETTER",
        "margin-top": "1.0cm",
        "margin-right": "1.0cm",
        "margin-bottom": "1.0cm",
        "margin-left": "1.0cm",
        "encoding": "UTF-8",
    }

    pdf = pdfkit.from_string(out, options=options)

    return Response(pdf, mimetype="application/pdf")