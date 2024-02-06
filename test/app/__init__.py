from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    from .home import home_bp
    from .connect_db import connect_db
    from .billing_data import billing_data
    from .sitedetail_data import sitedetail_data
    from .Manualpoll_data import Manualpoll_data
    from .write_evc import write_evc
    from .ASGS_HOME import ASGS_HOME
    from .billing_data_asgs import billing_data_asgs

    app.register_blueprint(home_bp)
    app.register_blueprint(connect_db)
    app.register_blueprint(sitedetail_data)
    app.register_blueprint(billing_data)
    app.register_blueprint(Manualpoll_data)
    app.register_blueprint(write_evc)
    app.register_blueprint(ASGS_HOME)
    app.register_blueprint(billing_data_asgs)
    app.secret_key = "your_secret_key_here"
    return app
