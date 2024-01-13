#!/usr/bin/env python
# coding: utf-8

# In[53]:


import pandas as pd
import numpy as np
import matplotlib
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
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42


# In[48]:


bases = ["commons-cli","commons-text","joda-money","jline-reader","commons-validator","cdk-data","spotify-web-api","commons-codec","jfreechart","dyn4j"]


# In[49]:


lg = "#c5edc5"
lr = "#efc6c6"


# # Conditional Boundary
# 

# In[27]:


figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]
p = 0
f = 0

for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]=='org.pitest.mutationtest.engine.gregor.mutators.ConditionalsBoundaryMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]
    
    p = p + len(df[df["test_status"]=="pass"])
    f = f + len(df[df["test_status"]=="fail"])

values = total_values
total = values[0]
percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(total)*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(total)*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(total)*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(total)*100,1)) + "%)"

labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"


# In[28]:


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
    
#       x = [0, 0.15,   0.3,  0.3, 0.6,0.6,0.6,0.6,1  ,1],
#       y = [0, 0.545, 0.25,  0.7, 0.15,0.3,0.4,0.75,0.3,0.7],
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.545, 0.25,  0.7, 0.2, 0.5, 0.6, 0.8, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)

fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)


fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)
fig.write_image("ConditionalBoundary(" + str(total) + ")" + "Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# In[ ]:





# # NegateConditional

# In[29]:



data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]
p = 0
f = 0
for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]=='org.pitest.mutationtest.engine.gregor.mutators.NegateConditionalsMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

    p = p + len(df[df["test_status"]=="pass"])
    f = f + len(df[df["test_status"]=="fail"])

values = total_values
total = values[0]
percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(total)*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(total)*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(total)*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(total)*100,1)) + "%)"

labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"


# In[30]:


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
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.545, 0.25,  0.7, 0.1, 0.2, 0.3, 0.7, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)

fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)

# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
# total_count[1] = total
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("NegateConditional(" +str(total) + ")" + "Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# # VoidMethodCall

# In[31]:


figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]
p = 0
f = 0
for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]=='org.pitest.mutationtest.engine.gregor.mutators.VoidMethodCallMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

    p = p + len(df[df["test_status"]=="pass"])
    f = f + len(df[df["test_status"]=="fail"])

values = total_values
total = values[0]
percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(total)*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(total)*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(total)*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(total)*100,1)) + "%)"

labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"


# In[32]:


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
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.545, 0.25,  0.7, 0.1, 0.3, 0.4, 0.7, 0.3,0.8],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)
fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)

# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("VoidMethodCall(" +str(total)+ ")Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# # NullReturns

# In[33]:


figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]
p = 0
f = 0
for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]=='org.pitest.mutationtest.engine.gregor.mutators.returns.NullReturnValsMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

    p = p + len(df[df["test_status"]=="pass"])
    f = f + len(df[df["test_status"]=="fail"])

values = total_values
total = values[0]
percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(total)*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(total)*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(total)*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(total)*100,1)) + "%)"

labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"


# In[34]:


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
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.45,  0.15,  0.55, 0.1, 0.2, 0.3, 0.7, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)

fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)


# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("NullReturns(" + str(total) + ")Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# # Math Mutator

# In[35]:


figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]

for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]=='org.pitest.mutationtest.engine.gregor.mutators.MathMutator']
    sum_df = sum_df + len(df)
    
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
    

#         values = [len(df), len(middle_same),len(middle_diff),
#                   len(middle_same_end_same),len(middle_same_end_diff),
#                   len(middle_diff_end_same),len(middle_diff_end_diff),
#                   len(middle_same_end_same[middle_same_end_same["test_status"] == "pass"]),
#                   len(middle_same_end_same[middle_same_end_same["test_status"] == "fail"]),
#                   len(middle_same_end_diff[middle_same_end_diff["test_status"] == "pass"]),
#                   len(middle_same_end_diff[middle_same_end_diff["test_status"] == "fail"]),
#                   len(middle_diff_end_same[middle_diff_end_same["test_status"] == "pass"]),
#                   len(middle_diff_end_same[middle_diff_end_same["test_status"] == "fail"]),
#                   len(middle_diff_end_diff[middle_diff_end_diff["test_status"] == "pass"]),
#                   len(middle_diff_end_diff[middle_diff_end_diff["test_status"] == "fail"])]
        
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

values = total_values
total = values[0]

percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(values[3]+values[4])*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(values[3]+values[4])*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(values[5]+values[6])*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(values[5]+values[6])*100,1)) + "%)"
labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"
    
 


# In[36]:


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
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.45,  0.15,  0.55, 0.1, 0.3, 0.4, 0.7, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)
fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)


# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("Math(" + str(total) + ")Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# # Increment

# In[37]:


figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]

for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]=='org.pitest.mutationtest.engine.gregor.mutators.IncrementsMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

values = total_values
total = values[0]

percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(values[3]+values[4])*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(values[3]+values[4])*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(values[5]+values[6])*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(values[5]+values[6])*100,1)) + "%)"
labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"
    
 


# In[38]:


labels = ["<b>" + label + "<b>" for label in labels]
trace = go.Sankey(
    textfont = dict(size = 14),
    arrangement = "fixed",
    node = dict(
      pad = 40,
      thickness = 20,
      line = dict(color = "grey", width = 0.2),
      label = labels,
      color = ["#c9e3e8","red","green","red",
               "green","red","green","red",
               "green","red"],
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.45,  0.15,  0.55, 0.1, 0.2, 0.3, 0.7, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)

fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)

# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("increment(" + str(total) + ")Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# # Boolean False

# In[39]:


figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]
for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]=='org.pitest.mutationtest.engine.gregor.mutators.returns.BooleanFalseReturnValsMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

values = total_values
total = values[0]

percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(values[3]+values[4])*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(values[3]+values[4])*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(values[5]+values[6])*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(values[5]+values[6])*100,1)) + "%)"
labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"    
    
 


# In[40]:


labels = ["<b>" + label + "<b>" for label in labels]
trace = go.Sankey(
    textfont = dict(size = 14),
    arrangement = "fixed",
    node = dict(
      pad = 40,
      thickness = 20,
      line = dict(color = "grey", width = 0.2),
      label = labels,
      color = ["#c9e3e8","red","green","red",
               "green","red","green","red",
               "green","red"],
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.45,  0.15,  0.55, 0.1, 0.2, 0.35, 0.7, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)

fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)
# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("BooleanFalse(" + str(total) + ")Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# # BooleanTrue
# 

# In[41]:



figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]

for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]=='org.pitest.mutationtest.engine.gregor.mutators.returns.BooleanTrueReturnValsMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

values = total_values
total = values[0]

percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(values[3]+values[4])*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(values[3]+values[4])*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(values[5]+values[6])*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(values[5]+values[6])*100,1)) + "%)"
labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"
    
 


# In[42]:


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
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.55,  0.2,  0.65, 0.1, 0.3, 0.4, 0.7, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)

fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)

# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("BooleanTrue(" + str(total) + ")Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# # Empty Object Return

# In[43]:


figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]

for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]== 'org.pitest.mutationtest.engine.gregor.mutators.returns.EmptyObjectReturnValsMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

values = total_values
total = values[0]

percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(values[3]+values[4])*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(values[3]+values[4])*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(values[5]+values[6])*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(values[5]+values[6])*100,1)) + "%)"
labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"   
    
 


# In[44]:


labels = ["<b>" + label + "<b>" for label in labels]
trace = go.Sankey(
    textfont = dict(size = 14),
    arrangement = "fixed",
    node = dict(
      pad = 40,
      thickness = 20,
      line = dict(color = "grey", width = 0.2),
      label = labels,
      color = ["#c9e3e8","red","green","red",
               "green","red","green","red",
               "green","red"],
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.45,  0.15,  0.55, 0.1, 0.2, 0.3, 0.7, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)

fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)
# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("EmptyObjectReturn(" + str(total) + ")Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)


# # PrimitiveReturn

# In[45]:



figure = make_subplots(rows=2, cols=5)
data = [0 for i in range(15)]
total_values = [0 for i in range(15)]
sum_df = 0
labels = ["start", "E", "NI", "I",
                   "NP", "P", "NP", "P",
                   "PS","FL"]

for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0
    df = pd.read_csv(base + ".csv")
    df = df[df["mutator"]== 'org.pitest.mutationtest.engine.gregor.mutators.returns.PrimitiveReturnsMutator']
    sum_df = sum_df + len(df)
    
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
    for i in range(len(values)):
        total_values[i] = total_values[i] +values[i]

values = total_values
total = values[0]

percentages = [v/total * 100 for v in values]
labels[2] = labels[2] + "(" + str(round(values[1]/total*100,1)) + "%)"
labels[3] = labels[3] + "(" + str(round((values[5] + values[6])/total*100,1)) + "%)"

labels[4] = labels[4] + "(" + str(round(values[3]/(values[3]+values[4])*100,1)) + "%)"
labels[5] = labels[5] + "(" + str(round(values[4]/(values[3]+values[4])*100,1)) + "%)"
labels[6] = labels[6] + "(" + str(round(values[5]/(values[5]+values[6])*100,1)) + "%)"
labels[7] = labels[7] + "(" + str(round(values[6]/(values[5]+values[6])*100,1)) + "%)"
labels[8] = labels[8] + "(" + str(round(p/total*100,1)) + "%)"
labels[9] = labels[9] + "(" + str(round(f/total*100,1)) + "%)"   
    
 


# In[46]:


labels = ["<b>" + label + "<b>" for label in labels]
trace = go.Sankey(
    textfont = dict(size = 14),
    arrangement = "fixed",
    node = dict(
      pad = 40,
      thickness = 20,
      line = dict(color = "grey", width = 0.2),
      label = labels,
      color = ["#c9e3e8","red","green","red",
               "green","red","green","red",
               "green","red"],
      x = [0, 0.15,   0.3,  0.3, 0.6, 0.6, 0.6, 0.6, 1,  1],
      y = [0, 0.45,  0.15,  0.55, 0.1, 0.25, 0.4, 0.7, 0.2,0.7],
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
    x=0.09,y = -0.15,
    xref='paper', yref='paper',
    text='Execution',
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
    x=1,y =  -0.15,
    xref='paper', yref='paper',
    text='Revealability',
    showarrow=False,
    font=dict( size=25 )

)

fig.add_annotation(
    x=-0.02,y = -0.15,
    xref='paper', yref='paper',
    text='Start',
    showarrow=False,
    font=dict( size=25 )

)

# fig.add_annotation(
#     x=1,y =  -0.1,
#     xref='paper', yref='paper',
#     text='Revealed',
#     showarrow=False,
#     font=dict( size=15 )

# )

# fig.add_annotation(
#     x=1,y =  -0.15,
#     xref='paper', yref='paper',
#     text='Propagation',
#     showarrow=False,
#     font=dict( size=15 )

# )
fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
fig.update_layout(
    font=dict(family='sans-serif')
)

fig.write_image("PrimitiveReturn(" + str(total) + ")Sankey" + ".pdf",scale = 2000/96)
fig.show()
#     data.append(trace)
#     figure.add_trace(trace,row = 1, col = 1)
#     break
# figure = go.Figure(data=data)

