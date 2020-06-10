# -*- coding: utf-8 -*-
"""
Created on Sat Apr 18 22:40:04 2020

@author: micha
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import seaborn as sns
import matplotlib.patches as patches
import warnings
from IPython.display import clear_output
import time
warnings.filterwarnings('ignore')
plt.rcParams['figure.figsize'] = [10, 10]
plt.style.use('ggplot')
popdata=pd.read_excel('Population Data.xlsx',sheet_name='Sheet2')
storedata=pd.read_excel('Store Data.xlsx')
schooldata=pd.read_excel('School Data.xlsx')

num_stores=int(sum(storedata['Totals']))
area_width=100
area_height=100
avg_household=2.5
percent_kids=30
percent_adults=70
percent_old=20
run_scale=0.01
num_households=int(sum(popdata['Number of Households'])*run_scale)

def select_school(schools,xloc,yloc,county):
    dist=pd.DataFrame(columns=['School_ID','Distance'])
    sch=schools[schools['County']==county]
    dist['School_ID']=sch['School_ID']
    dist['Distance']=np.power(np.square((np.array(sch['Location X'])-xloc))+np.square((np.array(sch['Location Y'])-yloc)),0.5)
#    val=random.uniform(0,1)
#    proximity_factor=0.9
#    if val<=proximity_factor:
    school=int(dist.loc[dist['Distance']==min(dist['Distance']),'School_ID'])
#    else:
#        school=sch['School_ID'].values[random.randrange(1,sch.shape[0]-1, 1)]
    
    return school

def select_store(typ,xloc,yloc):
    global stores
    dist=pd.DataFrame(columns=['Store_ID','Distance'])
    stor=stores[stores['Type']==typ]
    dist['Store_ID']=stor['Store_ID']
    dist['Distance']=np.power(np.square((np.array(stor['Location X'])-xloc))+np.square((np.array(stor['Location Y'])-yloc)),0.5)
    val=random.uniform(0,1)
    proximity_factor=0.9
    if val<=proximity_factor:
        store=int(dist.loc[dist['Distance']==min(dist['Distance']),'Store_ID'])
    else:
        store=random.randrange(1,stores.shape[0], 1)
    return store

def select_friend(households,ID):
    dist=pd.DataFrame(columns=['Household','Distance'])
    dist['Household']=households['Household_ID']
    xloc=float(households.loc[households['Household_ID']==ID,'Location X'])
    yloc=float(households.loc[households['Household_ID']==ID,'Location Y'])
    dist['Distance']=np.power(np.square((np.array(households['Location X'])-xloc))+np.square((np.array(households['Location Y'])-yloc)),0.5)
    dist=dist.sort_values(by='Distance',ascending=True)
    val=random.uniform(0,1)
    if val<0.9:
        index=random.randrange(0,19, 1)
        friend=dist.iloc[index,0]
    else:
        index=random.randrange(0,households.shape[0]-1, 1)
        friend=dist.iloc[index,0]

    return friend

def select_work(workplaces,xloc,yloc,travel_time):
    dist=pd.DataFrame(columns=['Workplace_ID','Distance'])
    dist['Workplace_ID']=workplaces['Workplace_ID']
    dist['Distance']=np.power(np.square((np.array(workplaces['Location X'])-0))+np.square((np.array(workplaces['Location Y'])-0)),0.5)
    dist=dist[dist['Distance']<=0.3]
    workplace=dist['Workplace_ID'].values[random.randrange(1,dist.shape[0]-1, 1)]
    
    return workplace

county_info=pd.DataFrame(columns=['ID','Name','State','Shift X', 'Shift Y']) 
county_info['ID']=range(20) 
county_info['Name']=['Hamilton','Butler','Warren','Clermont','Clinton','Brown','Highland','Adams','Boone','Kenton','Campbell','Grant','Pendleton','Bracken','Gallatin','Switzerland','Ohio','Dearborn','Ripley','Franklin'] 
county_info['State']=['Ohio','Ohio','Ohio','Ohio','Ohio','Ohio','Ohio','Ohio','Kentucky','Kentucky','Kentucky','Kentucky','Kentucky','Kentucky','Kentucky','Indiana','Indiana','Indiana','Indiana','Indiana'] 
county_info['Shift X']=[0,1,1,0,2,2,3,3,0,1,2,0,1,2,-1,-2,-1,-1,-2,-1] 
county_info['Shift Y']=[0,0,1,1,1,0,1,0,-1,-1,-1,-2,-2,-2,-2,-1,-1,0,0,1]

print('Creating Stores')
global stores
stores=pd.DataFrame(columns=['Store_ID','County','Type','Location X','Location Y'])
stores['Store_ID']=range(num_stores)
index=0
for county in county_info['Name']:
    shiftx=int(county_info.loc[county_info['Name']==county,'Shift X'])
    shifty=int(county_info.loc[county_info['Name']==county,'Shift Y'])
    for _ in range(int(storedata.loc[storedata['County']==county,'Grocery'])):
        stores.loc[stores['Store_ID']==index,'Type']='Grocery'
        stores.loc[stores['Store_ID']==index,'County']=county
        stores.loc[stores['Store_ID']==index,'Location X']=shiftx+random.uniform(0,1)
        stores.loc[stores['Store_ID']==index,'Location Y']=shifty+random.uniform(0,1)
        index+=1
    for _ in range(int(storedata.loc[storedata['County']==county,'Supercenter'])):
        stores.loc[stores['Store_ID']==index,'Type']='Supercenter'
        stores.loc[stores['Store_ID']==index,'County']=county
        stores.loc[stores['Store_ID']==index,'Location X']=shiftx+random.uniform(0,1)
        stores.loc[stores['Store_ID']==index,'Location Y']=shifty+random.uniform(0,1)
        index+=1
    for _ in range(int(storedata.loc[storedata['County']==county,'Convenience'])):
        stores.loc[stores['Store_ID']==index,'Type']='Convenience'
        stores.loc[stores['Store_ID']==index,'County']=county
        stores.loc[stores['Store_ID']==index,'Location X']=shiftx+random.uniform(0,1)
        stores.loc[stores['Store_ID']==index,'Location Y']=shifty+random.uniform(0,1)
        index+=1
        
print('Setting up Schools')
schools=pd.DataFrame(columns=['School_ID', 'Location X', 'Location Y','County','State'])
schools['School_ID']=range(sum(schooldata['Schools Scaled']))
index=0

for county in county_info['Name']:
    shiftx=int(county_info.loc[county_info['Name']==county,'Shift X'])
    shifty=int(county_info.loc[county_info['Name']==county,'Shift Y'])
    state=county_info.loc[county_info['Name']==county,'State']
    for _ in range(int(schooldata.loc[schooldata['County']==county,'Schools Scaled'])):
        schools.loc[schools['School_ID']==index,['Location X']]=shiftx+random.uniform(0,1)
        schools.loc[schools['School_ID']==index,['Location Y']]=shifty+random.uniform(0,1)
        schools.loc[schools['School_ID']==index,['County']]=county
        schools.loc[schools['School_ID']==index,['State']]=state
        index+=1

print('Finding Workplaces')        
workplaces=pd.DataFrame(columns=['Workplace_ID', 'Location X', 'Location Y','County','State'])
workplaces['Workplace_ID']=range(sum(popdata['Num Workplaces']))
index=0
for county in county_info['Name']:
    shiftx=int(county_info.loc[county_info['Name']==county,'Shift X'])
    shifty=int(county_info.loc[county_info['Name']==county,'Shift Y'])
    state=county_info.loc[county_info['Name']==county,'State'].max()
    for _ in range(int(popdata.loc[popdata['County']==county,'Num Workplaces'])):
        workplaces.loc[workplaces['Workplace_ID']==index,['Location X']]=shiftx+random.uniform(0,1)
        workplaces.loc[workplaces['Workplace_ID']==index,['Location Y']]=shifty+random.uniform(0,1)
        workplaces.loc[workplaces['Workplace_ID']==index,['County']]=county
        workplaces.loc[workplaces['Workplace_ID']==index,['State']]=state
        index+=1

print('Determining Households')        
households=pd.DataFrame(columns=['Household_ID', 'Location X', 'Location Y', 'Num People','County','State','School','Grocery','Supercenter','Convenience','Work'])
households['Household_ID']=range(num_households)
index=0

for county in county_info['Name']:
    shiftx=int(county_info.loc[county_info['Name']==county,'Shift X'])
    shifty=int(county_info.loc[county_info['Name']==county,'Shift Y'])
    state=county_info.loc[county_info['Name']==county,'State'].max()
    num_hh=int(popdata.loc[popdata['County']==county,'Number of Households']*run_scale)
    print(county)
    print(num_hh)
    for num in range(num_hh):
        x_location=shiftx+random.uniform(0,1)
        households.loc[households['Household_ID']==index,['Location X']]=x_location
        y_location=shifty+ random.uniform(0,1)
        households.loc[households['Household_ID']==index,['Location Y']]=y_location
        households.loc[households['Household_ID']==index,['County']]=county
        households.loc[households['Household_ID']==index,['State']]=state
        households.loc[households['Household_ID']==index,['Num People']]=random.randrange(1, avg_household*2, 1)
        households.loc[households['Household_ID']==index,['School']]=select_school(schools,x_location,y_location,county)
        households.loc[households['Household_ID']==index,['Work']]=select_work(workplaces,x_location,y_location,float(popdata.loc[popdata['County']==county,'Travel Time']))
        households.loc[households['Household_ID']==index,['Grocery']]=select_store('Grocery',x_location,y_location)
        households.loc[households['Household_ID']==index,['Supercenter']]=select_store('Supercenter',x_location,y_location)
        households.loc[households['Household_ID']==index,['Convenience']]=select_store('Convenience',x_location,y_location)
        index+=1

households=households.dropna(thresh=3)

print('Finding Friends...')
friends=pd.DataFrame(columns=['Household','0','1','2','3','4'])
friends['Household']=households['Household_ID']
for household in households['Household_ID']:
    for col in range(5):
        friend=select_friend(households,household)
        friends.loc[households['Household_ID']==household,str(col)]=friend
        
#%%
print('Building Population...')         
global people
people=pd.DataFrame(columns=['Person_ID','Household_ID','State','County','Location X', 'Location Y','Household X','Household Y','School ID','School X','School Y','Workplace_ID','Work X','Work Y','Age','Sex','Infected_State'])
people['Person_ID']=range(sum(households['Num People']))
index=0
for household in households['Household_ID']:
    sch=int(households.loc[households['Household_ID']==household,'School'])
    wrk=int(households.loc[households['Household_ID']==household,'Work'])
    gro=int(households.loc[households['Household_ID']==household,'Grocery'])
    spc=int(households.loc[households['Household_ID']==household,'Supercenter'])
    con=int(households.loc[households['Household_ID']==household,'Convenience'])
    for _ in range(int(households.loc[households['Household_ID']==household,'Num People'])):
        people.loc[people['Person_ID']==index,'Location X']=float(households.loc[households['Household_ID']==household,'Location X'])
        people.loc[people['Person_ID']==index,'Location Y']=float(households.loc[households['Household_ID']==household,'Location Y'])
        state=households.loc[households['Household_ID']==household,'State'].max()
        county=households.loc[households['Household_ID']==household,'County'].max()
        people.loc[people['Person_ID']==index,'Household_ID']=household
        people.loc[people['Person_ID']==index,'State']=state
        people.loc[people['Person_ID']==index,'County']=county
        people.loc[people['Person_ID']==index,'School ID']=sch
        people.loc[people['Person_ID']==index,'Workplace_ID']=wrk
        people.loc[people['Person_ID']==index,'Work X']=float(workplaces.loc[workplaces['Workplace_ID']==wrk,'Location X'])
        people.loc[people['Person_ID']==index,'Work Y']=float(workplaces.loc[workplaces['Workplace_ID']==wrk,'Location Y'])
        people.loc[people['Person_ID']==index,'School X']=float(schools.loc[schools['School_ID']==sch,'Location X'])
        people.loc[people['Person_ID']==index,'School Y']=float(schools.loc[schools['School_ID']==sch,'Location Y'])
        people.loc[people['Person_ID']==index,'Household X']=float(households.loc[households['Household_ID']==household,'Location X'])
        people.loc[people['Person_ID']==index,'Household Y']=float(households.loc[households['Household_ID']==household,'Location Y'])
        people.loc[people['Person_ID']==index,'Grocery X']=float(stores.loc[stores['Store_ID']==gro,'Location X'])
        people.loc[people['Person_ID']==index,'Grocery Y']=float(stores.loc[stores['Store_ID']==gro,'Location Y'])
        people.loc[people['Person_ID']==index,'Supercenter X']=float(stores.loc[stores['Store_ID']==spc,'Location X'])
        people.loc[people['Person_ID']==index,'Supercenter Y']=float(stores.loc[stores['Store_ID']==spc,'Location Y'])
        people.loc[people['Person_ID']==index,'Convenience X']=float(stores.loc[stores['Store_ID']==con,'Location X'])
        people.loc[people['Person_ID']==index,'Convenience Y']=float(stores.loc[stores['Store_ID']==con,'Location Y'])
        f0=int(friends.loc[friends['Household']==household,'0'])
        f1=int(friends.loc[friends['Household']==household,'1'])
        f2=int(friends.loc[friends['Household']==household,'2'])
        f3=int(friends.loc[friends['Household']==household,'3'])
        f4=int(friends.loc[friends['Household']==household,'4'])
        people.loc[people['Person_ID']==index,'f0x']=float(households.loc[households['Household_ID']==f0,'Location X'])
        people.loc[people['Person_ID']==index,'f0y']=float(households.loc[households['Household_ID']==f0,'Location Y'])
        people.loc[people['Person_ID']==index,'f1x']=float(households.loc[households['Household_ID']==f1,'Location X'])
        people.loc[people['Person_ID']==index,'f1y']=float(households.loc[households['Household_ID']==f1,'Location Y'])
        people.loc[people['Person_ID']==index,'f2x']=float(households.loc[households['Household_ID']==f2,'Location X'])
        people.loc[people['Person_ID']==index,'f2y']=float(households.loc[households['Household_ID']==f2,'Location Y'])
        people.loc[people['Person_ID']==index,'f3x']=float(households.loc[households['Household_ID']==f3,'Location X'])
        people.loc[people['Person_ID']==index,'f3y']=float(households.loc[households['Household_ID']==f3,'Location Y'])
        people.loc[people['Person_ID']==index,'f4x']=float(households.loc[households['Household_ID']==f4,'Location X'])
        people.loc[people['Person_ID']==index,'f4y']=float(households.loc[households['Household_ID']==f4,'Location Y'])

        
        
        val=random.uniform(0,100)

        if val<int(popdata.loc[popdata['County']==county,'Group 0']):
            age=0
        elif val<int(popdata.loc[popdata['County']==county,'Group 1']):
            age=1
        elif val<int(popdata.loc[popdata['County']==county,'Group 2']):
            age=2
        elif val<int(popdata.loc[popdata['County']==county,'Group 3']):
            age=3
        elif val<int(popdata.loc[popdata['County']==county,'Group 4']):
            age=4
        elif val<int(popdata.loc[popdata['County']==county,'Group 5']):
            age=5
        elif val<int(popdata.loc[popdata['County']==county,'Group 6']):
            age=6
        elif val<int(popdata.loc[popdata['County']==county,'Group 7']):
            age=7
        elif val<int(popdata.loc[popdata['County']==county,'Group 8']):
            age=8

        if val<int(popdata.loc[popdata['County']==county,'Male (%)']):
            sex='Male'
        else:
            sex='Female'

        people.loc[people['Person_ID']==index,'Age']=age
        people.loc[people['Person_ID']==index,'Sex']=sex    


        index+=1
        
print('Finished')
#%%
people.to_csv('Population_180 Days Quaterntine at 5% and Fade Work Return at 1%. 50% Work During.csv')

#%%
people['Infected_State']=0
people.loc[people['Person_ID']==2,'Infected_State']=1
people['Infected_Duration']=0
people['Infected_By']=0
people['PVal']=np.random.uniform(0, 1, people.shape[0])
people.head(10)

#%%
def move1(tcurr,day,flag,num):
    global people
    people['Val']=0

    people['Val']=np.random.uniform(0, 1, people.shape[0])
    
    if day<=4:
        
        if tcurr<2:
            
            if flag==0:
                people.loc[people['Age']<=2,'Location X']=people.loc[people['Age']<=2,'School X']
                people.loc[people['Age']<=2,'Location Y']=people.loc[people['Age']<=2,'School Y']
            else:
                people.loc[people['Age']<=2,'Location X']=people.loc[people['Age']<=2,'Household X']
                people.loc[people['Age']<=2,'Location Y']=people.loc[people['Age']<=2,'Household Y']
            
            if flag<=1:
                people.loc[(people['Age']>2) & (people['Age']<=5),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=5),'Work X']
                people.loc[(people['Age']>2) & (people['Age']<=5),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=5),'Work Y']
            elif flag==2:
                people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']<0.4),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']<0.4),'Supercenter X']
                people.loc[(people['Age']>2) & (people['Age']<=5)& (people['PVal']>num) & (people['Val']<0.4),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']<0.4),'Supercenter Y']
                
                people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']>=0.4) & (people['Val']<0.8),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']>=0.4) & (people['Val']<0.8),'Grocery X']
                people.loc[(people['Age']>2) & (people['Age']<=5)& (people['PVal']>num) & (people['Val']>=0.4) & (people['Val']<0.8),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']>=0.4) & (people['Val']<0.8),'Grocery Y']
                
                people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']>=0.8),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']>=0.8),'Household X']
                people.loc[(people['Age']>2) & (people['Age']<=5)& (people['PVal']>num) & (people['Val']>=0.8),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num) & (people['Val']>=0.8),'Household Y']
                
                people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']<=num),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']<=num),'Work X']
                people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']<=num),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']<=num),'Work Y']
            elif flag>2:
                people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num),'Household X']
                people.loc[(people['Age']>2) & (people['Age']<=5)& (people['PVal']>num),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']>num),'Household Y']
                
                people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']<=num),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']<=num),'Work X']
                people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']<=num),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=5) & (people['PVal']<=num),'Work Y']
                
            if flag<=1:
                people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']<=0.5),'Location X']=people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']<=0.5),'Work X']
                people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']<=0.5),'Location Y']=people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']<=0.5),'Work Y']
            else:
                people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']<=0.5),'Location X']=people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']<=0.5),'Household X']
                people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']<=0.5),'Location Y']=people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']<=0.5),'Household Y']
            
            people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']>0.5),'Location X']=people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']>0.5),'Household X']
            people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']>0.5),'Location Y']=people.loc[(people['Age']>5) & (people['Age']<=6) & (people['Val']>0.5),'Household Y']

            people.loc[(people['Age']>6) & (people['Val']<=0.25),'Location X']=people.loc[(people['Age']>6) & (people['Val']<=0.25),'Grocery X']
            people.loc[(people['Age']>6) & (people['Val']<=0.25),'Location Y']=people.loc[(people['Age']>6) & (people['Val']<=0.25),'Grocery Y']
            
            people.loc[(people['Age']>6) & (people['Val']>0.25) & (people['Val']<=0.5),'Location X']=people.loc[(people['Age']>6) & (people['Val']>0.25) & (people['Val']<=0.5),'Supercenter X']
            people.loc[(people['Age']>6) & (people['Val']>0.25) & (people['Val']<=0.5),'Location Y']=people.loc[(people['Age']>6) & (people['Val']>0.25) & (people['Val']<=0.5),'Supercenter Y']

            people.loc[(people['Age']>6) & (people['Val']>0.5),'Location X']=people.loc[(people['Age']>6) & (people['Val']>0.5),'Household X']
            people.loc[(people['Age']>6) & (people['Val']>0.5),'Location Y']=people.loc[(people['Age']>6) & (people['Val']>0.5),'Household Y']
            
                
        elif tcurr==2:

            people.loc[people['Age']<=2,'Location X']=people.loc[people['Age']<=2,'Household X']
            people.loc[people['Age']<=2,'Location Y']=people.loc[people['Age']<=2,'Household Y']

            people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']<=0.143),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']<=0.143),'Grocery X']
            people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']<=0.143),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']<=0.143),'Grocery Y']
            
            people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.143) & (people['Val']<=0.286),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.143) & (people['Val']<=0.286),'Supercenter X']
            people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.143) & (people['Val']<=0.286),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.143) & (people['Val']<=0.286),'Supercenter Y']
            
            people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.286) & (people['Val']<=0.429),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.286) & (people['Val']<=0.429),'Convenience X']
            people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.286) & (people['Val']<=0.429),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.286) & (people['Val']<=0.429),'Convenience Y']
            
            people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.429),'Location X']=people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.429),'Household X']
            people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.429),'Location Y']=people.loc[(people['Age']>2) & (people['Age']<=6) & (people['Val']>0.429),'Household Y']
            
            people.loc[people['Age']>6,'Location X']=people.loc[people['Age']>6,'Household X']
            people.loc[people['Age']>6,'Location Y']=people.loc[people['Age']>6,'Household Y']

        
        elif tcurr==3:
            people['Location X']=people['Household X']
            people['Location Y']=people['Household Y']                        
                                          

    elif day==5:
        
        if tcurr<2:
            people.loc[(people['Age']<6) & (people['Val']<=0.3),'Location X']=people.loc[(people['Age']<6) & (people['Val']<=0.3),'Supercenter X']
            people.loc[(people['Age']<6) & (people['Val']<=0.3),'Location Y']=people.loc[(people['Age']<6) & (people['Val']<=0.3),'Supercenter Y']
            
            people.loc[(people['Age']<6) & (people['Val']>0.3),'Location X']=people.loc[(people['Age']<6) & (people['Val']>0.3),'Household X']
            people.loc[(people['Age']<6) & (people['Val']>0.3),'Location Y']=people.loc[(people['Age']<6) & (people['Val']>0.3),'Household Y']
            
        if tcurr==2:
            
            people.loc[(people['Age']<6) & (people['Val']<=0.5),'Location X']=people.loc[(people['Age']<6) & (people['Val']<=0.5),'Supercenter X']
            people.loc[(people['Age']<6) & (people['Val']<=0.5),'Location Y']=people.loc[(people['Age']<6) & (people['Val']<=0.5),'Supercenter Y']
            ref=random.randrange(0,4, 1)
            people.loc[(people['Age']<6) & (people['Val']>0.5),'Location X']=people.loc[(people['Age']<6) & (people['Val']>0.5),str('f'+str(ref)+'x')]
            people.loc[(people['Age']<6) & (people['Val']>0.5),'Location Y']=people.loc[(people['Age']<6) & (people['Val']>0.5),str('f'+str(ref)+'y')]
        if tcurr==3:
            people['Location X']=people['Household X']
            people['Location Y']=people['Household Y'] 
    
    elif day==6:
        people['Location X']=people['Household X']
        people['Location Y']=people['Household Y'] 
    
    #Counter Measures
    people.loc[(people['Infected_State']==2) & (people['Val']<0.9),'Location X']=people.loc[(people['Infected_State']==2) & (people['Val']<0.9),'Household X']
    people.loc[(people['Infected_State']==2) & (people['Val']<0.9),'Location Y']=people.loc[(people['Infected_State']==2) & (people['Val']<0.9),'Household Y']

#%%

num_days=180
num_ts=4
contagous_factor=0.25
days_no_symp=5
days_contagous=7
flag=0
stats=pd.DataFrame(columns=['Time Step','Num Infected','Num Recovered','Flag'])
output=pd.DataFrame(columns=['Person_ID'])
output['Person_ID']=people['Person_ID']
stats['Time Step']=range(num_days*num_ts)
# plt.scatter(people['Location X'],people['Location Y'],c=people['Infected_State']) 
# plt.show()
dayweek=1
flag=0
nn=0.1
for day in range(num_days):
    print('Day:')
    print(day)
    if day>0:
        print('People Infected:')
        print(infected.shape[0])
        print('Flag')
        print(flag)
    
    for tcurr in range(num_ts):
        print(tcurr)
        move1(tcurr,dayweek,flag,nn)
           
    
        people.loc[people['Infected_Duration']>days_no_symp*num_ts,'Infected_State']=2
        people.loc[people['Infected_Duration']>days_contagous*num_ts,'Infected_State']=3
        people.loc[(people['Infected_State']==1) | (people['Infected_State']==2),'Infected_Duration']=people.loc[(people['Infected_State']==1) | (people['Infected_State']==2),'Infected_Duration']+1
        
        infected=people[(people['Infected_State']==1) | (people['Infected_State']==2)]
        
        if (flag==0) & (infected.shape[0]>(people.shape[0]*0.05)):
            flag=2
            nn=0.5
        if (flag==2) & (infected.shape[0]<(people.shape[0]*0.01)):
            if (nn<1):
                nn=nn+0.02
            flag=1
        
#         atrisk=people.loc[(people['Location X'].isin(infected['Location X'])) & (people['Location Y'].isin(infected['Location Y'])) & (people['Infected_State']==0)]
#         atrisk['Num Exposed']=
        for index,row in infected.iterrows():
            x=float(infected.loc[infected['Person_ID']==index,'Location X'])
            y=float(infected.loc[infected['Person_ID']==index,'Location Y'])
            
            atrisk=people[(people['Location X']==x) & (people['Location Y']==y)]
            people['Val']=np.random.uniform(0, 1, people.shape[0])
            people.loc[(people['Location X']==x) & (people['Location Y']==y) & (people['Infected_State']==0) & (people['Val']<=contagous_factor/atrisk.shape[0]),'Infected_By']=index
            people.loc[(people['Location X']==x) & (people['Location Y']==y) & (people['Infected_State']==0) & (people['Val']<=contagous_factor/atrisk.shape[0]),'Infected_State']=1
            
`
        output[str(str(day)+str(tcurr)+'x')]=people['Location X']
        output[str(str(day)+str(tcurr)+'y')]=people['Location Y']
        output[str(str(day)+str(tcurr)+'i')]=people['Infected_State']
        stats.loc[stats['Time Step']==(day*num_ts)+tcurr,'Num Infected']=infected.shape[0]
        stats.loc[stats['Time Step']==(day*num_ts)+tcurr,'Num Recovered']=people[people['Infected_State']==3].shape[0]
        stats.loc[stats['Time Step']==(day*num_ts)+tcurr,'Flag']=flag
    dayweek+=1
    if dayweek>7:
        dayweek=1
    clear_output(wait=True)
        
#    plt.scatter(people['Location X'],people['Location Y'],c=people['Infected_State'])     
#    plt.show()
     
#%%
plt.rcParams['figure.figsize'] = [10, 10]
plt.style.use('ggplot')


#plt.plot(stats['Day'],stats['Num Infected'])
#plt.plot(stats['Day'],stats['Clean']+stats['Num Infected'])
qbegin=stats.loc[stats['Flag']==2,'Time Step'].min()
qend=stats.loc[stats['Flag']==2,'Time Step'].max()
stats['Clean']=people.shape[0]-(stats['Num Infected']+stats['Num Recovered'])
plt.fill_between(stats['Time Step']/num_ts, stats['Num Infected'],stats['Clean']+stats['Num Infected'],color='cornflowerblue',label='Susceptible')
plt.fill_between(stats['Time Step']/num_ts, stats['Num Infected'],0,color='salmon',label='Infected')
plt.fill_between(stats['Time Step']/num_ts, people.shape[0],stats['Clean']+stats['Num Infected'],color='plum', label='Recovered')
plt.plot([qbegin/num_ts, qbegin/num_ts],[0, people.shape[0]],color='black')
plt.plot([qend/num_ts, qend/num_ts],[0, people.shape[0]],color='black')
plt.ylabel('Population')
plt.xlabel('Days')
plt.title('SIR Plot 180 Days Quarantine at 5% and Fade Work Return at 1%. 50% Work During')
plt.legend()
plt.show() 
    
#%%
output.to_csv('Output_file_180 Days Quaterntine at 5% and Fade Work Return at 1%. 50% Work During.csv')



#%%
fig,ax = plt.subplots(1)
sns.scatterplot(workplaces['Location X'],workplaces['Location Y'],hue=workplaces['County'])
#sns.scatterplot(schools['Location X'],schools['Location Y'],hue=schools['County'])
#sns.scatterplot(households['Location X'],households['Location Y'],hue=households['County'],size=1)
#plt.scatter(households['Location X'],households['Location Y'],s=1,c='navy')
#sns.scatterplot(stores['Location X'],stores['Location Y'],hue=stores['Type'])
plt.xlim(-3,5)
plt.ylim(-3,3)
plt.title('Scaled School Locations')
rect=patches.Rectangle((0,0),1,1,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((0,1),1,1,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((1,0),1,1,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((1,1),1,1,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((2,0),1,1,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((2,1),1,1,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((3,0),1,1,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((3,1),1,1,linewidth=1,edgecolor='r',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((0,-1),1,1,linewidth=1,edgecolor='b',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((1,-1),1,1,linewidth=1,edgecolor='b',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((2,-1),1,1,linewidth=1,edgecolor='b',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((0,-2),1,1,linewidth=1,edgecolor='b',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((1,-2),1,1,linewidth=1,edgecolor='b',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((2,-2),1,1,linewidth=1,edgecolor='b',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((-1,-2),1,1,linewidth=1,edgecolor='b',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((-1,-1),1,1,linewidth=1,edgecolor='m',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((-2,-1),1,1,linewidth=1,edgecolor='m',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((-2,0),1,1,linewidth=1,edgecolor='m',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((-1,0),1,1,linewidth=1,edgecolor='m',facecolor='none')
ax.add_patch(rect)
rect=patches.Rectangle((-1,1),1,1,linewidth=1,edgecolor='m',facecolor='none')
ax.add_patch(rect)
plt.show()

#%%
people