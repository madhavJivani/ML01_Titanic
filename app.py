import pickle
from flask import Flask,render_template,request
# Pclass	Sex	Age	Fare
app = Flask(__name__)
model = pickle.load(open("train_model.pkl",'rb'))

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/predict", methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Retrieve form data
        pclass = request.form.get('Pclass')
        sex = request.form.get('Sex')
        age = request.form.get('Age')
        fare = request.form.get('Fare')
        try:
            pclass = int(pclass) if pclass else None
            sex = int(sex) if sex else None
            age = float(age) if age else None
            fare = float(fare) if fare else None
        except ValueError:
            return "Invalid input data. Please enter valid numbers.", 400
        
        # Check if any value is None
        if None in (pclass, sex, age, fare):
            return "Please fill in all fields with valid data.", 400
        
        # Predict
        prediction = model.predict([[pclass, sex, age, fare]])
        if prediction[0] == 1:
            return render_template("index.html",prediction_txt = "Voyage returned Alive")
        else:
            return render_template("index.html",prediction_txt = "Voyage didn't return")


if __name__ == "__main__":
    app.run(debug=True)