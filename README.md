# Multi-Stage-Cyber-Attack-Detection-repo
An AI-Driven Cyber Kill Chain-Aware Framework for Multi-Stage Cyber Attack Detection system that classifies network traffic into **Cyber Kill Chain (CKC) stages** using machine learning.

---

##  Overview

Traditional IDS detect attacks but lack context.  
This project identifies **which stage of an attack is happening**, improving threat understanding and response.

---

##  CKC Stages Mapped

- Reconnaissance  
- Exploitation  
- Installation  
- Command & Control  
- Actions on Objectives  
- Benign  

---

##  Methodology

- Data preprocessing (cleaning, filtering)
- CKC mapping (label + behavior-based)
- Stratified sampling (~2M rows)
- Random Forest classification
- Alert generation system

---

##  Results

- Accuracy: ~92%  
- Strong detection: C2, DDoS  
- Lower performance: Reconnaissance, Installation  

---

##  Alert System

- Alerts for non-benign traffic  
- Severity levels based on CKC stage  
- Simulated real-time detection  

---

##  Tech Stack

Python, Pandas, Scikit-learn, Matplotlib, Streamlit  

---

##  Run

```bash
python src/train_random_forest_ckc.py
streamlit run src/app.py
