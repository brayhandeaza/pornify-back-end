from flask import Flask
from flask_cors import CORS
from blueprints.videos import register_blueprints
from flask_caching import Cache

app = Flask(__name__)
app.config["CACHE_TYPE"] = "simple"

cache = Cache()
cache.init_app(app)
CORS(app, origins="http://localhost:3000")
register_blueprints(app)

if __name__ == '__main__':
    app.run(debug=True)