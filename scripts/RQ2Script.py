#!/usr/bin/env python
# coding: utf-8

# In[9]:


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
import matplotlib.ticker as mticker
bases = ["commons-cli","commons-text","joda-money","jline-reader","commons-validator","cdk-data","spotify-web-api","commons-codec","jfreechart","dyn4j"]
for index,base in enumerate(bases):

    df = pd.read_csv(base + ".csv")
    non_return = df[~df["mutator"].str.contains("return")]
    x = len(non_return)
    non_return = non_return[non_return["test_status"]=="fail"]

    anomaly = non_return[ (non_return["mr_exception"]!= non_return["nmr_exception"])
               |(non_return["mr_athrow"]!= non_return["nmr_athrow"])
               |(non_return["mr_return"]!= non_return["nmr_return"])]
    athrow = anomaly[anomaly["mr_athrow"]==1]
    
    a = x
    failings = len(non_return)
    b = len(anomaly)/len(non_return)
    c = len(athrow)/len(anomaly)
    
    print(f"{base:<18}"  
          + f"{a:10,} "   
          + f"{failings:10,} ({failings/a * 100:6.2f}%) "  
          + f"{len(anomaly):10,} ({b * 100:6.2f}%) "
          + f"{len(athrow):10,} ({c * 100:6.2f}%)")

