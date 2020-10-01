#!/usr/bin/env python
# coding: utf-8

# In[67]:


import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


# In[68]:


np.version


# In[69]:


confirmed_global_link="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
deaths_global_link="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
recovered_global_link="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
cases_country_link="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/web-data/data/cases_country.csv"


# In[70]:


confirmed_df=pd.read_csv(confirmed_global_link)
print(confirmed_df.shape)
deaths_df=pd.read_csv(deaths_global_link)
print(deaths_df.shape)
recovered_df=pd.read_csv(recovered_global_link)
print(recovered_df.shape)
cases_country_df=pd.read_csv(cases_country_link)
print(cases_country_df.shape)


# In[71]:


confirmed_df.columns


# In[72]:


cases_country_df.columns


# In[73]:


confirmed_df.head()


# In[74]:


confirmed_df[confirmed_df["Country/Region"]=="India"]


# In[75]:


confirmed_df[confirmed_df["Country/Region"]=="Australia"]


# In[76]:


confirmed_df["Country/Region"].nunique()


# In[77]:


# confirmed_df=confirmed_df.replace(np.nan,'',regex=True)
# deaths_df=deaths_df.replace(np.nan,'',regex=True)
# recovered_df=recovered_df.replace(np.nan,'',regex=True)
# cases_country_df=cases_country_df.replace(np.nan,'',regex=True)


# # Exploratory Analysis

# ### For Global Count

# In[78]:


global_data=cases_country_df.copy().drop(['Lat','Long_','Country_Region','Last_Update'],axis=1)
global_summary=pd.DataFrame(global_data.sum()).transpose()


# In[ ]:





# In[79]:


global_summary.style.format('{:,.0f}')


# ### Total Confirmed Corona Virus Cases(Global)

# In[80]:


confirmed_to=confirmed_df.copy().drop(['Lat','Long','Country/Region','Province/State'],axis=1)
confirmed_to_summary=confirmed_df.sum()
confirmed_to_summary


# In[81]:


fig_1=go.Figure(data=go.Scatter(x=confirmed_to_summary.index, y=confirmed_to_summary.values,mode='lines+markers'))
fig_1.update_layout(title="Total Confirmed Cases(Globally)",yaxis_title="Confirmed Cases", xaxis_tickangle=315)
fig_1.show()


# In[82]:


confirmed_agg_to=confirmed_df.copy().drop(['Lat','Long','Country/Region','Province/State'],axis=1).sum()
death_agg_to=deaths_df.copy().drop(['Lat','Long','Country/Region','Province/State'],axis=1).sum()
recovered_agg_to=recovered_df.copy().drop(['Lat','Long','Country/Region','Province/State'],axis=1).sum()



# In[ ]:





# ## To find active cases, active=confirmed-(death+recovered)

# #### since Active cases do not have timeseries data, therefore we need to do it in a diff way

# In[83]:


active_agg_to=pd.Series(
    data=np.array([x1-x2-x3 for (x1,x2,x3) in zip(confirmed_agg_to.values,death_agg_to.values,recovered_agg_to.values)]),
    index=confirmed_agg_to.index)


# In[84]:


import matplotlib.pyplot as plt
fig = plt.figure()
labels=["Confirmed","Death","Active","Recovered"]

i=0
for frame in [confirmed_agg_to, death_agg_to, active_agg_to, recovered_agg_to]:
   plt.plot(frame.index, frame.values,label=labels[i])
   i=i+1

    
plt.title("Covid-19 Case Status(22nd Jan to 29th Sept)")
plt.xlabel("Date")
plt.ylabel("Case Count")
# plt.xlim(1/24/2020,9/25/2020)
# plt.ylim(0,3500000)
plt.legend()

plt.show()


# In[85]:



fig = go.Figure()
dfs=[confirmed_agg_to,death_agg_to,active_agg_to,recovered_agg_to]
labels=["Confirmed","Death","Active","Recovered"]
i=0
for df in dfs:
    fig.add_trace(go.Scatter(x=df.index, y=df.values,mode='lines+markers',name=labels[i] ))
    i+=1
fig.update_layout(title="Global Analysis",yaxis_title="Cases", xaxis_tickangle=315)
fig.show()


# # Country Wise
# ### Sort according to Recovered

# In[88]:


cases_country_df.copy().drop(['Lat','Long_','Last_Update'],axis=1).sort_values('Recovered',ascending=False).reset_index(drop=True).style.bar(align="left",width=100,color="#d5678f")


# # Covid-19 India analysis

# In[90]:


confirmed_india_to=confirmed_df[confirmed_df["Country/Region"]=="India"].drop(['Lat','Long','Country/Region','Province/State'],axis=1).sum()
death_india_to=deaths_df[deaths_df["Country/Region"]=="India"].drop(['Lat','Long','Country/Region','Province/State'],axis=1).sum()
recovered_india_to=recovered_df[recovered_df["Country/Region"]=="India"].drop(['Lat','Long','Country/Region','Province/State'],axis=1).sum()
active_india_to=pd.Series(
    data=np.array([x1-x2-x3 for (x1,x2,x3) in zip(confirmed_india_to.values,death_india_to.values,recovered_india_to.values)]),
    index=confirmed_india_to.index)


# In[92]:


fig1 = go.Figure()
dfs=[confirmed_india_to,death_india_to,active_india_to,recovered_india_to]
labels=["Confirmed","Death","Active","Recovered"]
i=0
for df in dfs:
    fig1.add_trace(go.Scatter(x=df.index, y=df.values,mode='lines+markers',name=labels[i] ))
    i+=1
fig1.update_layout(title="India Analysis",yaxis_title="Cases", xaxis_tickangle=315)
fig1.show()


# ### Covid-19 Transmission Timeline in India 

# In[100]:


fig2 = go.Figure()
dfs=[confirmed_india_to[61:128],death_india_to[61:128],active_india_to[61:128],recovered_india_to[61:128]]
labels=["Confirmed","Death","Active","Recovered"]
i=0
for df in dfs:
    fig2.add_trace(go.Scatter(x=df.index, y=df.values,mode='lines+markers',name=labels[i] ))
    i+=1
fig2.update_layout(title="Semi-Log Plot of India Analysis during Lockdown",yaxis_title="Cases", xaxis_tickangle=315,yaxis_type="log")
fig2.show()


# In[101]:


fig3 = go.Figure()
dfs=[confirmed_india_to[130:],death_india_to[130:],active_india_to[130:],recovered_india_to[130:]]
labels=["Confirmed","Death","Active","Recovered"]
i=0
for df in dfs:
    fig3.add_trace(go.Scatter(x=df.index, y=df.values,mode='lines+markers',name=labels[i] ))
    i+=1
fig3.update_layout(title="Semi-Log Plot of India Analysis After Lockdown",yaxis_title="Cases", xaxis_tickangle=315,yaxis_type="log")
fig3.show()


# In[116]:


statewise_test_df=pd.read_csv("StatewiseTestingDetails.csv")


# In[117]:


statewise_test_df.head()


# In[105]:


covid_19_india_df=pd.read_csv("covid_19_india.csv")


# In[106]:


covid_19_india_df.head()


# In[107]:


hospital_beds_df=pd.read_csv("COVID-19 in India/HospitalBedsIndia.csv")


# In[109]:


ICMR_testing_labs_df=pd.read_csv("COVID-19 in India/ICMRTestingLabs.csv")
age_group_df=pd.read_csv("COVID-19 in India/AgeGroupDetails.csv")


# In[110]:


labels = list(age_group_df['AgeGroup'])
sizes = list(age_group_df['TotalCases'])

explode = []

for i in labels:
    explode.append(0.05)
    
plt.figure(figsize= (15,10))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=9, explode =explode)
centre_circle = plt.Circle((0,0),0.70,fc='white')

fig = plt.gcf()
fig.gca().add_artist(centre_circle)
plt.title('India - Age Group wise Distribution',fontsize = 20)
plt.axis('equal')  
plt.tight_layout()


# ### We could see that the age group <40 is the most affected which is against the trend which says elderly people are more at risk of being affected. Only 17% of people >60 are affected.

# In[111]:


individual_details_df=pd.read_csv("COVID-19 in India/IndividualDetails.csv")


# In[113]:


labels = ['Missing', 'Male', 'Female']
sizes = []
sizes.append(individual_details_df['gender'].isnull().sum())
sizes.append(list(individual_details_df['gender'].value_counts())[0])
sizes.append(list(individual_details_df['gender'].value_counts())[1])

explode = (0, 0.1, 0)
colors = ['#ffcc99','#66b3ff','#ff9999']

plt.figure(figsize= (15,10))
plt.title('Percentage of Gender',fontsize = 20)
plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',shadow=True, startangle=90)
plt.axis('equal')
plt.tight_layout()


# In[118]:


state_cases =covid_19_india_df.groupby('State/UnionTerritory')['Confirmed','Deaths','Cured'].max().reset_index()

#state_cases = state_cases.astype({'Deaths': 'int'})
state_cases['Active'] = state_cases['Confirmed'] - (state_cases['Deaths']+state_cases['Cured'])
state_cases["Death Rate (per 100)"] = np.round(100*state_cases["Deaths"]/state_cases["Confirmed"],2)
state_cases["Cure Rate (per 100)"] = np.round(100*state_cases["Cured"]/state_cases["Confirmed"],2)
state_cases.sort_values('Confirmed', ascending= False).fillna(0).style.background_gradient(cmap='Blues',subset=["Confirmed"])                        .background_gradient(cmap='Blues',subset=["Deaths"])                        .background_gradient(cmap='Blues',subset=["Cured"])                        .background_gradient(cmap='Blues',subset=["Active"])                        .background_gradient(cmap='Blues',subset=["Death Rate (per 100)"])                        .background_gradient(cmap='Blues',subset=["Cure Rate (per 100)"])


# In[126]:


import seaborn as sns
statewise_df=statewise_test_df.groupby(statewise_test_df["State"]).sum()
statewise_df.head()


# In[ ]:





# In[ ]:




