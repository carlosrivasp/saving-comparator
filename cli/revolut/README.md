# 📊 CLI Tools — Saving Comparator

This folder contains **command-line Python scripts** for comparing remunerated bank accounts available for contracting in Spain.

Each subfolder is dedicated to a specific bank or financial product, containing its own comparator script.

## 📂 Structure

cli/
├── revolut/
│ └── revolut_comparator.py
├── tbd-comparator/
|    └── tbd_plans.py

## 📌 How to use

1. Install dependencies (if needed):
   ```bash
   pip install -r ../requirements.txt

2. Run any script from its folder:
    ```bash
    python revolut/revolut_comparator.py

The scripts run via terminal input and generate comparative charts using Matplotlib.

## 📃 Notes
These tools are intended for use in command-line interfaces (CLI) like VS Code terminal, PowerShell, or any Python environment.

No web interface or Streamlit app is included here — see the /web folder for that.