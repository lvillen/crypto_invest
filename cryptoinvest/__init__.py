from flask import Flask

application = app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

from cryptoinvest import views