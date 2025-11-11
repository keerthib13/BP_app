import streamlit as st
import pandas as pd
from sklearn.linear_model import LinearRegression
import os

# Title
st.title("💓 Blood Pressure Prediction App")
st.write("Enter your details to check your BP level — with ❤️ from Cheloo & Keerthi")

# Load dataset
data = pd.read_csv("bp_data.csv")

# Train model
X = data[["Age", "BMI", "ExerciseHours"]]
y = data["BloodPressure"]
model = LinearRegression()
model.fit(X, y)

# Input form
st.header("🧍‍♂️ Enter Your Details")
name = st.text_input("Name:")
age = st.number_input("Age", min_value=1, max_value=120)
bmi = st.number_input("BMI", min_value=10.0, max_value=60.0)
exercise = st.number_input("Exercise Hours per week", min_value=0.0, max_value=20.0)

if st.button("🔍 Check My BP"):
    # Predict BP
    predicted_bp = model.predict([[age, bmi, exercise]])[0]
    predicted_bp = round(predicted_bp, 1)

    # Determine BP category
    if predicted_bp < 90:
        level = "Low"
        msg = f"🩵 Hello {name}, your BP is {predicted_bp} mmHg — **Low BP**, take care!"
    elif 90 <= predicted_bp <= 120:
        level = "Normal"
        msg = f"💚 Hello {name}, your BP is {predicted_bp} mmHg — **Normal**, no worries!"
    else:
        level = "High"
        msg = f"❤️‍🔥 Hello {name}, your BP is {predicted_bp} mmHg — **High BP**, be careful!"

    st.success(msg)

    # Save result to history.csv
    history_data = pd.DataFrame({
        "Name": [name],
        "Age": [age],
        "BMI": [bmi],
        "ExerciseHours": [exercise],
        "PredictedBP": [predicted_bp],
        "Level": [level]
    })

    if os.path.exists("history.csv"):
        old = pd.read_csv("history.csv")
        updated = pd.concat([old, history_data], ignore_index=True)
        updated.to_csv("history.csv", index=False)
    else:
        history_data.to_csv("history.csv", index=False)

# Show history if available
st.header("📜 BP Check History")
if os.path.exists("history.csv"):
    history = pd.read_csv("history.csv")
    st.dataframe(history)
else:
    st.info("No history found yet. Be the first to check your BP!")
