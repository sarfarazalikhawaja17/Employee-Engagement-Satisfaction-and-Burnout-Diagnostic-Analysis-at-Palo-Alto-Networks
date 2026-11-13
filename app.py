import pandas as pd, numpy as np
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Palo Alto Networks | Engagement & Burnout", page_icon="🛡️", layout="wide")

# ---------- Data + feature engineering (same logic as the notebook) ----------
@st.cache_data
def load():
    df = pd.read_csv("Palo Alto Networks.csv")
    eng = ["JobInvolvement", "JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction"]
    z = (df[eng] - df[eng].mean()) / df[eng].std()
    s = z.mean(axis=1)
    df["EngagementIndex"] = 100 * (s - s.min()) / (s.max() - s.min())
    q1, q3 = df.EngagementIndex.quantile([0.25, 0.75])
    df["EngagementBand"] = pd.cut(df.EngagementIndex, [-1, q1, q3, 101], labels=["Low", "Medium", "High"])
    df["OverTimeFlag"] = (df.OverTime == "Yes").astype(int)
    df["LowWLBFlag"] = (df.WorkLifeBalance <= 2).astype(int)
    df["BurnoutRiskScore"] = df.OverTimeFlag + df.LowWLBFlag
    df["BurnoutRisk"] = pd.Categorical(df.BurnoutRiskScore.map({0: "Low", 1: "Medium", 2: "High"}),
                                       ["Low", "Medium", "High"], ordered=True)
    df["SatisfactionStability"] = (100 * (1 - df[eng].std(axis=1) / 1.5)).clip(0, 100)
    df["WorkloadStress"] = df.BusinessTravel.map({"Non-Travel": 0, "Travel_Rarely": 1, "Travel_Frequently": 2}) + df.OverTimeFlag
    df["Commute"] = pd.cut(df.DistanceFromHome, [0, 5, 15, 30], labels=["Short (1-5)", "Medium (6-15)", "Long (16-29)"])
    df["TenureBand"] = pd.cut(df.YearsAtCompany, [-1, 2, 5, 10, 40], labels=["0-2", "3-5", "6-10", "10+"])
    df["PriorityScore"] = (2 * (df.BurnoutRisk == "High") + 1 * (df.BurnoutRisk == "Medium") + 1 * (df.EngagementBand == "Low")
                           + 1 * (df.BusinessTravel == "Travel_Frequently")
                           + 1 * ((df.JobLevel == 1) & (df.YearsAtCompany <= 2))).astype(int)
    return df

df = load()
COLORS = {"Low": "#4C9F70", "Medium": "#F2A541", "High": "#D64545"}

# ---------- Sidebar filters ----------
st.sidebar.title("Filters")
depts = st.sidebar.multiselect("Department", sorted(df.Department.unique()), default=sorted(df.Department.unique()))
roles_avail = sorted(df[df.Department.isin(depts)].JobRole.unique())
roles = st.sidebar.multiselect("Job role", roles_avail, default=roles_avail)
ot = st.sidebar.radio("Overtime", ["All", "Yes only", "No only"], horizontal=True)
thr = st.sidebar.slider("Low-engagement threshold (index)", 0, 100, 40,
                        help="Employees below this Engagement Index appear as low-engagement alerts.")
ten = st.sidebar.slider("Tenure (years at company)", 0, int(df.YearsAtCompany.max()), (0, int(df.YearsAtCompany.max())))

f = df[df.Department.isin(depts) & df.JobRole.isin(roles) & df.YearsAtCompany.between(*ten)]
if ot == "Yes only": f = f[f.OverTime == "Yes"]
if ot == "No only": f = f[f.OverTime == "No"]

st.title("🛡️ Employee Engagement & Burnout Diagnostic")
st.caption("Palo Alto Networks | early-warning HR analytics (Unified Mentor project)")
if f.empty:
    st.warning("No employees match these filters. Widen the filters in the sidebar."); st.stop()

tab1, tab2, tab3, tab4 = st.tabs(["Engagement Health", "Burnout Risk", "Role & Career Stage", "Manager Action Panel"])

# ---------- Tab 1 ----------
with tab1:
    c = st.columns(5)
    c[0].metric("Employees", f"{len(f):,}")
    c[1].metric("Engagement Index", f"{f.EngagementIndex.mean():.1f}")
    c[2].metric("Work-Life Balance (1-4)", f"{f.WorkLifeBalance.mean():.2f}")
    c[3].metric("Satisfaction Stability", f"{f.SatisfactionStability.mean():.1f}")
    c[4].metric("Attrition (context)", f"{f.Attrition.mean():.1%}")
    a, b = st.columns(2)
    a.plotly_chart(px.histogram(f, x="EngagementIndex", nbins=25, title="Engagement Index distribution",
                                color_discrete_sequence=["#2F6DB5"]), width="stretch")
    long = f.melt(value_vars=["JobInvolvement", "JobSatisfaction", "EnvironmentSatisfaction", "RelationshipSatisfaction", "WorkLifeBalance"],
                  var_name="Dimension", value_name="Rating")
    dist = long.groupby(["Dimension", "Rating"]).size().reset_index(name="n")
    dist["%"] = dist.n / dist.groupby("Dimension").n.transform("sum") * 100
    b.plotly_chart(px.bar(dist, x="Dimension", y="%", color=dist.Rating.astype(str), title="Satisfaction rating distribution (1 = low, 4 = high)",
                          barmode="stack"), width="stretch")
    st.markdown("**Stayed vs left (context only):**")
    cmp = f.groupby("Attrition").EngagementIndex.mean().rename({0: "Stayed", 1: "Left"}).round(1)
    st.dataframe(cmp.to_frame("Avg Engagement Index"), width=300)

# ---------- Tab 2 ----------
with tab2:
    s = f.groupby("BurnoutRisk", observed=True).agg(Employees=("Age", "size"), Engagement=("EngagementIndex", "mean"),
                                                    Attrition=("Attrition", "mean")).reset_index()
    c = st.columns(3)
    c[0].metric("High burnout risk", f"{(f.BurnoutRisk == 'High').mean():.1%}")
    c[1].metric("Avg Workload Stress (0-3)", f"{f.WorkloadStress.mean():.2f}")
    c[2].metric("Avg Burnout Score (0-2)", f"{f.BurnoutRiskScore.mean():.2f}")
    a, b = st.columns(2)
    a.plotly_chart(px.bar(s, x="BurnoutRisk", y="Employees", color="BurnoutRisk", color_discrete_map=COLORS,
                          title="Employees by burnout risk"), width="stretch")
    b.plotly_chart(px.bar(s, x="BurnoutRisk", y="Attrition", color="BurnoutRisk", color_discrete_map=COLORS,
                          title="Attrition rate by burnout risk", labels={"Attrition": "Attrition rate"}).update_yaxes(tickformat=".0%"),
                   width="stretch")
    heat = f.pivot_table(index="WorkLifeBalance", columns="OverTime", values="Attrition", aggfunc="mean")
    cnt = f.pivot_table(index="WorkLifeBalance", columns="OverTime", values="Attrition", aggfunc="size")
    a, b = st.columns(2)
    a.plotly_chart(px.imshow(heat, text_auto=".0%", color_continuous_scale="Reds", aspect="auto",
                             title="Attrition: work-life balance x overtime"), width="stretch")
    wl = f.groupby(["BusinessTravel", "OverTime"]).Attrition.mean().reset_index()
    b.plotly_chart(px.bar(wl, x="BusinessTravel", y="Attrition", color="OverTime", barmode="group",
                          title="Attrition: travel x overtime").update_yaxes(tickformat=".0%"), width="stretch")
    st.info("Note: high-risk staff are not less engaged than others, so burnout stays invisible in engagement scores alone.")

# ---------- Tab 3 ----------
with tab3:
    r = f.groupby("JobRole").agg(Employees=("Age", "size"), Engagement=("EngagementIndex", "mean"), Attrition=("Attrition", "mean")).reset_index().sort_values("Engagement")
    a, b = st.columns(2)
    a.plotly_chart(px.bar(r, x="Engagement", y="JobRole", orientation="h", title="Engagement by job role", color_discrete_sequence=["#2F6DB5"]), width="stretch")
    lv = f.groupby("JobLevel").agg(Engagement=("EngagementIndex", "mean"), Attrition=("Attrition", "mean")).reset_index()
    b.plotly_chart(px.bar(lv, x="JobLevel", y="Attrition", title="Attrition by job level", color_discrete_sequence=["#D64545"]).update_yaxes(tickformat=".0%"), width="stretch")
    tn = f.groupby("TenureBand", observed=True).agg(Engagement=("EngagementIndex", "mean"), Attrition=("Attrition", "mean")).reset_index()
    a, b = st.columns(2)
    a.plotly_chart(px.line(tn, x="TenureBand", y="Engagement", markers=True, title="Tenure vs engagement").update_yaxes(range=[40, 65]), width="stretch")
    b.plotly_chart(px.line(tn, x="TenureBand", y="Attrition", markers=True, title="Tenure vs attrition").update_yaxes(tickformat=".0%"), width="stretch")
    stag = f[(f.YearsInCurrentRole >= 4) & (f.YearsSinceLastPromotion >= 4)]
    st.write(f"**Stagnation check:** {len(stag)} employees have 4+ years in role and 4+ years since promotion. "
             f"Their average engagement is {stag.EngagementIndex.mean():.1f} vs {f.EngagementIndex.mean():.1f} overall: "
             "stagnation is not linked to lower engagement in this data.")

# ---------- Tab 4 ----------
with tab4:
    low = f[f.EngagementIndex < thr]
    c = st.columns(3)
    c[0].metric(f"Low-engagement alerts (< {thr})", len(low))
    c[1].metric("High-priority (score >= 3)", int((f.PriorityScore >= 3).sum()))
    c[2].metric("High burnout risk", int((f.BurnoutRisk == "High").sum()))
    st.subheader("Priority intervention areas")
    pa = f.groupby("JobRole").agg(Employees=("Age", "size"), HighBurnout=("BurnoutRisk", lambda s: (s == "High").sum()),
                                  AvgPriority=("PriorityScore", "mean"), Attrition=("Attrition", "mean")).sort_values("AvgPriority", ascending=False).round(2)
    st.dataframe(pa, width="stretch")
    st.subheader("Employees to talk to first")
    cols = ["Department", "JobRole", "JobLevel", "YearsAtCompany", "OverTime", "WorkLifeBalance", "BusinessTravel", "EngagementIndex", "BurnoutRisk", "PriorityScore"]
    top = f.sort_values(["PriorityScore", "EngagementIndex"], ascending=[False, True])[cols].head(25).round(1)
    st.dataframe(top, width="stretch")
    st.download_button("Download full filtered list (CSV)", f.sort_values("PriorityScore", ascending=False)[cols].to_csv(index=False), "priority_list.csv")
    st.caption("Priority score = 2xHigh burnout + 1xMedium burnout + Low engagement band + Frequent travel + (Level 1 & tenure <= 2 yrs).")
