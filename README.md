
# 🩺 Maternal Risk Decision Support System

This project provides a lightweight and interpretable **web-based decision support application** for assessing pregnancy-related risk levels based on vital signs.

Developed using **Streamlit**, the application enables healthcare professionals and students to enter basic clinical parameters and receive an instant risk level classification:  
🟥 High, 🟧 Moderate, or 🟩 Low.

---

## 📝 Project Title
**Analysis of Clinical Risk Thresholds During Pregnancy and Development of a Web-Based Decision Support Application**

---

## 👨‍⚕️ Developed by
**Dr. Georgios Bouchouras**

---

## 👥 Team Members
- Angela Lavntarakou, BSc (Hons) Midwifery  
- Eleni Samara, BSc (Hons) Midwifery  
- Georgios Bouchouras, BSc (Hons) Midwifery  
- Emmanouela Dimoveli, BSc (Hons) Midwifery  
- Georgios Sofianidis, BSc (Hons) Midwifery

---

## 📊 Clinical Parameters Used
- Systolic Blood Pressure (mmHg)
- Diastolic Blood Pressure (mmHg)
- Blood Sugar (mmol/L)
- Heart Rate (bpm)
- Body Temperature (°F)
- Age (years)

---

## 🧪 Methodology

This application is based entirely on real clinical data from the **Maternal Health Risk Dataset** (n=1014), published by:

> Ahmed M., Kashem M.A., Rahman M., Khatun S. (2020).  
> *Review and Analysis of Risk Factor of Maternal Health in Remote Area Using the Internet of Things (IoT).*  
> In: Kasruddin Nasir A. et al. (eds) **InECCE2019**. *Lecture Notes in Electrical Engineering*, vol 632. Springer, Singapore.

Thresholds such as **BS > 10 mmol/L**, **Systolic BP > 120 mmHg**, and **Diastolic BP > 85 mmHg** were derived from statistical analysis across risk levels in the dataset.

In cases where user inputs exceed the maximum values present in the dataset (e.g., **Systolic BP > 160 mmHg**, **Diastolic BP > 100 mmHg**), the system classifies based on **widely accepted general medical guidelines**, and an advisory note is displayed to reflect this.

---

## 🚀 How to Run

To run locally:

```bash
pip install -r requirements.txt
streamlit run app.py
```

To deploy online, you can use [https://streamlit.io/cloud](https://streamlit.io/cloud).

---

## 📃 License & Use

This project is intended for educational and academic use. Please cite the original data source if using this work in publications.

