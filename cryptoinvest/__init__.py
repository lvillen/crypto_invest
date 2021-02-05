from flask import Flask

application = Flask(__name__, instance_relative_config=True)
application.config.from_object('config')

from cryptoinvest import views