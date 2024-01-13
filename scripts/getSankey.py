#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import random
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
import plotly.subplots as sp
import math
# Read the CSV file into a DataFrame
import pandas as pd
import plotly.express as px
import plotly.io as pio
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


# In[3]:


lg = "#c5edc5"
lr = "#efc6c6"
bases = ["commons-cli","commons-text","joda-money","jline-reader","commons-validator","cdk-data","spotify-web-api","commons-codec","jfreechart","dyn4j"]


# # number of mutations

# In[8]:


# for index,base in enumerate(bases):
#     df = pd.read_csv("data/" + base + ".csv")
#     print(base)
#     print(len(set(df["m_id"])))
        


# # propagation and fail

# In[6]:


# for index,base in enumerate(bases):
#     df = pd.read_csv("data/" + base + ".csv")
#     x = len(df[(df["end_same"]==False) | (df["test_status"]=="fail") ])
#     y = len((df[df["test_status"]=="fail"]))
#     print(base)
#     print(y/x * 100)
        


# # no infection + propagation

# In[7]:


# for index,base in enumerate(bases):
#     df = pd.read_csv("data/" + base + ".csv")
#     x = df[(df["middle_same"] == True)
#                     & (df["mr_exception"] == df["nmr_exception"])
#                     & (df["mr_athrow"] == df["nmr_athrow"])
#                     & (df["mr_return"] == df["nmr_return"])]
#     x = x[(x["end_same"]==False) | (x["test_status"]=="fail")]

#     print(base)
#     print(len(x)/len(df) * 100)
        


# In[9]:



data = []

for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0

    df = pd.read_csv( base + ".csv")

    
    middle_same = df[(df["middle_same"] == True)
                    & (df["mr_exception"] == df["nmr_exception"])
                    & (df["mr_athrow"] == df["nmr_athrow"])
                    & (df["mr_return"] == df["nmr_return"])]
    
    middle_diff = df[(df["middle_same"] == False)
                    | (df["mr_exception"] != df["nmr_exception"])
                    | (df["mr_athrow"] != df["nmr_athrow"])
                    | (df["mr_return"] != df["nmr_return"])]
    assert len(df) == len(middle_same) + len(middle_diff)
    
    middle_same_end_same = middle_same[(middle_same["end_same"]==True) & (middle_same["test_status"]=="pass")]
    middle_same_end_diff = middle_same[(middle_same["end_same"]==False) | (middle_same["test_status"]=="fail")]
    assert len(middle_same_end_same) + len(middle_same_end_diff) == len(middle_same)
    
    middle_diff_end_same = middle_diff[(middle_diff["end_same"]==True) & (middle_diff["test_status"]=="pass")]
    middle_diff_end_diff = middle_diff[(middle_diff["end_same"]==False) | (middle_diff["test_status"]=="fail")]
    assert len(middle_diff_end_same) + len(middle_diff_end_diff) == len(middle_diff)
    
    labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]
    values = [len(df), len(middle_same),len(middle_diff),
                  len(middle_same_end_same),len(middle_same_end_diff),
                  len(middle_diff_end_same),len(middle_diff_end_diff),
                  len(middle_same_end_same[middle_same_end_same["test_status"] == "pass"]),
                  len(middle_same_end_same[middle_same_end_same["test_status"] == "fail"]),
                  len(middle_same_end_diff[middle_same_end_diff["test_status"] == "pass"]),
                  len(middle_same_end_diff[middle_same_end_diff["test_status"] == "fail"]),
                  len(middle_diff_end_same[middle_diff_end_same["test_status"] == "pass"]),
                  len(middle_diff_end_same[middle_diff_end_same["test_status"] == "fail"]),
                  len(middle_diff_end_diff[middle_diff_end_diff["test_status"] == "pass"]),
                  len(middle_diff_end_diff[middle_diff_end_diff["test_status"] == "fail"])]
    total = sum(values)
    percentages = [v/total * 100 for v in values]
    
    labels[2] = labels[2] + "(" + str(round(len(middle_same)/len(df)*100,1)) + "%)"
    labels[3] = labels[3] + "(" + str(round(len(middle_diff)/len(df)*100,1)) + "%)"
    
    labels[4] = labels[4] + "(" + str(round(len(middle_same_end_same)/len(df)*100,1)) + "%)"
    labels[5] = labels[5] + "(" + str(round(len(middle_same_end_diff)/len(df)*100,1)) + "%)"
    labels[6] = labels[6] + "(" + str(round(len(middle_diff_end_same)/len(df)*100,1)) + "%)"
    labels[7] = labels[7] + "(" + str(round(len(middle_diff_end_diff)/len(df)*100,1)) + "%)"
    labels[8] = labels[8] + "(" + str(round(len(df[df["test_status"]=="pass"])/len(df)*100,1)) + "%)"
    labels[9] = labels[9] + "(" + str(round(len(df[df["test_status"]=="fail"])/len(df)*100,1)) + "%)"
    
    labels = ["<b>" + label + "<b>" for label in labels]
    
    trace = go.Sankey(
        
        textfont = dict(size = 24),
        arrangement = "fixed",
        node = dict(
          pad = 40,
          thickness = 20,
          line = dict(color = "grey", width = 0.2),
          label = labels,
          color = ["#c9e3e8","red","green","red",
                   "green","red","green","red",
                   "green","red"],
          x = [0, 0.15,   0.3,  0.3, 0.6,0.6,0.6,0.6,1  ,1],
          y = [0, 0.545, 0.25,  0.7, 0.15,0.3,0.4,0.75,0.3,0.7],
    #       x = [0, 0.15,   0.3,  0.3, 0.8, 0.8, 0.8, 0.8,  1,  1],
    #       y = [0, 0.545, 0.25,  0.7, 0.2, 0.35, 0.45, 0.8,0.2,0.8  ],
        ),
        link = dict(
          source = [0,1,1,2,2,3,3,4,4,5,5,6,6,7,7], # indices correspond to labels, eg A1, A2, A1, B1, ...
          target = [1,2,3,4,5,6,7,8,9,8,9,8,9,8,9],
          value = values,
                color = [lg,lg,lr,
                         lg,lr,lg,lr,
                         "green","red","green","red","green","red","green","red"],
                label=[f"{p:.1f}%" for p in percentages]))
    fig = go.Figure(data=[trace],)
    
    fig.add_annotation(
        x=-0.02,y = -0.15,
        xref='paper', yref='paper',
        text='Start',
        showarrow=False,
        font=dict( size=25 )

    )
        
    fig.add_annotation(
        x=0.09,y = -0.15,
        xref='paper', yref='paper',
        text='Reaching',
        showarrow=False,
        font=dict( size=25 )

    )
    
    fig.add_annotation(
        x=0.275,y =  -0.15,
        xref='paper', yref='paper',
        text='Infection',
        showarrow=False,
        font=dict( size=25 )

    )
        
    fig.add_annotation(
        x=0.75,y =  -0.15,
        xref='paper', yref='paper',
        text='Propagation',
        showarrow=False,
        font=dict( size=25 )

    )
    
    fig.add_annotation(
        x=1.02,y =  -0.15,
        xref='paper', yref='paper',
        text='Revealability',
        showarrow=False,
        font=dict( size=25 )

    )
    
#     fig.add_annotation(
#         x=1.02,y =  -0.1,
#         xref='paper', yref='paper',
#         text='Revealed',
#         showarrow=False,
#         font=dict( size=15 )

#     )
        
#     fig.add_annotation(
#         x=1.02,y =  -0.15,
#         xref='paper', yref='paper',
#         text='Propagation',
#         showarrow=False,
#         font=dict( size=15 )

#     )
    fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
    fig.update_layout(
        font=dict(family='sans-serif')
    )
    
    fig.write_image(base + ".pdf")
    fig.show()

