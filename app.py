import streamlit as st

# App title
st.title("Optimal Chemical Production Route")
st.markdown("Select a chemical, year, and optimization goal to get the optimal route.")

# Dropdowns for inputs
chemical = st.selectbox("Choose a chemical", ["Methanol", "Hydrogen"])
year = st.selectbox("Choose a year", [2030, 2050])
objective = st.selectbox("Optimization goal", ["Minimize Cost", "Minimize Impact"])

# Logic for optimal route
if objective == "Minimize Impact":
    if year == 2030:
        route = "Green"
    else:
        route = "Biomethane"
else:
    route = "Fossil"

# Show result
st.markdown(f"### ✅ Optimal Route: **{route}**")
