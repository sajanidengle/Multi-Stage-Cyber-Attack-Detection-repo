import pandas as pd
import os
import glob

input_folder = "data/base_clean"
output_folder = "data/ckc_mapped"

os.makedirs(output_folder, exist_ok=True)

# CKC Mapping Dictionary
ckc_map = {
    # Command & Control
    "Bot": "Command_and_Control",

    # Exploitation
    "FTP-BruteForce": "Exploitation",
    "SSH-Bruteforce": "Exploitation",
    "Brute Force -Web": "Exploitation",
    "Brute Force -XSS": "Exploitation",
    "SQL Injection": "Exploitation",

    # Installation
    "Infilteration": "Installation",

    # Actions on Objectives
    "DoS attacks-Hulk": "Actions_on_Objectives",
    "DoS attacks-SlowHTTPTest": "Actions_on_Objectives",
    "DoS attacks-GoldenEye": "Actions_on_Objectives",
    "DoS attacks-Slowloris": "Actions_on_Objectives",
    "DDoS attacks-LOIC-HTTP": "Actions_on_Objectives",
    "DDOS attack-HOIC": "Actions_on_Objectives",
    "DDOS attack-LOIC-UDP": "Actions_on_Objectives",

    # Benign
    "Benign": "Benign"
}

files = glob.glob(os.path.join(input_folder, "*.csv"))

for file in files:
    print(f"\nProcessing {file}...")

    df = pd.read_csv(file)

    # STEP 1: Label-based mapping
    df["CKC_Stage"] = df["Label"].map(ckc_map)

    # STEP 2: Dynamic thresholds (DATA-DRIVEN)
    duration_threshold = df["Flow Duration"].quantile(0.25)
    pkt_threshold = df["Tot Fwd Pkts"].quantile(0.30)
    rate_threshold = df["Flow Pkts/s"].quantile(0.70)

    # STEP 3: Behavior-based Reconnaissance detection
    recon_mask = (
        (df["CKC_Stage"] == "Benign") &
        (df["Flow Duration"] < duration_threshold) &
        (df["Tot Fwd Pkts"] < pkt_threshold) &
        (df["Flow Pkts/s"] > rate_threshold)
    )

    df.loc[recon_mask, "CKC_Stage"] = "Reconnaissance"

    # STEP 4: Check unmapped labels
    unmapped = df[df["CKC_Stage"].isna()]["Label"].unique()
    if len(unmapped) > 0:
        print("WARNING: Unmapped labels found:", unmapped)

    # STEP 5: Save file
    filename = os.path.basename(file)
    output_path = os.path.join(output_folder, f"ckc_{filename}")

    df.to_csv(output_path, index=False)
    print(f"Saved CKC mapped file: ckc_{filename}")

print("\nCKC mapping completed successfully.")