from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register Blueprints
    from .home import home_bp
    from .connect_db import connect_db
    from .billing_data import billing_data
    from .sitedetail_data import sitedetail_data
    

    app.register_blueprint(home_bp)
    
    app.register_blueprint(connect_db)
    app.register_blueprint(sitedetail_data)
    app.register_blueprint(billing_data)
    return app
