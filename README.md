# 🚦 Traffic Violations Insight System

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?style=for-the-badge&logo=python)
![Pandas](https://img.shields.io/badge/Pandas-2.0-green?style=for-the-badge&logo=pandas)
![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?style=for-the-badge&logo=streamlit)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?style=for-the-badge&logo=sqlite)
![Plotly](https://img.shields.io/badge/Plotly-5.x-purple?style=for-the-badge&logo=plotly)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**An end-to-end data analytics system that transforms 2M+ raw traffic violation records into actionable insights through EDA, data cleaning, SQL integration, and an interactive Streamlit dashboard.**

[📊 View Dashboard](#-streamlit-dashboard) • [🚀 Quick Start](#-quick-start) • [📁 Project Structure](#-project-structure) • [💡 Key Insights](#-key-insights) • [🚧 Challenges](#-challenges--solutions)

</div>

---

## 📌 Project Overview

Urban safety agencies generate millions of traffic-violation records each year. This project builds a **complete data analytics pipeline** for Montgomery County, Maryland traffic violation data (2012–2025), covering:

- 🧹 **Data Cleaning & Preprocessing** — handling 2M+ messy records
- 📊 **Exploratory Data Analysis** — uncovering patterns and trends
- 🗄️ **SQL Integration** — structured querying with SQLite
- 🖥️ **Interactive Dashboard** — built with Streamlit + Plotly

| Field | Details |
|---|---|
| **Domain** | Transportation / Urban Safety |
| **Dataset** | Montgomery County Traffic Violations |
| **Records** | 2,070,115 rows × 43 columns |
| **Date Range** | January 2012 – December 2025 |
| **Tools** | Python, Pandas, Plotly, Streamlit, SQLite |

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Language** | Python 3.11 |
| **Data Processing** | Pandas, NumPy |
| **Visualization** | Matplotlib, Seaborn, Plotly |
| **Dashboard** | Streamlit |
| **Database** | SQLite3, SQLAlchemy |
| **Version Control** | Git, GitHub, Git LFS |
| **IDE** | VS Code + Jupyter Notebooks |

---

## 📁 Project Structure

```
traffic_violations/
│
├── 📂 data/
│   ├── raw/                        ← Original dataset (via Git LFS)
│   │   └── Traffic_Violations.csv
│   └── cleaned/                    ← Cleaned output (via Git LFS)
│       ├── traffic_clean.csv
│       ├── chart_violation_categories.png
│       ├── chart_hourly.png
│       ├── chart_daily.png
│       ├── chart_tod_gender.png
│       ├── chart_makes.png
│       └── chart_accidents.png
│
├── 📂 notebooks/
│   ├── 01_exploration.ipynb        ← Initial data exploration
│   ├── 02_eda.ipynb                ← EDA charts & insights
│   └── 03_sql.ipynb               ← SQL queries & analysis
│
├── 📂 src/
│   ├── cleaning.py                 ← Data cleaning module
│   └── database.py                 ← SQL integration module
│
├── 📂 app/
│   └── streamlit_app.py            ← Interactive dashboard
│
├── requirements.txt                ← Python dependencies
├── README.md                       ← Project documentation
└── .gitignore
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Git + Git LFS
- VS Code (recommended)

### Installation

**1. Clone the repository**
```bash
git clone https://github.com/dhanasekaranmariappan/traffic-violations-insight-system.git
cd traffic-violations-insight-system
```

**2. Pull large files via Git LFS**
```bash
git lfs pull
```

**3. Create and activate virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

**4. Install dependencies**
```bash
pip install -r requirements.txt
```

**5. Run the cleaning pipeline**

Open `notebooks/exploration.ipynb` and run all cells, then open `notebooks/visualization.ipynb`.

**6. Load data into SQLite**

Open `notebooks/dbcheck.ipynb` and run all cells.

**7. Launch the dashboard**
```bash
cd app
streamlit run traffic_violation_insight.py
```

Open your browser at `http://localhost:8501` 🎉

---

## 📊 Streamlit Dashboard

The interactive dashboard has **3 tabs**:

### 📈 Charts & Insights Tab
- KPI cards — Total violations, Accidents, Fatal, Alcohol, HAZMAT
- Violations by Category (horizontal bar)
- Violations by Hour of Day (area chart)
- Violations by Day of Week (bar chart)
- Time of Day breakdown (donut chart)
- Top 10 Vehicle Makes (horizontal bar)
- Monthly Violation Trend (line chart)
- Demographics — Race & Gender (bar + donut)

### 🗺️ Geographic Map Tab
- Toggle between **Density Heatmap** and **Scatter Points**
- 1.9M+ incidents plotted on real map
- Montgomery County, MD hotspot clearly visible

### 🗄️ Raw Data Tab
- Search by description or location
- Sortable, scrollable data table
- **Download filtered data as CSV**

### 🔍 Sidebar Filters
All charts update dynamically when you filter by:
- 📅 Date Range
- 👤 Gender
- 🚦 Violation Category
- 🚗 Vehicle Make
- 🏢 District
- 📋 Violation Type

---

## 🧹 Data Cleaning Summary

| Step | Action | Details |
|---|---|---|
| 1 | Load data | 2,070,115 rows × 43 columns |
| 2 | Fix datetime | Converted `Date Of Stop` & `Time Of Stop` to proper formats |
| 3 | Fix booleans | Standardized Yes/No → True/False for 12 columns |
| 4 | Fix coordinates | Replaced 0 with NaN, validated US ranges (lat 24–50, lon -65 to -125) |
| 5 | Fix categoricals | Standardized Gender, Race, State, Agency, Violation Type |
| 6 | Fix vehicles | Expanded abbreviations (CHEV→CHEVROLET, BLK→BLACK) |
| 7 | Fix years | Removed impossible values outside 1960–2025 |
| 8 | Engineer features | Added Hour, Month, DayOfWeek, TimeOfDay, ViolationCategory, SeverityScore |
| **Result** | **50 columns** | **43 original + 7 new engineered features** |

---

## 📊 Exploratory Data Analysis

### Key Questions Answered

| Question | Finding |
|---|---|
| Most common violation? | Speeding (17.4%) → 360,764 cases |
| Peak violation hour? | 22:00 (10 PM) → 156,808 violations |
| Busiest day? | Tuesday → 365,668 violations |
| Most cited vehicle? | Toyota → 358,506 violations |
| Most dangerous district? | 4th District, Wheaton → 3.73% accident rate |
| Night vs Day? | Night = 36.7% of all violations |
| Gender split? | Male = 67.4% (1.39M) vs Female = 32.5% (672K) |

---

## 🗄️ SQL Analysis

Structured queries answering business questions:

```sql
-- Top violation types with percentage
SELECT ViolationCategory,
       COUNT(*) as total,
       ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM violations), 2) as pct
FROM violations
GROUP BY ViolationCategory
ORDER BY total DESC;
```

| Query | Purpose |
|---|---|
| Query 1 | Top violation types with percentage breakdown |
| Query 2 | Districts ranked by accident rate |
| Query 3 | Repeat offenders (SeqID with 3+ charges) |
| Query 4 | Vehicle makes with highest accident rates |
| Query 5 | Summary statistics (fatal, alcohol, HAZMAT) |

---

## 💡 Key Insights

```
📊 DATASET SUMMARY
══════════════════════════════════════════════
  Total violations        :  2,070,115
  Violations w/ accidents :     56,683  (2.74%)
  Fatal violations        :        568
  Alcohol-related         :      2,622
  HAZMAT involved         :        153
  Date range              :  2012 → 2025
══════════════════════════════════════════════

⏰ TIME PATTERNS
  Peak hour    →  22:00 (10 PM)
  Busiest day  →  Tuesday
  Night stops  →  36.7% of all violations

🚗 VEHICLE INSIGHTS
  #1 Make  →  Toyota  (358,506 stops)
  #2 Make  →  Honda   (307,693 stops)
  #3 Make  →  Ford    (187,749 stops)

🏢 DISTRICT INSIGHTS
  Highest accident rate  →  4th District, Wheaton  (3.73%)
  Most active district   →  4th District, Wheaton  (449,193 stops)
```

---

## 🚧 Challenges & Solutions

| # | Challenge | Cause | Solution |
|---|---|---|---|
| 1 | `jupyter notebook` not recognized | Not installed globally | Used VS Code built-in Jupyter extension |
| 2 | `KeyError: 'Date of Stop'` | Column name case mismatch | Used flexible column finder with `.str.title()` |
| 3 | Old module kept running after edits | Python module caching | Used `importlib.reload()` + cleared `sys.modules` |
| 4 | `OperationalError: near "EXIST"` | Typo in SQL keyword | Fixed to `IF NOT EXISTS` |
| 5 | `no such table: main.violations` | different DB filenames | Standardized `DB_PATH` as single constant |
| 6 | Sidebar values invisible | CSS `color:white` overrode input text | Targeted only label/span tags specifically |
| 7 | `GH001: Large files rejected` | Files exceed GitHub 100MB limit | Used Git LFS for large data files |

---

## 💡 Lessons Learned

1. **Always inspect exact column names** before writing cleaning code
2. **Module caching in Jupyter** — always reload after editing `.py` files
3. **Define file paths as constants** — prevents subtle bugs across functions
4. **SQL syntax is strict** — one missing letter breaks everything
5. **CSS in Streamlit** needs careful targeting to avoid overriding inputs
6. **Never commit large files to Git** — use LFS, Google Drive, or Kaggle
7. **`@st.cache_data`** is essential for performance with large datasets

---

## 📦 Requirements

```
pandas
numpy
matplotlib
seaborn
plotly
streamlit
folium
streamlit-folium
sqlalchemy
openpyxl
ipykernel
jupyter
```

Install all with:
```bash
pip install -r requirements.txt
```

---

## 👤 Author

**Dhanasekaran Mariappan**
- GitHub: [@dhanasekaranmariappan](https://github.com/dhanasekaranmariappan)
- Project: [traffic-violations-insight-system](https://github.com/dhanasekaranmariappan/traffic-violations-insight-system)

---

## 📄 License

This project is licensed under the MIT License.

---

<div align="center">
  <em>Python • Pandas • Plotly • Streamlit • SQLite</em>
</div>