from unicodedata import name
from pkg_resources import require
from quart import Blueprint, render_template, request, flash, redirect, url_for
from models.user import User
from quart_bcrypt import check_password_hash, async_generate_password_hash


user_route = Blueprint('user',  __name__, url_prefix='/user',template_folder='templates')

@user_route.route("/register", methods=['GET', 'POST'])
async def user_register():

    if request.method == 'POST':
        form: dict = await request.form
        
        name = form.get("name", "")
        username = form.get("email", "")
        password = form.get("password", "")
        password_confirm = form.get("password_confirm", "")
        
        password_hash = await async_generate_password_hash(password)
        
        user = User.find_one(User.email == username)
        
        if not username or not password:
            await flash("Usuario y / o contraseña oblogatorios.    ", category="error")
        
        if user:
            await flash("Usuario ya existe", category="error")
        else:
            user =  User(full_name=name, email=username, password= password_hash)      
            await user.create()         
        
    
    return await render_template('user/register.html')
    

@user_route.route("/login", methods=['GET', 'POST'])
async def user_login():   
    
    if request.method == 'POST':
        form: dict = await request.form
        username = form.get("email", "")      
        password = form.get("password", "")
        
        if not username or not password:
            await flash("Usuario y / o contraseña oblogatorios.    ", category="error")   
            
        user = await User.find_one(User.email == username)
        
        if user:            
            if check_password_hash(user.password, password):
                redirect(url_for('cuestionario.index'))
            else:
                print("no son")
            
            
            
        return await render_template('user/login.html')
    
    
    return await render_template('user/login.html' )
