import pandas as pd

# Load crop data
crop_data = pd.read_csv('crop_data.csv')

def analyze_soil_conditions(pH, nitrogen, phosphorus, potassium, soil_type, threshold=5.0):
    """Analyze the soil conditions to find the best crops and improvements."""
    # Check for suitable crops based on the provided soil parameters
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
        # Calculate distance to crop requirements
        nitrogen_distance = max(0, crop['N_min'] - nitrogen, nitrogen - crop['N_max']) * 2  # Higher weight for N
        phosphorus_distance = max(0, crop['P_min'] - phosphorus, phosphorus - crop['P_max']) * 1.5  # Moderate weight for P
        potassium_distance = max(0, crop['K_min'] - potassium, potassium - crop['K_max']) * 1  # Normal weight for K
        pH_distance = max(0, crop['pH_min'] - pH, pH - crop['pH_max']) * 0.5  # Lower weight for pH

        # Total distance
        total_distance = nitrogen_distance + phosphorus_distance + potassium_distance + pH_distance

        # Only consider crops that are within the threshold
        if total_distance <= threshold:
            nearest_crops.append((crop, total_distance))  # Store the crop and its distance

    # Sort crops by distance and return the closest ones within the threshold
    nearest_crops.sort(key=lambda x: x[1])  # Sort by total distance
    return pd.DataFrame([crop[0] for crop in nearest_crops[:3]])  # Return top 3 closest crops

def soil_improvement_suggestions(soil_type):
    """Provide soil improvement suggestions based on the soil type."""
    suggestions = {
        'loamy': "Maintain good organic matter levels.\nConsider adding compost or aged manure.",
        'clay': "Improve drainage by adding sand and organic matter.\nConsider using raised beds.",
        'sandy': "Enhance nutrient retention by adding organic matter.\nUse mulch to retain moisture.",
        'acidic': "Add lime to increase pH.\nUse organic matter to improve nutrient retention.",
        'alkaline': "Consider adding sulfur to lower pH.\nEnsure good drainage to prevent salt accumulation."
    }
    
    return suggestions.get(soil_type.lower(), "No specific suggestions available for this soil type.")

def crop_improvement_suggestions(suitable_crops):
    """Provide improvement suggestions for crops."""
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

def display_suitable_crops(suitable_crops):
    """Display the suitable crops and their specific suggestions."""
    print("\nBest crops for the given soil conditions:")
    for _, crop in suitable_crops.iterrows():
        print(f"- {crop['Crop']}")

def main():
    print("Crop Selection Based on Soil Conditions")

    # Get soil parameters from the user
    try:
        pH = float(input("Enter soil pH: "))
        nitrogen = float(input("Enter nitrogen (N) level (mg/kg): "))
        phosphorus = float(input("Enter phosphorus (P) level (mg/kg): "))
        potassium = float(input("Enter potassium (K) level (mg/kg): "))
        soil_type = input("Enter your soil type (Loamy, Clay, Sandy, Acidic, Alkaline, etc.): ").strip()

        suitable_crops = analyze_soil_conditions(pH, nitrogen, phosphorus, potassium, soil_type)

        if not suitable_crops.empty:
            display_suitable_crops(suitable_crops)
            crop_improvements = crop_improvement_suggestions(suitable_crops)
            print("\nImprovement Suggestions for Selected Crops:")
            for improvement in crop_improvements:
                print(f"\n* {improvement}")
        else:
            print("No suitable crops found for the given soil conditions.")
            # Suggest the nearest crops if no exact match found
            nearest_crops = analyze_soil_conditions(pH, nitrogen, phosphorus, potassium, soil_type)
            if not nearest_crops.empty:
                print("\nThe closest matches based on your input are:")
                display_suitable_crops(nearest_crops)
                crop_improvements = crop_improvement_suggestions(nearest_crops)
                print("\nImprovement Suggestions for Closest Crops:")
                for improvement in crop_improvements:
                    print(f"- {improvement}\n")
                improvement_suggestions = soil_improvement_suggestions(soil_type)
                print(f"\nSoil Improvement Suggestions: {improvement_suggestions}")
            else:
                print("\nNo crops found for the given data.")
        

    except ValueError:
        print("Invalid input. Please enter numeric values for pH, nitrogen, phosphorus, and potassium.")

if __name__ == "__main__":
    main()
