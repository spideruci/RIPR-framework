#!/usr/bin/env python
# coding: utf-8

# In[4]:


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
import math
import os
import matplotlib.ticker as ticker
import matplotlib
import numpy as np
import matplotlib.ticker as mtick
matplotlib.rcParams['pdf.fonttype'] = 42
matplotlib.rcParams['ps.fonttype'] = 42
bases = ["commons-cli","commons-text","joda-money","jline-reader","commons-validator","cdk-data","spotify-web-api","commons-codec","jfreechart","dyn4j"]


# In[6]:


# fig, ax = plt.subplots(2,5,figsize = (50,10))
data_end = []
data_all = []
for index,base in enumerate(bases):
    
    df = pd.read_csv(base + ".csv")
    df = df[df["mutation_status"]=="SURVIVED"]
    num_killable_end = len(set(df[df["end_same"] == False]["m_id"]))
    num_killable_all = len(set(df[(df["end_same"] == False)
                                 | (df["middle_same"]==False)
                                 | (df["mr_return"] != df["nmr_return"])
                                 | (df["mr_athrow"] != df["nmr_athrow"])
                                 | (df["mr_exception"] != df["nmr_exception"])]["m_id"]))
    num_survive = len(set(df["m_id"]))
    
    data_end.append(num_killable_end/num_survive)
    data_all.append(num_killable_all/num_survive)
    

x = np.arange(len(bases))
# Create bars
bar_width = 0.4
plt.bar(x, data_end, width=bar_width, label='Propagation Kill')
plt.bar(x + bar_width, data_all, width=bar_width, label='Propagation or Infection Kill')
plt.xticks(x + bar_width / 2, bases)

plt.xticks(rotation=45,fontsize=8)
plt.legend()
plt.ylabel("Killable Surviving Mutants")
plt.savefig("RQ3.pdf", bbox_inches='tight')

