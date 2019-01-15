# from flask_mail import Message
# from flask import render_template
# from flask_app import mail
# from .. import config
#
# def send_email(to, subject, template, **kwargs):
#     msg = Message(subject,
#     sender='<from1213284679@qq.com>', recipients=[to])
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     mail.send(msg)
#
# # send_email()
# print(config)