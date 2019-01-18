from flask_mail import Message
from flask import render_template
from flask_app import mail
from threading import Thread
from flask import current_app


def send_async_email(app, msg):
    # print('***********************async')
    with app.app_context():
        mail.send(msg)

def send_email(to, subject, template, **kwargs):
    msg = Message(subject,
    sender='<1213284679@qq.com>', recipients=[to])
    # msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    # mail.send(msg)
    # print('********************send')
    app = current_app._get_current_object()
    thr = Thread(target=send_async_email, args=(app, msg))
    thr.start()
    return thr




