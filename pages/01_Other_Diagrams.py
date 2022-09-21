import streamlit as st
import math

@st.cache
def getData():
    df = pd.read_json("https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/bart-stations.json")
     # Use pandas to calculate additional data
    df["exits_radius"] = df["exits"].apply(lambda exits_count: math.sqrt(exits_count))
    return df

st.title('Other Diagrams')
tab1, tab2 = st.tabs(["graphviz", "pydeck"])

with tab1:
    st.markdown('[graphviz](https://graphviz.org/gallery/)')
    with st.echo():
        st.graphviz_chart('''
            digraph {
                run -> intr
                intr -> runbl
                runbl -> run
                run -> kernel
                kernel -> zombie
                kernel -> sleep
                kernel -> runmem
                sleep -> swap
                swap -> runswap
                runswap -> new
                runswap -> runmem
                new -> runmem
                sleep -> runmem
                }
        ''')

with tab2:
    st.markdown('[pydeck](https://deckgl.readthedocs.io/en/latest/)')
    with st.echo():
        import pydeck as pdk
        import pandas as pd

        df = getData()

        # Define a layer to display on a map
        layer = pdk.Layer(
            "ScatterplotLayer",  df,
            pickable=True,
            opacity=0.8,
            stroked=True,
            filled=True,
            radius_scale=6,
            radius_min_pixels=1,
            radius_max_pixels=100,
            line_width_min_pixels=1,
            get_position="coordinates",
            get_radius="exits_radius",
            get_fill_color=[255, 140, 0],
            get_line_color=[0, 0, 0],
        )

        # Set the viewport location
        view_state = pdk.ViewState(latitude=37.7749295, longitude=-122.4194155, zoom=10, bearing=0, pitch=0)

        r = pdk.Deck(map_style=None, layers=[layer], initial_view_state=view_state, tooltip={"text": "{name}\n{address}"})
        
        # From streamlit docs: https://docs.streamlit.io/en/stable/api.html#streamlit.deck_gl_chart
        st.pydeck_chart(r)
