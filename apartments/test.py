from flask import Flask, render_template, request, flash
from pymongo import MongoClient
from forms import ContactForm
from flask_mail import Mail, Message

app = Flask(__name__)
app.secret_key = 'my_secrest_key'

mail = Mail()
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'itykutyku@gmail.com'
app.config["MAIL_PASSWORD"] = 'nmmz plqo jmin lsae '

mail.init_app(app)


def get_mongo_client():
    return MongoClient("mongodb+srv://Admin:ZAQ!2wsx@student-apartments.t7wirup.mongodb.net/")

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
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      msg = Message(form.subject.data, sender='contact@example.com', recipients=['itykutyku@gmail.com'])
      msg.body = """
From: %s &lt;%s&gt;
%s
""" % (form.name.data, form.email.data, form.message.data)
      mail.send(msg)
      return render_template('contact.html', success=True)
  elif request.method == 'GET':
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

@app.route("/login")
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run(ssl_context=('cert.pem', 'key.pem'))
