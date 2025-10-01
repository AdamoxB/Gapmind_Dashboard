# Gapmind_Data_Dashboard– Streamlit + Plotly

🚀 Quick Start
# 1️⃣ Create & activate a virtual environment (optional but recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# 2️⃣ Install dependencies
pip install streamlit pandas plotly

# 3️⃣ Clone or copy the repo into a folder, then run:
streamlit run app.py
Open the URL shown in your terminal (usually http://localhost:8501) and start exploring!

📋 Features
Feature	Description
Sidebar controls	Year slider, continent multiselect, X/Y metric selection, log‑scale toggle, country selector for time‑series.
Tabs	Scatter, Line chart, Bar chart, World map, Data table.
Dynamic filtering	All plots react instantly to any control change.
Plotly Express visualisations	High‑quality scatter, line, bar and choropleth maps.
Caching	Data loads once (@st.cache_data) – fast even on many interactions.
Download CSV	Export the currently filtered data directly from the UI.

📖 How It Works
Data loading – The built‑in Gapminder dataset is loaded once using @st.cache_data.
Sidebar widgets – All interactive elements live here; changing them triggers a re‑render.
Filtering – Two subsets are created: one for the selected year & continents, another for the chosen countries over all years.
Tabs & Plots – Each tab contains a Plotly Express chart that automatically resizes with use_container_width=True.
Data table & download – A DataFrame view plus a CSV download button in the final tab.

## 📄 License

This project is open source under the [MIT License](LICENSE).  
Feel free to fork, modify and share!
