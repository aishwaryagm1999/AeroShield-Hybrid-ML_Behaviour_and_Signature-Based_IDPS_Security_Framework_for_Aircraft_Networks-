
# Hybrid-IDS for Aviation Networks

This repository contains the reference implementation of a **Hybrid Intrusion Detection System (Hybrid-IDS)** for modern aircraft networks, as described in the accompanying manuscript.

The system combines:

- **Behaviour-based anomaly detection**
  - Random Forest (RF) for supervised intrusion detection  
  - Isolation Forest (IF) for novelty detection (ADS-C, ACARS, ARINC 429)
- **Signature-based malware detection**
  - YARA rules  
  - Import-hash (ImpHash) matching  
  - Inverted n-gram index for polymorphic / obfuscated binaries
- **Zero-Trust Architecture (ZTA)**
  - Segmented zones: Cockpit, Communications, Cabin Crew, Entertainment  
  - Policy Enforcement Points (PEPs) and a Trust Evaluation Engine (TEE)
- **Virtualized aircraft network testbed (conceptual)**
  - Scripts simulate reconnaissance, DoS, ADS-B/ADS-C anomalies, and malware infiltration

The code here is a **clean, self-contained reference implementation** aligned with the pipeline described in the paper (Experimentation & Results, Real-Time Simulation, ZTA, etc.).

---

## 1. Repository Layout

Suggested directory layout :

```text
.
├── README.md
├── requirements.txt
├── config/                 # (optional) YAML config files if you want them
│   ├── ids_config.yaml     # NOT provided here: you may define thresholds, paths, etc.
│   ├── datasets.yaml
│   └── logging.yaml
├── data/                   # You place the datasets here (see section 4)
│   ├── unsw-nb15/
│   ├── adsb_injection/
│   ├── milstd1553/
│   ├── adsc/
│   ├── acars/
│   ├── arinc429/
│   └── malware/
├── models/                 # RF/IF models + metrics (generated after training)
├── rules/
│   ├── yara/
│   │   ├── base_rules.yar          # your base YARA rules
│   │   └── generated_rules.yar     # auto-extended by yara_rule_update.py
│   └── metadata/
│       └── imphash_index.json      # imphash → malware family mappings
├── src/
│   ├── core/
│   │   ├── anomaly_detection.py
│   │   ├── feature_engineering.py
│   │   ├── malware_scanner.py
│   │   ├── model_utils.py
│   │   ├── metrics.py
│   ├── zta/
│   │   ├── alerting.py
│   │   ├── pep.py
│   │   ├── tee.py
│   │   └── zones.py
│   ├── simulation/
│   │   ├── generate_traffic.py
│   │   └── simulate_attacks.py
│   ├── training/
│   │   ├── cross_validation.py
│   │   ├── feature_importance.py
│   │   └── train_rf_if.py
│   └── maintenance/
│       ├── model_update_pipeline.py
│       ├── post_flight_learning.py
│       └── yara_rule_update.py
├── scripts/
│   ├── run_zone_ids.sh
│   ├── run_full_simulation.sh
│   └── retrain_models.sh







## Datasets and Sources

This repository does **not** redistribute third-party datasets.  
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
