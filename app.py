from flask import Flask, jsonify, request, render_template, redirect
import sklearn
import pickle

app = Flask(__name__)

# Loading models
model = pickle.load(open('pkl/fertilizer_model.pkl', 'rb'))
crop_encoder = pickle.load(open('pkl/crop_encoder.pkl', 'rb'))
fert_encoder = pickle.load(open('pkl/fert_encoder.pkl', 'rb'))
soil_encoder = pickle.load(open('pkl/soil_encoder.pkl', 'rb'))
crop_pred = pickle.load(open('pkl/crop_pred.pkl', 'rb'))

# Home route
@app.route('/')
def home():
    return render_template('krishimitra.html')

@app.route('/fertilizer')
def fertilizer():
    return render_template('fertilizer_frontend.html')

# Fertilizer Prediction route
@app.route('/predict-fertilizer', methods=['POST'])
def predict_fertilizer():
    data = request.form

    features = [
        int(data['Temperature']),
        int(data['Humidity']),
        int(data['Moisture']),
        soil_encoder.transform([data['Soil']])[0],
        crop_encoder.transform([data['Crop']])[0],
        int(data['Nitrogen']),
        int(data['Potassium']),
        int(data['Phosphorous']),
    ]

    prediction = model.predict([features])[0]
    fertilizer = fert_encoder.inverse_transform([prediction])[0]

    return render_template('fertilizer_frontend.html', prediction_text=f"Recommended Fertilizer: {fertilizer}") 

@app.route('/crop')
def crop():
    return render_template('crop_prediction.html')

# Crop Prediction route
@app.route('/predict-crop', methods=['POST'])
def predict_crop():
    Nitrogen = float(request.form['nitrogen'])
    Phosphorus = float(request.form['phosphorus'])
    Potassium = float(request.form['potassium'])
    Temperature = float(request.form['temperature'])
    Humidity = float(request.form['humidity'])
    pH = float(request.form['ph'])
    Rainfall = float(request.form['rainfall'])

    values = [Nitrogen, Phosphorus, Potassium, Temperature, Humidity, pH, Rainfall]

    if pH > 0 and pH <= 14 and Temperature < 100 and Humidity > 0:
        arr = [values]
        acc = crop_pred.predict(arr)
        return render_template('crop_prediction.html', predictedCrop=acc[0]) 
    else:
        return "Sorry, please check the values and try again."

@app.route('/crop-disease-prediction')
def predict_disease():
    return redirect("https://appapppy-qozfumcmiwrph76libcuqw.streamlit.app/")


@app.route('/fertilizer_feature')
def fert_feature():
    return render_template("fertilizer.html")

@app.route('/crop_recommend_feature')
def crop_feature():
    return render_template('croprecommendation.html')

@app.route('/govt_schemes_feature')
def govt():
    return render_template("govtschemes.html")

@app.route('/disease_pred_feature')
def disease():
    return render_template("diseaseprediction.html")

if __name__ == '__main__':
    app.run(debug=True)
