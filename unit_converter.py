import streamlit as st
from datetime import datetime

# Set page config with an emoji in title
st.set_page_config(page_title="🔢 Smart Unit Converter", layout="centered")

# Define unit conversions with categories and formulas
conversions = {
    "📏 Length": {"Meter": 1, "Kilometer": 0.001, "Centimeter": 100, "Millimeter": 1000, 
                 "Mile": 0.000621371, "Yard": 1.09361, "Foot": 3.28084, "Inch": 39.3701},
    "⚖️ Weight": {"Kilogram": 1, "Gram": 1000, "Milligram": 1e6, "Pound": 2.20462, "Ounce": 35.274},
    "🌡 Temperature": {
        "Celsius": lambda x: (x, "Celsius remains the same."),
        "Fahrenheit": lambda x: ((x * 9/5) + 32, "Multiply Celsius by 9/5 and add 32."),
        "Kelvin": lambda x: (x + 273.15, "Add 273.15 to Celsius.")
    },
    "🚗 Speed": {"Meters per second": 1, "Kilometers per hour": 3.6, "Miles per hour": 2.23694},
    "⏳ Time": {"Second": 1, "Minute": 1/60, "Hour": 1/3600, "Day": 1/86400},
    "📐 Area": {"Square Meter": 1, "Square Kilometer": 1e-6, "Hectare": 1e-4, 
               "Acre": 0.000247105, "Square Mile": 3.861e-7},
    "🧪 Volume": {"Liter": 1, "Milliliter": 1000, "Cubic Meter": 0.001, 
                 "Gallon": 0.264172, "Cup": 4.16667}
}

# Initialize session state for category and history
if "category" not in st.session_state:
    st.session_state.category = "📏 Length"
if "history" not in st.session_state:
    st.session_state.history = []

# Function to convert units
def convert_units(value, from_unit, to_unit, category):
    if category == "🌡 Temperature":
        base_value, explanation = conversions[category][from_unit](value)
        result, explanation = conversions[category][to_unit](base_value)
        return result, f"📖 Formula: {explanation}"

    base_value = value / conversions[category][from_unit]
    result = base_value * conversions[category][to_unit]
    return result, f"📖 Formula: {value} {from_unit} × {conversions[category][to_unit] / conversions[category][from_unit]} = {result:.4f} {to_unit}"

# UI Header
st.markdown("<h1 style='text-align: center;'>🔢 Smart Unit Converter</h1>", unsafe_allow_html=True)
st.markdown(f"<h4 style='text-align: center;'>📅 {datetime.now().strftime('%A, %d %B %Y')}</h4>", unsafe_allow_html=True)
st.write("✨ Quickly convert between different units of measurement.")

# Select category
category = st.selectbox("📌 Choose a category", list(conversions.keys()), index=list(conversions.keys()).index(st.session_state.category))
st.session_state.category = category
unit_options = list(conversions[category].keys())

# Ensure selected units exist
from_unit = st.session_state.get("from_unit", unit_options[0])
to_unit = st.session_state.get("to_unit", unit_options[1])

if from_unit not in unit_options:
    from_unit = unit_options[0]
if to_unit not in unit_options:
    to_unit = unit_options[1]

# Layout for unit selection
col1, col2, col3 = st.columns([3, 1, 3])

with col1:
    from_unit = st.selectbox("🔽 Convert from", unit_options, index=unit_options.index(from_unit))

with col2:
    if st.button("🔄 Swap"):
        from_unit, to_unit = to_unit, from_unit
        st.session_state.from_unit = from_unit
        st.session_state.to_unit = to_unit
        st.rerun()

with col3:
    to_unit = st.selectbox("🔼 Convert to", unit_options, index=unit_options.index(to_unit))

st.session_state.from_unit = from_unit
st.session_state.to_unit = to_unit

# Input value
value = st.number_input("✍️ Enter value", step=0.01, format="%.2f", key="input_value")

# Convert button and logic
if st.button("🔄 Convert Now"):
    if value is not None:
        result, formula = convert_units(value, from_unit, to_unit, category)
        st.success(f"✅ {value} {from_unit} = {result:.4f} {to_unit}")
        st.info(formula)

        # Store history
        st.session_state.history.append(f"{value} {from_unit} ➝ {result:.4f} {to_unit}")
    else:
        st.warning("⚠️ Please enter a value to convert.")

# Display conversion history
if st.session_state.history:
    st.subheader("📜 Recent Conversions")
    for record in reversed(st.session_state.history[-5:]):
        st.write(record)

# Clear history button
if st.button("🗑 Clear History"):
    st.session_state.history.clear()
    st.rerun()

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center;'>❤️ Made by <b>Sabeh Shaikh</b></h5>", unsafe_allow_html=True)