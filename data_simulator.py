import numpy as np
import random

def generate_sensor_data():
    # 20% chance of anomaly
    if random.random() < 0.2:
        return {
            "pH": np.random.uniform(9.5, 11),     # extreme
            "TDS": np.random.randint(900, 1500),  # extreme
            "Turbidity": np.random.uniform(7, 12) # extreme
        }
    else:
        return {
            "pH": np.round(np.random.uniform(6.5, 8.5), 2),
            "TDS": np.random.randint(100, 500),
            "Turbidity": np.round(np.random.uniform(0.5, 4.5), 2)
        }