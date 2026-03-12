# ✈️ AeroShield-Hybrid-ML_Behaviour_and_Signature-Based_IDPS_Security_Framework_for_Aircraft_Networks

### Reinforcing Aircraft Network Security using Machine Learning, YARA Rules, and Zero Trust Architecture

---

## 📌 Overview

Modern aircraft rely on highly interconnected digital communication systems to manage avionics, navigation, maintenance, and passenger services. While these networks increase operational efficiency, they also introduce cybersecurity risks.

This project implements a **Hybrid Intrusion Detection and Prevention System (Hybrid-IDPS)** designed to detect cyber threats in aircraft communication networks using a combination of:

- Machine Learning-based anomaly detection
- Signature-based malware detection
- Aviation protocol traffic analysis
- Zero Trust network architecture

The framework integrates **Random Forest and Isolation Forest models** with **YARA-based malware detection** and **zone-based security enforcement** to detect both known and unknown threats within simulated aircraft network environments.

The system simulates realistic aviation network traffic and cyber attacks through a **cyber-range simulation environment**, enabling evaluation of security defenses without requiring access to real aircraft systems.

---

## 🎯 Problem Statement

Aircraft communication networks such as:

- **ACARS (Aircraft Communications Addressing and Reporting System)**
- **ADS-B (Automatic Dependent Surveillance – Broadcast)**
- **ADS-C**
- **MIL-STD-1553 avionics bus**
- **ARINC 429 communication bus**

were originally designed without strong cybersecurity mechanisms.

This makes them vulnerable to attacks such as:

- Aircraft spoofing
- Message tampering
- Command injection
- Malware infiltration
- Denial-of-Service attacks
- Unauthorized network access

Traditional rule-based intrusion detection systems struggle to detect **zero-day attacks** and **unknown anomalies**.

This project proposes a **hybrid detection architecture** combining:

- Machine learning anomaly detection
- Malware signature scanning
- Network segmentation using Zero Trust principles

to improve aircraft cybersecurity resilience.

---

## 🏗️ System Architecture

The system is built as a **multi-layer hybrid cybersecurity architecture**.

Aircraft Network Traffic Generator
↓
Attack Simulation Engine
↓
Feature Engineering Pipeline
↓
Machine Learning Anomaly Detection
↓
Malware Detection Engine
(YARA + Import Hash)
↓
Zone Intrusion Detection Sensors
↓
Trust Evaluation Engine (TEE)
↓
Policy Enforcement Point (PEP)
↓
Security Response
(Alert / Block / Throttle)


This layered approach enables detection of both **behavioral anomalies** and **known malware signatures**.

---

## ✈️ Aircraft Network Zones

The system models aircraft communication architecture using logical zones.

| Zone | Description |
|-----|-------------|
| Cockpit | Critical avionics and flight control systems |
| Communications | Aircraft-ground communication links |
| Cabin Crew | Crew operational systems |
| In-Flight Entertainment | Passenger internet and entertainment networks |
| Maintenance | Diagnostic and software update systems |

Each zone is monitored by a **local intrusion detection sensor**, while a centralized **Trust Evaluation Engine** evaluates alerts and enforces security policies.

---

## 🧠 Machine Learning Methodology

The anomaly detection system uses two complementary machine learning models.

| Model | Purpose |
|------|--------|
| Random Forest | Supervised anomaly classification |
| Isolation Forest | Unsupervised anomaly detection |

### Why Hybrid Models?

- **Random Forest** detects known attack patterns using labeled data.
- **Isolation Forest** detects unknown anomalies by identifying abnormal data distributions.

Combining both models improves detection of both **known and novel cyber attacks**.

---

## 🦠 Malware Detection Engine

The malware detection subsystem integrates multiple detection techniques.

### 1️⃣ YARA Rule Scanning

YARA rules detect malware using pattern-matching signatures.

This allows detection of known malware families such as:

- Trojans
- Ransomware
- Spyware
- Botnets

---

### 2️⃣ Import Hash Detection

Executable files are analyzed using **PE import hashing (ImpHash)** to identify known malware families.

Library used:
pefile


---

### 3️⃣ N-Gram Rule Indexing

To improve scanning performance, an **n-gram index** is used to filter candidate rules before running full YARA scans.

This significantly reduces malware detection latency.

---

## 🔬 Feature Engineering

Feature engineering extracts statistical and behavioral indicators from aviation network traffic.

Examples of extracted features include:

- altitude change rate
- route deviation distance
- communication frequency
- packet inter-arrival time
- telemetry value fluctuations
- avionics bus waveform characteristics

Feature selection is performed using:
ExtraTreeClassifiers


Class imbalance is handled using:
SMOTE (Synthetic Minority Over-sampling Technique)


---

## 📂 Datasets Used

The framework utilizes multiple aviation-related datasets and simulated attack data.

| Dataset | Description |
|------|-------------|
| UNSW-NB15 | General network intrusion dataset |
| ADS-B Injection Dataset | Simulated aircraft spoofing attacks |
| MIL-STD-1553 Dataset | Avionics bus communication logs |
| ADS-C Dataset | Aircraft-ground communication data |
| ACARS Dataset | Aircraft messaging protocol traffic |
| ARINC 429 Dataset | Aircraft data bus communication |
| MalwareBazaar / VirusShare | Malware samples for signature detection |

Due to use of 3rd Party Resources, Datasets are not included in the repository.

Download them from the original publishers and place them under `data/`:

### UNSW-NB15 (Network baseline)

- Moustafa & Slay, *UNSW-NB15: a comprehensive data set for network intrusion detection systems*, MilCIS 2015.  
- Dataset: https://research.unsw.edu.au/projects/unsw-nb15-dataset  
- Mirror:  https://www.kaggle.com/datasets/mrwellsdavid/unsw-nb15  
- Place processed CSV as: `data/unsw-nb15/unsw_processed.csv`.

### ADS-B Message Injection Attacks

- Ould Slimane et al., *ADS-B message injection attacks dataset*, Mendeley Data v1 (2022).  
- DOI: https://doi.org/10.17632/6fhw732ccz.1  
- Place processed CSV as: `data/adsb_injection/adsb_injection_processed.csv`.

### ISOT MIL-STD-1553 Dataset

- Ahmed et al., *A Collection of Datasets for Intrusion Detection in MIL-STD-1553 Platforms*, Springer (2022).  
- Info: https://www.uvic.ca/ecs/ece/isot/datasets/index.php  
- Place processed CSV as: `data/milstd1553/milstd1553_processed.csv`.

### ADS-C (Automatic Dependent Surveillance–Contract)

- Xapelli, Strohmeier, Lüscher, *ADS-C Air Traffic Data Collected by the OpenSky Network*, Zenodo (2023).  
- DOI: https://doi.org/10.5281/zenodo.10041840  
- After parsing, save features as: `data/adsc/adsc_features.csv`.

### ACARS / STORMFEST

- Klein et al., *STORMFEST: Aviation Communication and Meteorological Dataset for ACARS-based Flight Event Analysis*, Zenodo (2024).  
- DOI: https://doi.org/10.5281/zenodo.11149086  
- After preprocessing into 5-sample windows, save as: `data/acars/acars_features.csv`.

### ARINC 429 Oscilloscope Waveforms

- Strohmeier & Lüscher, *ARINC 429 Oscilloscope Waveform Dataset from Hardware-in-the-Loop Avionics Simulator*, Zenodo (2023).  
- DOI: https://doi.org/10.5281/zenodo.7964088  
- Convert waveforms into word-level features and save as: `data/arinc429/arinc429_waveform_features.csv`.

### Malware Corpus

- MalwareBazaar (abuse.ch): https://bazaar.abuse.ch  
- VirusShare: https://virusshare.com  

Store samples in `data/malware/`.  
**Warning:** These contain live malware; only handle in isolated lab environments.

---

## 📁 Project Structure
Reinforcing-Aircraft-Network-Security-main/
│
└── Aircraft Security Codes/
│
└── hybrid_ids/
│
├── readme.txt
├── requirements.txt
│
├── scripts/
│ ├── retrain_models.sh
│ ├── run_full_simulation.sh
│ └── run_zone_ids.sh
│
└── src/
│
├── core/
│ ├── anomaly_detection.py
│ ├── feature_engineering.py
│ ├── malware_scanner.py
│ ├── metrics.py
│ └── model_utils.py
│
├── maintenance/
│ ├── model_update_pipelines.py
│ ├── post_flight_learning.py
│ └── yara_rule_update.py
│
├── simulation/
│ ├── generate_traffic.py
│ └── simulate.attacks.py
│
├── training/
│ ├── cross_validation.py
│ ├── feature_importance.py
│ └── train_rf_if.py
│
└── zta/
├── alerting.py
├── pep.py
├── tee.py
└── zones.py


---

## 📜 Description of Key Modules

### Core Modules

**anomaly_detection.py**

Implements anomaly detection using Random Forest and Isolation Forest models.

**feature_engineering.py**

Processes raw aviation network traffic and extracts features used for machine learning models.

**malware_scanner.py**

Implements malware detection using YARA rules and PE import hashing.

**metrics.py**

Provides evaluation metrics such as:

- accuracy
- confusion matrix
- ROC curves

**model_utils.py**

Handles model saving, loading, and artifact management.

---

### Maintenance Modules

**model_update_pipelines.py**

Automates model retraining using updated datasets.

**post_flight_learning.py**

Implements continuous learning by incorporating new data from detected anomalies.

**yara_rule_update.py**

Updates malware detection rules dynamically.

---

### Simulation Modules

**generate_traffic.py**

Generates simulated aircraft network traffic.

**simulate.attacks.py**

Injects cyber attack scenarios into simulated traffic streams.

Examples include:

- spoofed aircraft messages
- telemetry manipulation
- malicious command injection

---

### Training Modules

**train_rf_if.py**

Trains the Random Forest and Isolation Forest models.

**cross_validation.py**

Performs k-fold cross validation to evaluate model robustness.

**feature_importance.py**

Computes feature importance scores for model interpretability.

---

### Zero Trust Architecture Modules

**zones.py**

Defines aircraft network segmentation.

**alerting.py**

Generates alerts when anomalies are detected.

**pep.py**

Implements Policy Enforcement Points to block or throttle suspicious traffic.

**tee.py**

Implements the Trust Evaluation Engine which aggregates alerts and determines appropriate responses.

---

## 🛠️ Requirements

### Tested Environment

- Python 3.8+
- Windows / Linux / macOS

---

### Install Dependencies
pip install -r requirements.txt


Key libraries used include:

- scikit-learn
- pandas
- numpy
- joblib
- pefile
- yara-python
- matplotlib

---

## 🔧 Train Models
python src/training/train_rf_if.py


This script performs:

- dataset loading
- feature extraction
- SMOTE balancing
- model training
- performance evaluation
- artifact storage

---

## ▶️ Run Full Simulation
bash scripts/run_full_simulation.sh


Pipeline:

1. Train models
2. Generate aviation traffic
3. Simulate attacks
4. Run intrusion detection
5. Generate alerts

---

## 🔁 Retrain Models
bash scripts/retrain_models.sh


Used to retrain models with updated datasets.

---

## 📊 Experimental Results

| Metric | Value |
|------|------|
| Random Forest Accuracy | ~97% |
| Isolation Forest Detection Rate | ~95% |
| Malware Detection Accuracy | ~94% |
| False Positive Rate | <3% |

The system successfully detects:

- spoofed aircraft broadcasts
- abnormal telemetry patterns
- command injection attacks
- malware infiltration attempts

---

## 🔐 Security Response Actions

Detected threats trigger automated responses through the **Policy Enforcement Point (PEP)**.

Examples include:

- blocking suspicious traffic
- throttling abnormal communication flows
- isolating compromised network zones
- generating security alerts

---

## 🔄 Continuous Learning

The system supports adaptive defense using **post-flight learning**.

Workflow:
Detected Alerts
↓
Analyst Validation
↓
Dataset Augmentation
↓
Model Retraining
↓
Improved Detection Accuracy



---

## 🎓 Skills Demonstrated

- Machine Learning for Cybersecurity
- Aviation Network Security
- Intrusion Detection Systems
- Malware Analysis
- Cyber Range Simulation
- Zero Trust Architecture
- Network Traffic Analysis
- Security Automation

---

## 👩‍💻 Author

Developed as a research-driven framework for **reinforcing aircraft network cybersecurity** using hybrid intrusion detection, malware analysis, and zero trust network segmentation.


