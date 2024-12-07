from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)

# Load datasets (make sure the path is correct on PythonAnywhere)
hardware_inventory_data = pd.read_csv('hardware_inventory_realistic_prices.csv')
budget_data = pd.read_csv('budgetval.csv')

# Route to check if the Flask app is working
@app.route('/')
def index():
    return "Hello, Flask API is working!"

# Route for category maintenance cost
@app.route('/api/category_maintenance_cost', methods=['GET'])
def category_maintenance_cost():
    category_cost = hardware_inventory_data.groupby('Category')['Maintenance_Charge'].sum().reset_index()
    return jsonify(category_cost.to_dict(orient='records'))

# Route for condition maintenance cost
@app.route('/api/condition_maintenance_cost', methods=['GET'])
def condition_maintenance_cost():
    condition_cost = hardware_inventory_data.groupby('Condition')['Maintenance_Charge'].sum().reset_index()
    return jsonify(condition_cost.to_dict(orient='records'))

# Route for age group maintenance cost
@app.route('/api/age_group_maintenance_cost', methods=['GET'])
def age_group_maintenance_cost():
    bins = range(0, int(hardware_inventory_data['Item_Age'].max()) + 100, 100)
    hardware_inventory_data['Age_Group'] = pd.cut(hardware_inventory_data['Item_Age'], bins)
    grouped_data = hardware_inventory_data.groupby('Age_Group')['Average_Maintenance_Cost'].mean().reset_index()
    grouped_data['Age_Group'] = grouped_data['Age_Group'].astype(str)
    return jsonify(grouped_data.to_dict(orient='records'))

# Route for budget category spending
@app.route('/api/budget_category_spending', methods=['GET'])
def budget_category_spending():
    budget_data['Total Cost'] = budget_data['Price'] + budget_data['Maintenance_Charge']
    category_summary = budget_data.groupby('Category')[['Price', 'Maintenance_Charge', 'Total Cost']].sum().reset_index()
    return jsonify(category_summary.to_dict(orient='records'))

# Route for yearly spending trends
@app.route('/api/yearly_spending_trends', methods=['GET'])
def yearly_spending_trends():
    if 'Year' in budget_data.columns:
        yearly_summary = budget_data.groupby('Year')[['Price', 'Maintenance_Charge', 'Total Cost']].sum().reset_index()
        return jsonify(yearly_summary.to_dict(orient='records'))
    return jsonify([])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
