import os

from flask import Flask
from flask import render_template
from flask import request
import datetime


from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "infodatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)


#class FoodEntry(db.Model):
    # id, date, foodItem, calories




if __name__ == "__main__":
    app.run(debug=True)
