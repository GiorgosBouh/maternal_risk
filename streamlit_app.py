import re
from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Maternal Risk & EACI Dashboard", page_icon="🩺", layout="wide")


# ============================================================
# CONFIG
# ============================================================

EXCEL_PATH = Path("GiorgosBouh/maternal_risk/hosp-epis-stat-mat-dqanlys-2017-18.xlsx")


# ============================================================
# HELPERS
# ============================================================

def interpret_eaci(score):
    if score > 0.85:
        return "Πολύ καλή επίδοση"
    elif score >= 0.70:
        return "Καλή επίδοση"
    elif score >= 0.50:
        return "Μέτρια επίδοση"
    else:
        return "Χαμηλή επίδοση"


def classify_booking_week(text, early_limit_weeks=12):
    """
    Επιστρέφει:
    - label
    - group: 'Early' / 'Late' / None
    - representative_week
    """
    if pd.isna(text):
        return None, None, None

    s = str(text).strip().lower()
    s = re.sub(r"\s+", " ", s)

    invalid_tokens = ["unknown", "not known", "missing", "not stated", "other"]
    if any(token in s for token in invalid_tokens):
        return str(text), None, None

    range_match = re.search(r"(\d+)\s*-\s*(\d+)", s)
    if range_match:
        start_week = int(range_match.group(1))
        end_week = int(range_match.group(2))
        label = f"{start_week}-{end_week} εβδομάδες"
        representative_week = (start_week + end_week) / 2
        group = "Early" if end_week <= early_limit_weeks else "Late"
        return label, group, representative_week

    plus_match = re.search(r"(\d+)\s*\+", s)
    if plus_match:
        week = int(plus_match.group(1))
        label = f"{week}+ εβδομάδες"
        representative_week = week
        group = "Early" if week <= early_limit_weeks else "Late"
        return label, group, representative_week

    single_match = re.search(r"(\d+)", s)
    if single_match:
        week = int(single_match.group(1))
        label = f"{week} εβδομάδες"
        representative_week = week
        group = "Early" if week <= early_limit_weeks else "Late"
        return label, group, representative_week

    return str(text), None, None


@st.cache_data
def load_flat_file(excel_path):
    return pd.read_excel(excel_path, sheet_name="Flat file")


@st.cache_data
def compute_eaci(excel_path, early_limit_weeks=12):
    df = load_flat_file(excel_path)

    booking = df[df["Dimension"].astype(str).str.strip() == "GestationAtBooking"].copy()

    if "Org_Level" in booking.columns:
        mask_all_submitters = booking["Org_Level"].astype(str).str.strip().str.lower() == "all submitters"
        if mask_all_submitters.any():
            booking = booking[mask_all_submitters].copy()

    parsed = booking["Measure1"].apply(lambda x: classify_booking_week(x, early_limit_weeks))
    booking["Booking_Label"] = parsed.apply(lambda x: x[0])
    booking["Booking_Group"] = parsed.apply(lambda x: x[1])
    booking["Week_Num"] = parsed.apply(lambda x: x[2])

    booking["Value"] = pd.to_numeric(booking["Value"], errors="coerce")
    booking = booking.dropna(subset=["Value"])

    valid_booking = booking[booking["Booking_Group"].notna()].copy()

    distribution_df = (
        valid_booking.groupby(["Booking_Label", "Week_Num", "Booking_Group"], as_index=False)["Value"]
        .sum()
        .sort_values(["Week_Num", "Booking_Label"])
    )

    weekly_df = (
        distribution_df.groupby("Week_Num", as_index=False)["Value"]
        .sum()
        .sort_values("Week_Num")
    )

    early_total = valid_booking.loc[valid_booking["Booking_Group"] == "Early", "Value"].sum()
    late_total = valid_booking.loc[valid_booking["Booking_Group"] == "Late", "Value"].sum()
    grand_total = early_total + late_total

    if grand_total == 0:
        raise ValueError("Δεν βρέθηκαν έγκυρα δεδομένα για τον υπολογισμό του EACI.")

    eaci = early_total / grand_total
    late_ratio = late_total / grand_total
    interpretation = interpret_eaci(eaci)

    cumulative_df = weekly_df.copy()
    cumulative_df["Cumulative"] = cumulative_df["Value"].cumsum()
    cumulative_df["Cumulative_Percent"] = 100 * cumulative_df["Cumulative"] / cumulative_df["Value"].sum()

    return {
        "raw_df": df,
        "distribution_df": distribution_df,
        "weekly_df": weekly_df,
        "cumulative_df": cumulative_df,
        "early_total": early_total,
        "late_total": late_total,
        "grand_total": grand_total,
        "eaci": eaci,
        "late_ratio": late_ratio,
        "interpretation": interpretation,
        "early_limit_weeks": early_limit_weeks,
    }


# ============================================================
# PAGE 1: RISK DECISION SUPPORT
# ============================================================

def render_risk_decision_support():
    st.title("Σύστημα Υποστήριξης Απόφασης για Κίνδυνο στην Εγκυμοσύνη")

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
    """)

    st.markdown("""
    ---
    ⚠️ **Disclaimer**

    This tool is intended strictly for educational and research purposes. It is not a diagnostic tool and must never replace medical advice. Always consult a qualified healthcare provider for medical concerns.
    ---
    """)

    age = st.slider("Ηλικία", 15, 50, 30)
    systolic = st.slider("Συστολική Πίεση (mmHg)", 30, 200, 120)
    diastolic = st.slider("Διαστολική Πίεση (mmHg)", 10, 160, 80)
    bs = st.slider("Σάκχαρο (mmol/L)", 4.0, 25.0, 7.0)
    hr = st.slider("Καρδιακός Ρυθμός (bpm)", 30, 150, 75)

    note = ""
    if systolic > 160 or diastolic > 100 or bs > 20 or hr > 120 or systolic < 90 or diastolic < 50 or hr < 60:
        note = (
            "⚠️ Σημείωση: Μία ή περισσότερες τιμές που καταχωρήθηκαν υπερβαίνουν "
            "(ή υπολείπονται) των ορίων του αρχικού dataset. Η εκτίμηση βασίζεται "
            "σε κοινώς αποδεκτές ιατρικές κατευθυντήριες οδηγίες και όχι σε εμπειρικά δεδομένα."
        )

    if systolic < 90 or diastolic < 50 or hr < 60:
        level = "🟥 Υψηλή Επιτήρηση"
    elif systolic > 160 or diastolic > 100 or hr > 120 or bs > 20:
        level = "🟥 Υψηλή Επιτήρηση"
    elif bs > 10 and systolic > 120:
        level = "🟥 Υψηλή Επιτήρηση"
    elif bs > 9 or systolic > 130 or diastolic > 85:
        level = "🟧 Μέτρια Επιτήρηση"
    else:
        level = "🟩 Χαμηλή Επιτήρηση"

    st.markdown(f"## ✅ Προτεινόμενο Επίπεδο Επιτήρησης: {level}")

    if note:
        st.info(note)

    st.markdown("### Κλινικές Τιμές")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Ηλικία", age)
    col2.metric("Συστολική", systolic)
    col3.metric("Διαστολική", diastolic)
    col4.metric("Σάκχαρο", bs)
    col5.metric("Καρδιακός Ρυθμός", hr)


# ============================================================
# PAGE 2: EACI DASHBOARD
# ============================================================

def render_eaci_dashboard():
    st.title("Δείκτης Έγκαιρης Προγεννητικής Φροντίδας (EACI)")
    st.markdown("""
    ### 📝 Τίτλος Έργου
    **Ανάπτυξη δείκτη έγκαιρης προγεννητικής φροντίδας μέσω ανάλυσης ανοικτών δεδομένων μαιευτικών υπηρεσιών**

    Ο δείκτης **Early Antenatal Care Index (EACI)** υπολογίζεται ως το ποσοστό των εγκύων
    που πραγματοποιούν την πρώτη προγεννητική επίσκεψη μέχρι και τη 12η εβδομάδα κύησης
    σε σχέση με το σύνολο των εγκύων με διαθέσιμα δεδομένα booking.

    Ο πίνακας και τα γραφήματα βασίζονται στο αρχείο Excel:
    `GiorgosBouh/maternal_risk/hosp-epis-stat-mat-dqanlys-2017-18.xlsx`
    """)

    if not EXCEL_PATH.exists():
        st.error(f"Δεν βρέθηκε το αρχείο Excel στο path: {EXCEL_PATH}")
        st.stop()

    early_limit_weeks = st.sidebar.number_input(
        "Όριο έγκαιρης έναρξης (εβδομάδες)",
        min_value=1,
        max_value=40,
        value=12,
        step=1
    )

    try:
        results = compute_eaci(EXCEL_PATH, early_limit_weeks)
    except Exception as e:
        st.error(f"Σφάλμα κατά την ανάλυση του Excel: {e}")
        st.stop()

    early_total = results["early_total"]
    late_total = results["late_total"]
    grand_total = results["grand_total"]
    eaci = results["eaci"]
    late_ratio = results["late_ratio"]
    interpretation = results["interpretation"]
    distribution_df = results["distribution_df"]
    weekly_df = results["weekly_df"]
    cumulative_df = results["cumulative_df"]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Σύνολο εγκύων", f"{grand_total:,.0f}")
    col2.metric(f"Έγκαιρη έναρξη (≤ {early_limit_weeks} εβδ.)", f"{early_total:,.0f}")
    col3.metric(f"Καθυστερημένη έναρξη (> {early_limit_weeks} εβδ.)", f"{late_total:,.0f}")
    col4.metric("EACI", f"{eaci:.3f} ({eaci*100:.1f}%)")

    st.success(f"Ερμηνεία δείκτη: **{interpretation}**")

    st.markdown("## Γραφήματα")

    colA, colB = st.columns(2)

    with colA:
        fig1, ax1 = plt.subplots(figsize=(8, 5))
        ax1.plot(weekly_df["Week_Num"], weekly_df["Value"], marker="o")
        ax1.set_title("Κατανομή πρώτης προγεννητικής επίσκεψης")
        ax1.set_xlabel("Εβδομάδα κύησης")
        ax1.set_ylabel("Αριθμός γυναικών")
        ax1.grid(True, alpha=0.3)
        st.pyplot(fig1)

    with colB:
        fig2, ax2 = plt.subplots(figsize=(8, 5))
        ax2.bar(
            [f"Έγκαιρη\n≤{early_limit_weeks}", f"Καθυστερημένη\n>{early_limit_weeks}"],
            [early_total, late_total]
        )
        ax2.set_title("Έγκαιρη vs Καθυστερημένη έναρξη")
        ax2.set_ylabel("Αριθμός γυναικών")
        st.pyplot(fig2)

    colC, colD = st.columns(2)

    with colC:
        fig3, ax3 = plt.subplots(figsize=(7, 7))
        ax3.pie(
            [early_total, late_total],
            labels=["Έγκαιρη έναρξη", "Καθυστερημένη έναρξη"],
            autopct="%1.1f%%",
            startangle=90
        )
        ax3.set_title("Ποσοστιαία κατανομή")
        st.pyplot(fig3)

    with colD:
        fig4, ax4 = plt.subplots(figsize=(8, 5))
        ax4.plot(cumulative_df["Week_Num"], cumulative_df["Cumulative_Percent"], marker="o")
        ax4.axhline(50, linestyle="--")
        ax4.axhline(80, linestyle="--")
        ax4.axhline(90, linestyle="--")
        ax4.set_title("Σωρευτικό ποσοστό booking")
        ax4.set_xlabel("Εβδομάδα κύησης")
        ax4.set_ylabel("Σωρευτικό ποσοστό (%)")
        ax4.set_ylim(0, 100)
        ax4.grid(True, alpha=0.3)
        st.pyplot(fig4)

    st.markdown("## Αναλυτικός πίνακας")
    st.dataframe(
        distribution_df.rename(columns={
            "Booking_Label": "Ετικέτα",
            "Week_Num": "Εβδομάδα",
            "Booking_Group": "Κατηγορία",
            "Value": "Αριθμός γυναικών"
        }),
        use_container_width=True
    )

    st.markdown("## Αυτόματη ερμηνεία αποτελεσμάτων")

    report_text = f"""
### Αποτελέσματα
Η ανάλυση των δεδομένων έδειξε ότι το σύνολο των εγκύων με έγκυρες εγγραφές GestationAtBooking ήταν **{grand_total:,.0f}**.
Από αυτές, οι **{early_total:,.0f} ({eaci*100:.1f}%)** ξεκίνησαν την προγεννητική φροντίδα έγκαιρα, δηλαδή μέχρι και την **{early_limit_weeks}η εβδομάδα κύησης**,
ενώ οι **{late_total:,.0f} ({late_ratio*100:.1f}%)** την ξεκίνησαν αργότερα.
Ο δείκτης **Early Antenatal Care Index (EACI)** υπολογίστηκε ίσος με **{eaci:.3f}**, τιμή που αντιστοιχεί σε **{interpretation.lower()}**.

### Συζήτηση
Η πλειονότητα των γυναικών φαίνεται να εντάσσεται στην προγεννητική παρακολούθηση στο πρώτο τρίμηνο της κύησης,
γεγονός που συμφωνεί με τις βασικές κατευθύνσεις για έγκαιρη μαιευτική φροντίδα.
Η παρουσία όμως περιπτώσεων καθυστερημένης έναρξης δείχνει ότι εξακολουθούν να υπάρχουν εμπόδια στην πρόσβαση,
στην ενημέρωση ή στην έγκαιρη αναγνώριση της ανάγκης για προγεννητική φροντίδα.

### Συμπεράσματα
Ο προτεινόμενος δείκτης **EACI** αποτελεί ένα απλό αλλά χρήσιμο εργαλείο καινοτομίας,
καθώς μετατρέπει ανοικτά δεδομένα μαιευτικών υπηρεσιών σε έναν άμεσα ερμηνεύσιμο δείκτη αξιολόγησης.
Μπορεί να χρησιμοποιηθεί σε μελλοντικές συγκρίσεις μεταξύ περιόδων, μονάδων υγείας ή περιοχών
και να υποστηρίξει ερευνητικές και εκπαιδευτικές εφαρμογές στη μαιευτική.
"""
    st.markdown(report_text)

    st.markdown("## Λήψη αποτελεσμάτων")
    csv_data = distribution_df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 Λήψη πίνακα κατανομής σε CSV",
        data=csv_data,
        file_name="eaci_distribution.csv",
        mime="text/csv"
    )


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

st.sidebar.title("Μενού εφαρμογής")

page = st.sidebar.radio(
    "Επιλογή ενότητας",
    [
        "Maternal Risk Decision Support",
        "EACI Dashboard"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Repository path**")
st.sidebar.code(str(EXCEL_PATH))

if page == "Maternal Risk Decision Support":
    render_risk_decision_support()
else:
    render_eaci_dashboard()