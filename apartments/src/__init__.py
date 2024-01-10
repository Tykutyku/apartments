from flask import Flask, render_template, request, flash, redirect, url_for, session
from pymongo import MongoClient
from forms import ContactForm, RegistrationForm, LoginForm
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

load_dotenv() 

app = Flask(__name__)
app.secret_key = 'my_secret_key'

mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = os.getenv('MAIL_USERNAME')
app.config["MAIL_PASSWORD"] = os.getenv('MAIL_PASSWORD')
app.config["MONGO_URI"] = os.getenv('MONGO_URI')

mail.init_app(app)

def get_mongo_client():
    return MongoClient(app.config["MONGO_URI"])

@app.route("/")
def home():
    with get_mongo_client() as client:
        db = client.apartments
        news_collection = db.news

        all_news = list(news_collection.find())  

    return render_template("home.html", news=all_news)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate():
            msg = Message(form.subject.data, sender='contact@example.com', recipients=['itykutyku@gmail.com'])
            msg.body = f"From: {form.name.data} <{form.email.data}>\n{form.message.data}"
            mail.send(msg)
            return render_template('contact.html', success=True)
        else:
            flash('All fields are required.')

    return render_template('contact.html', form=form)

@app.route("/energy")
def energy():
    return render_template('energy.html')

@app.route("/rent")
def rent():
    return render_template('rent.html')

@app.route("/tenant")
def tenant():
    return render_template('tenant.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        with get_mongo_client() as client:
            db = client.apartments
            users_collection = db.users

            # Check if the user already exists
            if users_collection.find_one({'email': form.email.data}):
                flash('Email address is already registered.')
                return render_template('register.html', form=form)

            # Add the user to the database (hash the password in production)
            result = users_collection.insert_one({
                'username': form.username.data,
                'email': form.email.data,
                'password': form.password.data,  # Note: In production, hash the password
            })

            if result.inserted_id:
                flash('Registration successful. You can now log in.')
                return redirect(url_for('login'))
            else:
                flash('Registration failed. Please try again.')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'POST' and form.validate():
        with get_mongo_client() as client:
            db = client.apartments
            users_collection = db.users

            user = users_collection.find_one({
                'email': form.email.data,
                'password': form.password.data  # Note: In production, hash the password
            })

            if user:
                # User authenticated, you can add session handling here if needed
                session['user_id'] = str(user['_id'])  # Store user ID in the session
                flash('Login successful!')
                return redirect(url_for('home'))
            else:
                flash('Invalid email or password.')

    return render_template('login.html', form=form)

if __name__ == "__main__":
    app.run()
