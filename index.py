from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, request, redirect, url_for, session

import firebase_admin
from firebase_admin import credentials,auth,firestore

cred = credentials.Certificate("dashboard-temas-iot-firebase-adminsdk-z4sc1-9d8cd4dd29.json")
firebase_app = firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Clave para manejar las sesiones

""" 
# Crea un documento en la colección "users"
doc_ref = db.collection('users').document('alopez')
doc_ref.set({

    'first': 'Alan',

    'last': 'Lopez',

    'born': 1997

})
""" 
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
        '''try:
            docs = db.collection('recopilar_datos').stream()
            for doc in docs:
                data = doc.to_dict()
                co2_ppm = data.get('co2_ppm', 'No data')
                temperature = data.get('temperature', 'No data')
                timestamp = data.get('timestamp', 'No data')
                print(f"Documento ID: {doc.id}")
                print(f"  CO2 PPM: {co2_ppm}")
                print(f"  Temperatura: {temperature}")
                print(f"  Timestamp: {timestamp}")
                print("-" * 20)
        except Exception as e:
            print(f"Error al acceder a Firestore: {e}")
        '''
        return render_template('home.html', user=session['user'])
    return redirect(url_for('login'))

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

#esto es para enviar los datos al dashboard en tiempo real owo
@app.route('/api/data', methods=['GET'])
def get_data():
    try:
        docs = db.collection('recopilar_datos').stream()
        data = []

        for doc in docs:
            document = doc.to_dict()
            data.append({
                'co2_ppm': document.get('co2_ppm', -128),
                'temperature': document.get('temperature', -128),
                'timestamp': document.get('timestamp', 'Sin fecha')
            })

        return {"data": data}, 200
    except Exception as e:
        print(f"Error al acceder a Firestore: {e}")
        return {"error": str(e)}, 500


#cambio port a 8080
if __name__ == '__main__':
    app.run(host='0.0.0.0',port='8080',debug=True)


