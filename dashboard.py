import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Instant Noodles Dashboard",
    page_icon="🍜",
    layout="wide",
)

# Load dataset
@st.cache
def load_data():
    df = pd.read_csv('noodles.csv')
    return df

df = load_data()

# Header Section
st.markdown("""
<div style="background-color:#f7c948;padding:10px;border-radius:10px;">
    <h1 style="text-align:center;color:#1c1c1c;">🍜 Instant Noodles Consumption Dashboard (2018-2022)</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="font-size:18px;color:#8b8b8b;">
Explore the fascinating world of instant noodles! This dashboard provides insights into consumption trends, per capita data, and key global patterns over the years.
</p>
""", unsafe_allow_html=True)

# Sidebar filters
st.sidebar.markdown("### 🔍 Filters")
continent = st.sidebar.selectbox('🌍 Select Continent', options=df['Continent'].unique())
year = st.sidebar.selectbox('📅 Select Year', options=[2018, 2019, 2020, 2021, 2022])

# Filter dataset based on selected continent
filtered_df = df[df['Continent'] == continent]

# Main Content Layout
st.markdown(f"### Top Instant Noodles Consumers in **{continent}** in **{year}**")
year_column = str(year)
top_consumers = filtered_df[['Country/Region', year_column, '2022 Population']].sort_values(by=year_column, ascending=False).head(10)

st.dataframe(top_consumers)

st.download_button(
    label="📥 Download Filtered Data",
    data=top_consumers.to_csv(index=False),
    file_name=f'filtered_noodles_data_{continent}.csv',
    mime='text/csv'
)

# Consumption Trend Line Chart
st.markdown(f"### 📈 Instant Noodles Consumption Trend in **{continent}**")
fig_line = px.line(
    filtered_df, 
    x='Country/Region', 
    y=['2018', '2019', '2020', '2021', '2022'], 
    title=f"Noodle Consumption Trend for {continent}",
    labels={"value": "Consumption", "variable": "Year"}
)
fig_line.update_layout(template="plotly_dark")
st.plotly_chart(fig_line, use_container_width=True)

# Per Capita Bar Chart
st.markdown(f"### 🍜 Per Capita Instant Noodles Consumption in **{continent}** for **{year}**")
filtered_df['Per Capita Consumption'] = filtered_df[year_column] / filtered_df['2022 Population'] * 1000000
fig_bar = px.bar(
    filtered_df, 
    x='Country/Region', 
    y='Per Capita Consumption', 
    title=f"Per Capita Consumption in {continent} for {year}",
    labels={"Per Capita Consumption": "Per Capita Consumption (in millions)"}
)
fig_bar.update_traces(marker_color="#FFA07A")
st.plotly_chart(fig_bar, use_container_width=True)

# Global Distribution Pie Chart
st.markdown(f"### 🌎 Global Distribution of Instant Noodles Consumption in **{year}**")
top_countries = df[['Country/Region', year_column]].sort_values(by=year_column, ascending=False).head(10)
fig_pie = px.pie(
    top_countries, 
    names='Country/Region', 
    values=year_column, 
    title=f"Top 10 Countries by Noodle Consumption in {year}",
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig_pie, use_container_width=True)

# Scatter Plot: Population vs. Noodle Consumption
st.markdown(f"### 📊 Population vs. Noodle Consumption in **{year}**")
fig_scatter = px.scatter(
    df, 
    x='2022 Population', 
    y=year_column, 
    color='Continent', 
    hover_name='Country/Region', 
    title=f"Population vs Noodle Consumption in {year}",
    labels={"2022 Population": "Population", year_column: "Noodle Consumption"}
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Country Detail
st.sidebar.markdown("### 🗺️ Country Detail")
country = st.sidebar.selectbox('Select Country', options=df['Country/Region'])
country_data = df[df['Country/Region'] == country]
st.markdown(f"### 📋 Consumption Data for **{country}**")
st.write(country_data[['Country/Region', '2018', '2019', '2020', '2021', '2022']])

# Key Insights
st.markdown("""
<div style="background-color:#000000;padding:10px;border-radius:10px;">
    <h3>🔑 Key Insights</h3>
    <ul>
        <li>Asian countries dominate instant noodle consumption, with China and Indonesia leading.</li>
        <li>Consumption trends highlight growth despite socio-economic changes, with a surge during the pandemic years.</li>
        <li>Per capita data reveals lifestyle differences influencing noodle consumption patterns.</li>
    </ul>
</div>
""", unsafe_allow_html=True)
