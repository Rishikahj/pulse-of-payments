import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3

st.set_page_config(
    page_title="Pulse of Payments — India Fraud Intelligence",
    page_icon="💳",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('data/india_payments_clean.csv')
    return df

df = load_data()

# ── SIDEBAR ──
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

# Apply filters
filtered = df[
    (df['payment_method'].isin(payment_filter)) &
    (df['state'].isin(state_filter)) &
    (df['month'].between(month_filter[0], month_filter[1]))
]

# ── PAGE 1: EXECUTIVE OVERVIEW ──
st.title("💳 Pulse of Payments — India Digital Payment Fraud Intelligence")
st.markdown("**Full Stack Fraud Analytics System | 50,000 Indian Payment Transactions (2023–2024)**")
st.markdown("---")

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Transactions", f"{len(filtered):,}")
col2.metric("Fraud Cases", f"{filtered['fraud_label'].sum():,}")
col3.metric("Fraud Rate", f"{filtered['fraud_label'].mean()*100:.2f}%")
col4.metric("Avg Transaction", f"₹{filtered['transaction_amount'].mean():,.0f}")

st.markdown("---")

# Charts Row 1
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud by Payment Method")
    pm_fraud = filtered.groupby('payment_method')['fraud_label'].agg(['sum','count']).reset_index()
    pm_fraud['fraud_rate'] = pm_fraud['sum']/pm_fraud['count']*100
    pm_fraud = pm_fraud.sort_values('sum', ascending=True)
    fig1 = px.bar(pm_fraud, x='sum', y='payment_method', orientation='h',
                  color='fraud_rate', color_continuous_scale='Reds',
                  labels={'sum':'Fraud Count', 'payment_method':'Payment Method', 'fraud_rate':'Fraud Rate %'})
    fig1.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Monthly Fraud Trend")
    monthly = filtered.groupby('month')['fraud_label'].sum().reset_index()
    fig2 = px.line(monthly, x='month', y='fraud_label',
                   markers=True, color_discrete_sequence=['#E53935'])
    fig2.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ── PAGE 2: FRAUD INTELLIGENCE ──
st.header("🔍 Fraud Intelligence — Pattern & Behavior Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud by Hour of Day")
    hourly = filtered.groupby('hour')['fraud_label'].sum().reset_index()
    hourly['risk'] = hourly['hour'].apply(lambda x: 'High Risk' if x >= 22 or x <= 4 else 'Medium Risk' if x <= 8 else 'Low Risk')
    color_map = {'High Risk': '#F44336', 'Medium Risk': '#FFC107', 'Low Risk': '#4CAF50'}
    fig3 = px.bar(hourly, x='hour', y='fraud_label', color='risk',
                  color_discrete_map=color_map,
                  labels={'fraud_label':'Fraud Count', 'hour':'Hour of Day'})
    fig3.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    st.subheader("Fraud by Merchant Category")
    merch = filtered.groupby('merchant_category')['fraud_label'].sum().reset_index()
    merch = merch.sort_values('fraud_label', ascending=True)
    fig4 = px.bar(merch, x='fraud_label', y='merchant_category', orientation='h',
                  color='fraud_label', color_continuous_scale='Reds',
                  labels={'fraud_label':'Fraud Count', 'merchant_category':'Merchant'})
    fig4.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig4, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Risk Category Distribution")
    risk_data = filtered.groupby('risk_category')['fraud_label'].count().reset_index()
    fig5 = px.pie(risk_data, values='fraud_label', names='risk_category',
                  color_discrete_sequence=['#4CAF50','#FFC107','#F44336'],
                  hole=0.4)
    fig5.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.subheader("Fraud by Bank Provider")
    bank = filtered.groupby('bank_provider')['fraud_label'].sum().reset_index()
    bank = bank.sort_values('fraud_label', ascending=True)
    fig6 = px.bar(bank, x='fraud_label', y='bank_provider', orientation='h',
                  color_discrete_sequence=['#1565C0'],
                  labels={'fraud_label':'Fraud Count', 'bank_provider':'Bank/Provider'})
    fig6.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")

# ── PAGE 3: GEOGRAPHIC RISK ──
st.header("🗺️ Geographic Risk — State & City Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top States by Fraud Count")
    state_fraud = filtered.groupby('state')['fraud_label'].sum().reset_index()
    state_fraud = state_fraud.sort_values('fraud_label', ascending=True).tail(10)
    fig7 = px.bar(state_fraud, x='fraud_label', y='state', orientation='h',
                  color='fraud_label', color_continuous_scale='Reds')
    fig7.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig7, use_container_width=True)

with col2:
    st.subheader("Top Cities by Fraud Count")
    city_fraud = filtered.groupby('city')['fraud_label'].sum().reset_index()
    city_fraud = city_fraud.sort_values('fraud_label', ascending=True).tail(10)
    fig8 = px.bar(city_fraud, x='fraud_label', y='city', orientation='h',
                  color='fraud_label', color_continuous_scale='Oranges')
    fig8.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig8, use_container_width=True)

st.markdown("---")

# ── PAGE 4: INVESTIGATION FUNNEL ──
st.header("🔎 Investigation Funnel — Fraud Detection Pipeline")

total = len(filtered)
suspicious = len(filtered[filtered['fraud_risk_score'] > 40])
flagged = len(filtered[filtered['fraud_risk_score'] > 60])
investigated = len(filtered[filtered['investigation_status'].isin(['Under Investigation','Confirmed Fraud','Resolved'])])
confirmed = len(filtered[filtered['investigation_status'] == 'Confirmed Fraud'])
resolved = len(filtered[filtered['investigation_status'] == 'Resolved'])

col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("Total", f"{total:,}")
col2.metric("Suspicious", f"{suspicious:,}")
col3.metric("Flagged", f"{flagged:,}")
col4.metric("Investigated", f"{investigated:,}")
col5.metric("Confirmed", f"{confirmed:,}")
col6.metric("Resolved", f"{resolved:,}")

funnel_fig = go.Figure(go.Funnel(
    y=['Total Transactions', 'Suspicious', 'Flagged', 'Investigated', 'Confirmed Fraud', 'Resolved'],
    x=[total, suspicious, flagged, investigated, confirmed, resolved],
    textinfo="value+percent initial",
    marker=dict(color=['#1565C0','#FFA000','#F57C00','#E64A19','#B71C1C','#2E7D32'])
))
funnel_fig.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0))
st.plotly_chart(funnel_fig, use_container_width=True)

st.markdown("---")

# ── PAGE 5: CUSTOMER INTELLIGENCE ──
st.header("👥 Customer Intelligence — Behavior & Device Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud by Age Group")
    age_fraud = filtered.groupby('customer_age_group')['fraud_label'].sum().reset_index()
    fig9 = px.bar(age_fraud, x='customer_age_group', y='fraud_label',
                  color='fraud_label', color_continuous_scale='Reds',
                  labels={'fraud_label':'Fraud Count', 'customer_age_group':'Age Group'})
    fig9.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig9, use_container_width=True)

with col2:
    st.subheader("Fraud by Device Type")
    device_fraud = filtered.groupby('device_type')['fraud_label'].sum().reset_index()
    fig10 = px.bar(device_fraud, x='fraud_label', y='device_type', orientation='h',
                   color_discrete_sequence=['#7B1FA2'],
                   labels={'fraud_label':'Fraud Count', 'device_type':'Device'})
    fig10.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig10, use_container_width=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Fraud by Day of Week")
    day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    day_fraud = filtered.groupby('day_of_week')['fraud_label'].sum().reset_index()
    day_fraud['day_of_week'] = pd.Categorical(day_fraud['day_of_week'], categories=day_order, ordered=True)
    day_fraud = day_fraud.sort_values('day_of_week')
    fig11 = px.bar(day_fraud, x='day_of_week', y='fraud_label',
                   color_discrete_sequence=['#00838F'],
                   labels={'fraud_label':'Fraud Count', 'day_of_week':'Day'})
    fig11.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig11, use_container_width=True)

with col2:
    st.subheader("Fraud by Time Category")
    time_fraud = filtered.groupby('time_category')['fraud_label'].sum().reset_index()
    fig12 = px.bar(time_fraud, x='fraud_label', y='time_category', orientation='h',
                   color_discrete_sequence=['#E65100'],
                   labels={'fraud_label':'Fraud Count', 'time_category':'Time'})
    fig12.update_layout(height=300, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig12, use_container_width=True)

st.markdown("---")
st.markdown("**Built by Rishika H J | Tools: Python, SQL, Power BI, Streamlit | Data: 50,000 Indian Payment Transactions**")