import streamlit as st
import pandas as pd
import numpy as np
import streamlit.components.v1 as components
import plotly.express as px
from calculations import Bschole_calc
import matplotlib.pyplot as plt
import seaborn as sns
#sidebar stuff
st.sidebar.title('Black-Scholes Model')

st.sidebar.text("By:")
st.sidebar.page_link("https://www.linkedin.com/in/anirudh-kk-009885212/", label="Anirudh Krishnakumar")
current_asset_price = st.sidebar.number_input(
    'Current Asset Price',
    float(0.01),float(1 << 52), step=0.01
)
strike_price = st.sidebar.number_input(
    'Strike Price',
    float(0.01),float(1 << 52), step=0.01
)

ttm = st.sidebar.number_input(
    'Time to Maturity(years)',
    float(0.01),float(1 << 52), step=0.01
)

vol = st.sidebar.number_input(
    'Volatility',
    float(0.01),1.0, step=0.01
)

Rfir = st.sidebar.number_input(
    'Risk Free Interest Rate',
    float(0.01),float(1 << 52), step=0.01
)
st.sidebar.divider()
st.sidebar.text("Heatmap parameters")
min_spot = st.sidebar.number_input(
    'Minimum spot price',
    float(0.01),float(1 << 52), step=0.01
)
max_spot = st.sidebar.number_input(
    'Maximum spot price',
    float(0.01),float(1 << 52), step=0.01
)


volatility_min= st.sidebar.slider("Minimum volatility", 0.0, 1.0, 0.1)
volatility_max= st.sidebar.slider("Maximum volatility", 0.0, 1.0, 0.1)

st.title("Black Scholes pricing model")

df = pd.DataFrame({
    'Current Asset Price': [current_asset_price],
    'Strike Price': [strike_price],
    'Time to Maturity(years)':[ttm],
    "Volatility":[vol],
    "Risk free Interest Rate": [Rfir],
    })
st.table(df)

call, put = st.columns(2)

# call.write("new stuff")
# with stylable_container(
#     key="green_button",
#     css_styles="""
#         button {
#             background-color: green;
#             color: green;
#             border-radius: 40px;
#         }
#         """,
# ):
#     call.button("Green button")

class Shout(object):
    def __init__(self, text, bgcol, typeof, price):
        self.text = text
        self.bgcol = bgcol
        self.typeof = typeof
        self.price = price

    def _repr_html_(self):
        return "<div style='border-radius: 25px; width: 20rem; height: 10rem; background-color:"+self.bgcol+"'>" + "<div style = 'display: flex; flex-direction:column; justify-content: space-evenly; align-items: center'>"+ "<div style = 'flex-grow: 3; padding: 30px'>"+self.typeof+" OPTION PRICE:"+"</div>" + "<div style = 'flex-grow: 4'>"+"$ "+str(round(self.price, 3))+"</div>"+"</div>" + "</div>"
typeo = "Call"
typez = "Put"
call_p = Bschole_calc(strike_price, current_asset_price, ttm, vol, Rfir, typeo).__calc__()
put_p = Bschole_calc(strike_price, current_asset_price, ttm, vol, Rfir, typez).__calc__()
c = Shout(str(current_asset_price), "#32de84", "CALL", call_p)
p = Shout(str(current_asset_price), "#FFC0CB", "PUT", put_p)
call.markdown(c._repr_html_(), unsafe_allow_html=True)
put.markdown(p._repr_html_(), unsafe_allow_html=True)
st.markdown('#') 
st.title("Options Price - Interactive Map")

st.text("This is a volatility map that shows the black scholes model over various strike prices and various volatilities to give you a good idea of at which prices and volatility the stock will most optimally trade at.")


callmap, putmap = st.columns(2)

data=[[0]*10 for i in range(10)]

step_vol = (volatility_max-volatility_min)/9
step_pr = (max_spot-min_spot)/9
ex = []
why = []
#the ex represents volatility
for i in range(10):
    ex.append(round(volatility_min+i*step_vol,2))
#the why represents the spot price
for j in range(10):
    why.append(round(min_spot+j*step_pr,2))

minn = float('inf')
maxx = -1
type_for_heatmap="Call"

for xx in range(len(ex)):
    for yy in range(len(why)):
        option = Bschole_calc(strike_price, why[yy], ttm, ex[xx], Rfir,type_for_heatmap)
        data[yy][xx] = round(option.__calc__(),2)
        if data[yy][xx] > maxx:
            maxx = data[yy][xx]
        if data[yy][xx]<minn:
            minn = data[yy][xx]
# ex= [str(xx) for xx in ex]
# why = [str(yy) for yy in why]
# color_scale = [[minn,"Red"], [maxx,"Green"]]
fig_call = px.imshow(data, labels=dict(x="Volatility", y="Strike Price"), color_continuous_scale='Viridis', text_auto=True)
# import numpy as np
# img_rgb = np.array(data, dtype=np.uint8)
# # Display the heatmap
# fig = px.imshow(img_rgb)
callmap.subheader("Call Heatmap")
callmap.plotly_chart(fig_call, use_container_width=True)

type_for_heatmapp="Put"
for xx in range(len(ex)):
    for yy in range(len(why)):
        option = Bschole_calc(strike_price, why[yy], ttm, ex[xx], Rfir,type_for_heatmapp)
        data[yy][xx] = round(option.__calc__(),2)
        if data[yy][xx] > maxx:
            maxx = data[yy][xx]
        if data[yy][xx]<minn:
            minn = data[yy][xx]
putmap.subheader("Put Heatmap")
fig_put = px.imshow(data, labels=dict(x="Volatility", y="Strike Price"), text_auto=True, color_continuous_scale='Viridis')
putmap.plotly_chart(fig_put, use_container_width=True)