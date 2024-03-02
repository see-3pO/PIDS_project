from flask import session, redirect, url_for
def logging_out():
    #removing the session data to log out the user
    session.pop('loggedin', None)
    session.pop('user_id', None)
    session.pop('username',None)

    #return to loginpage
    return redirect(url_for('login'))