from flask import Flask,redirect,url_for,render_template,request,session,flash
from flask_mysqldb import MySQL,MySQLdb
import MySQLdb.cursors
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager, login_user, logout_user, login_required
import datetime as dt
from datetime import datetime as dt2
from certificado import certificado
# Models:
from models.ModelUser import ModelUser
# Entities:
from models.entities.User import User

#Ingreso a la base de datos
app=Flask(__name__)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Chvzpon98.jachp'
app.config['MYSQL_DB'] = 'softapp'
mysql = MySQL(app)
login_manager_app = LoginManager(app)


#Rutas de ingreso

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(mysql, id)
    

@app.route("/",methods=['GET','POST'])
def home():
    return render_template("contenido.html")


@app.route('/layout', methods = ["GET", "POST"])
def layout():
    session.clear()
    return render_template("contenido.html")

@app.route("/Resultado")
def resultado():
    return render_template('Resultado.pdf')

#Registro de datos

@app.route('/registro', methods = ["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form['nombre']
        apellidos = request.form['apellidos']
        tipo_documento = request.form['tipo_documento']
        nro_documento = request.form['nro_documento']
        direccion = request.form['direccion']
        lugar_muestra = request.form['lugar_muestra']
        tipo_muestra = request.form['tipo_muestra']
        fecha_obtencion = request.form['fecha_obtencion']
        fecha_resultado = request.form['fecha_resultado']
        analisis = request.form['analisis']
        metodo = request.form['metodo']
        resultado = request.form['resultado']
        valores = request.form['decision_clinica']
        rango = request.form['rango_referencia']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("INSERT INTO pacientes (nombres, apellidos,tipo_documento,nro_documento,direccion,lugar_muestra,tipo_muestra,fecha_obtencion,fecha_resultado,analisis,metodo,resultado,valores,rango) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (nombre,apellidos,tipo_documento,nro_documento,direccion,lugar_muestra,tipo_muestra,fecha_obtencion,fecha_resultado,analisis,metodo,resultado,valores,rango,))
        mysql.connection.commit()
        certificado(nombre,apellidos,tipo_documento,nro_documento,direccion,lugar_muestra,tipo_muestra,fecha_obtencion,fecha_resultado,analisis,metodo,resultado,valores,rango)
        flash("Prueba registrada")
        return(redirect(url_for('registro')))
    else:
        return render_template('registro.html')

@app.route('/lista_pacientes', methods = ["GET", "POST"])
def lista_pacientes():

    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM pacientes")
    pacientes = cur.fetchall()
    mysql.connection.commit()

    return render_template("lista_pacientes.html", pacientes = pacientes)

@app.route('/imprimir/<idpacientes>')
def imprimir(idpacientes):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("SELECT * FROM pacientes WHERE idpacientes=%s", (idpacientes,))
    paciente = cur.fetchone()
    certificado(nombres=paciente["nombres"],apellidos=paciente["apellidos"],tipo_documento=paciente["tipo_documento"],nro_documento=paciente["nro_documento"],direccion=paciente["direccion"],lugar_muestra=paciente["lugar_muestra"],tipo_muestra=paciente["tipo_muestra"],fecha_obtencion=paciente["fecha_obtencion"],fecha_resultado=paciente["fecha_resultado"],analisis=paciente["analisis"],metodo=paciente["metodo"],resultado=paciente["resultado"],valores=paciente["valores"],rango=paciente["rango"])
    return redirect("/print")


@app.route("/destroy/<idpacientes>")
def destroy(idpacientes):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute("DELETE FROM pacientes WHERE idpacientes=%s", (idpacientes,))
    mysql.connection.commit()

    return redirect('/lista_pacientes')

@app.route('/print', methods = ["GET", "POST"])
def print():
    return render_template("print.html")

@app.route('/tipouser', methods = ["GET", "POST"])
def tipouser():
    session.clear()
    return render_template("tipouser.html")

@app.route('/about', methods = ["GET", "POST"])
def about():
    session.clear()
    return render_template("about.html")

@app.route('/categoria', methods = ["GET", "POST"])
def categoria():
    return render_template("categoria.html")

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name_day = dt.datetime.now()
        day = name_day.strftime("%A")
        time = name_day.strftime("%X")
        admin = User(0,0,0,request.form['email'],request.form['password'],"","","")
        logged_user = ModelUser.login(mysql, admin)
        hora_in = str(dt2.strptime(str(logged_user.Hora), '%X'))
        hora_fi = str(dt2.strptime(str(logged_user.Hora_final), '%X'))
        hora_inic = hora_in.split(sep=' ')
        hora_fina = hora_fi.split(sep=' ')
        hora_inicio = dt2.strptime(hora_inic[1],'%X')
        hora_final = dt2.strptime(hora_fina[1],'%X')
        hour = dt2.strptime(time,'%X')
        if logged_user != None:
            if day == logged_user.Turno and hora_inicio<=hour<=hora_final:
                if logged_user.Password:
                    login_user(logged_user)
                    return redirect(url_for('categoria'))
                else:
                    flash("Contraseña o Usuario Incorrecto")
                    return render_template('login.html')
            else:
                flash("Revise su turno, por favor!")
                return render_template('login.html')
        else:
            flash("Usuario no encontrado")
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

def status_401(error):
    return redirect(url_for('login'))
def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.run(debug=True)