import streamlit as st

st.set_page_config(page_title="Maternal Risk Decision Support", page_icon="🩺")

# Τίτλος εφαρμογής
st.title("Σύστημα Υποστήριξης Απόφασης για Κίνδυνο στην Εγκυμοσύνη")

# Περιγραφή έργου και ομάδα
st.markdown("""
### 📝 Project Title:
**Analysis of Clinical Risk Thresholds During Pregnancy and Development of a Web-Based Decision Support Application**

---

### 👨‍⚕️ Developed by:
**Dr. Georgios Bouchouras**

---

### 👥 Team Members:
- Angela Lavntarakou, BSc (Hons) Midwifery  
- Eleni Samara, BSc (Hons) Midwifery  
- Georgios Bouchouras, BSc (Hons) Midwifery  
- Emmanouela Dimoveli, BSc (Hons) Midwifery  
- Georgios Sofianidis, BSc (Hons) Midwifery

---
""")

# Εισαγωγή κλινικών τιμών
age = st.slider("Ηλικία", 15, 50, 30)
systolic = st.slider("Συστολική Πίεση (mmHg)", 80, 180, 120)
diastolic = st.slider("Διαστολική Πίεση (mmHg)", 50, 120, 80)
bs = st.slider("Σάκχαρο (mmol/L)", 4.0, 20.0, 7.0)
hr = st.slider("Καρδιακός Ρυθμός (bpm)", 50, 120, 75)

# Κανόνες απόφασης
if bs > 10 and systolic > 120:
    level = "🟥 Υψηλή Επιτήρηση"
elif bs > 9 or systolic > 130 or diastolic > 85:
    level = "🟧 Μέτρια Επιτήρηση"
else:
    level = "🟩 Χαμηλή Επιτήρηση"

# Εμφάνιση αποτελέσματος
st.markdown(f"## ✅ Προτεινόμενο Επίπεδο Επιτήρησης: {level}")
