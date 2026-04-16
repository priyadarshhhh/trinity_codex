def check_anomaly(ph, tds, turb):
    return {
        "ph": ph < 6.5 or ph > 8.5,
        "tds": tds > 500,
        "turb": turb > 5
    }

def calculate_risk(ph, tds, turb):
    return (
        abs(ph - 7) * 10 +
        (tds / 500) * 20 +
        (turb / 5) * 30
    )

def classify_contamination(ph, tds, turb, chlorine=1):
    if tds > 500:
        return "Chemical", 0.9
    elif turb > 5:
        return "Physical", 0.85
    elif chlorine < 0.5 and turb > 3:
        return "Biological", 0.8
    else:
        return "Safe", 0.95