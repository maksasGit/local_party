# app.py

from flask import Flask
from routes.bestiary import bestiary_bp
from routes.admin import admin_bp
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.register_blueprint(bestiary_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run()
