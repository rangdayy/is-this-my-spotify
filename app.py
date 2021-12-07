from flask import Flask

def create_app():
    app = Flask(__name__)
    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')
    with app.app_context():
        import routes
    
        return app

if __name__ == "__main__":
    create_app().run()