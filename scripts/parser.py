#!/usr/bin/env python
# coding: utf-8

# In[6]:


import os
import hashlib
import pickle
import zipfile


# In[7]:


def is_same_NMR(l):
     return all(x == l[0] for x in l)
    
def compute_hash(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        hash = hashlib.sha256(content).hexdigest()
        return hash
    
def compute_hash_in_zip(file_path):
    with zip_ref.open(file_path, 'r') as file:
        content = file.read()
        hash = hashlib.sha256(content).hexdigest()
        return hash
    
def get_first_level_directories(path):
    first_level_dirs = []
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_dir():
                first_level_dirs.append(entry.name)
    return first_level_dirs

def get_all_file_paths(path):
    files = []
    for filename in os.listdir(path):
        if os.path.isfile(os.path.join(path, filename)) and filename !='.DS_Store':
            files.append(os.path.join(path,filename))
    return files

def get_first_level_files(path):
    first_level_files = []
    with os.scandir(path) as entries:
        for entry in entries:
            if entry.is_file():
                first_level_files.append(entry.name)
    return first_level_files

def count_temp_xml_files(path):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('temp.xml'):
                count += 1
    return count

def read_text_file_from_zip_line_by_line(file_name):   
    with zip_ref.open(file_name, 'r') as file:
            lines = file.readlines()
    lines = [line.decode().strip() for line in lines]
    return lines


# In[8]:



NS_data = {}
processed = []
unprocessed = []
for progress,MR_path in enumerate(get_all_file_paths("target/everything")):
    try:

        processed.append(progress)
        if progress % 100 == 0:
            print("processed " + str(progress) + "mutations")
        m_data = {}
        with zipfile.ZipFile(MR_path,'r') as zip_ref:
            # 1. testInfo
            lines = read_text_file_from_zip_line_by_line("testInfo.txt")
            m_data["test_info"] = []
            for line in lines:
                t_info = "".join(line.split(" ")[1:])
                t_info = t_info.strip()
                m_data["test_info"].append(t_info)

            # 2. mutation_status
            lines = read_text_file_from_zip_line_by_line("status.txt")
            m_data["status"] = lines[0].strip()
            if m_data["status"]=="NON_VIABLE":
                print("ha")
                continue


            # 3. killing Tests
            lines = read_text_file_from_zip_line_by_line("killingTests.txt")
            m_data["killing_tests"] = []
            for index, line in enumerate(lines):
                temp = line.strip().split(" ")
                temp = [_.strip() for _ in temp]
                t = "".join(temp)

                # validate it ? need correction

                # handle parameterized test failure which fails when fetching parameters
                try:
                    k_index = m_data["test_info"].index(t)
                    m_data["killing_tests"].append(t)
                except:
    #                     if ("test-template-invocation") not in t:
                    for t_info in m_data["test_info"]:
                        if t in t_info and t_info not in m_data["killing_tests"]:
                            m_data["killing_tests"].append(t_info)

            # 4. failing reasons
            lines = read_text_file_from_zip_line_by_line("failingReasons.txt")
            m_data["failing_reasons"] = []
            for line in lines:
                m_data["failing_reasons"].append(line)
    #                 m_data["failing_reasons"].append(line.split(":")[0])

            # 5. mutation_info
            lines = read_text_file_from_zip_line_by_line("mutationInfo.txt")
            m_data["MR_NMR"] = []
            m_data["mutation_info"] = lines[0].split(" ")[0].strip()," ".join(lines[0].split(" ")[1:]), lines[1].strip()

            # 6. MRs

            lines = read_text_file_from_zip_line_by_line("MRs.txt")
            lines_len = read_text_file_from_zip_line_by_line("MRlens.txt")

            for index, line in enumerate(lines):
                test_info = {}
                # len
                l1,l2 = lines_len[index].split(" ")
                l2 = l2.strip()

                b1, b2, b3, b4, b5 = line.split(" ")
                b5 = b5.strip()
                # states are dumped 
                test_info["MR_state_middle"] = {}

                # fix it later
                temp_p = "MR/" + str(index) + "/temp.xml"
                if temp_p in zip_ref.namelist():
    #             if b5 == "1":
                    test_info["MR_state_middle"]["hash"] = compute_hash_in_zip(temp_p)
                    line = read_text_file_from_zip_line_by_line("MR/" + str(index) + "/stateInfo.txt")[0]
                    test_info["MR_state_middle"]["state_bits"] = line

                test_info["MR_state_after"] = {}
                if 'MR/' + str(index) + "/AfterAll.xml" in zip_ref.namelist():

                    # we assume that if AfterAll.xml exist, AfterAllStatic exist
                    temp_p = "MR/" + str(index)
                    test_info["MR_state_after"]["path"] = [temp_p + "/AfterAll.xml",
                                                           temp_p + "/AfterAllStatic.xml"] 
                    test_info["MR_state_after"]["hash"] = [compute_hash_in_zip(temp_p + "/AfterAll.xml"),
                                                           compute_hash_in_zip(temp_p + "/AfterAllStatic.xml")]
                else:
                    test_info["MR_state_after"] = None


                if m_data["test_info"][index] in m_data["killing_tests"]:
                    test_info["test_state"] = "fail"
                else:
                    test_info["test_state"] = "pass"

                test_info["MR_state_middle"]["probes"] = [b1,b2,b3,b4,b5]
                test_info["MR_len"] = [l1,l2]
                m_data["MR_NMR"].append(test_info)


            # 7. NMRs
            lines = read_text_file_from_zip_line_by_line("NMRs.txt")
            lines_len = read_text_file_from_zip_line_by_line("NMRlens.txt")
            num_tests = len(m_data["test_info"])
            for t_id in range(num_tests):

                test_info = m_data["MR_NMR"][t_id]

                test_info["NMRs"] = []
                NMR_bits = lines[t_id::num_tests]
                len_info = lines_len[t_id::num_tests]
                new_bits = []
                lens = []
                for line in NMR_bits:
                    b1,b2 = line.split(" ")
                    b2 = b2.strip()
                    new_bits.append([b1,b2])
                for line in len_info:
                    l = line.strip()
                    lens.append(l)


                for index, temp in enumerate(new_bits):
                    NMR_test_run = {}
                    NMR_test_run["NMR_state_middle"] = {"probes":temp}
                    NMR_test_run["NMR_state_after"] = {}
                    NMR_test_run["NMR_len"] = lens[index]
                    dumped = temp [1]
                    temp_p = "NMR/" + str(t_id) + "/" + str(index)

    #                 if dumped == "1":
                    # fix it later
                    if temp_p + "NMR.xml" in zip_ref.namelist():
                        NMR_test_run["NMR_state_middle"]["path"] = temp_p + "NMR.xml"
                        NMR_test_run["NMR_state_middle"]["hash"] = compute_hash_in_zip(temp_p + "NMR.xml")
                        line = read_text_file_from_zip_line_by_line(temp_p + "stateInfo.txt")[0]
                        NMR_test_run["NMR_state_middle"]["state_bits"] = line

                    if temp_p + "AfterAll.xml" in zip_ref.namelist():
                        NMR_test_run["NMR_state_after"]["path"] = [temp_p + "AfterAll.xml",
                                                                   temp_p + "AfterAllStatic.xml"]
                        NMR_test_run["NMR_state_after"]["hash"] = [compute_hash_in_zip(temp_p + "AfterAll.xml"),
                                                                   compute_hash_in_zip(temp_p + "AfterAllStatic.xml")]

                    test_info["NMRs"].append(NMR_test_run)


        m_id = MR_path.split("/")[2][:-4]
        NS_data[m_id] = m_data
    except:
        unprocessed.append(MR_path)
        


# In[10]:


with open('hash_data.pickle', 'wb') as f:
    pickle.dump(NS_data, f)
    

with open('hash_data.pickle', 'rb') as f:
    data = pickle.load( f)
    
excludes = set()
try:
    with open("target/failingInOriginal.txt") as f:
        lines = f.read().split("\n")
    for line in lines[:-1]:
        mutation = line.split(" ")[1]
        test_name = line.split(" ")[3]
        excludes.add((mutation, test_name))
except:
    pass


result = {}
num_e = 0
num1 = 0
num2 = 0
num3 = 0
num4 = 0
num5 = 0
process = 0
for key, content in data.items():
    
    process += 1
    result[key] ={}
    result[key]["mutation_info"] = content["mutation_info"][0]
    result[key]["mutation_status"] = content["status"]
    result[key]["tests"] = {}
    for test_name in content["test_info"]:
        result[key]["tests"][test_name] ={"state": "pass"}

    for index,test_name in enumerate(content["killing_tests"]):
        flag = False

        reason = content["failing_reasons"][index]
        for t_id in result[key]["tests"]:
            if test_name in t_id:
                result[key]["tests"][t_id]["state"] = "fail"
                flag = True                
                if 'junit' in reason or "mockito" in reason or "assertj" in reason:
                    result[key]["tests"][t_id]["failing_reason"] = "test_assertion"
                else:
                    result[key]["tests"][t_id]["failing_reason"] = "others"
                flag = True
        if not flag:
            raise Exception("there is something wrong in labeling failing tests")
            
    temp = content["MR_NMR"]
    for index,t in enumerate(temp):
        # 1. fail to cover the mutation
        if t["MR_state_middle"]["probes"][0]!='1':
            result[key]["tests"][content["test_info"][index]] =None
            num_e += 1
            num1 +=1
            continue
        # 2. middle state diff
        _ = t["NMRs"]
        isSame = True
        if "hash" in _[0]["NMR_state_middle"]:
            hashes = [t["NMR_state_middle"]["hash"] for t in _]
            # middle states are not always collected
            if len(hashes) != 10:
                isSame = False
            for i in hashes:
                if i != hashes[0]:
                    isSame = False
        else:
            # fail to collet middle state
            isSame = False
        if not isSame:
            num2 +=1
            num_e += 1
            result[key]["tests"][content["test_info"][index]] =None
            continue
        # 3. end state diff

        isSame = True
        if "hash" in _[0]["NMR_state_after"]:
            hashes = [t["NMR_state_after"]["hash"] for t in _]
            if len(hashes) != 10:
                isSame = False
            for i,j in hashes:
                if i != hashes[0][0] or j!= hashes[0][1]:
                    isSame = False
        else:
            isSame = False
        if not isSame:
            num_e += 1
            num3+=1
            result[key]["tests"][content["test_info"][index]] =None
            continue
                    
        # 4.probe info diff                    
        r = [r["NMR_state_middle"]["probes"] for r in _]
        if len(r) != 10:
            raise Exception("probe info collection error")
        isSame = True
        for i,j in r:
            if i!=r[0][0] or j!=r[0][1]:
                isSame = False
        if not isSame:
            num_e += 1
            num4 += 1
            result[key]["tests"][content["test_info"][index]] =None
            continue
            
        # 5. excludes = set()
        if (key,content["test_info"][index]) in excludes:
            result[key]["tests"][content["test_info"][index]] =None
            num5 += 1
            num_e += 1
            continue

      
        ####################collect results########################
        result[key]["tests"][content["test_info"][index]]["MR_probes"] = t["MR_state_middle"]["probes"]
        
        result[key]["tests"][content["test_info"][index]]["NMR_probes"] = t["NMRs"][0]["NMR_state_middle"]["probes"]
        
        MR_states = [None, None, None, None]
        NMR_states = [None, None, None, None]
  
        #MR
        if "hash" in t["MR_state_middle"]:
     
            MR_states[0] = t["MR_state_middle"]["hash"]
            MR_states[3] = t["MR_state_middle"]["state_bits"]
        if t["MR_state_after"] == None:
            num2+=1
            num_e += 1
            result[key]["tests"][content["test_info"][index]] =None
            continue
        if "hash" in t["MR_state_after"]:
            MR_states[1] = t["MR_state_after"]["hash"][0]
            MR_states[2] = t["MR_state_after"]["hash"][1]
        
        
        if "hash" in t["NMRs"][0]["NMR_state_middle"]:
            NMR_states[0] = t["NMRs"][0]["NMR_state_middle"]["hash"]
            NMR_states[3] = t["NMRs"][0]["NMR_state_middle"]["state_bits"]
        if "hash" in t["NMRs"][0]["NMR_state_after"]:
            NMR_states[1] = t["NMRs"][0]["NMR_state_after"]["hash"][0]
            NMR_states[2] = t["NMRs"][0]["NMR_state_after"]["hash"][1]
        
        result[key]["tests"][content["test_info"][index]]["MR_states"] = MR_states
        result[key]["tests"][content["test_info"][index]]["NMR_states"] = NMR_states
        result[key]["tests"][content["test_info"][index]]["MR_len"] = t["MR_len"]
        result[key]["tests"][content["test_info"][index]]["NMR_len"] = [i["NMR_len"] for i in t["NMRs"]]
        
#         if "hash" in t["NMRs"][0]["NMR_state_middle"])


# In[11]:


import csv
num_e1 = 0

# Create the data to be written to the file
head = ["m_id", "mutation_status", "mutator","test_name","test_status", 
        "mr_m_1st","mr_m_all", "mr_e", "nmr_m_all",
        "middle_same","end_same",
        "mr_return","mr_athrow","mr_exception","mr_this","mr_args","mr_static",
        "nmr_return","nmr_athrow","nmr_exception","nmr_this","nmr_args","nmr_static",
        "MR_len_before","MR_len_after","NMR_len_same","NMR_len_avg","len_ratio","failing_reason"]

# Open the file for writing
with open("hashResult.csv", "w", newline="") as f:
    # Create a CSV writer
    writer = csv.writer(f)
    # Write the rows to the file
    writer.writerow(head)
    
    for key, content in result.items():

        m_id = key
        mutator = content["mutation_info"]
        mutation_status = content["mutation_status"]

        for test_name, t in content["tests"].items():

            if t == None:
                num_e1 += 1
                continue
            
            failing_reason = "unknown"
            if "failing_reason" in t:
                failing_reason = t["failing_reason"]
                
            test_status = t["state"]
            # probe info
            MR_probes = t["MR_probes"]
            MR_m_1st= int(MR_probes[1])
            MR_m_all = int(MR_probes[2])
            MR_e = int(MR_probes[3])
            
            NMR_probes = t["NMR_probes"]
            NMR_m_all = int(NMR_probes[0])

            # state info
            MR_middle = t["MR_states"][0]
            MR_end = t["MR_states"][1]
            MR_end_static = t["MR_states"][2]
            NMR_middle = t["NMR_states"][0]
            NMR_end = t["NMR_states"][1]
            NMR_end_static = t["NMR_states"][2]
            middle_same = MR_middle == NMR_middle
            end_same = (MR_end == NMR_end) & (NMR_end_static == NMR_end_static)
            
            #len info

            # how states in the middle are organized
            # numReturn + " " + numAthrow + numUnexpectedException + " " + numThis+ " " + numArgs + " " + numStatic;
            if(t["MR_states"][3] != None):
                MR_state_bits = t["MR_states"][3].split(" ")
                MR_return = int(MR_state_bits[0])
                MR_athrow = int(MR_state_bits[1]) 
                MR_exception = int(MR_state_bits[2])
                MR_this = int(MR_state_bits[3])
                MR_args = int(MR_state_bits[4])
                MR_static = int(MR_state_bits[5])
            else:
                MR_return, MR_athrow, MR_exception, MR_this, MR_args, MR_static = -1,-1,-1,-1,-1,-1
            
            NMR_state_bits = t["NMR_states"][3].split(" ")
            NMR_return = int(NMR_state_bits[0])
            NMR_athrow = int(NMR_state_bits[1]) 
            NMR_exception = int(NMR_state_bits[2])
            NMR_this = int(NMR_state_bits[3])
            NMR_args = int(NMR_state_bits[4])
            NMR_static = int(NMR_state_bits[5])
            
            #len
            MR_len_before = int(t["MR_len"][0])
            MR_len_after = int(t["MR_len"][1])
            same = True
            for i in t["NMR_len"]:
                if i != t["NMR_len"][0]:
                    same = False
            NMR_len_same = same

            assert len(t["NMR_len"])==10
            NMR_len_avg = sum([int(i) for i in t["NMR_len"]])/len(t["NMR_len"])
            len_ratio = (MR_len_after + 1 - MR_len_before)/(NMR_len_avg - MR_len_before+1)
            if (len(t["NMR_len"]) == 0) :
                print(len(t["NMR_len"]))
            if (len_ratio<0):
                print(key)
                print(len_ratio)
                
                print(NMR_len_avg)
                print(MR_len_before)
                print(MR_len_after)
            assert len_ratio > 0
           
            
            row = [m_id, mutation_status, mutator,test_name, test_status,
                   # probe info
                   MR_m_1st, MR_m_all, MR_e, NMR_m_all, 
                   # state info
                   middle_same, end_same,
                   # state bits
                   MR_return, MR_athrow, MR_exception, MR_this, MR_args, MR_static,
                   NMR_return, NMR_athrow,  NMR_exception, NMR_this, NMR_args, NMR_static,
                   MR_len_before,MR_len_after,NMR_len_same,NMR_len_avg,len_ratio,failing_reason]

            writer.writerow(row)

assert(num_e1 == num_e)


# In[12]:


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


# In[16]:


lg = "#c5edc5"
lr = "#efc6c6"
bases = ["hashResult"]


# In[26]:


figure = make_subplots(rows=1, cols=1)
data = []

for index,base in enumerate(bases):
    a = index % 5
    if index // 5:
        b = 0.5
    else:
        b = 0

    df = pd.read_csv(base + ".csv")

    
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
    
    labels = ["start", "execution",       "infected",
                         "propagated",
                       "pass","fail"]
    values = [len(df), len(middle_diff),len(middle_diff_end_diff),
                  len(middle_diff_end_diff[middle_diff_end_diff["test_status"] == "pass"]),
                  len(middle_diff_end_diff[middle_diff_end_diff["test_status"] == "fail"])]
    total = sum(values)
    percentages = [v/total * 100 for v in values]
    
    labels[0] = labels[0] + "(" + str(len(df)) + " test runs)"
    labels[2] = labels[2] + "(" + str(round(len(middle_diff)/len(df)*100,1)) + "%)"

    if len(middle_diff_end_diff) == 0:
        labels[3] = labels[3] + "(0%)" 
    else:
        labels[3] = labels[3] + "(" + str(round(len(middle_diff_end_diff)/len(middle_diff)*100,1)) + "%)"
    
    
    trace = go.Sankey(
        arrangement = "fixed",
        node = dict(
          pad = 40,
          thickness = 20,
          line = dict(color = "grey", width = 0.2),
          label = labels,
          color = ["#c9e3e8","red","red","red",
                   "green","red"]

        ),
        link = dict(
          source = [0,1,2,3,3], # indices correspond to labels, eg A1, A2, A1, B1, ...
          target = [1,2,3,4,5],
          value = values,
                color = [lg,lr,lr,
                         "green","red"],
                label=[f"{p:.1f}%" for p in percentages]))
    fig = go.Figure(data=[trace],)
    fig.add_annotation(
        x=0.125,y = -0.1,
        xref='paper', yref='paper',
        text='Execution',
        showarrow=False,
        font=dict( size=15 )

    )
    
    fig.add_annotation(
        x=0.275,y =  -0.1,
        xref='paper', yref='paper',
        text='Infection',
        showarrow=False,
        font=dict( size=15 )
    

    )
        
    fig.add_annotation(
        x=0.8,y =  -0.1,
        xref='paper', yref='paper',
        text='Propagation',
        showarrow=False,
        font=dict( size=15 )

    )
    fig.update_layout( font_size=10, margin=dict(l=20, r=20, t=60, b=60))
    fig.update_layout(
        font=dict(family='sans-serif')
    )
    
    fig.write_image(str(index) + "sankey" + ".png",scale = 2000/96)
    fig.show()


