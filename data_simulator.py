import numpy as np
import pandas as pd

def generate_sensor_data():
    return {
        "pH": np.round(np.random.uniform(6.0, 9.5), 2),
        "TDS": np.random.randint(100, 800),
        "Turbidity": np.round(np.random.uniform(0.5, 8.0), 2)
    }

def update_buffer(df):
    new_data = generate_sensor_data()
    df = pd.concat([df, pd.DataFrame([new_data])]).tail(50)
    return df