from flask import Flask
from backend.models.basics_models import *

app = Flask(__name__)

app.config.from_object('backend.models.config')
db = db_setup(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
