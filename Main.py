import streamlit as st
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import datetime

st.set_page_config(page_title="Stock Price w/ Different Chart Packages", layout="wide")

st.markdown('Select from the following tabs to see different chart packages in action.')

@st.cache
def getTickers():
    table = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")[0]
    return list(table['Symbol'])

@st.cache
def retrieveTicker(ticker,startdate):
    df = yf.download(ticker, start=startdate, progress=False)
    return df

cols = getTickers()
startdate = st.sidebar.date_input("Start Date", datetime.date(2022, 1, 1)) # '2022-01-01'
ticker = st.sidebar.selectbox('Select a Stock', cols, index=cols.index("JPM"))

df = retrieveTicker(ticker,startdate)
# st.table(Chase[:10])

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["matplotlib", "plotly", "altair", "vega-lite", "seaborn", "bokeh"])

# matplotlib
with tab1:
    st.markdown('Go to [matplotlib](https://matplotlib.org/stable/gallery/index.html) for more examples.')
    with st.echo(): # echo() to show code on streamlit
        figm, ax = plt.subplots()
        ax.title.set_text(ticker)
        ax.plot(df['Close'])
        st.pyplot(figm) 

# plotly
with tab2:
    st.markdown('Go to [plotly](https://plotly.com/python/) for more examples.')
    with st.echo():
        import plotly.graph_objects as go
        stock = df.reset_index()
        figp = go.Figure(data=[go.Candlestick(x=stock['Date'],open=stock['Open'],high=stock['High'],low=stock['Low'],close=stock['Close'])])
        st.plotly_chart(figp, use_container_width=True) 

# altair
with tab3:
    st.markdown('Go to [Altair](https://altair-viz.github.io/gallery/index.html) for more examples.')
    with st.echo():
        import altair as alt
        figa = alt.Chart(stock).mark_area(color="lightblue",interpolate='step-after', line=True).encode(x='Date',y='Open')
        st.altair_chart(figa, use_container_width=True)

# vega-lite
with tab4:
    st.markdown('Go to [vega-lite](https://vega.github.io/vega-lite/examples/) for more examples.')
    with st.echo():
        st.vega_lite_chart(stock, {
            'mark': {'type': 'line', 'tooltip': True},
            'encoding': {
                'x': {'field': 'Date', 'type': 'temporal'},
                'y': {'field': 'Close', 'type': 'quantitative'},
            }},use_container_width=True)
with tab5:
    st.markdown('[seaborn](https://seaborn.pydata.org/examples/index.html) and other matplotlib-based packages (GeoPandas, NetworkX, plotnine, etc.) all render to the last figure.')
    with st.echo():
        import seaborn as sns
        figs, ax = plt.subplots()
        ax.title.set_text(ticker)
        sns.lineplot(data=stock, x="Date", y="Close", ax=ax)
        st.pyplot(figs)
with tab6:
    st.markdown('Go to [bokeh](https://docs.bokeh.org/en/latest/docs/gallery.html) for more examples.')
    with st.echo():
        from math import pi
        from bokeh.plotting import figure, show

        df = stock[:30] # shorten for example
        # df["date"] = pd.to_datetime(df["date"])

        inc = df.Close > df.Open
        dec = df.Open > df.Close
        w = 12*60*60*1000 # half day in ms

        TOOLS = "pan,wheel_zoom,box_zoom,reset,save"

        p = figure(x_axis_type="datetime", tools=TOOLS, width=1000, title = ticker+" Candlestick")
        p.xaxis.major_label_orientation = pi/4
        p.grid.grid_line_alpha=0.3

        p.segment(df.Date, df.High, df.Date, df.Low, color="black")
        p.vbar(df.Date[inc], w, df.Open[inc], df.Close[inc], fill_color="#D5E1DD", line_color="black")
        p.vbar(df.Date[dec], w, df.Open[dec], df.Close[dec], fill_color="#F2583E", line_color="black")

        st.bokeh_chart(p, use_container_width=True)