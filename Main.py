import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf

st.set_page_config(page_title="JPM Prices", layout="wide")

@st.cache
def getData():
    df = yf.download('JPM', start='2019-01-01',end='2019-12-31', progress=False)
    return df

st.title('Stock Price w/ Different Chart Packages')

df = getData()
# st.table(Chase[:10])

tab1, tab2, tab3, tab4, tab5 = st.tabs(["matplotlib", "plotly", "altair", "vega-lite", "bokeh"])

# matplotlib
with tab1:
    st.markdown('[matplotlib](https://matplotlib.org/stable/gallery/index.html)')
    figm, ax = plt.subplots()
    ax.title.set_text('Chase')
    ax.plot(df['Close'])
    st.pyplot(figm) 

# plotly
with tab2:
    st.markdown('[plotly](https://plotly.com/python/)')
    import plotly.graph_objects as go
    jpm = df.reset_index()
    figp = go.Figure(data=[go.Candlestick(x=jpm['Date'],
            open=jpm['Open'],high=jpm['High'],low=jpm['Low'],close=jpm['Close'])])
    st.plotly_chart(figp, use_container_width=True) 

# altair
with tab3:
    st.markdown('[Altair](https://altair-viz.github.io/gallery/index.html)')
    import altair as alt
    figa = alt.Chart(jpm).mark_area(color="lightblue",
        interpolate='step-after', line=True).encode(x='Date',y='Open')
    st.altair_chart(figa, use_container_width=True)

# vega-lite
with tab4:
    st.markdown('[vega-lite](https://vega.github.io/vega-lite/examples/)')
    st.vega_lite_chart(jpm, {
        'mark': {'type': 'line', 'tooltip': True},
        'encoding': {
            'x': {'field': 'Date', 'type': 'temporal'},
            'y': {'field': 'Close', 'type': 'quantitative'},
        }},use_container_width=True)

with tab5:
    st.markdown('[bokeh](https://docs.bokeh.org/en/latest/docs/gallery.html)')

    from math import pi
    from bokeh.plotting import figure, show

    df = jpm[:30] # shorten for example
    # df["date"] = pd.to_datetime(df["date"])

    inc = df.Close > df.Open
    dec = df.Open > df.Close
    w = 12*60*60*1000 # half day in ms

    TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

    p = figure(x_axis_type="datetime", tools=TOOLS, width=1000, title = "JPM Candlestick")
    p.xaxis.major_label_orientation = pi/4
    p.grid.grid_line_alpha=0.3

    p.segment(df.Date, df.High, df.Date, df.Low, color="black")
    p.vbar(df.Date[inc], w, df.Open[inc], df.Close[inc], fill_color="#D5E1DD", line_color="black")
    p.vbar(df.Date[dec], w, df.Open[dec], df.Close[dec], fill_color="#F2583E", line_color="black")

    st.bokeh_chart(p, use_container_width=True)