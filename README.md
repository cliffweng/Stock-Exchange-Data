# Stock Exchange Data

This app showcases different plotting packages Streamlit supports. It uses them to plot the same stock price data, but each package has a vast number of options to customize the plot. Below are their galleries:
- [matplotlib](https://matplotlib.org/stable/gallery/index.html)
- [plotly](https://plotly.com/python/)
- [Altair](https://altair-viz.github.io/gallery/index.html)
- [vega-lite](https://vega.github.io/vega-lite/examples/)
- [Bokeh](https://docs.bokeh.org/en/latest/docs/gallery.html)
- [graphviz](https://graphviz.org/gallery/)
- [pydeck](https://deckgl.readthedocs.io/en/latest/)
- [Seaborn](https://seaborn.pydata.org/examples/index.html) and other matplotlib-based packages (GeoPandas, NetworkX, plotnine, etc.)

To see this repository in action, please visit [Streamlit Cloud](https://cliffweng-stock-exchange-data-main-yjtxbo.streamlitapp.com/).

## Development with Docker
Run the following commands to build the dev docker image and run the container that use local files throughout development process:
```
docker build -t stcharts .
docker run -p 8501:8501 -v %cd%:/home/streamlit stcharts
```
Note 1: replace `stcharts` with `[your_docker_hub_username]/stcharts` if you want to push the image to your docker hub account.

Note 2: %cd% is the current directory of the project. Also the mounting (-v) will overshadow the files in the container, so your local file will be used, instead of the ones in the container. See notes below. 
## Package with Docker
Run the following command to build the production docker image and test run it:
```
docker build -t stcharts .
docker run -p 8501:8501 stcharts (1)
```
Then visit [localhost:8501](http://localhost:8501/)

Note 1: can be launched anywhere, no need to mount local files,as they were copied over in Dockerfile.
## Concepts
- [API Reference](https://docs.streamlit.io/library/api-reference)
- [State](https://docs.streamlit.io/library/advanced-features/session-state)
- [Pages](https://blog.streamlit.io/introducing-multipage-apps/)
- [Custom Components](https://docs.streamlit.io/library/components)
- [Caching](https://docs.streamlit.io/en/stable/caching.html)
- [Data Sources](https://docs.streamlit.io/knowledge-base/tutorials/databases)

## Notes
- Packages installed with Streamlit. [reference here](https://github.com/streamlit/streamlit/blob/develop/lib/setup.py)
- If you bind-mount into a non-empty directory on the container, the directory’s existing contents are obscured by the bind mount. [reference](https://docs.docker.com/storage/bind-mounts/#mount-into-a-non-empty-directory-on-the-container)
- This is a Streamlit-Cloud-deployable repository, which means that it can be deployed to Streamlit Cloud with a single click. To learn more, visit [Streamlit Cloud](https://streamlit.io/cloud).