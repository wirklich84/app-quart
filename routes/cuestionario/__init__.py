from quart import Blueprint, render_template, session, request, redirect, url_for, flash, Response, make_response, jsonify
from quart_auth import login_required, current_user
from models.user import User, UserAdminView
from models.cuestionario import FortalecimientoSegudadInfo, LineamientoSeguridadInfo, UserData, Cuestionarios
import pdfkit
from datetime import datetime

cuestionario_route = Blueprint('cuestionario', __name__, url_prefix='/cuestionario', template_folder='templates')

@cuestionario_route.route('/', methods=['GET', 'POST'])
@login_required
async def index():
   
    return await render_template('cuestionario/index.html')



@cuestionario_route.after_request
async def set_response_headers(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

@cuestionario_route.route('/fortalecimiento', methods=['GET', 'POST'])
@login_required
async def fortalecimiento():
    
    if "fortalecimiento_info" in session:
        take_info = session["fortalecimiento_info"]        
        
        if take_info == 1:
            return redirect(url_for('cuestionario.fortalecimiento_examen'))    
    

    return await render_template('cuestionario/fortalecimiento.html')



@cuestionario_route.after_request
async def set_response_headers(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response



@cuestionario_route.route('/fortalecimiento/examen', methods=['GET', 'POST'])
@login_required
async def fortalecimiento_examen():
    pregunta_1 : str = ""
    pregunta_2 : str = ""
    pregunta_3 : str = ""
    pregunta_4 : str = ""
    pregunta_5 : str = ""  


    if "fortalecimiento_cuestionario_completado" in session:
        cuestionario_completado = session["fortalecimiento_cuestionario_completado"]

        if cuestionario_completado == 1:
            return redirect(url_for('cuestionario.fotalecimiento_end'))


    session["fortalecimiento_info"] = 1
        
        
    if  request.method == 'POST':
        form: dict = await request.form
        
        pregunta_1 = form.get("pregunta_1", "")
        pregunta_2 = form.get("pregunta_2", "")
        pregunta_3 = form.get("pregunta_3", "")
        pregunta_4 = form.get("pregunta_4", "")
        pregunta_5 = form.get("pregunta_5", "")

        
        if not pregunta_1 or not pregunta_2 or not pregunta_3 or not pregunta_4 or not pregunta_5:
            await flash("Falta algun campo por llenar", category="error")

        else:
            usuario = await User.get(current_user.auth_id)

            fecha_realizado = datetime.now()
            
            user_encuesta = UserData(user_id=current_user.auth_id  ,name=usuario.full_name, email=usuario.email, dep=usuario.dep)
            encuesta = FortalecimientoSegudadInfo(fecha_realizado=fecha_realizado, user_info=user_encuesta, pregunta_1=pregunta_1, pregunta_2=pregunta_2, pregunta_3=pregunta_3, pregunta_4=pregunta_4, pregunta_5=pregunta_5)
            
            encuesta_id = await encuesta.create()

            session["fortalecimiento_id"] = str(encuesta_id.id)
            session["fortalecimiento_cuestionario_completado"] = 1

            return redirect(url_for('cuestionario.fotalecimiento_end'))        
        
        
    return await render_template('cuestionario/fortalecimiento_examen.html')






@cuestionario_route.route('/fortalecimiento/end', methods=['GET', 'POST'])
@login_required
async def fotalecimiento_end():

    if 'fortalecimiento_id' in session:
        id_cuestionario = session["fortalecimiento_id"]
    
    return await render_template("cuestionario/fortalecimiento_end.html", id_cuestionario=id_cuestionario)

    


@cuestionario_route.route('/fortalecimiento/pdf/<string:id>', methods=['GET','POST'])
@login_required
async def fortalecimiento_pdf(id):

    cuestionario = await FortalecimientoSegudadInfo.get(id)

    fecha_realizado = str(cuestionario.fecha_realizado)[:10]

    respuesta1 = {"opcion1": " ", "opcion2" : " ", "opcion3" : " "}

    if cuestionario.pregunta_1 == "1":
        respuesta1["opcion1"] = "X"

    if cuestionario.pregunta_1 == "2":
        respuesta1["opcion2"] = "X"
    
    if cuestionario.pregunta_1 == "3":
        respuesta1["opcion3"] = "X"

    

    respuesta3 = {"opcion1": " ", "opcion2" : " ", "opcion3" : " "}

    if cuestionario.pregunta_3 == "1":
        respuesta3["opcion1"] = "X"

    if cuestionario.pregunta_3 == "2":
        respuesta3["opcion2"] = "X"
    
    if cuestionario.pregunta_3 == "3":
        respuesta3["opcion3"] = "X"


    respuesta5 = {"opcion1": " ", "opcion2" : " ", "opcion3" : " "}

    if cuestionario.pregunta_5 == "1":
        respuesta5["opcion1"] = "X"

    if cuestionario.pregunta_5 == "2":
        respuesta5["opcion2"] = "X"
    
    if cuestionario.pregunta_5 == "3":
        respuesta5["opcion3"] = "X"


    respuestas = {"fecha": fecha_realizado, "respuesta1" : respuesta1, "respuesta3" : respuesta3, "respuesta5" : respuesta5}

    nombre_archivo = f"Fortalecimiento - {cuestionario.user_info.name} - {cuestionario.fecha_realizado}.pdf"

    out = await render_template('cuestionario/fortalecimiento_pdf.html', cuestionario=cuestionario, respuestas=respuestas)

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

    response = await make_response(pdf)

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={nombre_archivo}'

    return response




##LINEAMIENTOS

@cuestionario_route.after_request
async def set_response_headers(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

@cuestionario_route.route('/lineamiento', methods=['GET', 'POST'])
@login_required
async def lineamiento():
    
    if "lineamiento_info" in session:
        take_info = session["lineamiento_info"]        
        
        if take_info == 1:
            return redirect(url_for('cuestionario.lineamiento_examen'))    
    

    return await render_template('cuestionario/lineamiento.html')




@cuestionario_route.after_request
async def set_response_headers(response):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response


@cuestionario_route.route('/lineamiento/examen', methods=['GET', 'POST'])
@login_required
async def lineamiento_examen():
    pregunta_1 : str = ""
    pregunta_2 : str = ""
    pregunta_3 : str = ""
    pregunta_4 : str = ""
    pregunta_5 : str = ""  


    if "lineamiento_cuestionario_completado" in session:
        cuestionario_completado = session["lineamiento_cuestionario_completado"]

        if cuestionario_completado == 1:
            return redirect(url_for('cuestionario.lineamiento_end'))


    session["lineamiento_info"] = 1
        
        
    if  request.method == 'POST':
        form: dict = await request.form
        
        pregunta_1 = form.get("pregunta_1", "")
        pregunta_2 = form.get("pregunta_2", "")
        pregunta_3 = form.get("pregunta_3", "")
        pregunta_4 = form.get("pregunta_4", "")
        pregunta_5 = form.get("pregunta_5", "")

        
        if not pregunta_1 or not pregunta_2 or not pregunta_3 or not pregunta_4 or not pregunta_5:
            await flash("Falta algun campo por llenar", category="error")

        else:
            usuario = await User.get(current_user.auth_id)

            fecha_realizado = datetime.now()
            
            user_encuesta = UserData(user_id=current_user.auth_id  ,name=usuario.full_name, email=usuario.email, dep=usuario.dep)
            encuesta = LineamientoSeguridadInfo(fecha_realizado=fecha_realizado, user_info=user_encuesta, pregunta_1=pregunta_1, pregunta_2=pregunta_2, pregunta_3=pregunta_3, pregunta_4=pregunta_4, pregunta_5=pregunta_5)
            
            encuesta_id = await encuesta.create()

            session["lineamiento_id"] = str(encuesta_id.id)
            session["lineamiento_cuestionario_completado"] = 1

            return redirect(url_for('cuestionario.lineamiento_end'))        
        
        
    return await render_template('cuestionario/lineamiento_examen.html')



@cuestionario_route.route('/lineamiento/end', methods=['GET', 'POST'])
@login_required
async def lineamiento_end():

    if 'lineamiento_id' in session:
        id_cuestionario = session["lineamiento_id"]

    
    return await render_template("cuestionario/lineamiento_end.html", id_cuestionario=id_cuestionario)



@cuestionario_route.route('/lineamiento/pdf/<string:id>', methods=['GET','POST'])
@login_required
async def lineamiento_pdf(id):

    cuestionario = await LineamientoSeguridadInfo.get(id)

    fecha_realizado = str(cuestionario.fecha_realizado)[:10]

    respuesta1 = {"opcion1": " ", "opcion2" : " ", "opcion3" : " "}

    if cuestionario.pregunta_1 == "1":
        respuesta1["opcion1"] = "X"

    if cuestionario.pregunta_1 == "2":
        respuesta1["opcion2"] = "X"
    
    if cuestionario.pregunta_1 == "3":
        respuesta1["opcion3"] = "X"

    
    respuesta2 = {"opcion1": " ", "opcion2" : " ", "opcion3" : " "}

    if cuestionario.pregunta_2 == "1":
        respuesta2["opcion1"] = "X"

    if cuestionario.pregunta_2 == "2":
        respuesta2["opcion2"] = "X"
    
    if cuestionario.pregunta_2 == "3":
        respuesta2["opcion3"] = "X"

    

    respuesta3 = {"opcion1": " ", "opcion2" : " ", "opcion3" : " "}

    if cuestionario.pregunta_3 == "1":
        respuesta3["opcion1"] = "X"

    if cuestionario.pregunta_3 == "2":
        respuesta3["opcion2"] = "X"
    
    if cuestionario.pregunta_3 == "3":
        respuesta3["opcion3"] = "X"

    
    respuesta4 = {"opcion1": " ", "opcion2" : " ", "opcion3" : " "}

    if cuestionario.pregunta_4 == "1":
        respuesta4["opcion1"] = "X"

    if cuestionario.pregunta_4 == "2":
        respuesta4["opcion2"] = "X"
    
    if cuestionario.pregunta_4 == "3":
        respuesta4["opcion3"] = "X"



    respuesta5 = {"opcion1": " ", "opcion2" : " ", "opcion3" : " "}

    if cuestionario.pregunta_5 == "1":
        respuesta5["opcion1"] = "X"

    if cuestionario.pregunta_5 == "2":
        respuesta5["opcion2"] = "X"
    
    if cuestionario.pregunta_5 == "3":
        respuesta5["opcion3"] = "X"


    respuestas = {"fecha": fecha_realizado, "respuesta1" : respuesta1, "respuesta2" : respuesta2, "respuesta3" : respuesta3, "respuesta4" : respuesta4, "respuesta5" : respuesta5}

    nombre_archivo = f"Lineamiento - {cuestionario.user_info.name} - {cuestionario.fecha_realizado}.pdf"

    out = await render_template('cuestionario/lineamiento_pdf.html', cuestionario=cuestionario, respuestas=respuestas)

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

    response = await make_response(pdf)

    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={nombre_archivo}'

    return response


@cuestionario_route.route('/all', methods=['GET', 'POST'])
@login_required
async def all():

    return await render_template("cuestionario/cuestionarios_all.html")

@cuestionario_route.route('ajaxAll', methods=['GET','POST'])
@login_required
async def ajaxAll():

    if request.method == 'POST':
        form: dict = await request.form
        draw: str = ""
        start: int = 0
        rowperpager: int = 0
        searchValue: str = ""

        draw = form.get("draw", "")
        start = int(form.get("start", 0))
        rowperpager = int(form.get("length", 0))
        searchValue = form.get("search[value]", "")

        print(draw)  
        print(start)
        print(rowperpager)
        print(searchValue)
        
        totalRows = await Cuestionarios.all().count() 
        
        if searchValue == "":
            cuestionarios = await Cuestionarios.find().skip(start).limit(rowperpager).to_list()
        else:
            cuestionarios = await Cuestionarios.find(FortalecimientoSegudadInfo.user_info.name == f"{searchValue}", 
                                                 LineamientoSeguridadInfo.user_info.name == f"{searchValue}").skip(start).limit(rowperpager).to_list()
        
        
        #print(cuestinario_fortalecimiento)
        
        totalRowsFilter = len(cuestionarios)
        
        print('total filtrado', totalRowsFilter)

        data = []

        for row in cuestionarios:          
            

            if row.codigo == "FO-OR-019 - Fortalecimiento":
                url_codigo = f"/cuestionario/fortalecimiento/pdf/{row.id}"
            else:
                url_codigo = f"/cuestionario/lineamiento/pdf/{row.id}"


            data.append({
                'fecha' : row.fecha_realizado,
                'nombre' : row.user_info.name,
                'codigo' : row.codigo,
                'pdf' :  f'<a role="button" href="{url_codigo}" class="btn btn-danger"> Descargar PDF</a>'
            })
            
        response = {
            'draw' : draw,
            'recordsTotal' : totalRowsFilter,
            'recordsFiltered' : totalRows,
            'aaData' : data
        }
        
        
        
        return jsonify(response)  
