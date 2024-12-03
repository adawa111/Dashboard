from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Clave para manejar las sesiones

# Usuarios válidos
users = {
    "admin": "123456",
    "user": "654321"
}

# Ruta del dashboard
@app.route('/dashboard')
def dashboard():
    # Verifica si el usuario ha iniciado sesión
    if 'user' in session:
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))
app.secret_key = 'tu_clave_secreta'  # Clave para manejar las sesiones

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Verifica si las credenciales son correctas
        if username in users and users[username] == password:
            session['user'] = username  # Guarda el usuario en la sesión
            return redirect(url_for('dashboard'))
        else:
            return "Usuario o contraseña incorrectos", 401
    return render_template('login.html')

@app.route('/')
def without():
    return redirect(url_for('dashboard'))


# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('user', None)  # Elimina al usuario de la sesión
    return redirect(url_for('login'))
def without():
    return redirect(url_for('dashboard'))

@app.route('/<path:invalid_path>')
def handle_invalid_path(invalid_path):
    # Redirigir a la página principal (dashboard)
    return redirect(url_for('dashboard'))

#cambio port a 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080',debug=True)

