import pandas as pd
import os
import json

# Create Excel data
os.makedirs("data/knowledge_docs", exist_ok=True)
df = pd.DataFrame({"sales": [100, 120, 110, 130, 150, 90]}) # Last one is a drop
df.to_excel("data/sales.xlsx", index=False)

# Create a dummy text doc for RAG
with open("data/knowledge_docs/info.txt", "w") as f:
    f.write("Sales decline reasons include seasonality and supply chain delays.")

# Create empty memory file
os.makedirs("memory", exist_ok=True)
with open("memory/decisions.json", "w") as f:
    f.write("")

print("✅ Data initialized!")