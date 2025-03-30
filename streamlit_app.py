import streamlit as st

st.set_page_config(page_title="Maternal Risk Decision Support", page_icon="🩺")

# Τίτλος εφαρμογής
st.title("Σύστημα Υποστήριξης Απόφασης για Κίνδυνο στην Εγκυμοσύνη")

# Περιγραφή έργου και ομάδα
st.markdown("""
### 📝 Τίτλος Έργου:
**Analysis of Clinical Risk Thresholds During Pregnancy and Development of a Web-Based Decision Support Application**

---

### 👨‍⚕️ Δημιουργία:
**Dr. Georgios Bouchouras**

---

### 👥 Μέλη ομάδας:
- Angela Lavntarakou, BSc (Hons) Midwifery  
- Eleni Samara, BSc (Hons) Midwifery  
- Georgios Bouchouras, BSc (Hons) Midwifery  
- Emmanouela Dimoveli, BSc (Hons) Midwifery  
- Georgios Sofianidis, BSc (Hons) Midwifery

---

### 📚 Προέλευση δεδομένων:
This application is based entirely on real clinical data from the **Maternal Health Risk Dataset** (n=1014), published in:

Ahmed M., Kashem M.A., Rahman M., Khatun S. (2020). *Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things (IoT).* In: Kasruddin Nasir A. et al. (eds) InECCE2019. Lecture Notes in Electrical Engineering, vol 632. Springer, Singapore.

Clinical thresholds were derived from statistical analysis of blood pressure, blood sugar, heart rate, and temperature distributions across different risk levels.

---
""")

# Εισαγωγή κλινικών τιμών
age = st.slider("Ηλικία", 15, 50, 30)
systolic = st.slider("Συστολική Πίεση (mmHg)", 30, 180, 120)
diastolic = st.slider("Διαστολική Πίεση (mmHg)", 10, 120, 80)
bs = st.slider("Σάκχαρο (mmol/L)", 4.0, 20.0, 7.0)
hr = st.slider("Καρδιακός Ρυθμός (bpm)", 30, 120, 75)

# Ανανεωμένοι κανόνες απόφασης με ελέγχους και για χαμηλές τιμές
if systolic < 90 or diastolic < 50 or hr < 60:
    level = "🟥 Υψηλή Επιτήρηση"
elif bs > 10 and systolic > 120:
    level = "🟥 Υψηλή Επιτήρηση"
elif bs > 9 or systolic > 130 or diastolic > 85:
    level = "🟧 Μέτρια Επιτήρηση"
else:
    level = "🟩 Χαμηλή Επιτήρηση"

# Εμφάνιση αποτελέσματος
st.markdown(f"## ✅ Προτεινόμενο Επίπεδο Επιτήρησης: {level}")
