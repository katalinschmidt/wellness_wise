from flask import Flask
from app.routes import main_bp

# Instantiate Flask app
app = Flask(__name__)

# Register Blueprints with a URL prefix
app.register_blueprint(main_bp, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
