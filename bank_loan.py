import streamlit as st
import pandas as pd
import plotly.express as px


import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------
# 🎨 PAGE CONFIGURATION
# --------------------------
st.set_page_config(
    page_title="Bank Loan Dashboard",
    page_icon="💰",
    layout="wide"
)

# --------------------------
# 💅 CUSTOM CSS STYLING
# --------------------------
st.markdown("""
    <style>
    /* Background */
    .stApp {
        background-color: #F8FAFD;
        background-image: linear-gradient(180deg, #F8FAFD 0%, #EAF1F9 100%);
        background-attachment: fixed;
    }

    /* Header Banner */
    .main-header {
        background-color: #2E86C1;
        padding: 18px;
        border-radius: 10px;
        text-align: center;
        color: white;
        font-size: 32px;
        font-weight: bold;
        letter-spacing: 1px;
    }

    /* Section titles */
    h2 {
        color: #1A5276 !important;
        font-weight: 700 !important;
        border-left: 6px solid #2E86C1;
        padding-left: 10px;
        margin-top: 30px;
    }

    /* KPI boxes */
    [data-testid="stMetricValue"] {
        color: #2E86C1;
        font-size: 28px;
        font-weight: bold;
    }

    /* Chart container style */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #EBF5FB;
    }

    /* Remove top padding */
    header, footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --------------------------
# 🏦 HEADER SECTION
# --------------------------
st.markdown("<div class='main-header'>🏦 Bank Loan Performance Dashboard</div>", unsafe_allow_html=True)
st.write(" ")

#load data
uploaded_file = st.file_uploader(r"C:\Users\hp\OneDrive\Documents\R files\bank_data.xlsx", type=["xlsx"])
if uploaded_file is not None:
    data = pd.read_excel(uploaded_file, sheet_name="a")
    st.write("✅ File successfully loaded!")
    st.dataframe(data.head())


#sidebar filter
# Sidebar filters with "Select All" buttons

# --- Year Filter ---
# --------------------------
# 🎛 SIDEBAR FILTERS WITH SELECT ALL
# --------------------------
st.sidebar.header("🔍 Filter Options")

# --- Year Filter with Select All ---
all_months = sorted(data["issue_date"].dt.strftime("%B").unique())
select_all_Months = st.sidebar.checkbox("Select All Months", value=True)

if select_all_Months:
    month= st.sidebar.multiselect("Select months:", options=all_months, default=all_months)
else:
    month= st.sidebar.multiselect("Select months:", options=all_months)

# --- State Filter with Select All ---
all_states = sorted(data["address_state"].unique())
select_all_states = st.sidebar.checkbox("Select All States", value=True)

if select_all_states:
    state = st.sidebar.multiselect("Select State(s):", options=all_states, default=all_states)
else:
    state = st.sidebar.multiselect("Select State(s):", options=all_states)

# Apply filters to data
filtered = data.copy()
if month:
    filtered = filtered[filtered["issue_date"].dt.strftime("%B").isin(month)]
if state:
    filtered = filtered[filtered["address_state"].isin(state)]

# --- KPI SECTION ---
total_loan_applications = filtered["id"].count()
total_funded_amount = filtered["loan_amount"].sum()
avg_interest_rate = filtered["int_rate"].mean()
Total_amount_received=data['total_payment'].sum()
Total_amount_received_millions=Total_amount_received/1000000
Average_Dti=data['dti'].mean()*100

col1, col2, col3 ,col4, col5= st.columns(5)
col1.metric("Total Loan Applications", f"{total_loan_applications:,}")
col2.metric("Total Funded Amount", f"${total_funded_amount/1_000_000:.2f} M")
col3.metric("Average Interest Rate", f"{avg_interest_rate:.2f}%")
col4.metric("total amount received",f" {Total_amount_received_millions:.2f} $")
col5.metric("average dti",f" {Average_Dti:.2f}%")

st.markdown("---")

# --- ⿡ Monthly Trend by Issue Date ---
st.subheader("📅 Monthly Trend by Issue Date")
monthly_trend = (
    filtered.groupby(filtered["issue_date"].dt.to_period("M"))["loan_amount"]
    .sum()
    .reset_index()
)
monthly_trend["issue_date"] = monthly_trend["issue_date"].astype(str)
fig1 = px.line(
    monthly_trend,
    x="issue_date",
    y="loan_amount",
    title="Monthly Funded Amount Trend",
    markers=True,
)
fig1.update_layout(xaxis_title="Month", yaxis_title="Funded Amount ($)")
st.plotly_chart(fig1, use_container_width=True)

# --- ⿢ Total Loan Applications by Month ---
st.subheader("📈 Total Loan Applications by Month")
monthly_apps = (
    filtered.groupby(filtered["issue_date"].dt.to_period("M"))["id"]
    .count()
    .reset_index()
)
monthly_apps["issue_date"] = monthly_apps["issue_date"].astype(str)
fig2 = px.bar(
    monthly_apps,
    x="issue_date",
    y="id",
    text="id",
    title="Total Loan Applications per Month",
)
fig2.update_traces(textposition="outside")
st.plotly_chart(fig2, use_container_width=True)

# --- ⿣ Regional Analysis by Total Funded Amount ---
st.subheader("🗺 Regional Analysis by Total Funded Amount")
state_funding = filtered.groupby("address_state")["loan_amount"].sum().reset_index()
fig3 = px.choropleth(
    state_funding,
    locations="address_state",
    locationmode="USA-states",
    color="loan_amount",
    color_continuous_scale="Blues",
    scope="usa",
    title="Total Funded Amount by State",
)
st.plotly_chart(fig3, use_container_width=True)

# --- ⿤ Total Funded by Term ---
st.subheader("📊 Total Funded Amount by Loan Term")
term_funding = filtered.groupby("term")["loan_amount"].sum().reset_index()
fig4 = px.pie(
    term_funding,
    names="term",
    values="loan_amount",
    title="Total Funded Amount by Term",
    hole=0.4,
)
st.plotly_chart(fig4, use_container_width=True)

# --- ⿥ Total Funded by Employment Length ---
st.subheader("👷 Total Funded Amount by Employment Length")
emp_funding = filtered.groupby("emp_length")["loan_amount"].sum().reset_index().sort_values("loan_amount", ascending=False)
fig5 = px.bar(
    emp_funding,
    x="emp_length",
    y="loan_amount",
    title="Total Funded Amount by Employment Length",
    color="loan_amount",
)
st.plotly_chart(fig5, use_container_width=True)

# --- ⿦ Total Funded by Loan Purpose ---
st.subheader("🎯 Total Funded Amount by Loan Purpose")
purpose_funding = filtered.groupby("purpose")["loan_amount"].sum().reset_index().sort_values("loan_amount", ascending=False)
fig6 = px.bar(
    purpose_funding,
    x="purpose",
    y="loan_amount",
    title="Total Funded Amount by Purpose",
    color="loan_amount",
)
fig6.update_layout(xaxis={'categoryorder':'total descending'})
st.plotly_chart(fig6, use_container_width=True)

# --- 7️⃣ Total Funded by Home Ownership (HEATMAP) ---
st.subheader("🏠 Total Funded Amount by Home Ownership")

# Aggregate data
home_funding = filtered.groupby(["home_ownership", "term"])["loan_amount"].sum().reset_index()

# Create a pivot table for heatmap
heatmap_data = home_funding.pivot(index="home_ownership", columns="term", values="loan_amount")

# Plot heatmap
fig7 = px.imshow(
    heatmap_data,
    color_continuous_scale="Blues",
    title="Total Funded Amount by Home Ownership and Term",
    labels=dict(x="Loan Term", y="Home Ownership", color="Funded Amount"),
    text_auto=True
)

st.plotly_chart(fig7, use_container_width=True)
