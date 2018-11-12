import os

from flask import Flask, render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'myfavshows.sqlite'),
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
    import db
    db.init_app(app)

    import auth
    app.register_blueprint(auth.bp)

    import search
    app.register_blueprint(search.bp)

    import myfav
    app.register_blueprint(myfav.bp)

    import myshow
    app.register_blueprint(myshow.bp)

    @app.route('/about', methods=('GET',))
    def about():
        """About page"""
        return render_template('about.html')

    @app.route('/error', methods=('GET',))
    def error():
        """Error occurance page"""
        return render_template('error.html')

    return app


application = create_app()