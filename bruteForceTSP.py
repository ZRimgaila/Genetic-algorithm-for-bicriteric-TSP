#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import pprint

routes = []

def find_paths(node, cities, path, distance):
    # Add way point
    path.append(node)

    # Calculate path length from current to last node
    if len(path) > 1:
        distance += cities[path[-2]][node]

    # If path contains all cities and is not a dead end,
    # add path from last to first city and return.
    if (len(cities) == len(path)) and (path[0] in cities[path[-2]]):
        global routes
        path.append(path[0])
        distance += cities[path[-2]][path[0]]
        # print (path, distance)
        routes.append([distance, path])
        return

    # Fork paths for all possible cities not yet used
    for city in cities:
        if (city not in path) and (node in cities[city]):
            find_paths(city, dict(cities), list(path), distance)

def get_distance(start, stop):
    api = "AIzaSyCPtz6n9Cuskc0rq8PHmSlvXiIMfG_MQ-w" 
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + start + "&destinations=" + stop + "&key=" + api
    link = requests.get(url)
    json_loc = link.json()
    d = json_loc['rows'][0]['elements'][0]['distance']['value']
    d = d*0.001
    return d

def get_duration(start, stop):
    api = "AIzaSyCPtz6n9Cuskc0rq8PHmSlvXiIMfG_MQ-w" 
    url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + start + "&destinations=" + stop + "&key=" + api
    link = requests.get(url)
    json_loc = link.json()
    d = json_loc['rows'][0]['elements'][0]['duration']['value']
    d = d/60
    return d

def findRouteDistance(route):
    suma = 0
    for i in range(len(route)-1):
        city_a = route[i]
        city_b = route[i+1]
        d = getDistance(city_a,city_b)
        suma += d
    return suma

def findRouteDuration(route):
    suma = 0
    for i in range(len(route)-1):
        city_a = route[i]
        city_b = route[i+1]
        d = getDuration(city_a,city_b)
        suma += d
    return suma

def getDuration(cityA, cityB):
    durations = {
        'Vilnius': {'Kaunas': 4657, 'Klaipėda': 11087, 'Šiauliai': 8863, 'Panevėžys': 5379, 'Alytus': 5334, 'Marijampolė': 6664, 'Mažeikiai': 12471, 'Jonava': 4605, 'Utena': 4668, 'Kėdainiai': 6146, 'Tauragė': 9143, 'Telšiai': 11045, 'Ukmergė': 3082},
        'Kaunas': {'Vilnius': 4761, 'Klaipėda': 7551, 'Šiauliai': 7264, 'Panevėžys': 5171, 'Alytus': 3704, 'Marijampolė': 2740, 'Mažeikiai': 9463, 'Jonava': 1986, 'Utena': 6715, 'Kėdainiai': 2701, 'Tauragė': 5608, 'Telšiai': 7510, 'Ukmergė': 3928},
        'Klaipėda': {'Vilnius': 11183, 'Kaunas': 7520, 'Šiauliai': 7049, 'Panevėžys': 9833, 'Alytus': 10259, 'Marijampolė': 9295, 'Mažeikiai': 5590, 'Jonava': 8324, 'Utena': 12981, 'Kėdainiai': 7233, 'Tauragė': 4690, 'Telšiai': 4378, 'Ukmergė': 10283},
        'Šiauliai': {'Vilnius': 8763, 'Kaunas': 7280, 'Klaipėda': 7025, 'Panevėžys': 4553, 'Alytus': 10019, 'Marijampolė': 9055, 'Mažeikiai': 3903, 'Jonava': 6276, 'Utena': 8564, 'Kėdainiai': 4798, 'Tauragė': 
5044, 'Telšiai': 3454, 'Ukmergė': 6160},
        'Panevėžys': {'Vilnius': 5468, 'Kaunas': 5184, 'Klaipėda': 9797, 'Šiauliai': 4226, 'Alytus': 7922, 'Marijampolė': 6958, 'Mažeikiai': 7834, 'Jonava': 4155, 'Utena': 4892, 'Kėdainiai': 3299, 'Tauragė': 7854, 'Telšiai': 7385, 'Ukmergė': 2864},
        'Alytus': {'Vilnius': 5270, 'Kaunas': 3665, 'Klaipėda': 10323, 'Šiauliai': 10035, 'Panevėžys': 7942, 'Marijampolė': 3043, 'Mažeikiai': 12234, 'Jonava': 4673, 'Utena': 9374, 'Kėdainiai': 5473, 'Tauragė': 8379, 'Telšiai': 10281, 'Ukmergė': 6615},
        'Marijampolė': {'Vilnius': 6723, 'Kaunas': 2704, 'Klaipėda': 9361, 'Šiauliai': 9074, 'Panevėžys': 6981, 'Alytus': 3039, 'Mažeikiai': 11273, 'Jonava': 4021, 'Utena': 8750, 'Kėdainiai': 4511, 'Tauragė': 
6176, 'Telšiai': 9320, 'Ukmergė': 5962},
        'Mažeikiai': {'Vilnius': 12597, 'Kaunas': 9477, 'Klaipėda': 5608, 'Šiauliai': 3949, 'Panevėžys': 8387, 'Alytus': 12215, 'Marijampolė': 11252, 'Jonava': 10110, 'Utena': 12041, 'Kėdainiai': 8632, 'Tauragė': 6777, 'Telšiai': 2157, 'Ukmergė': 9994},
        'Jonava': {'Vilnius': 4552, 'Kaunas': 1945, 'Klaipėda': 8375, 'Šiauliai': 6262, 'Panevėžys': 4126, 'Alytus': 4661, 'Marijampolė': 3953, 'Mažeikiai': 10044, 'Utena': 4760, 'Kėdainiai': 1730, 'Tauragė': 
6432, 'Telšiai': 8333, 'Ukmergė': 1972},
        'Utena': {'Vilnius': 4612, 'Kaunas': 6719, 'Klaipėda': 13063, 'Šiauliai': 8661, 'Panevėžys': 4913, 'Alytus': 9126, 'Marijampolė': 8726, 'Mažeikiai': 12000, 'Jonava': 4766, 'Kėdainiai': 5881, 'Tauragė': 11120, 'Telšiai': 11550, 'Ukmergė': 3240},
        'Kėdainiai': {'Vilnius': 6117, 'Kaunas': 2717, 'Klaipėda': 7227, 'Šiauliai': 4800, 'Panevėžys': 3317, 'Alytus': 5456, 'Marijampolė': 4492, 'Mažeikiai': 8582, 'Jonava': 1754, 'Utena': 5870, 'Tauragė': 5283, 'Telšiai': 7185, 'Ukmergė': 3196},
        'Tauragė': {'Vilnius': 9149, 'Kaunas': 5486, 'Klaipėda': 4645, 'Šiauliai': 4962, 'Panevėžys': 7799, 'Alytus': 8225, 'Marijampolė': 6111, 'Mažeikiai': 6664, 'Jonava': 6290, 'Utena': 10947, 'Kėdainiai': 
5199, 'Telšiai': 4729, 'Ukmergė': 8249},
        'Telšiai': {'Vilnius': 11143, 'Kaunas': 7480, 'Klaipėda': 4402, 'Šiauliai': 3439, 'Panevėžys': 7877, 'Alytus': 10219, 'Marijampolė': 9255, 'Mažeikiai': 2123, 'Jonava': 8284, 'Utena': 11531, 'Kėdainiai': 7193, 'Tauragė': 4804, 'Ukmergė': 9484},
        'Ukmergė': {'Vilnius': 3169, 'Kaunas': 3931, 'Klaipėda': 10361, 'Šiauliai': 6344, 'Panevėžys': 2860, 'Alytus': 6647, 'Marijampolė': 5938, 'Mažeikiai': 9952, 'Jonava': 1978, 'Utena': 3170, 'Kėdainiai': 
3181, 'Tauragė': 8417, 'Telšiai': 9502}}

    t = durations[cityA][cityB] / 3600
    return t

# Miestai ir atstumai tarp jų gauti iš Google MAPS API 
def getDistance(cityA, cityB):
    cities = {
        'Vilnius': {'Kaunas': 103, 'Klaipėda': 306, 'Šiauliai': 213, 'Panevėžys': 137, 'Alytus': 109, 'Marijampolė': 161, 'Mažeikiai': 301, 'Jonava': 92, 'Utena': 97, 'Kėdainiai': 136, 'Tauragė': 237, 'Telšiai': 283, 'Ukmergė': 73},
        'Kaunas': {'Vilnius': 101, 'Klaipėda': 214, 'Šiauliai': 176, 'Panevėžys': 109, 'Alytus': 70, 'Marijampolė': 61, 'Mažeikiai': 232, 'Jonava': 31, 'Utena': 133, 'Kėdainiai': 56, 'Tauragė': 145, 'Telšiai': 191, 'Ukmergė': 70},
        'Klaipėda': {'Vilnius': 308, 'Kaunas': 215, 'Šiauliai': 172, 'Panevėžys': 240, 'Alytus': 276, 'Marijampolė': 267, 'Mažeikiai': 116, 'Jonava': 231, 'Utena': 326, 'Kėdainiai': 205, 'Tauragė': 110, 'Telšiai': 90, 'Ukmergė': 269},
        'Šiauliai': {'Vilnius': 211, 'Kaunas': 177, 'Klaipėda': 171, 'Panevėžys': 87, 'Alytus': 239, 'Marijampolė': 230, 'Mažeikiai': 80, 'Jonava': 126, 'Utena': 197, 'Kėdainiai': 93, 'Tauragė': 102, 'Telšiai': 72, 'Ukmergė': 143},
        'Panevėžys': {'Vilnius': 137, 'Kaunas': 110, 'Klaipėda': 238, 'Šiauliai': 79, 'Alytus': 171, 'Marijampolė': 162, 'Mažeikiai': 167, 'Jonava': 88, 'Utena': 103, 'Kėdainiai': 64, 'Tauragė': 169, 'Telšiai': 159, 'Ukmergė': 68},
        'Alytus': {'Vilnius': 108, 'Kaunas': 70, 'Klaipėda': 277, 'Šiauliai': 239, 'Panevėžys': 172, 'Marijampolė': 55, 'Mažeikiai': 295, 'Jonava': 98, 'Utena': 203, 'Kėdainiai': 119, 'Tauragė': 208, 'Telšiai': 254, 'Ukmergė': 137},
        'Marijampolė': {'Vilnius': 136, 'Kaunas': 62, 'Klaipėda': 269, 'Šiauliai': 231, 'Panevėžys': 164, 'Alytus': 55, 'Mažeikiai': 286, 'Jonava': 93, 'Utena': 196, 'Kėdainiai': 111, 'Tauragė': 125, 'Telšiai': 245, 'Ukmergė': 132},
        'Mažeikiai': {'Vilnius': 293, 'Kaunas': 233, 'Klaipėda': 114, 'Šiauliai': 80, 'Panevėžys': 168, 'Alytus': 295, 'Marijampolė': 286, 'Jonava': 207, 'Utena': 263, 'Kėdainiai': 175, 'Tauragė': 142, 'Telšiai': 39, 'Ukmergė': 224},
        'Jonava': {'Vilnius': 91, 'Kaunas': 34, 'Klaipėda': 238, 'Šiauliai': 126, 'Panevėžys': 88, 'Alytus': 103, 'Marijampolė': 92, 'Mažeikiai': 212, 'Utena': 101, 'Kėdainiai': 34, 'Tauragė': 169, 'Telšiai': 
214, 'Ukmergė': 38},
        'Utena': {'Vilnius': 97, 'Kaunas': 137, 'Klaipėda': 339, 'Šiauliai': 198, 'Panevėžys': 103, 'Alytus': 206, 'Marijampolė': 195, 'Mažeikiai': 262, 'Jonava': 101, 'Kėdainiai': 121, 'Tauragė': 270, 'Telšiai': 254, 'Ukmergė': 64},
        'Kėdainiai': {'Vilnius': 136, 'Kaunas': 57, 'Klaipėda': 205, 'Šiauliai': 93, 'Panevėžys': 64, 'Alytus': 118, 'Marijampolė': 110, 'Mažeikiai': 180, 'Jonava': 34, 'Utena': 121, 'Tauragė': 136, 'Telšiai': 181, 'Ukmergė': 58},
        'Tauragė': {'Vilnius': 238, 'Kaunas': 145, 'Klaipėda': 110, 'Šiauliai': 102, 'Panevėžys': 170, 'Alytus': 206, 'Marijampolė': 125, 'Mažeikiai': 142, 'Jonava': 160, 'Utena': 255, 'Kėdainiai': 135, 'Telšiai': 95, 'Ukmergė': 198},
        'Telšiai': {'Vilnius': 285, 'Kaunas': 192, 'Klaipėda': 89, 'Šiauliai': 71, 'Panevėžys': 159, 'Alytus': 253, 'Marijampolė': 244, 'Mažeikiai': 39, 'Jonava': 208, 'Utena': 254, 'Kėdainiai': 182, 'Tauragė': 95, 'Ukmergė': 215},
        'Ukmergė': {'Vilnius': 72, 'Kaunas': 73, 'Klaipėda': 276, 'Šiauliai': 143, 'Panevėžys': 68, 'Alytus': 141, 'Marijampolė': 131, 'Mažeikiai': 232, 'Jonava': 38, 'Utena': 64, 'Kėdainiai': 58, 'Tauragė': 207, 'Telšiai': 223}
    }
    d = cities[cityA][cityB]
    return d

if __name__ == '__main__':
    # data = """Vilnius, Kaunas, Klaipėda, Šiauliai, Panevėžys, Alytus, Marijampolė, Mažeikiai, Jonava, Utena, Kėdainiai, Tauragė, Telšiai, Ukmergė"""
    # cit = data.split(", ")
    # print(cit)
    # dist = {}
    # for i in range(len(cit)):
    #     d = {}
    #     for j in range(len(cit)):
    #         if i != j:
    #             distance = get_distance(cit[i], cit[j])
    #             duration = get_duration(cit[i], cit[j])

    #             d[cit[j]] = round(int(distance)+duration, 2)
    #     dist[cit[i]] = d
    
    # print("{" + ",\n".join("{!r}: {!r}".format(k, v) for k, v in dist.items()) + "}")

    cities = {
        'Vilnius': {'Kaunas': 180.57, 'Klaipėda': 494.93, 'Šiauliai': 361.83, 'Panevėžys': 227.58, 'Alytus': 198.1, 'Marijampolė': 272.45, 'Mažeikiai': 509.98, 'Jonava': 169.07, 'Utena': 174.48, 'Kėdainiai': 239.02, 'Tauragė': 390.4, 'Telšiai': 468.57, 'Ukmergė': 124.78},
        'Kaunas': {'Vilnius': 180.32, 'Klaipėda': 344.32, 'Šiauliai': 298.68, 'Panevėžys': 195.82, 'Alytus': 132.0, 'Marijampolė': 107.23, 'Mažeikiai': 391.65, 'Jonava': 64.23, 'Utena': 244.95, 'Kėdainiai': 101.42, 'Tauragė': 239.8, 'Telšiai': 317.97, 'Ukmergė': 135.5},
        'Klaipėda': {'Vilnius': 499.55, 'Kaunas': 345.68, 'Šiauliai': 293.97, 'Panevėžys': 408.95, 'Alytus': 452.43, 'Marijampolė': 427.68, 'Mažeikiai': 209.37, 'Jonava': 374.82, 'Utena': 547.83, 'Kėdainiai': 330.62, 'Tauragė': 188.65, 'Telšiai': 163.13, 'Ukmergė': 445.38},
        'Šiauliai': {'Vilnius': 358.38, 'Kaunas': 270.17, 'Klaipėda': 291.75, 'Panevėžys': 163.25, 'Alytus': 376.93, 'Marijampolė': 352.17, 'Mažeikiai': 145.02, 'Jonava': 230.93, 'Utena': 340.6, 'Kėdainiai': 173.1, 'Tauragė': 186.6, 'Telšiai': 129.43, 'Ukmergė': 246.45},
        'Panevėžys': {'Vilnius': 229.1, 'Kaunas': 196.87, 'Klaipėda': 405.1, 'Šiauliai': 149.35, 'Alytus': 303.62, 'Marijampolė': 278.85, 'Mažeikiai': 297.52, 'Jonava': 157.45, 'Utena': 184.92, 'Kėdainiai': 119.07, 'Tauragė': 300.58, 'Telšiai': 281.93, 'Ukmergė': 117.17},
        'Alytus': {'Vilnius': 196.23, 'Kaunas': 131.28, 'Klaipėda': 453.43, 'Šiauliai': 407.8, 'Panevėžys': 304.93, 'Marijampolė': 105.73, 'Mažeikiai': 500.77, 'Jonava': 175.95, 'Utena': 355.72, 'Kėdainiai': 210.53, 'Tauragė': 348.92, 'Telšiai': 427.08, 'Ukmergė': 247.22},
        'Marijampolė': {'Vilnius': 248.35, 'Kaunas': 107.67, 'Klaipėda': 429.83, 'Šiauliai': 384.18, 'Panevėžys': 281.32, 'Alytus': 105.8, 'Mažeikiai': 476.17, 'Jonava': 160.6, 'Utena': 342.32, 'Kėdainiai': 186.93, 'Tauragė': 228.1, 'Telšiai': 402.47, 'Ukmergė': 231.88},
        'Mažeikiai': {'Vilnius': 504.47, 'Kaunas': 393.43, 'Klaipėda': 207.58, 'Šiauliai': 145.88, 'Panevėžys': 308.35, 'Alytus': 501.18, 'Marijampolė': 476.43, 'Jonava': 376.03, 'Utena': 464.48, 'Kėdainiai': 319.2, 'Tauragė': 255.12, 'Telšiai': 74.98, 'Ukmergė': 391.55},
        'Jonava': {'Vilnius': 167.18, 'Kaunas': 66.55, 'Klaipėda': 381.92, 'Šiauliai': 230.68, 'Panevėžys': 157.07, 'Alytus': 180.78, 'Marijampolė': 158.43, 'Mažeikiai': 379.95, 'Utena': 180.27, 'Kėdainiai': 62.92, 'Tauragė': 277.4, 'Telšiai': 354.57, 'Ukmergė': 70.82},
        'Utena': {'Vilnius': 173.9, 'Kaunas': 249.07, 'Klaipėda': 561.38, 'Šiauliai': 321.07, 'Panevėžys': 185.3, 'Alytus': 355.32, 'Marijampolė': 340.95, 'Mažeikiai': 462.47, 'Jonava': 180.43, 'Kėdainiai': 219.32, 'Tauragė': 456.87, 'Telšiai': 446.88, 'Ukmergė': 118.15},
        'Kėdainiai': {'Vilnius': 238.88, 'Kaunas': 102.67, 'Klaipėda': 329.58, 'Šiauliai': 173.17, 'Panevėžys': 119.58, 'Alytus': 210.42, 'Marijampolė': 185.65, 'Mažeikiai': 322.43, 'Jonava': 63.35, 'Utena': 219.32, 'Tauragė': 225.07, 'Telšiai': 302.23, 'Ukmergė': 111.75},
        # 'Tauragė': {'Vilnius': 391.5, 'Kaunas': 237.63, 'Klaipėda': 187.88, 'Šiauliai': 185.07, 'Panevėžys': 300.9, 'Alytus': 344.4, 'Marijampolė': 227.23, 'Mažeikiai': 253.32, 'Jonava': 265.77, 'Utena': 438.8, 'Kėdainiai': 222.57, 'Telšiai': 173.97, 'Ukmergė': 336.35}
        # 'Telšiai': {'Vilnius': 472.93, 'Kaunas': 319.07, 'Klaipėda': 162.52, 'Šiauliai': 128.27, 'Panevėžys': 290.73, 'Alytus': 425.82, 'Marijampolė': 401.05, 'Mažeikiai': 74.5, 'Jonava': 348.18, 'Utena': 446.88, 'Kėdainiai': 303.98, 'Tauragė': 175.12, 'Ukmergė': 373.93}
        # 'Ukmergė': {'Vilnius': 125.32, 'Kaunas': 138.43, 'Klaipėda': 452.8, 'Šiauliai': 249.42, 'Panevėžys': 116.17, 'Alytus': 251.67, 'Marijampolė': 230.32, 'Mažeikiai': 398.58, 'Jonava': 70.8, 'Utena': 116.97, 'Kėdainiai': 111.17, 'Tauragė': 348.27, 'Telšiai': 382.0}
        }

    print ("Start: Vilnius")
    find_paths('Vilnius', cities, [], 0)
    print ("\n")
    routes.sort()
    if len(routes) != 0:
        print ("Shortest route: %s" % routes[0][1])
        bestLength = findRouteDistance(routes[0][1])
        bestTime = findRouteDuration(routes[0][1])
        print("Best route length: ", bestLength)
        print("Best route time: ", bestTime)
        print("Best route speed: ", bestLength/bestTime)
    else:
        print ("FAIL!")