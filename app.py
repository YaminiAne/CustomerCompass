from flask import Flask, render_template, request
import pickle
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)

with open('xgboost_model.pkl', 'rb') as file:
    model = pickle.load(file)

with open('scaler_age.pkl', 'rb') as file:
    scaler_age = pickle.load(file)

with open('scaler_balance.pkl', 'rb') as file:
    scaler_balance = pickle.load(file)

with open('scaler_salary.pkl', 'rb') as file:
    scaler_salary = pickle.load(file)

@app.route('/index.html')
def home():
    return render_template('index.html')

@app.route('/project.html')
def project():
    return render_template('project.html')

@app.route('/churn.html', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        try:
            CreditScore = float(request.form['CreditScore'])
            Geography = request.form['Geography']
            Gender = request.form['Gender']
            Age = float(request.form['Age'])
            Tenure = float(request.form['Tenure'])
            Balance = float(request.form['Balance'])
            NumOfProducts = float(request.form['NumOfProducts'])
            HasCrCard = request.form['HasCrCard']
            IsActiveMember = request.form['IsActiveMember']
            EstimatedSalary = float(request.form['EstimatedSalary'])

            if Geography == 'France':
                Geography = 1
            elif Geography == 'Germany':
                Geography = 2
            else:
                Geography = 3

            if Gender == 'Male':
                Gender = 1
            else: 
                Gender = 0

            HasCrCard = 1 if HasCrCard == 'Yes' else 0
            IsActiveMember = 1 if IsActiveMember == 'Yes' else 0

            data = pd.DataFrame({
                'CreditScore': [CreditScore],
                'Geography': [Geography],
                'Gender': [Gender],
                'Age': [Age],
                'Tenure': [Tenure],
                'Balance': [Balance],
                'NumOfProducts': [NumOfProducts],
                'HasCrCard': [HasCrCard],
                'IsActiveMember': [IsActiveMember],
                'EstimatedSalary': [EstimatedSalary]
            })

        
            data['Age'] = scaler_age.transform(data[['Age']])
            data['Balance'] = scaler_balance.transform(data[['Balance']])
            data['EstimatedSalary'] = scaler_salary.transform(data[['EstimatedSalary']])

           
            prediction = model.predict(data)
            print(prediction)
            if prediction == [1]:
                prediction_text = 'There is HIGH chance that this customer will churn.'
            else:
                prediction_text = 'Yay! This customer does not seem to churn.'

            
            return render_template('churn.html', prediction_text=prediction_text)

        except Exception as e:
            print(f"Error: {e}")
            return render_template('churn.html', prediction_text='An error occurred during prediction. Please try again.')

    return render_template('churn.html', prediction_text='')


if __name__ == '__main__':
    app.run(debug=True)


