# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
from scipy.optimize import minimize
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(layout="wide")

st.title('Max Sharpe Ratio Portfolio Optimization 😍')

#with st.expander('About this app'):
  #st.write('This app shows the comparison between equal weight portfolio againts Max ratio portfolio.')
  #st.image('https://streamlit.io/images/brand/streamlit-logo-secondary-colormark-darktext.png', width=250)

st.sidebar.header('You can change sharpe ratio')
#user_name = st.sidebar.text_input('What is your name?')

b = st.sidebar.slider("Select an Sharpe Ratio of Bond", 0.0, 5.0, 2.0)
g = st.sidebar.slider("Select an Sharpe Ratio of Gold", 0.0, 5.0, 1.67)
s = st.sidebar.slider("Select an Sharpe Ratio of Set50 index fund", 0.0, 5.0, 2.0)
c = st.sidebar.slider("Select an Sharpe Ratio of Bitcoin", 0.0, 5.0, 3.0)


#col1, col2 = st.columns(2)

#with col1:
 # if user_name != '':
 #   st.write(f'👋 Hello {user_name}! 😍')
  #else:
  #  st.write('👈  Please enter your **name**! 😴')


## Optimization Variables
BondSharpeRatio = b
GoldSharpeRatio = g
StockSharpeRatio = s
BTCSharpeRatio = c
df = [[b,g,s,c]]
df = pd.DataFrame(df, columns=['Bond', 'Gold', 'Set50 fund','Bitcoin'])
## Constraint
# invest 100% of budget
def constraint1(x):
  return (x[0]+x[1]+x[2]+x[3])-1 
# porpotion of bond and gold should invest at least 30%
def constraint2(x):
  return (x[0]+x[1])-0.3

#set min and max for each weight
bnds = ((0.1, None), (0.1, None), (0.1, None), (0.1, 0.3))
#set type of constrain funxtion
con1 = {'type': 'eq', 'fun':constraint1}
con2 = {'type': 'ineq', 'fun':constraint2}
cons = [con1, con2]

##Goal
def objective(x, sign=-1.0):
  x1 = x[0]
  x2 = x[1]
  x3 = x[2]
  x4 = x[3]
  return sign * ((x1*BondSharpeRatio)+(x2*GoldSharpeRatio)+(x3*StockSharpeRatio)+(x4*BTCSharpeRatio))

#set equal weight
weight = [0.25,0.25,0.25,0.25]
eq_port_sr = -objective(weight)
#find max ratio
sol = minimize(objective,weight,method='SLSQP',bounds=bnds,constraints=cons)
max_ratio_sr = -sol.fun

labels = ['Bond', 'Gold', 'Stock', 'Btc']
subTitle1 = "Equal weight Portfolio SharpRatio = " + str(round(-objective(weight),3))
subTitle2 = "Optimize Portfolio SharpRatio = " + str(round(-sol.fun,3))
fig = make_subplots(1, 2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                    subplot_titles=[subTitle1, subTitle2])
fig.add_trace(go.Pie(labels=labels, values=weight, scalegroup='one',
                     name="Equal weight Portfolio"), 1, 1)
fig.add_trace(go.Pie(labels=labels, values=sol.x, scalegroup='one',
                     name="Optimization Portfolio"), 1, 2)

fig.update_layout(height=500, width=800,title='Portfolio Comparision')



with st.container():

    st.write('Sharpe Ratio Table')
    st.dataframe(df)

    # You can call any Streamlit command, including custom components:
    #st.plotly_chart(fig, use_container_width=True)
    st.plotly_chart(fig)