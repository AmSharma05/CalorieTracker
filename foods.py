import os

from flask import Flask
from flask import render_template
from flask import request
import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from sqlalchemy.sql import label
from sqlalchemy import text

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "infodatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

####################### CLASSES that map to MODELS in database ############################
# This defines the structure of the database table for Personal Info
class PersonalInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(80), unique=True, nullable=False)
    gender = db.Column(db.String(60), unique=False, nullable=False)
    age = db.Column(db.Integer, unique=False, nullable=True, primary_key=False)
    def __repr__(self):
        return '<Person %r>' % self.fname


# This defines the structure of the database table for Food Intake
class FoodIntake(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    itemName = db.Column(db.String(80), unique=False, nullable=False)
    consumptionDate = db.Column(db.DateTime(), unique=False, nullable=False)
    caloricAmount = db.Column(db.Integer, unique=False, nullable=False)
      
    def __repr__(self):
        return 'Food Name: %r' % self.itemName

####################### ROUTES for different HTML Pagees ############################

@app.route("/profile", methods=["GET", "POST"])
def personalInfo():
    fname = ""
    gender = ""
    age = 0
    
    # this is to get all values submitted from the HTML form (info.html)
    if request.form:
        
        fname = request.form.get("fname")
        gender = request.form.get("gender")
        age = request.form.get("age")
        
        exists = False
        
        try:
          exists = PersonalInfo.query.filter_by(fname=fname).one()
        except:
          exists = False
          
        if exists:

            return render_template("info.html",ReturnMessage="Name already in the database")

        else:

            objPersonalInfo = PersonalInfo(fname=fname,gender=gender,age=age)

            # This is to save that information to my database table called personal_info
            try:
              db.session.add(objPersonalInfo)
              db.session.commit()
            except:
              return render_template("info.html",ReturnMessage="Some error occurred")
    
            # This is to confirm that the values were saved successfully
            pInfo = PersonalInfo.query.filter_by(fname=fname).one()
    
            return render_template("info.html",ReturnMessage = "Record created: " + pInfo.fname + ", " + pInfo.gender + ", " + str(pInfo.age))
            
    
            # This is to return the results of the query back to HTML
        
        
    return render_template("info.html",ReturnMessage="")


@app.route("/chart", methods=["GET", "POST"])
def renderChart():
    sql = text('select consumptionDate, sum(caloricAmount) from food_intake group by consumptionDate')
    chartData = db.engine.execute(sql)
    return render_template("chart.html",ChartData= chartData)

    
@app.route("/", methods=["GET", "POST"])
def foodIntake():
    itemName = ""
    consumptionDate = ""
    caloricAmount = 0
    
    # this is to get all values submitted from the HTML form (info.html)
    if request.form:

        # This is to save that information to my database table called personal_info
        try:
            # itemName = request.form.get("foods")
            itemName = request.form.get("foodItemName")
            consumptionDate =  datetime.datetime.strptime(request.form.get("datepicker"), '%m/%d/%Y')
            caloricAmount = request.form.get("foods")

            objFoodIntake = FoodIntake(itemName=itemName, consumptionDate=consumptionDate, caloricAmount=caloricAmount)

            db.session.add(objFoodIntake)
            db.session.commit()
        except:
            return render_template("food.html",ErrorMessage="Something went wrong")

        # This is to confirm that the values were saved successfully
        allFoodItems = FoodIntake.query.filter_by(consumptionDate=consumptionDate).all()
        
        #calculate total calories consumed for the day
        totalCalories = 0
        for X in allFoodItems:
            totalCalories = totalCalories + X.caloricAmount

        return render_template("food.html",SuccessObject = allFoodItems, TotalCalories = str(totalCalories))
        
        
    return render_template("food.html",ErrorMessage="")


if __name__ == "__main__":
    app.run(debug=True)
    
    
