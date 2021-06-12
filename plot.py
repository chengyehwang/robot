
import plotly.express as px
import pandas as pd

def plot(data,x,y,file_name):
    fig = px.scatter(data, x=x, y=y)
    fig.write_image(file_name)

