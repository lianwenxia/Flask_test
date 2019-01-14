from flask import Flask
from flask import request
# from flask import current_app
from flask import render_template
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')
    # user_agent = request.headers.get('user-agent')
    # return '这是该网页的user agent：%s' % user_agent


@app.route('/hello<name>/')
def hello(name):
    return '<h1>Hello %s!</h1>' % name


if __name__ == "__main__":
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )
