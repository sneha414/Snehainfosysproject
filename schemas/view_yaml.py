import yaml
from pprint import pprint

# Load YAML file
with open("anomaly_schema.yaml", "r") as file:
    data = yaml.safe_load(file)

print("\n=== ANOMALY RULES LOADED ===\n")

# Pretty display
for anomaly in data["anomalies"]:
    print("Name:", anomaly["name"])
    print("Description:", anomaly["description"])
    print("Severity:", anomaly["severity"])
    print("Action:", anomaly["action"])
    print("-" * 50)

print("\nAll rules loaded successfully!")
