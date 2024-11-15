from flask import Flask, render_template, request, jsonify 
import numpy as np 
import pickle

app = Flask(__name__)

model= pickle.load(open("model.pkl","rb"))

@app.route('/')
def home():
    return render_template('index.html')


    

@app.route("/predict",methods = ["POST"])
def predict():
    try:
        # Collect form data
        age = int(request.form.get("age"))
        sex = request.form.get("sex").strip().lower()
        sex = 0 if sex == "male" else 1
        
        bmi = float(request.form.get("bmi"))
        
        children = request.form.get("children").strip().lower()
        children = 1 if children == "yes" else 0
        
        smoker = request.form.get("smoker").strip().lower()
        smoker = 0 if smoker == "yes" else 1
        
        region = request.form.get("region").strip().lower()
        if region == "southeast":
            region = 0
        elif region == "southwest":
            region = 1
        elif region == "northeast":
            region = 2
        elif region == "northwest":
            region = 3
        else:
            return render_template("index.html", prediction_text="Invalid region input!")
        
        # Prepare input features
        features = np.array([[age, sex, bmi, children, smoker, region]])
        
        # Make prediction
        prediction = model.predict(features)
        insurance_value = round(prediction[0] * 84, 2)
        
        return render_template(
            "index.html", 
            prediction_text=f"Your estimated health insurance value is Rs. {insurance_value}"
        )
    except Exception as e:
        return render_template("index.html", prediction_text=f"Error occurred: {e}")

if __name__ == "__main__":
    app.run(debug=True)