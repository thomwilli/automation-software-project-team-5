# rqi_generator.py
import os

import pandas as pd
from datetime import datetime

# Required RQI columns (confirm with team later)
RQI_COLUMNS = [
    "first_name",
    "last_name",
    "email",
    "course",
    "location",
    "payment_status",
    "date_registered"
]


def generate_rqi_csv(student_list):

    # Convert student list into DataFrame
    df = pd.DataFrame(student_list)

    # Ensure correct column order
    df = df[RQI_COLUMNS]

    # Create timestamp-based filename
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    filename = f"RQI_UPLOAD_{timestamp}.csv"

    # Save CSV locally
    df.to_csv(filename, index=False)

    print("✅ RQI file created:", filename)

    return filename
