import streamlit as st
import pandas as pd

# Set page config
st.set_page_config(page_title="Calorie & Macro Tracker", page_icon="🍎")

# Initialize session state for daily totals
if 'daily_calories' not in st.session_state:
    st.session_state.daily_calories = 0
if 'daily_protein' not in st.session_state:
    st.session_state.daily_protein = 0
if 'daily_carbs' not in st.session_state:
    st.session_state.daily_carbs = 0
if 'daily_fat' not in st.session_state:
    st.session_state.daily_fat = 0
if 'daily_sugar' not in st.session_state:
    st.session_state.daily_sugar = 0

# Initialize session state for user info
if 'calorie_goal' not in st.session_state:
    st.session_state.calorie_goal = 2000
if 'protein_goal' not in st.session_state:
    st.session_state.protein_goal = 150
if 'carb_goal' not in st.session_state:
    st.session_state.carb_goal = 250
if 'fat_goal' not in st.session_state:
    st.session_state.fat_goal = 65
if 'sugar_goal' not in st.session_state:
    st.session_state.sugar_goal = 50  # WHO recommends max 50g per day

def calculate_bmr_and_goals(weight, height, age, gender, activity_level):
    """Calculate BMR using Mifflin-St Jeor equation and set macro goals"""
    
    # Calculate BMR
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:  # Female
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # Activity multipliers
    activity_multipliers = {
        "Sedentary (little/no exercise)": 1.2,
        "Lightly active (light exercise 1-3 days/week)": 1.375,
        "Moderately active (moderate exercise 3-5 days/week)": 1.55,
        "Very active (hard exercise 6-7 days/week)": 1.725,
        "Super active (very hard exercise, physical job)": 1.9
    }
    
    # Calculate total daily calories
    daily_calories = bmr * activity_multipliers[activity_level]
    
    # Calculate macro goals (typical recommendations)
    protein_grams = weight * 1.6  # 1.6g per kg body weight
    fat_grams = daily_calories * 0.25 / 9  # 25% of calories from fat
    carb_grams = (daily_calories - (protein_grams * 4) - (fat_grams * 9)) / 4  # Rest from carbs
    sugar_grams = min(50, daily_calories * 0.10 / 4)  # Max 10% of calories or 50g, whichever is lower
    
    return int(daily_calories), int(protein_grams), int(carb_grams), int(fat_grams), int(sugar_grams)

def get_daily_advice():
    """Generate personalized advice based on daily intake"""
    advice = []
    
    # Calculate percentages of goals
    cal_percent = (st.session_state.daily_calories / st.session_state.calorie_goal) * 100
    protein_percent = (st.session_state.daily_protein / st.session_state.protein_goal) * 100
    carb_percent = (st.session_state.daily_carbs / st.session_state.carb_goal) * 100
    fat_percent = (st.session_state.daily_fat / st.session_state.fat_goal) * 100
    sugar_percent = (st.session_state.daily_sugar / st.session_state.sugar_goal) * 100
    
    # Calorie advice
    if cal_percent < 80:
        advice.append("🍽️ **Too few calories!** You might not be eating enough to fuel your body properly. Try adding healthy snacks like nuts or fruits.")
    elif cal_percent > 120:
        advice.append("⚠️ **High calorie intake!** Consider smaller portions or choosing lower-calorie options like more vegetables and lean proteins.")
    elif 90 <= cal_percent <= 110:
        advice.append("✅ **Perfect calorie balance!** You're right on track with your daily calorie goals.")
    
    # Protein advice
    if protein_percent < 70:
        advice.append("💪 **Need more protein!** Add eggs, chicken, fish, or tofu. Try some satay or grilled chicken breast!")
    elif protein_percent > 150:
        advice.append("🥩 **Lots of protein today!** That's okay occasionally, but balance with more carbs and vegetables tomorrow.")
    elif protein_percent >= 90:
        advice.append("💪 **Great protein intake!** Perfect for muscle maintenance and feeling full.")
    
    # Fat advice
    if fat_percent > 140:
        advice.append("🧈 **High fat intake today!** Try grilling instead of frying, and choose lean meats. Avoid too much coconut milk and fried foods.")
    elif fat_percent < 50:
        advice.append("🥑 **Too little healthy fat!** Add some nuts, avocado, or olive oil for better nutrient absorption.")
    elif 80 <= fat_percent <= 120:
        advice.append("✅ **Good fat balance!** You're getting healthy fats without overdoing it.")
    
    # Sugar advice (this is the big one!)
    if sugar_percent > 150:
        advice.append("🍭 **Sugar overload!** You've had way too much sugar today. Cut back on sweet drinks, desserts, and processed foods tomorrow.")
    elif sugar_percent > 100:
        advice.append("🍰 **High sugar intake!** Watch out for hidden sugars in drinks and snacks. Try water instead of sweet beverages.")
    elif sugar_percent < 50:
        advice.append("🌟 **Excellent sugar control!** You're keeping sugar low - great for your health!")
    
    # Carb advice
    if carb_percent > 130:
        advice.append("🍚 **Carb-heavy day!** Try adding more protein and vegetables. Maybe less rice/noodles and more ulam next time!")
    elif carb_percent < 60:
        advice.append("🍞 **Low carbs today!** Add some healthy carbs like brown rice or oats for sustained energy.")
    
    # Overall encouragement
    if len([a for a in advice if "✅" in a or "🌟" in a or "💪" in a and "Great" in a]) >= 2:
        advice.append("🎉 **You're doing awesome!** Keep up the great eating habits!")
    elif sugar_percent > 120 and fat_percent > 120:
        advice.append("🥗 **Tomorrow's tip:** Focus on fresh foods - more ulam, grilled fish, and plain water!")
    
    return advice

# Food database (calories, protein, carbs, fat, sugar per 100g)
food_database = {
    # Original foods
    "chicken breast": [165, 31, 0, 3.6, 0],
    "rice": [130, 2.7, 28, 0.3, 0.1],
    "banana": [89, 1.1, 23, 0.3, 12],
    "egg": [155, 13, 1.1, 11, 1.1],
    "oatmeal": [68, 2.4, 12, 1.4, 0.4],
    "salmon": [208, 25, 0, 12, 0],
    "broccoli": [34, 2.8, 7, 0.4, 1.5],
    "apple": [52, 0.3, 14, 0.2, 10],
    "bread": [265, 9, 49, 3.2, 5],
    "milk": [42, 3.4, 5, 1, 5],
    
    # Fried & Fast Foods
    "fried chicken": [320, 19, 8, 21, 0.5],
    "kfc fried chicken": [290, 22, 9, 18, 1],
    "french fries": [365, 4, 63, 17, 0.3],
    "fried rice": [163, 3, 20, 7, 1],
    "fish and chips": [232, 12, 18, 13, 2],
    
    # Malaysian Foods
    "nasi lemak": [186, 4, 28, 6, 2],
    "rendang": [468, 26, 8, 37, 4],
    "char kway teow": [200, 8, 25, 8, 3],
    "laksa": [173, 7, 22, 7, 5],
    "satay chicken": [200, 25, 3, 9, 2],
    "mee goreng": [158, 6, 20, 6, 4],
    "roti canai": [301, 7, 43, 11, 2],
    "teh tarik": [83, 2, 14, 2, 12],
    "cendol": [180, 2, 45, 1, 35],
    "curry chicken": [149, 25, 5, 3, 3],
    "sambal sotong": [89, 16, 4, 1, 2],
    "ayam penyet": [250, 22, 12, 13, 8],
    "tom yam": [37, 2, 8, 0.5, 4],
    "wonton mee": [284, 14, 40, 8, 6],
    "bak kut teh": [120, 15, 3, 5, 1],
    "pan mee": [155, 6, 23, 4, 2],
    "chilli pan mee": [180, 7, 24, 6, 3],
    "curry mee": [195, 8, 26, 7, 4],
    "assam laksa": [165, 6, 25, 5, 8],
    "hokkien mee": [210, 9, 28, 7, 3],
    "mee rebus": [170, 7, 28, 4, 6],
    "mee siam": [160, 5, 26, 4, 8],
    "maggi goreng": [320, 8, 45, 12, 12],
    "nasi goreng kampung": [175, 6, 28, 5, 3],
    "nasi kerabu": [165, 4, 30, 4, 2],
    "nasi dagang": [190, 5, 35, 4, 2],
    "lemang": [143, 3, 32, 1, 1],
    "ketupat": [78, 1.5, 18, 0.1, 0],
    "lontong": [85, 2, 19, 0.2, 0],
    "rojak": [95, 2, 20, 2, 15],
    "pasembur": [120, 4, 18, 4, 8],
    "cakoi": [400, 6, 45, 22, 5],
    "yong tau foo": [85, 8, 6, 3, 1],
    "economy rice": [150, 8, 20, 5, 2],
    "mixed rice": [160, 9, 22, 5, 2],
    "dim sum": [250, 12, 20, 14, 3],
    "har gow": [180, 8, 20, 8, 2],
    "siu mai": [220, 10, 15, 14, 3],
    "chee cheong fun": [110, 3, 22, 1, 4],
    "lor mai gai": [200, 8, 30, 6, 2],
    
    # Rice & Noodles
    "white rice": [130, 2.7, 28, 0.3, 0.1],
    "brown rice": [111, 2.6, 23, 0.9, 0.4],
    "fried noodles": [138, 4.5, 20, 4.3, 2],
    "instant noodles": [448, 9, 58, 19, 6],
    "bee hoon": [348, 7, 77, 0.6, 1],
    
    # Vegetables (Asian style)
    "kangkung belacan": [45, 3, 7, 1, 2],
    "sayur lodeh": [65, 2, 8, 3, 4],
    "gado gado": [180, 6, 15, 11, 8],
    "acar": [35, 1, 8, 0.2, 6],
    
    # Fruits (Tropical)
    "durian": [147, 1.5, 27, 5.3, 25],
    "rambutan": [82, 0.9, 21, 0.2, 16],
    "mangosteen": [73, 0.4, 18, 0.6, 16],
    "papaya": [43, 0.5, 11, 0.3, 8],
    "mango": [60, 0.8, 15, 0.4, 14],
    "pineapple": [50, 0.5, 13, 0.1, 10],
    
    # Drinks
    "teh o": [34, 0, 9, 0, 9],
    "kopi o": [7, 0.3, 0.7, 0, 0],
    "milo": [95, 1.8, 20, 1.5, 18],
    "coconut water": [19, 0.7, 3.7, 0.2, 2.6],
    
    # Unique Malaysian Foods
    "bubur lambuk": [85, 3, 15, 2, 3],
    "tepung pelita": [160, 2, 35, 3, 25],
    "kuih seri muka": [180, 3, 38, 4, 30],
    "ondeh ondeh": [120, 1.5, 25, 2, 20],
    "pulut panggang": [220, 4, 45, 4, 15],
    "otak otak": [95, 12, 8, 2, 1],
    "kerabu mangga": [45, 1, 11, 0.5, 8],
    "ulam raja": [25, 2, 4, 0.3, 1],
    "pucuk paku": [30, 3, 5, 0.2, 1],
    "petai": [142, 6, 25, 1, 5],
    "jering": [157, 7, 27, 1.2, 6],
    "tempoyak": [120, 8, 15, 4, 10],
    "cincalok": [80, 15, 2, 1, 0],
    "budu": [35, 6, 3, 0.2, 1],
    "keropok keping": [380, 8, 65, 8, 5],
    "rempeyek": [480, 12, 45, 28, 8],
    "serunding": [520, 25, 15, 42, 3],
    "dendeng": [410, 55, 8, 18, 5],
    "ikan masin": [290, 62, 0, 2, 0],
    "telur masin": [180, 14, 1, 13, 0],
    "acar rampai": [40, 1, 9, 0.5, 7],
    "jeruk mangga": [65, 0.5, 16, 0.2, 14],
    "asinan": [50, 1, 12, 0.3, 10],
    "ais kacang": [150, 3, 35, 1, 30],
    "tau fu fa": [60, 4, 7, 2, 6],
    "soy bean": [45, 4, 4, 2, 2],
    "bubur kacang hijau": [110, 4, 22, 1, 8],
    "bubur cha cha": [140, 2, 32, 2, 25],
    "pengat": [180, 3, 42, 2, 35],
    "kolak": [160, 2, 38, 3, 30],
    "kuih talam": [140, 2, 32, 2, 25],
    "kuih ketayap": [190, 3, 35, 5, 28],
    "kuih dadar": [170, 3, 32, 4, 25],
    "pulut inti": [200, 3, 42, 4, 35],
    "kuih kosui": [120, 1, 28, 1, 22],
    "ang ku kueh": [180, 4, 38, 3, 30],
    "soon kueh": [150, 3, 30, 3, 8],
    "chai tow kway": [180, 4, 35, 3, 12],
    "mee sua": [320, 11, 70, 1.5, 2],
    "lor mee": [195, 8, 32, 4, 6],
    "mee hoon kueh": [165, 5, 32, 2, 3],
    "ban mian": [170, 6, 30, 3, 2],
    "fish head curry": [180, 22, 8, 7, 4],
    "sup tulang": [95, 12, 5, 3, 2],
    "soto ayam": [120, 15, 8, 4, 3],
    "gulai lemak": [160, 8, 12, 10, 5],
    "masak lemak cili padi": [140, 6, 15, 8, 6],
    "ikan patin tempoyak": [190, 25, 8, 7, 12],
    "ayam masak merah": [220, 28, 12, 8, 8],
    "daging salai": [380, 45, 5, 18, 2],
    "ikan bakar": [150, 28, 2, 3, 1],
    "ayam golek": [280, 35, 8, 12, 6],
    
    # Traditional Malaysian snacks with sugar content
    "kuih lapis": [190, 2, 35, 5, 28],
    "onde onde": [120, 1.5, 25, 2, 20],
    "pisang goreng": [150, 2, 25, 5, 18],
    "keropok lekor": [300, 12, 35, 12, 8],
    "murukku": [520, 11, 52, 29, 15],
    "kuih kapit": [450, 6, 65, 18, 45],
    "kuih bahulu": [380, 8, 70, 8, 55],
    "dodol": [320, 2, 75, 3, 65],
    "wajik": [250, 3, 55, 4, 45],
    "tapai": [110, 1, 26, 0.2, 20],
    "apam balik": [280, 6, 40, 11, 32],
    "roti john": [290, 15, 25, 16, 8],
    "murtabak": [350, 18, 30, 20, 12],
    "curry puff": [280, 8, 25, 17, 5],
    "karipap": [280, 8, 25, 17, 5],
    "epok epok": [260, 6, 28, 14, 6],
    "popiah": [120, 4, 18, 4, 8],
    "spring roll": [140, 4, 15, 8, 3],
}

# Main title
st.title("🍎 Calorie & Macro Tracker")
st.markdown("Track your daily nutrition with personalized goals!")

# Personal Info Section (Expandable)
with st.expander("⚙️ Set Your Personal Goals", expanded=False):
    st.subheader("Calculate Your Daily Calorie Needs")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=30.0, max_value=200.0, value=70.0, step=0.5)
        height = st.number_input("Height (cm)", min_value=120.0, max_value=220.0, value=170.0, step=1.0)
        age = st.number_input("Age", min_value=15, max_value=100, value=25, step=1)
    
    with col2:
        gender = st.selectbox("Gender", ["Male", "Female"])
        activity_level = st.selectbox("Activity Level", [
            "Sedentary (little/no exercise)",
            "Lightly active (light exercise 1-3 days/week)", 
            "Moderately active (moderate exercise 3-5 days/week)",
            "Very active (hard exercise 6-7 days/week)",
            "Super active (very hard exercise, physical job)"
        ])
    
    if st.button("Calculate My Goals"):
        cal_goal, prot_goal, carb_goal, fat_goal, sugar_goal = calculate_bmr_and_goals(
            weight, height, age, gender, activity_level
        )
        
        # Update session state
        st.session_state.calorie_goal = cal_goal
        st.session_state.protein_goal = prot_goal
        st.session_state.carb_goal = carb_goal
        st.session_state.fat_goal = fat_goal
        st.session_state.sugar_goal = sugar_goal
        
        st.success(f"""
        ✅ **Your Personalized Goals:**
        - **Calories:** {cal_goal} per day
        - **Protein:** {prot_goal}g per day  
        - **Carbs:** {carb_goal}g per day
        - **Fat:** {fat_goal}g per day
        - **Sugar:** {sugar_goal}g per day
        """)
    
    # Show current goals
    st.info(f"""
    **Current Goals:** 
    Calories: {st.session_state.calorie_goal} | Protein: {st.session_state.protein_goal}g | 
    Carbs: {st.session_state.carb_goal}g | Fat: {st.session_state.fat_goal}g | Sugar: {st.session_state.sugar_goal}g
    """)

# Sidebar for adding food
st.sidebar.header("Add Food")

# Food selection
food_name = st.sidebar.selectbox("Choose a food:", list(food_database.keys()))

# Amount input
grams = st.sidebar.number_input("How many grams?", min_value=0.0, value=100.0, step=10.0)

# Add food button
if st.sidebar.button("Add Food"):
    if grams > 0:
        # Calculate nutrition based on grams (database is per 100g)
        multiplier = grams / 100
        calories = food_database[food_name][0] * multiplier
        protein = food_database[food_name][1] * multiplier
        carbs = food_database[food_name][2] * multiplier
        fat = food_database[food_name][3] * multiplier
        sugar = food_database[food_name][4] * multiplier
        
        # Add to daily totals
        st.session_state.daily_calories += calories
        st.session_state.daily_protein += protein
        st.session_state.daily_carbs += carbs
        st.session_state.daily_fat += fat
        st.session_state.daily_sugar += sugar
        
        st.sidebar.success(f"Added {grams}g of {food_name}!")
    else:
        st.sidebar.error("Please enter a valid amount!")

# Reset button
if st.sidebar.button("Reset Day"):
    st.session_state.daily_calories = 0
    st.session_state.daily_protein = 0
    st.session_state.daily_carbs = 0
    st.session_state.daily_fat = 0
    st.session_state.daily_sugar = 0
    st.sidebar.success("Day reset!")

# Main content area
col1, col2 = st.columns(2)

# Today's totals
with col1:
    st.header("📊 Today's Totals")
    st.metric("Calories", f"{st.session_state.daily_calories:.1f}")
    st.metric("Protein", f"{st.session_state.daily_protein:.1f}g")
    st.metric("Carbs", f"{st.session_state.daily_carbs:.1f}g")
    st.metric("Fat", f"{st.session_state.daily_fat:.1f}g")
    st.metric("Sugar", f"{st.session_state.daily_sugar:.1f}g")

# Goal progress
with col2:
    st.header("🎯 Goal Progress")
    
    # Calculate percentages
    cal_percent = (st.session_state.daily_calories / st.session_state.calorie_goal) * 100
    protein_percent = (st.session_state.daily_protein / st.session_state.protein_goal) * 100
    carb_percent = (st.session_state.daily_carbs / st.session_state.carb_goal) * 100
    fat_percent = (st.session_state.daily_fat / st.session_state.fat_goal) * 100
    sugar_percent = (st.session_state.daily_sugar / st.session_state.sugar_goal) * 100
    
    # Progress bars
    st.progress(min(cal_percent / 100, 1.0))
    st.write(f"Calories: {st.session_state.daily_calories:.1f}/{st.session_state.calorie_goal} ({cal_percent:.1f}%)")
    
    st.progress(min(protein_percent / 100, 1.0))
    st.write(f"Protein: {st.session_state.daily_protein:.1f}g/{st.session_state.protein_goal}g ({protein_percent:.1f}%)")
    
    st.progress(min(carb_percent / 100, 1.0))
    st.write(f"Carbs: {st.session_state.daily_carbs:.1f}g/{st.session_state.carb_goal}g ({carb_percent:.1f}%)")
    
    st.progress(min(fat_percent / 100, 1.0))
    st.write(f"Fat: {st.session_state.daily_fat:.1f}g/{st.session_state.fat_goal}g ({fat_percent:.1f}%)")
    
    st.progress(min(sugar_percent / 100, 1.0))
    st.write(f"Sugar: {st.session_state.daily_sugar:.1f}g/{st.session_state.sugar_goal}g ({sugar_percent:.1f}%)")

# Daily Advice Section
if st.session_state.daily_calories > 0:
    st.header("💡 Daily Advice")
    advice_list = get_daily_advice()
    
    for advice in advice_list:
        st.markdown(advice)

# Food database display
st.header("📋 Food Database")
st.markdown("*Nutrition values per 100g*")

# Create a nice table
df = pd.DataFrame.from_dict(food_database, orient='index', 
                           columns=['Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)', 'Sugar (g)'])
df.index.name = 'Food'
st.dataframe(df, use_container_width=True)

# Instructions
st.header("📝 How to Use")
st.markdown("""
1. **Choose a food** from the dropdown in the sidebar
2. **Enter the amount** in grams
3. **Click "Add Food"** to add it to your daily totals
4. **View your progress** toward daily goals with the progress bars
5. **Get personalized advice** based on your daily intake
6. **Reset** your day anytime with the reset button
""")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ for healthy living!")