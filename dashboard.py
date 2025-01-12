import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
@st.cache
def load_data():
    df = pd.read_csv('noodles.csv')
    return df

df = load_data()

# Set title and description
st.title("World Instant Noodles Consumption Dashboard (2018-2022)")
st.markdown("""
This dashboard provides insights into the world consumption of instant noodles from 2018 to 2022, across various countries and regions. You can explore trends in noodle consumption, per capita data, and more.
""")

# Sidebar filters
st.sidebar.header("Filters")
continent = st.sidebar.selectbox('Select Continent', options=df['Continent'].unique())
year = st.sidebar.selectbox('Select Year', options=[2018, 2019, 2020, 2021, 2022])

# Filter dataset based on the selected continent
filtered_df = df[df['Continent'] == continent]

# Display selected continent data
st.subheader(f"Top Instant Noodles Consumers in {continent} in {year}")
year_column = str(year)
top_consumers = filtered_df[['Country/Region', year_column, '2022 Population']].sort_values(by=year_column, ascending=False).head(10)

st.dataframe(top_consumers)

# Add a download button for filtered data
st.download_button(
    label="Download Filtered Data",
    data=top_consumers.to_csv(index=False),
    file_name=f'filtered_noodles_data_{continent}.csv',
    mime='text/csv'
)

# Line chart for noodle consumption over years for selected continent
st.subheader(f"Instant Noodles Consumption Trend in {continent}")
fig = px.line(filtered_df, x='Country/Region', y=['2018', '2019', '2020', '2021', '2022'], title=f'Noodle Consumption Trend for {continent}')
st.plotly_chart(fig)

# Bar chart for per capita noodle consumption in the selected year
st.subheader(f"Per Capita Instant Noodles Consumption in {continent} for {year}")
filtered_df['Per Capita Consumption'] = filtered_df[year_column] / filtered_df['2022 Population'] * 1000000
fig = px.bar(filtered_df, x='Country/Region', y='Per Capita Consumption', title=f'Per Capita Consumption in {continent} for {year}')
st.plotly_chart(fig)

# Pie chart for the distribution of noodle consumption in the selected year
st.subheader(f"Global Distribution of Instant Noodles Consumption in {year}")
top_countries = df[['Country/Region', year_column]].sort_values(by=year_column, ascending=False).head(10)
fig = px.pie(top_countries, names='Country/Region', values=year_column, title=f'Top 10 Countries by Noodle Consumption in {year}')
st.plotly_chart(fig)

# Scatter plot: Population vs Noodle Consumption
st.subheader(f"Population vs Noodle Consumption in {year}")
fig = px.scatter(df, x='2022 Population', y=year_column, color='Continent', hover_name='Country/Region', title=f'Population vs Noodle Consumption in {year}')
st.plotly_chart(fig)

# Country Detail: Detailed consumption data for a selected country
st.sidebar.subheader("Country Detail")
country = st.sidebar.selectbox('Select Country', options=df['Country/Region'])
country_data = df[df['Country/Region'] == country]
st.subheader(f"Consumption Data for {country}")
st.write(country_data[['Country/Region', '2018', '2019', '2020', '2021', '2022']])

# Conclusion or Insights
st.subheader("Key Insights")
st.markdown("""
- The top consumers of instant noodles are primarily in Asia, with China being the largest.
- The consumption trends show a steady increase in many countries, with fluctuations due to various socio-economic factors.
- Per capita consumption is a significant indicator in understanding noodle consumption habits, with higher values in some developed countries.
""")
