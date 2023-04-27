from flask_login import login_required
from functools import wraps
from flask import session, render_template, flash

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("necesitas loguearte")
            return render_template('admin/login.html')
    return decorated_function

