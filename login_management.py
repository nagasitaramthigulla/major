from flask_sqlalchemy import SQLAlchemy
from app import login_manager,app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+app.config['CWD']+'/db/twtranlsys.db'
db = SQLAlchemy(app)
from flask_login import UserMixin,login_required,login_user,logout_user,current_user
from flask import Response,redirect,render_template,request,abort

#...

class User(db.Model):
    """An admin user capable of viewing reports.

    :param str email: email address of user
    :param str password: encrypted password for the user

    """
    __tablename__ = 'user'

    username = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    authenticated = db.Column(db.Boolean, default=False)

    def __init__(self,username,name,password,authenticated=False):
        self.username=username
        self.name=name
        self.password=password
        self.authenticated=authenticated


    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.username

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve

    """
    return User.query.get(user_id)

@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(request.args.get("next","home"))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']  
        user = User.query.filter_by(username=username).first()
        if user!=None and user.password==password:
            login_user(user)
            return redirect(request.args.get("next","home"))
        else:
            return abort(401)
    else:
        return render_template("login.html",login=True)

@app.route("/signup",methods=['GET','POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(request.args.get("next","home"))
    if request.method=="POST":
        username = request.form['username']
        name = request.form['name']
        password = request.form['password']
        if username=="" or name=="" or password=="" or User.query.filter_by(username=username).first()!=None:
            return abort(409)
        user = User(username,name,password,True)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(request.args.get("next","home"))
    else:
        return render_template("signup.html",login=True)
        

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')