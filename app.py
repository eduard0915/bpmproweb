from decouple import config
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_mail import Mail, Message
from flask_recaptcha import ReCaptcha

app = Flask(__name__)
recaptcha = ReCaptcha(app=app)

app.config.update(dict(
    RECAPTCHA_ENABLED=True,
    RECAPTCHA_SITE_KEY="6LeXPZceAAAAAN_kMEJh43DRHWFVdbjcvj63kzri",
    RECAPTCHA_SECRET_KEY="6LeXPZceAAAAAK4x3y4-nLCi5bZOQnsLVnEDD7Es",
))

recaptcha = ReCaptcha()
recaptcha.init_app(app)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')


@app.errorhandler(404)
@app.route('/404')
def page_not_found(e):
    title = 'Página No Encontrada'
    return render_template('404.html', title=title), 404


@app.route('/')
def home():
    title = 'BPMPro - Gestión Documental y Calidad'
    return render_template('home.html', title=title)


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
                      sender='bpmpro.noreply@gmail.com',
                      recipients=['ciel.techno@gmail.com']
                      )
        mail.send(msg)
        success_message = 'Su mensaje se ha enviado satisfactoriamente, uno de nuestros representantes se comunicará con usted'
        flash(success_message)
        render_template('contact2.html', success=True)
    title = 'BPMPro - Contáctenos'
    return render_template('contact2.html', title=title)


@app.route('/submit', methods=['POST'])
def submit():
    if recaptcha.verify():
        # flash('New Device Added successfully')
        return redirect(url_for('contact'))
    else:
        flash('Error!! Confirmar ReCaptcha')
        return redirect(url_for('conctact'))


if __name__ == '__main__':
    app.run()
