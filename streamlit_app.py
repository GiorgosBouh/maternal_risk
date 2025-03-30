import streamlit as st

st.set_page_config(page_title="Maternal Risk Decision Support", page_icon="🩺")

# Τίτλος εφαρμογής
st.title("Σύστημα Υποστήριξης Απόφασης για Κίνδυνο στην Εγκυμοσύνη")

# Περιγραφή έργου και ομάδα
st.markdown("""
### 📝 Τίτλος Έργου:
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

### 📚 Data & Validity
This application is based on real clinical data from the **Maternal Health Risk Dataset** (n=1014), published in:

Ahmed M., Kashem M.A., Rahman M., Khatun S. (2020). *Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things (IoT).* In: Kasruddin Nasir A. et al. (eds) InECCE2019. Lecture Notes in Electrical Engineering, vol 632. Springer, Singapore.

Risk thresholds have been derived from statistical analysis. When clinical values exceed the maximum range of the dataset, classification is based on widely accepted general medical guidelines.

---
""")

# Εισαγωγή τιμών
age = st.slider("Ηλικία", 15, 50, 30)
systolic = st.slider("Συστολική Πίεση (mmHg)", 30, 200, 120)
diastolic = st.slider("Διαστολική Πίεση (mmHg)", 10, 160, 80)
bs = st.slider("Σάκχαρο (mmol/L)", 4.0, 20.0, 7.0)
hr = st.slider("Καρδιακός Ρυθμός (bpm)", 30, 130, 75)

# Εντοπισμός τιμών εκτός ορίων του dataset
note = ""
if systolic > 160 or diastolic > 100:
    note = "⚠️ Σημείωση: Οι τιμές πίεσης που καταχωρήθηκαν υπερβαίνουν το εύρος του αρχικού dataset και η εκτίμηση βασίζεται σε κοινώς αποδεκτές κλινικές κατευθυντήριες οδηγίες."

# Λογική υποστήριξης απόφασης
if systolic < 90 or diastolic < 50 or hr < 60:
    level = "🟥 Υψηλή Επιτήρηση"
elif systolic > 160 or diastolic > 100 or hr > 110:
    level = "🟥 Υψηλή Επιτήρηση"
elif bs > 10 and systolic > 120:
    level = "🟥 Υψηλή Επιτήρηση"
elif bs > 9 or systolic > 130 or diastolic > 85:
    level = "🟧 Μέτρια Επιτήρηση"
else:
    level = "🟩 Χαμηλή Επιτήρηση"

# Εμφάνιση αποτελέσματος
st.markdown(f"## ✅ Προτεινόμενο Επίπεδο Επιτήρησης: {level}")
if note:
    st.info(note)
