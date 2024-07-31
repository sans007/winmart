from app import create_app
from config import Config

app = create_app()
env = Config()
evn_debug = env.FLASK_ENV == 'development'

if __name__ == "__main__":
    app.run(debug=evn_debug)
