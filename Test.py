#!/usr/bin/env python
# coding: utf-8
#By: Eduard Tatievski

from geopy.distance import distance
from geopy.point import Point
from math import sqrt
from math import atan2, degrees

sourceSat = "Sat117"
destenationSat = "Sat119"

satsLocations = {}
satFile = open('Sats_locations.csv')


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

print("EDI 1")
print(satsLocations)


def AVG(list):
    return sum(list) / len(list)

avgSatsLocations = {}
for key, value in satsLocations.items():
    if key not in avgSatsLocations.keys():
        avgSatsLocations[key] = [round(AVG(value[0]), 3), round(AVG(value[1]), 3), round(AVG(value[2]), 6)]

print("EDI 2")
print(avgSatsLocations)

allSatlites = {}
satlitiesNames = list(avgSatsLocations.keys())



for index, satName in enumerate(satlitiesNames):
    if index + 1 < len(satlitiesNames):
        pointALat = avgSatsLocations[satName][0]
        pointALon = avgSatsLocations[satName][1]
        pointAAlt = avgSatsLocations[satName][2]
        a = Point(pointALat, pointALon, 0)
        nextSatName = avgSatsLocations[sourceSat]
        pointBLat = avgSatsLocations[sourceSat][0]
        pointBLon = avgSatsLocations[sourceSat][1]
        pointBAlt = avgSatsLocations[sourceSat][2]
        b = Point(pointBLat, pointBLon, 0)
        allSatlites[(satlitiesNames[index], sourceSat)] = [round(sqrt((avgSatsLocations[sourceSat][0] - pointALat) ** 2 + (avgSatsLocations[sourceSat][1] - pointALon) ** 2),2), [pointAAlt, pointBAlt]]

print("TEST1")
satlitiesDis = list(allSatlites.items())
print(satlitiesDis)

closeSatlites = {}
for index, satName in enumerate(allSatlites):
    if satlitiesDis[index][1][0] < 200 and satlitiesDis[index][1][0] > 1:
        #print (str(satlitiesDis[index][0][1]) + " Distance "+ str(satlitiesDis[index][1][0]))
        #print(satName)
        closeSatlites[(satName[0],satName[1])]= [satlitiesDis[index][1][0]]

print("TEST")
print(closeSatlites)


def distanceW(value):
    return (1 - (value/ 200))

distances = {}
for key, value in (closeSatlites.items()):
    #print(closeSatlites[value][0])
    print(key)
    val=round((1-value[0]/200),4)
    distances[key] = val


print("EDI 5")
print(distances)

dataFile = open('testData.txt', 'w+')
for key, value in distances.items():
    sat1 = key[0]
    sat2 = key[1]
    data=value
    dataFile.write(sat1 + ' ' + sat2 + ' ' + str(data) + '\n')
dataFile.close()
