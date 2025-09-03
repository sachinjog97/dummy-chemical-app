import streamlit as st
import time
import plotly.graph_objects as go
import graphviz

# Title and instructions
st.title("Optimal Methanol Supply Chain")

# User selections
year = st.selectbox("Choose a year", [2030, 2040, 2050])
objective = st.selectbox("Optimization goal", ["Minimize Cost", "Minimize Global Warming Impact"])

# Button to simulate
if st.button("Run Optimization"):

    # Define steps
    steps = [
    "Creating process simulation",
    "Optimizing process simulation",
    "Creating hybrid process models",
    "Optimizing supply chain"
    ]

    # Create empty containers for each step's text and progress bar
    text_containers = [st.empty() for _ in steps]
    

    for i, step in enumerate(steps):
        # Show step text ABOVE the progress bar
        text_containers[i].markdown(f"**{step}...**")
        
        
        # Animate progress bar
        for pct in range(101):
            
            time.sleep(0.01)
        
        # After finishing, update text with a checkmark
        text_containers[i].markdown(f"**{step} ✅**")

    # Determine routes and locations
    route_locations = {}

    if objective == "Minimize Global Warming Impact":
        if year in [2030, 2040]:
            route_locations = {
                "Electrolytic": {
                    "color": "green",
                    "locations": [
                        {"name": "", "lat": 55.1262, "lon": 77.2090, "export": False}, # Canada
                        {"name": "", "lat": -53.1638, "lon": -70.9171, "export": True}, # Chile
                        {"name": "", "lat": 53.3326, "lon": 6.9135, "export": True}, # Netherlands
                        {"name": "", "lat": 63.2889, "lon": 18.7160, "export": False}, # Sweden
                    ]
                },
                "Biomethane": {
                    "color": "blue",
                    "locations": [
                        {"name": "", "lat": -21.8076, "lon": -41.1415, "export": True}, # Brazil
                        {"name": "", "lat": 18.3584, "lon": 81.8982, "export": False}, # India 
                    ]
                }
            }
        elif year == 2050:
            route_locations = {
                "Electrolytic": {
                    "color": "green",
                    "locations": [
                        {"name": "", "lat": -53.1638, "lon": -70.9171, "export": True}, # Chile
                        {"name": "", "lat": 53.3326, "lon": 6.9135, "export": False}, # Netherlands
                    ]
                },
                "Biomethane": {
                    "color": "blue",
                    "locations": [
                        {"name": "", "lat": -21.8076, "lon": -41.1415, "export": True}, # Brazil
                        {"name": "", "lat": 18.3584, "lon": 81.8982, "export": False}, # India 
                        {"name": "", "lat": 39.2810, "lon": 107.7657, "export": True}, # China 
                        {"name": "", "lat": -41.0524, "lon": 145.9064, "export": False}, # Australia 
                    ]
                }
            }
    else:
        if year in [2030, 2040]:
            route_locations = {
                "Fossil": {
                    "color": "#404040",
                    "locations": [
                        {"name": "", "lat": 28.8880, "lon": -96.0035, "export": True}, # US
                        {"name": "", "lat": 39.2810, "lon": 107.7657, "export": False}, # China
                        {"name": "", "lat": 18.3584, "lon": 81.8982, "export": False}, # India 
                        {"name": "", "lat": 31.2632, "lon": 32.3055, "export": True}, # Egypt
                    ]
                },
                "Biomethane": {
                    "color": "blue",
                    "locations": [
                        {"name": "", "lat": -21.8076, "lon": -41.1415, "export": True}, # Brazil
                    ]
                }
            }
        elif year == 2050:
            route_locations = {
                "Fossil": {
                    "color": "#404040",
                    "locations": [
                        {"name": "", "lat": 28.8880, "lon": -96.0035, "export": True}, # US
                        {"name": "", "lat": 39.2810, "lon": 107.7657, "export": False}, # China
                    ]
                },
                "Biomethane": {
                    "color": "blue",
                    "locations": [
                        {"name": "", "lat": -21.8076, "lon": -41.1415, "export": True}, # Brazil
                        {"name": "", "lat": 18.3584, "lon": 81.8982, "export": False}, # India  
                    ]
                }
            }

    # Display route info
    all_routes = ', '.join(route_locations.keys())
    


    # Create map figure
    fig = go.Figure()

    # Add dummy markers for production routes (Electrolytic, Biomethane, Fossil)
    fig.add_trace(go.Scattergeo(
        lon=[None], lat=[None], mode='markers',
        marker=dict(size=15, color="green"),
        name="Electrolytic production"
    ))
    fig.add_trace(go.Scattergeo(
        lon=[None], lat=[None], mode='markers',
        marker=dict(size=15, color="blue"),
        name="Biomethane production"
    ))
    fig.add_trace(go.Scattergeo(
        lon=[None], lat=[None], mode='markers',
        marker=dict(size=15, color="#404040"),
        name="Fossil production",
    ))

    fig.update_layout(
    legend=dict(
        font=dict(size=16)
    )
)

    # Add dummy marker for export locations with same color as current route, but square symbol
    fig.add_trace(go.Scattergeo(
        lon=[None],
        lat=[None],
        mode='markers',
        marker=dict(size=15, color="white", line=dict(color="black", width=1), symbol="square"),
        name="Export Locations"
    ))

    # Add actual location markers per technology
    for tech, data in route_locations.items():
        for loc in data["locations"]:
            fig.add_trace(go.Scattergeo(
                lon=[loc["lon"]],
                lat=[loc["lat"]],
                text=loc["name"],
                mode='markers+text',
                marker=dict(
                    size=10,
                    color=data["color"],
                    symbol="circle" if not loc.get("export") else "square"
                ),
                textposition="top center",
                showlegend=False
            ))

    fig.update_layout(
        geo=dict(
            scope='world',
            showland=True,
            landcolor="white",
            showocean=True,
            oceancolor="white",
            showcountries=True,
            countrycolor="black",
            countrywidth=0.3,
            coastlinecolor="black",
            coastlinewidth=0.3
        ),
        height=500,
        margin={"r":0,"t":0,"l":0,"b":0},
        legend_title="",
        legend=dict(orientation="h", yanchor="bottom", y=0.01, xanchor="center", x=0.5),
        paper_bgcolor='rgba(0,0,0,0)',  # Transparent outside the plotting area
        plot_bgcolor='rgba(0,0,0,0)'    # Transparent inside the plotting area
    )

    
    # Show the process flowchart below
    st.markdown(
    f"""<h3 style="margin-top:40px; margin-bottom:40px;">🔁 Process Flow</h3>""",
    unsafe_allow_html=True,
    )

    dot = graphviz.Digraph(
    graph_attr={'fontsize': '16'},
    node_attr={'fontsize': '16'},
    edge_attr={'fontsize': '16'}
    )

    if "Electrolytic" in route_locations:
        dot.edge("CO₂", "Methanol", label="+ H₂ (via electrolysis)", color="green")

    if "Biomethane" in route_locations:
        dot.edge("Biomethane", "Syngas", label="Steam methane reforming", color="blue")
        dot.edge("Syngas", "Methanol", color="blue")

    if "Fossil" in route_locations:
        dot.edge("Natural Gas", "Syngas", label="Steam methane reforming", color="#404040")
        dot.edge("Syngas", "Methanol", color="#404040")


    st.graphviz_chart(dot)

    st.markdown(
    f"""<h3 style="margin-top:0px; margin-bottom:-100px;">🌍 Production and export locations in {year}:</h3>""",
    unsafe_allow_html=True,
    )
    
    st.plotly_chart(fig, use_container_width=True, key="production_map")

    st.markdown(
    f"""<h3 style="margin-top:40px; margin-bottom:40px;">🌍 Sustainable Development Goals (SDGs)</h3>""",
    unsafe_allow_html=True,
    )
        
    # Decide which icons to use based on presence of "Fossil" route
    if "Fossil" in route_locations:
        icon_paths = [
            "sdg_icons/sdg3_dim.png",
            "sdg_icons/sdg6_dim.png",
            "sdg_icons/sdg13_dim.png",
            "sdg_icons/sdg14.png",
            "sdg_icons/sdg15_dim.png"
        ]
    elif "Electrolytic" in route_locations:
        icon_paths = [
            "sdg_icons/sdg3_dim.png",
            "sdg_icons/sdg6_dim.png",
            "sdg_icons/sdg13.png",
            "sdg_icons/sdg14_dim.png",
            "sdg_icons/sdg15_dim.png"
        ]
    elif "Biomethane" in route_locations:
        icon_paths = [
            "sdg_icons/sdg3_dim.png",
            "sdg_icons/sdg6.png",
            "sdg_icons/sdg13.png",
            "sdg_icons/sdg14_dim.png",
            "sdg_icons/sdg15_dim.png"    
        ]
    
    cols = st.columns(len(icon_paths))

    for col, path in zip(cols, icon_paths):
        col.image(path, width=100)  # smaller icons (width in pixels)

    