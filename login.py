from flask import Flask, render_template, url_for, request, redirect, session, flash
import bcrypt
import mysql.connector
from connect import connect_db

def login_user():
    if request.method == 'POST' and 'national-id' in request.form and 'password' in request.form:
        nationalid = request.form['national-id']
        password = request.form['password']

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM driver WHERE national_id = %s', (nationalid,))
            account = cursor.fetchone()

            if account:
                hashed_password = account[4]

                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    session['loggedin'] = True
                    session['driver_id'] = account[0]
                    session['first_name'] = account[1]
                    session['last_name'] = account[2]

                    flash('Login successful!', 'success')
                    return redirect(url_for('display_page'))
                else:
                    flash('Incorrect password. Please try again.', 'error')
            else:
                flash('Account does not exist. Please register.', 'error')

        except mysql.connector.Error as e:
            print(f"Error: {e}")
            flash('An error occurred. Please try again.', 'error')

        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')
