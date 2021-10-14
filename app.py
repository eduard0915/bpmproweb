from decouple import config
from flask import Flask, render_template, request, flash
from  flask_mail import Mail, Message


app = Flask(__name__)


@app.route('/')
def home():
    title = 'BPMPro'
    return render_template('home.html', title=title)


app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('message')
        subject = request.form.get('subject')

        mail = Mail(app)
        msg = Message(subject=subject,
                      body=f'Nombre cliente: {name}\nE-mail: {email}\nTelefóno: {phone}\n\n\n{message}',
                      sender=config('MAIL_USERNAME'),
                      recipients=[config('MAIL_RECIPIENTS')]
                      )
        mail.send(msg)
        success_message = 'Su mensaje se ha enviado satisfactoriamente'
        flash(success_message)
        render_template('contact2.html', success=True)
    title = 'BPMPro - Contáctenos'
    return render_template('contact2.html', title=title)


if __name__ == '__main__':
     app.run()
