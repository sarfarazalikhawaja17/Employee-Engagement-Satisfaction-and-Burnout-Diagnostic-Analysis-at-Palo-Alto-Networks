<div align="center">

# Employee Engagement, Satisfaction & Burnout Diagnostic Analysis
### Palo Alto Networks | People Analytics & HR Analytics Project

*An early-warning system that detects burnout and disengagement before employees decide to leave.*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![pandas](https://img.shields.io/badge/pandas-150458?logo=pandas&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?logo=plotly&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-F37626?logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-Complete-4C9F70)

</div>

---

## Project Summary

Employee attrition is usually analysed **after** people leave. This project flips that: it builds **engagement and burnout diagnostics** from survey and workload data on **1,470 employees (31 features)** so HR can intervene early.

**What I built:**
- A standardized **Engagement Index** (0-100) from four survey ratings
- A rule-based **Burnout Risk Score** (Low / Medium / High)
- Five HR KPIs, statistical testing, and a **manager priority score**
- An interactive **Streamlit dashboard** with filters and a Manager Action Panel
- A research paper and executive summary with recommendations

---

## Key Findings

| # | Insight | Evidence |
|---|---------|----------|
| 1 | **Burnout is hidden from engagement surveys** | High-risk employees score as engaged as others, yet **33% left** vs **9%** of low-risk staff |
| 2 | **Overtime is the strongest warning sign** | **31%** attrition with overtime vs **10%** without |
| 3 | **Workload stress compounds** | Attrition rises from **4% to 42%** as overtime and frequent travel combine |
| 4 | **Early tenure and entry level carry the most risk** | About **30%** attrition in years 0-2; **26%** at Job Level 1 |
| 5 | **Engagement still matters** | Employees who left scored about **9 points lower** on the Engagement Index (p < 0.001) |
| 6 | **Stagnation is not linked to disengagement here** | 285 stagnant employees were no less engaged (p = 0.92) |

> **Business takeaway:** Track burnout flags (overtime, work-life balance) *next to* engagement scores. Engagement alone misses the highest-risk group.

---

## Methodology

| Step | What was done |
|------|---------------|
| **Data validation** | Checked missing values, duplicates, and valid 1-4 ordinal scales (data was clean) |
| **Engagement Index** | Z-score standardization of JobInvolvement, JobSatisfaction, EnvironmentSatisfaction and RelationshipSatisfaction, averaged and rescaled to 0-100 |
| **Burnout Risk** | Flags: OverTime = Yes and WorkLifeBalance <= 2. Zero flags = Low, one = Medium, two = High |
| **Workload analysis** | Engagement and attrition by overtime, business travel and commute distance |
| **Career-stage analysis** | Job level, tenure, time in role, and a stagnation test (4+ years in role and since promotion) |
| **Attrition context** | Stayed vs left comparison using the Mann-Whitney U test |
| **Manager priority score** | Combines burnout level, low engagement, frequent travel and early-career status |

### KPIs

| KPI | Definition |
|-----|------------|
| Engagement Index | Standardized composite of four ratings (0-100) |
| Burnout Risk Score | Overtime flag + low work-life-balance flag (0-2) |
| Work-Life Balance Index | Average work-life-balance rating (1-4) |
| Satisfaction Stability Score | Consistency of the four satisfaction ratings (0-100) |
| Workload Stress Indicator | Travel frequency (0-2) + overtime (0-1) |

---

## Streamlit Dashboard

Four interactive modules with filters for department, job role, overtime, engagement threshold and tenure range:

1. **Engagement Health Overview:** organization-wide score and satisfaction distributions
2. **Burnout Risk Dashboard:** high-risk segments, overtime and work-life imbalance views
3. **Role & Career Stage Analysis:** engagement and attrition by role, level and tenure
4. **Manager Action Panel:** low-engagement alerts, priority intervention areas, downloadable priority list

<!-- Add a screenshot: save it as assets/dashboard.png, then uncomment the next line -->
<!-- ![Dashboard preview](assets/dashboard.png) -->

---

## Tech Stack

**Languages & Libraries:** Python, pandas, NumPy, SciPy, Matplotlib, seaborn, Plotly
**App & Tools:** Streamlit, Jupyter Notebook, Git, GitHub
**Skills demonstrated:** HR analytics, people analytics, exploratory data analysis (EDA), feature engineering, KPI design, statistical hypothesis testing, data visualization, dashboard development, business storytelling

---

## Repository Structure

```
├── Palo_Alto_Engagement_Burnout_Analysis.ipynb   # Full analysis notebook
├── app.py                                        # Streamlit dashboard
├── Palo_Alto_Networks.csv                        # Dataset (1,470 employees)
├── Palo_Alto_Engagement_Research_Paper.docx      # Research paper: EDA, insights, recommendations
├── Palo_Alto_Executive_Summary.docx              # One-page executive summary
├── requirements.txt                              # Python dependencies
└── README.md
```

---

## Run It Locally

```bash
# 1. Clone the repository
git clone https://github.com/sarfarazalikhawaja17/Employee-Engagement-Satisfaction-and-Burnout-Diagnostic-Analysis-at-Palo-Alto-Networks.git
cd Employee-Engagement-Satisfaction-and-Burnout-Diagnostic-Analysis-at-Palo-Alto-Networks

# 2. (Optional) create a virtual environment
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Launch the dashboard
streamlit run app.py

# 5. Or open the notebook
jupyter notebook Palo_Alto_Engagement_Burnout_Analysis.ipynb
```

---

## Recommendations for HR

1. **Cap and monitor overtime;** flag teams where it is routine.
2. **Report burnout flags beside engagement scores** in HR dashboards.
3. **Protect the first two years** with onboarding check-ins, mentoring and growth plans.
4. **Run role-specific workload reviews** for Sales Representatives, Laboratory Technicians and HR.
5. **Rotate frequent travellers** and limit consecutive travel weeks.
6. **Review the Manager Action Panel monthly.**

---

## Limitations

- Single-snapshot data: findings are **associations, not proven causes**.
- The four engagement ratings are only weakly correlated, so the index is a broad summary.
- The burnout rule is a simple screen defined in the project brief.
- The manager priority score was designed using patterns in this dataset, so its performance is optimistic and should be validated on new data.

---

## About the Author

**Sarfaraz Ali** | Junior Machine Learning Engineer | B.Tech Computer Science (AI/ML), 2025

Seeking full-time Machine Learning Engineer roles and open to relocation.

- GitHub: [@sarfarazalikhawaja17](https://github.com/sarfarazalikhawaja17)
- LinkedIn: *add your profile link here*
- Email: *add your email here*

*Built as part of the Unified Mentor internship program.*
