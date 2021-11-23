import streamlit as st
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup as bs
import seaborn as sn
import os
import altair as alt
import requests
import csv
import sys
import time

page = requests.get('https://en.wikipedia.org/wiki/List_of_mergers_and_acquisitions_by_Apple')
soup = bs(page.text, 'html.parser')   
table = soup.find_all('table')
df = pd.read_html(str(table))[0]
df['Year'] = df['Date'].str[-4:]
df.iloc[11,7] = '2000'
df['Year'] = df['Year'].astype('int32')
source = df.groupby('Year').count()[['Company']]

st.title('Apple\'s Acquisitions through the years')
#st.dataframe(df)

bars = alt.Chart(source.reset_index()).mark_bar(cornerRadiusTopLeft=3,
    cornerRadiusTopRight=3, size = 30, stroke = 'transparent').encode(
    alt.X('Year:O'),
    alt.Y('Company:Q', axis=alt.Axis(title='Number of Acquisitions', labels = False, grid=False)),
    # The highlight will be set on the result of a conditional statement
    color=alt.condition(
        alt.datum.Year > 2011,  # If the year is 1810 this test returns True,
        alt.value('steelblue'),     # which sets the bar orange.
        alt.value('grey')   # And if it's not true it sets the bar steelblue.
    )
).properties(title = 'Apple Acquisitions Through Time', width = 800, height = 400)

text = bars.mark_text(
    align='center',
    baseline='middle' , dy = -6
).encode(
    text='Company:Q'
)


st.altair_chart(bars + text, use_container_width = False)