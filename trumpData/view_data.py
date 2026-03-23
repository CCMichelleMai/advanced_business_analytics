import pandas as pd
import os

# File path
file_path = "realDonaldTrump_truths_2.json"

# Load JSON into DataFrame
df = pd.read_json(file_path, lines=True)

# Get file size in bytes
file_size_bytes = os.path.getsize(file_path)

# Convert to more readable units (MB)
file_size_mb = file_size_bytes / (1024 * 1024)

print("DataFrame loaded successfully!")
print(f"File size: {file_size_bytes} bytes ({file_size_mb:.2f} MB)")

# Preview DataFrame
print(df.head())

print(df.columns)
print(df.info())
print(df.iloc[0])