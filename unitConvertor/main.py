import streamlit as st

st.sidebar.title("Unit Converter")
conversion = st.sidebar.selectbox("Choose Conversion Type", ("Length", "Weight", "Temperature"))

st.title("🌎 Unit Converter")

def length_converter(value, from_unit, to_unit):
    conversions = {
        "kilometer": 1000,  # 1 kilometer = 1000 meters
        "meter": 1,         # 1 meter = 1 meter
        "centimeter": 0.01, # 1 centimeter = 0.01 meters
        "inch": 0.0254,     # 1 inch = 0.0254 meters
        "foot": 0.3048,     # 1 foot = 0.3048 meters
        "mile": 1609.34     # 1 mile = 1609.34 meters
    }
    try:
        value_in_meters = value * conversions[from_unit]
        return value_in_meters / conversions[to_unit]
    except KeyError:
        return None

def weight_converter(value, from_unit, to_unit):
    conversions = {
        "kilogram": 1,      # 1 kilogram = 1 kilogram
        "gram": 0.001,      # 1 gram = 0.001 kilograms
        "milligram": 0.000001,  # 1 milligram = 0.000001 kilograms
        "pound": 0.453592,  # 1 pound = 0.453592 kilograms
        "ounce": 0.0283495  # 1 ounce = 0.0283495 kilograms
    }
    try:
        value_in_kilograms = value * conversions[from_unit]
        return value_in_kilograms / conversions[to_unit]
    except KeyError:
        return None

def temperature_converter(value, from_unit, to_unit):
    if from_unit == "Celsius" and to_unit == "Fahrenheit":
        return (value * 9/5) + 32
    elif from_unit == "Fahrenheit" and to_unit == "Celsius":
        return (value - 32) * 5/9
    elif from_unit == "Celsius" and to_unit == "Kelvin":
        return value + 273.15
    elif from_unit == "Kelvin" and to_unit == "Celsius":
        return value - 273.15
    elif from_unit == "Fahrenheit" and to_unit == "Kelvin":
        return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin" and to_unit == "Fahrenheit":
        return (value - 273.15) * 9/5 + 32
    else:
        return None
value = st.number_input("Enter the value:")

if conversion == "Length":
    st.subheader("Convert Length:")
    from_unit = st.selectbox("From Unit:", ["kilometer", "meter", "centimeter", "inch", "foot", "mile"])
    to_unit = st.selectbox("To Unit:", ["kilometer", "meter", "centimeter", "inch", "foot", "mile"])
    result = length_converter(value, from_unit, to_unit)

elif conversion == "Weight":
    st.subheader("⚖️Convert Weight")
    from_unit = st.selectbox("From Unit:", ["kilogram", "gram", "milligram", "pound", "ounce"])
    to_unit = st.selectbox("To Unit:", ["kilogram", "gram", "milligram", "pound", "ounce"])
    result = weight_converter(value, from_unit, to_unit)

elif conversion == "Temperature":
    st.subheader("🌡️Convert Temperature")
    from_unit = st.selectbox("From Unit:", ["Celsius", "Fahrenheit", "Kelvin"])
    to_unit = st.selectbox("To Unit:", ["Celsius", "Fahrenheit", "Kelvin"])
    result = temperature_converter(value, from_unit, to_unit)

if st.button("Convert"):
   st.success(f"Result: {value} {from_unit} is equal to {result:.2f} {to_unit}.")