import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------------------------
# Page layout & title
# ------------------------------------------------------------
st.set_page_config(page_title="Gapmind_Data_Dashboard",
                   page_icon="📊",
                   layout="wide")

st.title("🌍 Gapmind_Data_Dashboard")
st.markdown(
    """
    *Built with Streamlit + Plotly*  
    Explore the Gapminder dataset interactively.
    """
)

# ------------------------------------------------------------
# Load data – cached so it only runs once
# ------------------------------------------------------------
@st.cache_data(show_spinner=False)
def load_gapminder():
    """Return the built‑in Gapminder dataframe."""
    return px.data.gapminder()

df_raw = load_gapminder()

# ------------------------------------------------------------
# Sidebar – user controls
# ------------------------------------------------------------
st.sidebar.header("🔧 Dashboard Controls")

# Year selector (slider)
year_min, year_max = int(df_raw.year.min()), int(df_raw.year.max())
selected_year = st.sidebar.slider(
    "Select Year",
    min_value=year_min,
    max_value=year_max,
    value=year_max,
    step=5
)

# Continents multiselect
continents_list = sorted(df_raw.continent.unique())
selected_continents = st.sidebar.multiselect(
    "Continents",
    options=continents_list,
    default=continents_list
)

# X‑ and Y‑axis metrics for the scatter plot
metrics = ["gdpPercap", "lifeExp", "pop"]
x_metric = st.sidebar.selectbox("X‑axis metric", options=metrics, index=0)
y_metric = st.sidebar.selectbox("Y‑axis metric", options=metrics, index=1)

# Log‑scale toggle for X‑axis
log_x = st.sidebar.checkbox("Logarithmic X‑axis")

# Countries for the time‑series line chart
countries_list = sorted(df_raw.country.unique())
selected_countries = st.sidebar.multiselect(
    "Countries (Line chart)",
    options=countries_list,
    default=["Poland", "Germany", "United States", "China", "India"]
)

# Optional: button to reset all filters
if st.sidebar.button("Reset Filters"):
    selected_year = year_max
    selected_continents = continents_list
    x_metric, y_metric = metrics[0], metrics[1]
    log_x = False
    selected_countries = ["Poland", "Germany", "United States", "China", "India"]

# ------------------------------------------------------------
# Filter data according to the controls
# ------------------------------------------------------------
df_year_filtered = df_raw[
    (df_raw.year == selected_year) &
    (df_raw.continent.isin(selected_continents))
]

df_line_filtered = df_raw[df_raw.country.isin(selected_countries)]

# ------------------------------------------------------------
# Tabs – each tab holds a different plot / table
# ------------------------------------------------------------
tabs = st.tabs(
    ["Scatter Plot", "Line Chart", "Bar Chart", "World Map", "Data Table"]
)

# ---------- Scatter ----------
with tabs[0]:
    fig_scatter = px.scatter(
        df_year_filtered,
        x=x_metric,
        y=y_metric,
        size="pop",
        color="continent",
        hover_name="country",
        log_x=log_x,
        title=f"{y_metric} vs {x_metric} ({selected_year})"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# ---------- Line ----------
with tabs[1]:
    fig_line = px.line(
        df_line_filtered,
        x="year",
        y=y_metric,
        color="country",
        title=f"{y_metric} over Time for Selected Countries"
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ---------- Bar ----------
with tabs[2]:
    top_n = st.slider("Top N countries", min_value=5, max_value=20, value=10)
    df_top = (
        df_year_filtered
        .sort_values(y_metric, ascending=False)
        .head(top_n)
    )
    fig_bar = px.bar(
        df_top,
        x="country",
        y=y_metric,
        color="continent",
        title=f"Top {top_n} Countries by {y_metric} ({selected_year})"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

# ---------- World Map ----------
with tabs[3]:
    fig_map = px.choropleth(
        df_year_filtered,
        locations="country",
        locationmode="country names",
        color=y_metric,
        hover_name="country",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"World Map: {y_metric} ({selected_year})"
    )
    st.plotly_chart(fig_map, use_container_width=True)

# ---------- Data Table ----------
with tabs[4]:
    # Show the raw filtered dataframe
    st.dataframe(df_year_filtered)
    # Download button (CSV)
    csv = df_year_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name=f"gapminder_{selected_year}.csv",
        mime="text/csv"
    )