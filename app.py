import json
import sys

# Load knowledge base
def load_knowledge_base(file_path='crop_knowledge.json'):
    with open(file_path, 'r') as f:
        return json.load(f)

# Recommendation engine
def generate_recommendations(inputs, knowledge):
    crop = inputs['crop'].title()
    if crop not in knowledge['crops']:
        return "Unsupported crop. Supported: Rice, Coconut, Pepper, Banana, Rubber."
    
    crop_data = knowledge['crops'][crop]
    location_zone = get_location_zone(inputs['location'])
    farm_size_cat = get_farm_size_category(inputs['farm_size'])
    
    # What to Do (step-by-step)
    steps = f"""
    *What to Do for {crop} in {inputs['location']} ({location_zone}):*
    1. *Soil Preparation*: Test soil (pH {crop_data['soil_type']}). Amend with lime if acidic.
    2. *Planting*: Time: {crop_data['planting_season']}. Use {crop_data['location_specific'].get(location_zone, 'local variety')}.
    3. *Care*: Water: {crop_data['water_needs']}. Fertilize: {crop_data['fertilizer']}. Monitor for {crop_data['pests_diseases']}.
    4. *Harvest*: Expect {crop_data['yield_estimate']} yield. Harvest when mature.
    """
    
    # Resource Optimization
    opt = f"""
    *Resource Optimization ({farm_size_cat} farm, {inputs['soil_type']} soil, {inputs['water_availability']} water):*
    - Water: Use drip if {inputs['water_availability']} is limited—saves 20-30%. Mulch with crop residue.
    - Fertilizers: Apply {crop_data['fertilizer']}; integrate organics to reduce costs by 40%. For {inputs['budget']}, seek subsidies.
    - Pests: IPM—biological controls over chemicals. Rotate crops to prevent soil depletion.
    - General ({farm_size_cat}): {knowledge['general_tips'][farm_size_cat.lower().replace(' ', '_')]}. For {inputs['experience']}, {knowledge['general_tips']['beginner'] if inputs['experience'] == 'beginner' else 'Consult experts.'}
    {crop_data['optimization']}
    """
    
    # Crop Knowledge
    knowledge_section = f"""
    *Detailed Knowledge on {crop}:*
    {crop_data['description']}
    - Soil: {crop_data['soil_type']}
    - Nutrition: Balanced NPK; add micronutrients if {inputs['soil_type']} is deficient.
    - Challenges: In Kerala monsoons, ensure drainage. Market price: ~₹20-50/kg (check e-NAM).
    - Sustainability: Use eco-friendly practices for GI tags (e.g., Wayanad spices).
    """
    
    return steps + opt + knowledge_section

# Helper functions
def get_location_zone(location):
    coastal = ['Thiruvananthapuram', 'Kollam', 'Alappuzha', 'Ernakulam', 'Thrissur', 'Kasaragod']
    highland = ['Wayanad', 'Palakkad', 'Idukki', 'Pathanamthitta', 'Kottayam']
    if any(d in location for d in coastal):
        return 'Coastal'
    elif any(d in location for d in highland):
        return 'Highland'
    return 'Inland'

def get_farm_size_category(size):
    if size < 2:
        return 'Small'
    elif size < 20:
        return 'Medium'
    else:
        return 'Large'

# Main function (CLI interface)
def main():
    knowledge = load_knowledge_base()
    
    # Sample inputs (replace with user input in production, e.g., via input() or web form)
    inputs = {
        'location': input("Enter district (e.g., Wayanad): ") or 'Wayanad',
        'farm_size': float(input("Enter farm size in acres: ") or 1.5),
        'crop': input("Enter crop name: ") or 'Pepper',
        'soil_type': input("Enter soil type (e.g., laterite): ") or 'laterite',
        'water_availability': input("Water (irrigated/rain-fed): ") or 'rain-fed',
        'experience': input("Experience (beginner/expert): ") or 'beginner',
        'budget': input("Budget (low/medium/high): ") or 'low'
    }
    
    recommendations = generate_recommendations(inputs, knowledge)
    print(recommendations)

if __name__ == "_main_":
    main()