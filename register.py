from flask import Flask, render_template, url_for, request, redirect, session, jsonify
from connect import connect_db
import bcrypt
import re
import mysql.connector

def registration():
    msg = ''

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        nationalid = request.form['national-id']
        password = request.form['password']
        email = request.form['email']

        if not all([firstname, lastname, nationalid, password, email]):
            msg = 'Please fill out the form'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z]+', firstname):
            msg = 'Firstname must contain only characters'
        elif not re.match(r'[A-Za-z]+', lastname):
            msg = 'Lastname must contain only characters'
        elif not re.match(r'[0-9]+', nationalid):
            msg = 'Nationalid must contain only numbers'
        else:
            try:
                conn = connect_db()
                cursor = conn.cursor()

                cursor.execute('SELECT * FROM driver WHERE national_id = %s', (nationalid,))
                account = cursor.fetchone()

                if account:
                    msg = 'Account already exists'
                    return redirect(url_for('login'))
                else:
                    salt = bcrypt.gensalt()
                    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
                    print(f"Hashed Password: {hashed_password}")

                    cursor.execute('INSERT INTO driver (first_name, last_name, national_id, password, email) VALUES (%s, %s, %s, %s, %s)',
                                   (firstname, lastname, nationalid, hashed_password, email))

                    conn.commit()
                    msg = 'You have successfully registered'
                    return redirect(url_for('login'))
                
            except mysql.connector.Error as e:
                print(f"Database error: {e}")
                msg = 'Database error'
            finally:
                cursor.close()
                conn.close()

    return render_template('register.html', msg=msg)
