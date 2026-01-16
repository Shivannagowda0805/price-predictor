from flask import Flask, render_template, request
import pandas as pd
import pickle
import json
import os

# Get the directory where this script is located
base_dir = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__, template_folder=os.path.join(base_dir, 'templates'))

# Check if data files exist and load them
try:
    cars = pd.read_csv('cleaned_cars.csv')
    print("Cars data loaded successfully")
    print(f"Cars shape: {cars.shape}")
    print(f"Cars columns: {cars.columns.tolist()}")
except Exception as e:
    print(f"Error loading cars data: {e}")
    cars = None

try:
    model = pickle.load(open('car_predictMode.pkl', 'rb'))
    print("Model loaded successfully")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

@app.route('/', methods=['GET', 'POST'])
def index():
    if cars is None or cars.empty:
        return "Error: Cars data not loaded", 500
    
    companies = sorted(cars['company'].unique().tolist()) if 'company' in cars.columns else []
    car_models = sorted(cars['name'].unique().tolist()) if 'name' in cars.columns else []
    years = sorted(cars['year'].unique().tolist(), reverse=True) if 'year' in cars.columns else []
    fuel_types = sorted(cars['fuel_type'].unique().tolist()) if 'fuel_type' in cars.columns else []
    
    print(f"Companies: {len(companies)} - {companies[:3] if companies else 'EMPTY'}")
    print(f"Models: {len(car_models)} - {car_models[:3] if car_models else 'EMPTY'}")
    
    # Create dict of models per company
    company_models = {}
    for company in companies:
        company_models[company] = sorted(cars[cars['company'] == company]['name'].unique().tolist())
    
    prediction = None
    if request.method == 'POST':
        company = request.form.get('company')
        model_name = request.form.get('model')
        year = int(request.form.get('year'))
        fuel_type = request.form.get('fuel_type')
        kms_driven = int(request.form.get('kilo_driven'))
        
        # Predict
        input_data = pd.DataFrame([[model_name, company, year, kms_driven, fuel_type]], 
                                  columns=['name', 'company', 'year', 'kms_driven', 'fuel_type'])
        prediction = model.predict(input_data)[0]
        prediction = round(prediction, 2)
    
    return render_template('index.html', companies=companies, car_models=car_models, years=years, fuel_types=fuel_types, company_models=company_models, prediction=prediction)

if __name__ == '__main__':
    app.run(debug=True)
