import yaml

print("\n=== ANOMALY RULES LOADED ===\n")

# Open file with UTF-8 encoding (important on Windows)
with open("anomaly_schema.yaml", "r", encoding="utf-8") as file:
    data = yaml.safe_load(file)

# Access anomalies list
anomalies = data["anomalies"]

# Loop through each anomaly rule
for anomaly in anomalies:
    print("Name        :", anomaly["name"])
    print("Description :", anomaly["description"])
    print("Severity    :", anomaly["severity"])
    print("Action      :", anomaly["action"])
    print("-" * 60)

print("\nAll anomaly rules loaded successfully!\n")