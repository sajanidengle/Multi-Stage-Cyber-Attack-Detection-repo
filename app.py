import streamlit as st
import pandas as pd

st.title("🔐 Cyber Kill Chain Intrusion Detection System")

df = pd.read_csv("data/final_ckc_dataset.csv")

st.subheader("Dataset Preview")
st.write(df.head())

st.subheader("CKC Stage Distribution")
st.bar_chart(df["CKC_Stage"].value_counts())

st.subheader("🚨 Live Alerts")

alerts = df.sample(20)

for i, row in alerts.iterrows():
    if row["CKC_Stage"] != "Benign":
        st.error(f"ALERT: {row['CKC_Stage']} detected at flow {i}")