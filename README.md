# Multi-Stage-Cyber-Attack-Detection-repo
An AI-Driven Cyber Kill Chain-Aware Framework for Multi-Stage Cyber Attack Detection system that classifies network traffic into **Cyber Kill Chain (CKC) stages** using machine learning.

---

##  Overview

Traditional IDS detect attacks but lack context.  
This project identifies **which stage of an attack is happening**, improving threat understanding and response.

---

##  Dataset

- **Dataset Used:** CIC-IDS2018  
- **Source:** Canadian Institute for Cybersecurity  
- **Download Link:** https://www.unb.ca/cic/datasets/ids-2018.html  

The CIC-IDS2018 dataset contains realistic network traffic with both benign and malicious activities. It includes multiple attack types such as DDoS, brute force, botnet, and infiltration, along with more than 80 network flow features.

In this project, the dataset was:
- Cleaned and preprocessed
- Mapped to Cyber Kill Chain (CKC) stages
- Sampled (~2 million rows) using stratified sampling for efficient training

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
