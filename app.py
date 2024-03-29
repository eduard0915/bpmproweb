from decouple import config
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_xcaptcha import XCaptcha
from flask_mail import Mail, Message
from flask_sitemap import Sitemap


app = Flask(__name__, static_folder='static', static_url_path='')
ext = Sitemap(app=app)

application = app

app.config['XCAPTCHA_SITE_KEY'] = config('XCAPTCHA_SITE_KEY')
app.config['XCAPTCHA_SECRET_KEY'] = config('XCAPTCHA_SECRET_KEY')
app.config['XCAPTCHA_VERIFY_URL'] = "https://hcaptcha.com/siteverify"
app.config['XCAPTCHA_API_URL'] = "https://hcaptcha.com/1/api.js"
app.config['XCAPTCHA_DIV_CLASS'] = "h-captcha"

# app.config.update(dict(
#     XCAPTCHA_SITE_KEY=config('RECAPTCHA_SITE_KEY'),
#     XCAPTCHA_SECRET_KEY=config('RECAPTCHA_SECRET_KEY'),
# ))

xcaptcha = XCaptcha(app=app)

app.config['SECRET_KEY'] = config('SECRET_KEY')
app.config['MAIL_SERVER'] = config('MAIL_SERVER')
app.config['MAIL_PORT'] = config('MAIL_PORT')
app.config['MAIL_USE_TLS'] = config('MAIL_USE_TLS')
app.config['MAIL_USERNAME'] = config('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = config('MAIL_PASSWORD')

mail = Mail(app)

@app.errorhandler(404)
@app.route('/404')
def page_not_found(e):
    title = 'Página No Encontrada'
    return render_template('404.html', title=title), 404


@app.route('/')
def home():
    title = 'BPMPro - Gestión Documental y Calidad'
    return render_template('home.html', title=title)


@ext.register_generator
def home():
    yield 'home', {}


@app.route('/contactanos', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        if xcaptcha.verify():
            name = request.form.get('name')
            company = request.form.get('company')
            cargo = request.form.get('cargo')
            email = request.form.get('email')
            phone = request.form.get('phone')
            message = request.form.get('message')
            subject = 'Solicitud de Cotización'

            msg = Message(subject=subject,
                          body=f'Nombre cliente: {name}, \nCargo: {cargo}, \nEmpresa: {company}, \nE-mail: {email}'
                               f'\nTeléfono: {phone}\n\n\n{message}',
                          sender=config('MAIL_USERNAME'),
                          recipients=[config('MAIL_RECIPIENTES')]
                          )
            mail.send(msg)
            flash(
                'Mensaje se ha enviado satisfactoriamente, uno de nuestros representantes se comunicará con usted',
                'info')
            title = 'Contáctenos'
            render_template('contact.html', success=True, title=title)
        else:
            flash('Error: Confirmar ReCaptcha!!', 'danger')
            return redirect(url_for('contact'))
    title = 'Contáctenos'
    return render_template('contact2.html', title=title)


@ext.register_generator
def contact():
    yield 'contact', {}


if __name__ == '__main__':
    app.run(debug=config('DEBUG'))
