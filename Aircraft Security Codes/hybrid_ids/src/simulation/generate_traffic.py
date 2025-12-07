"""
src/simulation/generate_traffic.py

Utility for generating synthetic network and avionics traffic samples used to
feed into simulate_attacks.py or unit tests.
"""

import numpy as np
import random


def generate_unsw_features(normal=True):
    if normal:
        return np.array([
            random.randint(30, 60),  
            random.randint(30, 60),
            random.randint(0, 2),
            random.uniform(50, 300),
            random.uniform(0.1, 1.0)
        ])
    else:
        return np.array([
            random.randint(1, 255),
            random.randint(1, 255),
            random.randint(0, 7),
            random.uniform(500, 5000),
            random.uniform(5.0, 30.0)
        ])


def generate_adsb_injection(anomaly=True):
    if anomaly:
        return np.array([
            random.uniform(-30, -5), 
            random.uniform(-180, 180),
            random.uniform(2000, 45000),
            random.uniform(2000, 45000),
            random.uniform(-90, 90)
        ])
    else:
        return np.array([
            random.uniform(-90, -50),
            random.uniform(-180, 180),
            random.uniform(10000, 38000),
            random.uniform(10000, 38000),
            random.uniform(-90, 90)
        ])
