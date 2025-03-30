# maternal_risk
A web-based clinical decision support system for evaluating maternal health risk levels based on vital signs such as blood pressure, blood sugar, heart rate, and temperature. Built with Streamlit for rapid and interpretable assessment. No machine learning required.

# 🩺 Maternal Health Risk Decision Support System

This project provides a lightweight and interpretable **web-based decision support application** for assessing pregnancy-related risk levels based on vital signs.

Developed using **Streamlit**, the application enables healthcare professionals and students to enter basic clinical parameters and receive an instant risk level classification: 🟥 High, 🟧 Moderate, or 🟩 Low.

---

## 📊 Parameters Used
- **Systolic Blood Pressure** (mmHg)
- **Diastolic Blood Pressure** (mmHg)
- **Blood Sugar (BS)** (mmol/L)
- **Heart Rate** (bpm)
- **Body Temperature** (°F)
- **Age** (Years)

---

## 💡 Methodology

The system uses simple threshold-based rules derived from the [Maternal Health Risk Dataset](https://link.springer.com/chapter/10.1007/978-981-15-2317-5_58), originally published by Ahmed et al. (2020). No machine learning is used, ensuring transparency and ease of interpretation.

Examples of clinical rules:
- If BS > 10 mmol/L and Systolic BP > 120 mmHg → 🟥 High Risk
- If BS > 9 or Diastolic BP > 85 → 🟧 Moderate Risk
- Otherwise → 🟩 Low Risk

---

## 🚀 Try It Online

You can deploy this app on **Streamlit Cloud** or run it locally using:

```bash
streamlit run app.py
