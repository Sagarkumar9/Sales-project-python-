#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os


# ### Creating new file with all the data

# In[2]:


path = "F:\project\sales_python\Sales_Data"
files = [file for file in os.listdir(path) if not file.startswith('.')]

all_months_data = pd.DataFrame()

for file in files:
    current_data = pd.read_csv(path+"/"+file)
    all_months_data = pd.concat([all_months_data, current_data])
    
all_months_data.to_csv("all_data.csv", index=False)


# In[3]:


all_data = pd.read_csv("all_data.csv")
all_data.head()


# ### Cleaning data

# In[4]:


all_data.info()


# In[5]:


all_data.isnull().sum()


# In[ ]:


#545 NaN values in each column 


# In[6]:


#axis=1 means "operate along the columns" (i.e., apply the function across each row)(0 for rows and 1 for columns)
nans=all_data[all_data.isna().any(axis=1)]
nans.head()


# In[7]:


# this data with NaN is useless,it would be best to drop these

all_data= all_data.dropna(how = 'all')
all_data.head()


# In[8]:


temp_df=all_data[all_data['Order Date'].str[0:2]=='Or']
temp_df.head()
#it's getting duplicated throughout the data frame


# In[9]:


all_data=all_data[all_data['Order Date'].str[0:2] !='Or']


# #### converting columns to their correct dtype 

# In[10]:


all_data["Quantity Ordered"] = pd.to_numeric(all_data['Quantity Ordered'])
all_data['Price Each']=pd.to_numeric(all_data['Price Each'])


# #### Adding month column

# In[11]:


all_data['Month']=all_data["Order Date"].str[0:2]
all_data['Month']=all_data['Month'].astype('int32')
all_data.head()


# ### Q1-> What is the best month for sales? How much was earned that month? 

# #### adding another column for sales
# 

# In[12]:


all_data['Sales']=all_data["Quantity Ordered"]*all_data['Price Each']
all_data.head()


# In[13]:


# answer for Q1

all_data.groupby('Month').sum()


# In[14]:


a=all_data.groupby('Month').sum()


# In[15]:


a1= max(a['Sales'])
a1


# In[16]:


import matplotlib.pyplot as plt
month=range(1,13)
plt.xticks(month)
plt.bar(month,a['Sales'])
plt.xlabel('Months')
plt.ylabel("Sales")
plt.show()

#december made most sales


# ### Q2-> which city made highest  number of sales

# #### adding city column 

# In[17]:


def get_city(address):
    return address.split(',')[1]
def get_state(address):
    return address.split(',')[2].split(' ')[1]

all_data['city']= all_data['Purchase Address'].apply(lambda x: get_city(x)+'(' +get_state(x)+')')

all_data.head()


# In[18]:


a2=all_data.groupby('city').sum()
a2


# In[ ]:


#San Francisco has the highest sales


# In[19]:


cities=[city for city, df in all_data.groupby('city')]
plt.bar(cities,a2['Sales'])
plt.xticks(month,rotation='vertical',size=8)
plt.xlabel('cities')
plt.ylabel("Sales")
plt.show()


# ### Q3-> what time should we display advertisements to maximise likeihood of customer's buying the product?

# In[20]:


all_data['Order Date']=pd.to_datetime(all_data['Order Date'])


# In[21]:


all_data['hour']=all_data['Order Date'].dt.hour
all_data['min']=all_data['Order Date'].dt.minute
all_data['count']=1
all_data.head()


# In[22]:


hours=[hour for hour, df in all_data.groupby('hour')]

plt.plot(hours,all_data.groupby('hour').count())
plt.xticks(hours)
plt.xlabel('hours')
plt.ylabel('No. of orders')
plt.grid()
plt.show()


# #### 11am, 12 noon, 7pm are the best time to advertise bacause most orders are at that time

# ### Q4->what products are often sold together?

# In[ ]:


#there are duplicate order id value, so if the same person has ordered multiple time, same order id will be displayed


# In[23]:


df = all_data[all_data['Order ID'].duplicated(keep=False)]
df['grouped']=df.groupby('Order ID')['Product'].transform(lambda x: ','.join(x))
df=df[['Order ID','grouped']].drop_duplicates()
df.head()


# In[24]:


#now we need to count what occurs the most together
from itertools import combinations
from collections import Counter

count=Counter()
for row in df['grouped']:
    row_list=row.split(',')
    count.update(Counter(combinations(row_list,2))) #here u can change 2 to any num to see that no. of pairs.
count.most_common(15)
    


# In[ ]:


# iPhone, Lightning Charging Cable were brought 1005 times. Most pairs items brought in the dataset. 


# ### what product sold the most? Why do you think it was sold the most? 

# In[25]:


all_data.head()


# In[ ]:


product_grp=all_data.groupby('Product').sum()
quantity_ordered=product_grp.sum()['Quantity Ordered']

products = [product for product, df in product_grp]

plt.bar(products,quantity_ordered)
plt.xticks(products, rotation='vertical',size=8)


# In[42]:


x = all_data.groupby('Product').sum()
quantity_ordered = x['Quantity Ordered']

# Access product names from the DataFrame index
products = x.index

# Plot the bar chart
plt.bar(products, quantity_ordered)
plt.xticks(products, rotation='vertical', size=8)
plt.xlabel('Products')
plt.ylabel('products sold')
plt.show()


# In[51]:


prices = all_data.groupby('Product').mean()['Price Each']
fig,ax1=plt.subplots()
ax2=ax1.twinx()
ax1.bar(products, quantity_ordered,color='g')
ax2.plot(products,prices, 'b-')

ax1.set_xlabel('product name')
ax1.set_ylabel('quantity ordered',color='g')
ax2.set_ylabel('Price',color='b')
ax1.set_xticklabels(products,rotation='vertical',size=8)



# In[ ]:


#AAA battries made the most number of sales. There can be various reasons, it's cheap, it's used in most of the electronics like clocks, toys, torch, emergency light etc.

