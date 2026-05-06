import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="Pulse of Payments — India Fraud Intelligence",
    page_icon="💳",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv('data/india_payments_clean.csv')
    return df

df = load_data()

# SIDEBAR FILTERS
st.sidebar.title("🔍 Filters")
payment_filter = st.sidebar.multiselect(
    "Payment Method",
    options=df['payment_method'].unique(),
    default=df['payment_method'].unique()
)
state_filter = st.sidebar.multiselect(
    "State",
    options=df['state'].unique(),
    default=df['state'].unique()
)
month_filter = st.sidebar.slider(
    "Month Range",
    min_value=1, max_value=12, value=(1, 12)
)

filtered = df[
    (df['payment_method'].isin(payment_filter)) &
    (df['state'].isin(state_filter)) &
    (df['month'].between(month_filter[0], month_filter[1]))
]

# PAGE TITLE
st.title("💳 Pulse of Payments — India Digital Payment Fraud Intelligence")
st.markdown("**Full Stack Fraud Analytics System | 50,000 Indian Payment Transactions (2023–2024)**")
st.markdown("---")

# KPI CARDS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{len(filtered):,}")
col2.metric("Fraud Cases", f"{filtered['fraud_label'].sum():,}")
col3.metric("Fraud Rate", f"{filtered['fraud_label'].mean()*100:.2f}%")
col4.metric("Avg Transaction", f"₹{filtered['transaction_amount'].mean():,.0f}")

st.markdown("---")

# SECTION 1 — FRAUD INTELLIGENCE
st.header("🔍 Fraud Intelligence")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud by Payment Method")
    pm = filtered.groupby('payment_method')['fraud_label'].sum().reset_index()
    pm = pm.sort_values('fraud_label', ascending=True)
    fig = px.bar(pm, x='fraud_label', y='payment_method', orientation='h',
                 color='fraud_label', color_continuous_scale='Reds',
                 labels={'fraud_label':'Fraud Count','payment_method':'Method'})
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Monthly Fraud Trend")
    monthly = filtered.groupby('month')['fraud_label'].sum().reset_index()
    fig = px.line(monthly, x='month', y='fraud_label',
                  markers=True, color_discrete_sequence=['#E53935'])
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud by Hour of Day")
    hourly = filtered.groupby('hour')['fraud_label'].sum().reset_index()
    hourly['risk'] = hourly['hour'].apply(
        lambda x: 'High Risk' if x >= 22 or x <= 4 else 'Medium Risk' if x <= 8 else 'Low Risk')
    color_map = {'High Risk':'#F44336','Medium Risk':'#FFC107','Low Risk':'#4CAF50'}
    fig = px.bar(hourly, x='hour', y='fraud_label', color='risk',
                 color_discrete_map=color_map,
                 labels={'fraud_label':'Fraud Count','hour':'Hour'})
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Fraud by Merchant Category")
    merch = filtered.groupby('merchant_category')['fraud_label'].sum().reset_index()
    merch = merch.sort_values('fraud_label', ascending=True)
    fig = px.bar(merch, x='fraud_label', y='merchant_category', orientation='h',
                 color='fraud_label', color_continuous_scale='Oranges',
                 labels={'fraud_label':'Fraud Count','merchant_category':'Merchant'})
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# SECTION 2 — GEOGRAPHIC RISK
st.header("🗺️ Geographic Risk")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top States by Fraud")
    state_fraud = filtered.groupby('state')['fraud_label'].sum().reset_index()
    state_fraud = state_fraud.sort_values('fraud_label', ascending=True).tail(10)
    fig = px.bar(state_fraud, x='fraud_label', y='state', orientation='h',
                 color='fraud_label', color_continuous_scale='Reds',
                 labels={'fraud_label':'Fraud Count','state':'State'})
    fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Cities by Fraud")
    city_fraud = filtered.groupby('city')['fraud_label'].sum().reset_index()
    city_fraud = city_fraud.sort_values('fraud_label', ascending=True).tail(10)
    fig = px.bar(city_fraud, x='fraud_label', y='city', orientation='h',
                 color='fraud_label', color_continuous_scale='Oranges',
                 labels={'fraud_label':'Fraud Count','city':'City'})
    fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# SECTION 3 — INVESTIGATION FUNNEL
st.header("🔎 Investigation Funnel")

total = len(filtered)
suspicious = len(filtered[filtered['fraud_risk_score'] > 40])
flagged = len(filtered[filtered['fraud_risk_score'] > 60])
investigated = len(filtered[filtered['investigation_status'].isin(
    ['Under Investigation','Confirmed Fraud','Resolved'])])
confirmed = len(filtered[filtered['investigation_status'] == 'Confirmed Fraud'])
resolved = len(filtered[filtered['investigation_status'] == 'Resolved'])

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total", f"{total:,}")
col2.metric("Suspicious", f"{suspicious:,}")
col3.metric("Flagged", f"{flagged:,}")
col4.metric("Investigated", f"{investigated:,}")
col5.metric("Confirmed", f"{confirmed:,}")
col6.metric("Resolved", f"{resolved:,}")

fig = go.Figure(go.Funnel(
    y=['Total','Suspicious','Flagged','Investigated','Confirmed Fraud','Resolved'],
    x=[total, suspicious, flagged, investigated, confirmed, resolved],
    textinfo="value+percent initial",
    marker=dict(color=['#1565C0','#FFA000','#F57C00','#E64A19','#B71C1C','#2E7D32'])
))
fig.update_layout(height=400, margin=dict(l=0,r=0,t=20,b=0))
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# SECTION 4 — CUSTOMER INTELLIGENCE
st.header("👥 Customer Intelligence")
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud by Age Group")
    age = filtered.groupby('customer_age_group')['fraud_label'].sum().reset_index()
    fig = px.bar(age, x='customer_age_group', y='fraud_label',
                 color='fraud_label', color_continuous_scale='Reds',
                 labels={'fraud_label':'Fraud Count','customer_age_group':'Age Group'})
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Fraud by Device Type")
    device = filtered.groupby('device_type')['fraud_label'].sum().reset_index()
    device = device.sort_values('fraud_label', ascending=True)
    fig = px.bar(device, x='fraud_label', y='device_type', orientation='h',
                 color_discrete_sequence=['#7B1FA2'],
                 labels={'fraud_label':'Fraud Count','device_type':'Device'})
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud by Day of Week")
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day = filtered.groupby('day_of_week')['fraud_label'].sum().reset_index()
    day['day_of_week'] = pd.Categorical(day['day_of_week'], categories=day_order, ordered=True)
    day = day.sort_values('day_of_week')
    fig = px.bar(day, x='day_of_week', y='fraud_label',
                 color_discrete_sequence=['#00838F'],
                 labels={'fraud_label':'Fraud Count','day_of_week':'Day'})
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Fraud by Risk Category")
    risk = filtered.groupby('risk_category')['fraud_label'].count().reset_index()
    fig = px.pie(risk, values='fraud_label', names='risk_category',
                 color_discrete_sequence=['#4CAF50','#FFC107','#F44336'],
                 hole=0.4)
    fig.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("**Built by Rishika H J | Python · SQL · Power BI · Streamlit | 50,000 Indian Payment Transactions**")