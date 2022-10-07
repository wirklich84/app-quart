from quart import Blueprint, render_template, request, flash, redirect, url_for, session
from models.user import User
from quart_bcrypt import check_password_hash, async_generate_password_hash
from quart_auth import login_user, AuthUser, logout_user, current_user

from routes import cuestionario


user_route = Blueprint('user',  __name__, url_prefix='/user',template_folder='templates')

@user_route.route("/register", methods=['GET', 'POST'])
async def user_register():
    name: str = ""
    username : str = ""
    password : str = ""
    password_confirm : str = ""

    if request.method == 'POST':
        form: dict = await request.form
        
        name = form.get("name", "")
        username = form.get("email", "")
        password = form.get("password", "")
        password_confirm = form.get("password_confirm", "")
        
        password_hash = await async_generate_password_hash(password)
        
        user = await User.find_one(User.email == username)
        
        print(user)
        
        if not username or not password:
            await flash("Usuario y / o contraseña oblogatorios.    ", category="error")
        
        if user:
            await flash("Usuario ya existe", category="error")
        else:
            user =  User(full_name=name, email=username, password= password_hash)      
            await user.create()
            print("se creo el usuario")
            return redirect(url_for('cuestionario.index'))    
        
    
    return await render_template('user/register.html')
    

@user_route.route("/login", methods=['GET', 'POST'])
async def user_login():   
    user_id : str = ""
    username : str = ""
    password : str = ""
    

    if await current_user.is_authenticated:
        return redirect(url_for('cuestionario.index'))
    
    if request.method == 'POST':
        form: dict = await request.form
        username = form.get("email", "")      
        password = form.get("password", "")
        
        if not username or not password:
            await flash("Usuario y / o contraseña oblogatorios.    ", category="error")   
            
        user = await User.find_one(User.email == username)
        
        if user:            
            if check_password_hash(user.password, password):
                session["fortalecimiento_info"] = 0
                login_user(AuthUser(str(user.id)))
                return redirect(url_for('cuestionario.index'))
            else:
                await flash("Usuario y / o contraseña no son validos", category="error")            
            
            
        return await render_template('user/login.html')
    
    
    return await render_template('user/login.html' )


@user_route.route("/logout", methods=['GET', 'POST'])
async def logout():    
    session.pop('fortalecimiento_info', None)
    session.pop('fortalecimiento_cuestionario_completado', None)
    session.pop('lineamiento_info', None)
    session.pop('lineamiento_cuestionario_completado', None)
    logout_user()
    return redirect(url_for('user.user_login'))
