import os
from dotenv import load_dotenv
from app import create_app

load_dotenv()

app = create_app()

# Access environment variables
env = os.getenv('FLASK_ENV', 'development')
port = int(os.getenv('PORT', 5000))

# Set DEBUG mode based on the FLASK_ENV environment variable
app.debug = (env != 'production')

print(env, port)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=port)
