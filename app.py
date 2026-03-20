import streamlit as st
import joblib
import numpy as np
import mysql.connector

# -------------------------------
# 1. Load trained model
# -------------------------------
model = joblib.load("model.pkl")

# -------------------------------
# 2. Connect to MySQL
# -------------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root1234",  # change this
    database="disease_db"
)
cursor = db.cursor()

# -------------------------------
# 3. Symptoms mapping
# -------------------------------
symptoms_dict = {
    "Heart Disease": ["Chest pain", "Shortness of breath", "Fatigue"],
    "Diabetes": ["Frequent urination", "Increased thirst", "Weight loss"],
    "Healthy": ["No major symptoms"]
}

# -------------------------------
# 4. UI
# -------------------------------
st.title("🏥 Disease Prediction System")

st.write("Enter clinical data:")

age = st.number_input("Age", 1, 100)
bp = st.number_input("Blood Pressure", 50, 200)
sugar = st.number_input("Blood Sugar", 50, 300)
chol = st.number_input("Cholesterol", 0, 400)

# -------------------------------
# 5. Prediction
# -------------------------------
if st.button("🔍 Predict"):

    features = np.array([[age, bp, sugar, chol]])

    prediction = model.predict(features)[0]

    symptoms = symptoms_dict.get(prediction, [])

    # Save to MySQL
    cursor.execute(
        "INSERT INTO predictions (age, bp, sugar, cholesterol, disease) VALUES (%s, %s, %s, %s, %s)",
        (age, bp, sugar, chol, prediction)
    )
    db.commit()

    # Show result
    st.success(f"Predicted Disease: {prediction}")

    st.subheader("Possible Symptoms:")
    for s in symptoms:
        st.write("•", s)

    st.warning("⚠️ This is a prediction system. Please consult a doctor.")