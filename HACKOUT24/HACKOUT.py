from flask import Flask, request, jsonify, render_template
import pandas as pd

app = Flask(__name__)

# Load crop data
crop_data = pd.read_csv('D:/TAHIR CODE/HACKOUT24/crop_data.csv')

def analyze_soil_conditions(pH, nitrogen, phosphorus, potassium, soil_type, threshold=5.0):
    suitable_crops = crop_data[
        (crop_data['pH_min'] <= pH) & (crop_data['pH_max'] >= pH) &
        (crop_data['N_min'] <= nitrogen) & (crop_data['N_max'] >= nitrogen) &
        (crop_data['P_min'] <= phosphorus) & (crop_data['P_max'] >= phosphorus) &
        (crop_data['K_min'] <= potassium) & (crop_data['K_max'] >= potassium) &
        (crop_data['Soil_Type'].str.lower() == soil_type.lower())
    ]

    if not suitable_crops.empty:
        return suitable_crops.head(3)  # Return the top 3 matching crops

    # If no exact matches found, calculate the best fits
    nearest_crops = []

    for _, crop in crop_data.iterrows():
        nitrogen_distance = max(0, crop['N_min'] - nitrogen, nitrogen - crop['N_max']) * 2
        phosphorus_distance = max(0, crop['P_min'] - phosphorus, phosphorus - crop['P_max']) * 1.5
        potassium_distance = max(0, crop['K_min'] - potassium, potassium - crop['K_max']) * 1
        pH_distance = max(0, crop['pH_min'] - pH, pH - crop['pH_max']) * 0.5

        total_distance = nitrogen_distance + phosphorus_distance + potassium_distance + pH_distance

        if total_distance <= threshold:
            nearest_crops.append((crop, total_distance))

    nearest_crops.sort(key=lambda x: x[1])
    return pd.DataFrame([crop[0] for crop in nearest_crops[:3]])

def crop_improvement_suggestions(suitable_crops):
    crop_suggestions = {
    'Corn': "\n- Ensure consistent moisture\n- Use nitrogen-rich fertilizers\n- Use practice crop rotation.",
    'Soybeans': "\n- Inoculate with rhizobium bacteria for better nitrogen fixation\n- Manage weeds effectively.",
    'Wheat': "\n- Apply phosphorus and potassium fertilizers\n- Consider disease-resistant varieties.",
    'Rice': "\n- Maintain water levels\n- Use nitrogen fertilizers\n- Ensure proper pest management.",
    'Potatoes': "\n- Ensure adequate drainage\n- Apply balanced fertilizers\n- Manage pests effectively.",
    'Carrots': "\n- Use sandy loam for best results\n- Thin seedlings\n- Keep soil consistently moist.",
    'Tomatoes': "\n- Provide support for plants\n- Use organic matter\n- Ensure consistent watering.",
    'Lettuce': "\n- Keep soil moist and shaded during hot weather\n- Consider planting in succession.",
    'Cabbage': "\n- Ensure adequate spacing\n- Monitor for pests\n- Apply nitrogen-rich fertilizers.",
    'Peppers': "\n- Provide consistent moisture\n- Apply mulch to retain soil temperature\n- Fertilize during the growing season.",
    'Strawberries': "\n- Ensure good drainage\n- Mulch to retain moisture\n- Fertilize during flowering.",
    'Barley': "\n- Incorporate good drainage\n- Use nitrogen and phosphorus fertilizers\n- Monitor for pests.",
    'Oats': "\n- Plant early in the season\n- Use nitrogen fertilizers\n- Ensure good drainage.",
    'Rye': "\n- Incorporate as a cover crop\n- Manage moisture levels\n- Practice crop rotation.",
    'Millet': "\n- Ensure good drainage\n- Use minimal fertilizers\n- Manage weeds effectively.",
    'Sorghum': "\n- Plant in warm soil\n- Provide sufficient water\n- Manage pests effectively.",
    'Cucumbers': "\n- Provide trellises for support\n- Keep soil consistently moist\n- Monitor for pests.",
    'Pumpkins': "\n- Provide plenty of space for growth\n- Maintain consistent moisture\n- Control pests.",
    'Peas': "\n- Inoculate with rhizobia\n- Provide support for climbing varieties\n- Keep soil cool and moist.",
    'Melons': "\n- Provide plenty of space for growth\n- Keep soil moist\n- Use mulch to retain moisture.",
    'Sugar Beets': "\n- Use well-drained soil\n- Apply nitrogen fertilizers\n- Monitor for pests.",
    'Tobacco': "\n- Use well-drained, fertile soil\n- Consider crop rotation to manage soil health.",
    'Cassava': "\n- Ensure adequate space for growth\n- Manage moisture levels\n- Control pests.",
    'Sweet Potatoes': "\n- Plant in well-drained, sandy loam\n- Monitor for pests and diseases.",
    'Chickpeas': "\n- Plant in well-drained soil\n- Manage weeds\n- Avoid overwatering."
    }

    improvements = []
    for _, crop in suitable_crops.iterrows():
        crop_name = crop['Crop']
        suggestion = crop_suggestions.get(crop_name, "No specific improvement suggestions available.")
        improvements.append(f"{crop_name}: {suggestion}")

    return improvements


@app.route('/')
def home():
    return render_template('home.html')



@app.route('/about3')
def about():
    return render_template('about3.html')

@app.route('/market')
def market():
    return render_template('market.html')


@app.route('/recommend3', methods=['GET','POST'])
def recommend():
    # Process the form submission
    if request.method == 'POST':
        soil_type = request.form['soil-type']
        pH = float(request.form['ph-level'])
        nitrogen = float(request.form['nitrogen'])
        phosphorus = float(request.form['phosphorus'])
        potassium = float(request.form['potassium'])

        suitable_crops = analyze_soil_conditions(pH, nitrogen, phosphorus, potassium, soil_type)
        
        if not suitable_crops.empty:
            crops_list = suitable_crops['Crop'].tolist()
            suggestions = crop_improvement_suggestions(suitable_crops)
            return jsonify({
                'suitable_crops': [{'Crop': crop} for crop in crops_list],
                'improvements': suggestions
            })
            
        else:
            return jsonify({'error': 'No suitable crops found for the given soil conditions.'})
    return render_template('recommend3.html')
    

if __name__ == '__main__':
    app.run(debug=True)
