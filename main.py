import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import plotly.express as px

st.set_page_config(page_title="Jay Milagroso",layout='wide')

st.write("""
# Covid-19 Infographics
""")

@st.cache_data
def get_data():
    base_url = "https://covid.ourworldindata.org/data/owid-covid-data.csv"
    return pd.read_csv(base_url)

df = get_data()

filter_duration = {
    1825: "Past 5 Years", 
    365: "Past Year", 
    183: "Past 6 Months", 
    91: "Past 3 Months", 
    31: "Past Month",
    16: "Past 2 Weeks",
    8: "Past 7 Days"
}

def format_func(option):
    return filter_duration[option]

st.write("Source: https://covid.ourworldindata.org")

df = df[df['continent'].notna()]

df['continent'] = df['continent'].apply(str)
continents = list(df['continent'].unique())
continents_sorted = sorted(continents)
continents_sorted.insert(0, "All")
continent_option = st.sidebar.multiselect("Continent", options=continents_sorted, default='All')

df = df if 'All' in continent_option else df[df['continent'].isin(continent_option)]

countries = list(df['location'].unique())
countries = sorted(countries)
countries.insert(0, "All")
country_option = st.sidebar.multiselect("Country", options=countries, default='All')
df = df if 'All' in country_option else df[df['location'].isin(country_option)]

date_option = st.sidebar.selectbox("Date Range", options=list(filter_duration.keys()), format_func=format_func, index=3)
today = datetime.now()
n_days_ago = today - timedelta(days=date_option)
df = df.loc[df['date'] >= str(n_days_ago.date())]

df['date'] = pd.to_datetime(df['date'], errors='coerce')

st.sidebar.divider()
st.sidebar.text("NEUST MS IT 2022-2023 2nd Sem")
st.sidebar.text("IT-273 Data Visualization")
st.sidebar.text("Jay Milagroso<j.milagroso@gmail.com>")

st.bar_chart(
    df,
    x="date",
    y=["total_cases", "total_deaths", "total_tests", "total_vaccinations"]
)

tab01, tab02, tab03 = st.tabs([
    "New Cases", "New Deaths", "New Vaccinations"
])

with tab01:
    fig_total_new_cases = px.bar(
        df, 
        x='date', 
        y='new_cases', 
        color='new_cases', 
        title='Total Number of New Cases'
    )
    st.plotly_chart(fig_total_new_cases, use_container_width=True)
with tab02:
    fig_total_new_deaths = px.bar(
        df, 
        x='date', 
        y='new_deaths', 
        color='new_deaths', 
        title='Total Number of New Deaths'
    )
    st.plotly_chart(fig_total_new_deaths, use_container_width=True)
with tab03:
    fig_total_new_vaccinations = px.bar(
        df, 
        x='date', 
        y='new_vaccinations', 
        color='new_vaccinations', 
        title='Total Number of New Vaccinations'
    )
    st.plotly_chart(fig_total_new_vaccinations, use_container_width=True)


tab11, tab12, tab13 = st.tabs([
    "Total Cases", "Total Deaths", "Total Vaccinations"
])

with tab11:
    fig_total_cases = px.bar(
        df, 
        x='date', 
        y='total_cases', 
        color='total_cases', 
        title='Total Number of Cases'
    )
    st.plotly_chart(fig_total_cases, use_container_width=True)
with tab12:
    fig_total_deaths = px.bar(
        df, 
        x='date', 
        y='total_deaths', 
        color='total_deaths', 
        title='Total Number of Deaths'
    )
    st.plotly_chart(fig_total_deaths, use_container_width=True)
with tab13:
    fig_total_vaccinations = px.bar(
        df, 
        x='date', 
        y='total_vaccinations', 
        color='total_vaccinations', 
        title='Total Number of Vaccinations'
    )
    st.plotly_chart(fig_total_vaccinations, use_container_width=True)


fig = px.scatter(
    df,
    x="gdp_per_capita",
    y="life_expectancy",
    size="population",
    color="continent",
    hover_name="location",
    log_x=True,
    size_max=60,
)
st.plotly_chart(fig, theme="streamlit", use_container_width=True)
