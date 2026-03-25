# 🚦 Traffic Violations Insight System

An end-to-end data analytics project analyzing 2M+ traffic violation 
records from Montgomery County, Maryland (2012–2025).

## 🛠️ Tech Stack
- Python, Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- Streamlit
- SQLite / SQLAlchemy

## 📁 Project Structure
traffic_violations/
├── data/
│   ├── raw/              ← original dataset
│   └── cleaned/          ← cleaned dataset + charts
├── notebooks/
│   ├── 01_exploration.ipynb
│   ├── 02_eda.ipynb
│   └── 03_sql.ipynb
├── src/
│   ├── cleaning.py       ← data cleaning module
│   └── database.py       ← SQL integration
├── app/
│   └── streamlit_app.py  ← dashboard
├── requirements.txt
└── README.md

## ⚙️ Setup Instructions
1. Clone the repo
2. Create virtual environment:
   python -m venv venv
   venv\Scripts\activate
3. Install dependencies:
   pip install -r requirements.txt
4. Place raw CSV in data/raw/
5. Run cleaning pipeline in notebooks/01_exploration.ipynb
6. Launch dashboard:
   cd app
   streamlit run streamlit_app.py

## 📊 Key Insights
- 2,070,115 total violations across 13 years
- Peak violation hour: 22:00 (10 PM)
- Busiest day: Tuesday
- Most cited vehicle: Toyota
- Top district by accident rate: 4th District, Wheaton (3.73%)
- 56,683 violations involved accidents (2.74%)
- 568 fatal violations recorded