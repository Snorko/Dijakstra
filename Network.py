#!/usr/bin/env python
# coding: utf-8
#By: Eduard Tatievski
# In[1]:


from geopy.distance import distance
from geopy.point import Point
from math import sqrt
from math import atan2, degrees

# In[2]:


satsLocations = {}
satFile = open('Sats_locations.csv')

# In[3]:


# getting all satelighr data from our csv file
for sat in satFile.readlines():
    sat = sat.split(',')
    sat = [i.replace("'", '').replace('"', '') for i in sat]
    if sat[0] != '\n':
        if sat[0].split(' ')[0] == 'Time':
            satName = sat[1].split('-')[0].strip()
            if satName not in satsLocations.keys():
                satsLocations[satName] = [list(), list(), list()]
        else:
            satsLocations[satName][0].append(float(sat[1]))
            satsLocations[satName][1].append(float(sat[2]))
            satsLocations[satName][2].append(float(sat[3]))


# In[4]:


def AVG(list):
    return sum(list) / len(list)


# In[5]:


avgSatsLocations = {}
for key, value in satsLocations.items():
    if key not in avgSatsLocations.keys():
        avgSatsLocations[key] = [round(AVG(value[0]), 3), round(AVG(value[1]), 3), round(AVG(value[2]), 6)]

# In[6]:


allSatlites = {}
satlitiesNames = list(avgSatsLocations.keys())
for index, satName in enumerate(satlitiesNames):
    if index + 1 < len(satlitiesNames):
        pointALat = avgSatsLocations[satName][0]
        pointALon = avgSatsLocations[satName][1]
        pointAAlt = avgSatsLocations[satName][2]
        a = Point(pointALat, pointALon, 0)
        nextSatName = satlitiesNames[index + 1]
        pointBLat = avgSatsLocations[nextSatName][0]
        pointBLon = avgSatsLocations[nextSatName][1]
        pointBAlt = avgSatsLocations[nextSatName][2]
        b = Point(pointBLat, pointBLon, 0)
        allSatlites[(satlitiesNames[index], satlitiesNames[index + 1])] = [distance(a, b).km, [pointAAlt, pointBAlt]]

# In[7]:


distances = {}
for sats, values in allSatlites.items():
    dis = sqrt(values[0] ** 2 + (values[1][0] - values[1][1]) ** 2)
    distances[sats] = round(dis, 2)


# In[8]:


def distance(value):
    return 1 - (value / 300)


# In[9]:


for key, value in distances.items():
    distances[key] = distance(value)

# In[10]:


distances

# In[11]:


avgSatsLocations


# In[12]:


def AngleBtw2Points(pointA, pointB):
    X = pointB[0] - pointA[0]
    Y = pointB[1] - pointA[1]
    return degrees(atan2(Y, X))


# In[15]:


angleSat = {}
satlitiesNames = list(avgSatsLocations.keys())
for index, satName in enumerate(satlitiesNames):
    if index + 1 < len(satlitiesNames):
        pointALat = avgSatsLocations[satName][0]
        pointALon = avgSatsLocations[satName][1]
        pointA = (pointALat, pointALon)
        nextSatName = satlitiesNames[index + 1]
        pointBLat = avgSatsLocations[nextSatName][0]
        pointBLon = avgSatsLocations[nextSatName][1]
        pointB = (pointBLat, pointBLon)
        angleSat[(satlitiesNames[index], satlitiesNames[index + 1])] = round(AngleBtw2Points(pointA, pointB), 2)

# In[16]:


angleSat

# In[17]:


dataFile = open('testData.txt', 'w+')
for key, value in distances.items():
    sat1 = key[0]
    sat2 = key[1]
    data = round(value + angleSat[key], 2)
    dataFile.write(sat1 + ' ' + sat2 + ' ' + str(data) + '\n')
dataFile.close()

# In[ ]:

print(angleSat)




