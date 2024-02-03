from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    from .home import home_bp
    from .login import login_bp
    # from .connect_db import connect_db
    from .sitedetail_data import sitedetail_data
    

    app.register_blueprint(home_bp)
    app.register_blueprint(login_bp)
    # app.register_blueprint(connect_db)
    app.register_blueprint(sitedetail_data)

    return app
