import streamlit as st

st.title("Σύστημα Υποστήριξης Απόφασης για Κίνδυνο στην Εγκυμοσύνη")

age = st.slider("Ηλικία", 15, 50, 30)
systolic = st.slider("Συστολική Πίεση (mmHg)", 80, 180, 120)
diastolic = st.slider("Διαστολική Πίεση (mmHg)", 50, 120, 80)
bs = st.slider("Σάκχαρο (mmol/L)", 4.0, 20.0, 7.0)
hr = st.slider("Καρδιακός Ρυθμός (bpm)", 50, 120, 75)

if bs > 10 and systolic > 120:
    level = "🟥 Υψηλή Επιτήρηση"
elif bs > 9 or systolic > 130 or diastolic > 85:
    level = "🟧 Μέτρια Επιτήρηση"
else:
    level = "🟩 Χαμηλή Επιτήρηση"

st.markdown(f"## Προτεινόμενο Επίπεδο Επιτήρησης: {level}")
