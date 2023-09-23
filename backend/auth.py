from flask import Blueprint, render_template, url_for, request, jsonify, redirect, flash, session
from backend.db import db
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# untuk membuat blueprint, kita harus mendeklarasikan sebuah variable 
# didalam blueprint ada 2 argument,
authapp = Blueprint('authapp', __name__)


# ini adalah fungsi untuk melakukan pengecekan apakah session ada atau tidak
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Anda harus login', 'danger')
            return redirect(url_for('authapp.login'))
    return wrapper


@authapp.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'POST':
        # tangkap data dari form
        data = {
            'username': request.form['username'],
            'password' : request.form['password']
        }
        # cek user
        user = db.collection('users').document(data['username']).get().to_dict()
        if user:
        # cek password form dan password di database
            if check_password_hash(user['password'], data['password']):
                session['user'] = user
                flash('Berhasil Login', 'success')
                return redirect(url_for('mahasiswa'))
            else:
                flash('Username/Password Anda Salah', 'danger')
                return redirect(url_for('authapp.login'))
        else:
        # redirect
            flash('Username/Password Anda Salah', 'danger')
            return redirect(url_for('authapp.login'))
        
    # cek session terlebih dahulu
    if 'user' in session:
        flash('Anda Sudah Login', 'warning')
        return redirect(url_for('mahasiswa'))
    return render_template('login.html')


@authapp.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        # tangkap data dari form
        data = {
            'nama_lengkap': request.form['nama_lengkap'],
            'username': request.form['username'],
        }
        # cek password dan cek password_1
        if request.form['password'] != request.form['password_1']:
            flash('Password Tidak Sama', 'danger')
            return redirect(url_for('authapp.register'))
        # cek username terdaftar atau tidak
        user = db.collection('users').document(data['username']).get().to_dict()
        if user:
            flash('Username Sudah Terdaftar', 'danger')
            return redirect(url_for('authapp.register'))
        # hash password
        data['password'] = generate_password_hash(request.form['password'], 'sha256')
        # simpan ke database
        db.collection('users').document(data['username']).set(data)
        # redirect ke login
        flash('Berhasil Membuat Akun, Silahkan Login', 'success')
        return redirect(url_for('authapp.login'))

    
    # proses get
    return render_template('register.html')


@authapp.route('/logout')
@login_required
def logout():
    session.clear()
    flash('Berhasil Logout', 'danger')
    return redirect(url_for('authapp.login'))

