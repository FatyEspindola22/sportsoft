from flask import Flask, render_template, request, redirect, url_for, flash, session,send_from_directory
from flask_session import Session
from flask_mysqldb import MySQL
from flask_socketio import SocketIO
import pandas as pd
import MySQLdb.cursors
import bcrypt
import string
import re
import random
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import cv2
import serial,time 
import sys 
import cv2
import mediapipe as mp
import numpy as np
import os 
from math import acos, degrees
from string import Template
import warnings
warnings.filterwarnings('ignore')


#clase para inicializar la aplicacion flask
#flask es un framework de software
app = Flask(__name__)
# Configurar la clave secreta para la sesión
app.secret_key = 'tu_clave_secreta_aqui'
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
#configuracion para acceder al servidor y base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Univalle'
app.config['MYSQL_DB'] = 'dbproyecto3'

#inicializar la clase mysql para conectar al servidor con la app web
mysql = MySQL(app)

#ruta para la vista home
#para crear una ruta en la pagina web se debe comenzar con @
#ventana principal de la app web
@app.route('/')
def home():
    return render_template('view_login.html')

#ruta para la vista login
#funcion para acceder la vista login o inicio de sesion
@app.route('/login_view')
def login_view():
    return render_template('view_login.html')

@app.route('/general_view')
def general_view():
    return render_template('view_principal.html')

@app.route('/view_register')
def view_register():
    return render_template('view_register.html')

@app.route('/angulos')
def angulos():
    return render_template('angulos_3.py')

@app.route('/view_register_patient')
def view_register_patient():
    return render_template('view_register_patient.html')

@app.route('/view_register_employe')
def view_register_employe():
    return render_template('view_register_employee.html')

@app.route('/view_patient')
def view_patient():
    return render_template('view_patient.html')

@app.route('/view_employe')
def view_employe():
    return render_template('view_employe.html')

@app.route('/monitoreo')
def Monitoreo1():
    return render_template('Monitoreo.html')
#mostrar las lista de registros
#funcion para acceder a la vista de registros de usuarios
@app.route('/list_users', methods=['GET'])
def users_list():
    #acceder a la base de datos
    #ejecutamos los comandos de sql
    #mostrar la lista de usuarios
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user')
    data = cursor.fetchall()
    return render_template('view_user.html', users=data)

@app.route('/list_patient', methods=['GET'])
def patient_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE role = 3')
    data = cursor.fetchall()
    return render_template('view_patient.html', users=data)

@app.route('/list_employe', methods=['GET'])
def employe_list():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE role = 2')
    data = cursor.fetchall()
    return render_template('view_employe.html', users=data)


@app.route('/register_patient')
def register_patient():
    # Consulta a la base de datos para obtener usuarios con rol igual a 3
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id_user,full_name FROM user WHERE role = 3')
    data = cursor.fetchall()
    return render_template('view_register_patient.html', users=data)

@app.route('/register_employe')
def register_employe():
    # Consulta a la base de datos para obtener usuarios con rol igual a 3
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id_user,full_name FROM user WHERE role = 2')
    data = cursor.fetchall()
    return render_template('view_register_employee.html', users=data)


@app.route('/Monitoreo', methods=['GET'])
def Monitoreo():
    # Verifica si hay un paciente en sesión
    username = session['username']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE username = %s', (username,))
    data = cursor.fetchall()
    print(data)  
    cursor.execute('SELECT * FROM patient WHERE user_id_user = %s', (data[0]['id_user'],))
    data1 = cursor.fetchall()
    print(data1)
    cursor.execute('SELECT * FROM angles WHERE patient_id_patient = %s', (data1[0]['id_patient'],))
    data2 = cursor.fetchall()
    print(data2)  
    return render_template('Monitoreo.html', users=data,users1=data1,users2=data2)
    
@app.route('/Monitoreop')
def Monitoreop():
    # Consulta a la base de datos para obtener usuarios con rol igual a 3
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT id_user,full_name FROM user WHERE role = 3')
    data = cursor.fetchall()
    return render_template('Monitoreo.html', user=data)

@app.route('/mom/<id>', methods=['GET','POST'])
def mom(id):
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE id_user = %s', (id,))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM patient WHERE user_id_user = %s', (id,))
    data1 = cursor.fetchall()
    print(data)
    print(data1)
    
    result_list = list(data1[0])
    id_patient = result_list[0]
    print(id_patient) 

    cursor.execute('SELECT * FROM angles WHERE patient_id_patient = %s', (data1[0]['id_patient'],))
    data2 = cursor.fetchall()
    print(data2) 
    return render_template('Monitoreo2.html', users=data, users1=data1, users2=data2)


@app.route('/monitoreo3/<id>', methods=['GET','POST'])
def monitoreo3(id): 
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE id_user = %s', (id,))
    data = cursor.fetchall()

    cursor.execute('SELECT * FROM patient WHERE user_id_user = %s', (id,))
    data1 = cursor.fetchall()
    print(data)
    print(data1)
    
    result_list = list(data1[0])
    id_patient = result_list[0]
    print(id_patient) 

    cursor.execute('SELECT * FROM angles WHERE patient_id_patient = %s', (data1[0]['id_patient'],))
    data2 = cursor.fetchall()
    print(data2) 
    return render_template('Monitoreo3.html', users=data[0], users1=data2[0])

#funcion para enviar correos
def send_email(email, message):
    smtp_server = "smtp.gmail.com"
    port = 587  # puerto para TLS
    sender_email = "fatyespindola34@gmail.com"
    sender_password = " "

    server = smtplib.SMTP(smtp_server, port)
    server.starttls()
    server.login(sender_email, sender_password)
    subject = message
    body = "Sportsoft le da la bienvenida al sitio web"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    server.sendmail(sender_email, email, message.as_string())
    
#funcion para registrar un nuevo usuario
#creamos una ruta para enviar los datos al servidor
@app.route('/add_user', methods=['POST'])
def add_user():
    #acceder a los campos de texto de tu formulario
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        ci = request.form['ci']
        birthdate = request.form['birthdate']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password'].encode('utf-8')
        #encriptar la contrasenha
        #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        if re.search(r"\.com$", email):
           
            #conectar al servidor para enviar los datos
            cursor = mysql.connection.cursor()
            #consulta para registrar datos
            cursor.execute('INSERT INTO user (full_name,username, ci,birthdate,email, role,password) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (full_name,username,ci,birthdate, email,role, password))
            mysql.connection.commit()
            
            session['full_name'] = full_name
            session['email'] = email 
            flash('Su cuenta ha sido creado con exito', "info")
            print("El correo electrónico ingresado tiene dominio .com")
        else:
           flash("El correo electrónico ingresado no tiene dominio .com", "info")
           print("El correo electrónico ingresado no tiene dominio .com")
    return redirect(url_for('users_list'))

@app.route('/add_user1', methods=['POST'])
def add_user1():
    #acceder a los campos de texto de tu formulario
    if request.method == 'POST':
        full_name = request.form['full_name']
        username = request.form['username']
        ci = request.form['ci']
        birthdate = request.form['birthdate']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password'].encode('utf-8')
        #encriptar la contrasenha
        #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())

        if re.search(r"\.com$", email):
           
            #conectar al servidor para enviar los datos
            cursor = mysql.connection.cursor()
            #consulta para registrar datos
            cursor.execute('INSERT INTO user (full_name,username, ci,birthdate,email, role,password) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (full_name,username,ci,birthdate, email,role, password))
            mysql.connection.commit()
            
            session['full_name'] = full_name
            session['email'] = email 
            flash('Su cuenta ha sido creado con exito', "info")
            print("El correo electrónico ingresado tiene dominio .com")
        else:
           flash("El correo electrónico ingresado no tiene dominio .com", "info")
           print("El correo electrónico ingresado no tiene dominio .com")
    return redirect(url_for('view_register_patient'))


@app.route('/add_patient', methods=['GET'])
def add_patient():
    if request.method == 'GET':
        # Obtener el ID del usuario seleccionado
        user_id_user = request.form['user_id_user']
        weigth = request.form['weigth']
        height = request.form['height']
        tren_superior = request.form['trensuperior']
        tren_inferior = request.form['treninferior']
        
            # Llenar los campos ocultos con el nombre y el ID del usuario seleccionado
        #request.form['selected_user_id'] = user_id_user
        user_id_user = request.form['user_id_user']
            #conectar al servidor para enviar los datos
        cursor = mysql.connection.cursor()
            #consulta para registrar datos
        cursor.execute('INSERT INTO patient (weigth,height, tren_superior,tren_inferior,user_id_user) VALUES (%s, %s, %s, %s, %s)',
        (weigth,height,tren_superior,tren_inferior, user_id_user))
        mysql.connection.commit()

        flash('los datos fueron creados con exito', "info")

    return redirect(url_for('register_patient'))


@app.route('/add_employe', methods=['POST'])
def add_employe():
    if request.method == 'POST':
        # Obtener el ID del usuario seleccionado
        user_id_user = request.form['user_id_user']
        position = request.form['position']
        
            # Llenar los campos ocultos con el nombre y el ID del usuario seleccionado
        #request.form['selected_user_id'] = user_id_user
        user_id_user = request.form['user_id_user']
            #conectar al servidor para enviar los datos
        cursor = mysql.connection.cursor()
            #consulta para registrar datos
        cursor.execute('INSERT INTO employee (position,user_id_user) VALUES (%s, %s)',
        (position, user_id_user))
        mysql.connection.commit()

        flash('los datos fueron creados con exito', "info")

    return redirect(url_for('register_employe'))

@app.route('/get/<id>', methods=['GET'])
def get_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM user WHERE id_user = %s', (id,))
    data = cursor.fetchall()
    print(data)
    return render_template('modificar_user.html', user=data[0])

@app.route('/guardar_video', methods=['POST'])
def guardar_video():
    print("Recibiendo solicitud para guardar video")
    user_id = request.form.get('userId')
    video = request.files['video']
    print(f"User ID: {user_id}")
    print(f"Video: {video}")

    if video:
        folder_name = f"videos/user_{user_id}"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        
        video_filename = f"{folder_name}/video.mp4"
        video.save(video_filename)
        return 'Video guardado exitosamente'

    return 'Error al guardar el video', 500

@app.route('/update/<id>', methods=['POST'])
def update_user(id):
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE user SET name = %s, email = %s, password = %s WHERE id_user = %s', (name, email, password, id))
        mysql.connection.commit()
        flash('Registro actualizado', 'info')
    return redirect(url_for('users_list'))

#eliminar registro existente de la tabla usuario
@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_user(id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT role FROM user WHERE id_user = %s', (id,))
    user = cursor.fetchone()

    if user and user[0] == 2:
        # El usuario tiene un rol de empleado, elimina relaciones foráneas en la tabla de empleados
        cursor.execute('DELETE FROM employee WHERE user_id_user = %s', (id,))
    elif user and user[0] == 3:
        # El usuario tiene un rol de paciente, elimina relaciones foráneas en la tabla de pacientes
        cursor.execute('DELETE FROM patient WHERE user_id_user = %s', (id,))

    # Elimina al usuario
    cursor.execute('DELETE FROM user WHERE id_user = %s', (id,))
    mysql.connection.commit()
    flash('Registro eliminado')
    return redirect(url_for('users_list'))


#funcion para iniciar sesion
@app.route('/login', methods=['GET','POST'])
def login():
    if request.method=="POST":
       username = request.form['username']
       password = request.form['password'].encode('utf-8')
    
       cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       cursor.execute('SELECT * FROM user WHERE username=%s',(username,))
       user = cursor.fetchone()
       cursor.close()
       if len(user) > 0:
           
            session['username'] = user['username']
            session['role'] = user['role']
               #session['full_name'] = user['full_name']
            return redirect(url_for('general_view')) 
       else:
           flash('Email o contrasenha incorrecto', "info")
           return "Error usuario o contrasenha"
    else:
       return redirect(url_for('home'))  

#funcion para cerrar sesion
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home')) 


# Ruta para mostrar la página web
@app.route('/angulos')
def angulos():
    
    return redirect(url_for('users_list'))



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=81, debug=True)

#calculo de los angulos




