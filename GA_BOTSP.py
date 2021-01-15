#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import array as arr
import string
import random
import math
import matplotlib.pyplot as plt
from random import randint
from random import choice
from random import shuffle
import requests
import json
import time as tm

class DNA:
    def __init__(self):
        self.genes = []
    
    def create(self, coords):
        newCoords = coords[:]
        newCoords.pop(0)
        newCoords.pop()
        random.shuffle(newCoords)
        newCoords.insert(0, 'Vilnius')
        newCoords.insert(len(newCoords), 'Vilnius')
        return newCoords
    
    def createFirstGene(self):
        data = """Vilnius, Kaunas, Klaipėda, Šiauliai, Panevėžys, Alytus, Marijampolė, Mažeikiai, Jonava, Utena, Kėdainiai, Vilnius"""#Tauragė, Telšiai, Ukmergė, Vilnius"""
        self.genes = data.split(", ")
        return self.genes
    
    def crossover(self, partner1, partner2, rate):
        newChild = []
        if(random.random() < rate):
            k = math.ceil(len(partner1)/3)
            start = math.ceil(random.randrange(1, k))
            end = math.floor(start + len(partner1)*(2/3)-1)
            newChild = partner1[start:end]
            partner2 = partner2[1:len(partner2)-1]
            for i in range(len(partner2)):
                city = partner2[i]
                if city not in newChild:
                    newChild.append(city)
            newChild.insert(0, 'Vilnius')
            newChild.insert(len(newChild), 'Vilnius')
        else:
            newChild = choice([partner1, partner2])
        return newChild
    
    def mutate(self, child, mutationRate):
        for i in range(len(child)):
            if(random.random() < mutationRate):
                x = randint(1,len(child)-2)
                y = choice([i for i in range(1,len(child)-2) if i!=x])
                temp = child[x]
                child[x] = child[y]
                child[y] = temp
        return child

class Population:
    def __init__(self, populationSize, mutationRate, crossoverRate):
        self.populationSize = populationSize
        self.mutationRate = mutationRate
        self.crossoverRate = crossoverRate
        self.nicheSize = 1
        self.dna = DNA()
        self.popFit = 0
        self.fit = []
        self.smallest = [1,1]
        self.biggest = [0,0]

    def create(self):
        self.population = []
        coords = self.dna.createFirstGene()
        for i in range(self.populationSize):
            self.population.append(self.dna.create(coords))
        return self.population
   
    def get_time(self, start, stop):
        api = "AIzaSyCPtz6n9Cuskc0rq8PHmSlvXiIMfG_MQ-w" 
        url = "https://maps.googleapis.com/maps/api/distancematrix/json?units=imperial&origins=" + start + "&destinations=" + stop + "&key=" + api
        link = requests.get(url)
        json_loc = link.json()
        d = json_loc['rows'][0]['elements'][0]['duration']['value']
        return d
    
    # Miestai ir keliavimo trukmės tarp jų gauti iš Google MAPS API 
    def getDuration(self, cityA, cityB):
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
    def getDistance(self, cityA, cityB):
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

    def calculateRouteDistances(self):
        distances = []
        for i in range(self.populationSize):
            dist = []
            for j in range(len(self.population[i])-1):
                city_a = self.population[i][j]
                city_b = self.population[i][j+1]
                d = self.getDistance(city_a,city_b)
                dist.append(d)
            distances.append(sum(dist))
        return distances

    def fitnessEvaluation(self, gen):
        f = []
        f1 = []
        self.fit = []
        
        # 3.1 Priskiriamas rangas kiekvienam sprendiniui
        p = self.getPopulationWithValues()
        self.ranks = self.ranking(p)

        # 3.2. Priskiriama tinkamumo reikšmė kiekvienam sprendiniui pagal jo rangą
        N = len(self.ranks)
        for i in range(len(self.ranks)):  
            suma = 0
            for k in range(self.ranks[i]):
                n_k = self.solutionsCount(k)
                suma += n_k
            f.append(N - suma - 0.5*(self.solutionsCount(self.ranks[i])-1))

        # nišos skaičius
        nc = self.nicheCount(p)

        for i in range(len(self.ranks)):
            f1.append(f[i]/nc[i])

        self.fit = self.normalizingFitness(f, f1)

        for i in range(len(self.fit)):
            if self.fit[i] > 1:
                print("ranks", self.ranks)
                print("fit", self.fit)
                print("something wrong with fitness probabilities")

        return self.fit

    def naturalSelection(self):
        matingPool = []
        f = 0
        for i in range(len(self.population)):
            f = self.fit[i]
            if f>0.5:
                n = int(f*150)
            else: n = int(f*100)
            for j in range(n):
                matingPool.append(self.population[i])
        return matingPool
                
    def reproduction(self, matingPool):
        length = len(self.population)
        self.population = []
        for i in range(length):
            a = int(random.randrange(len(matingPool)))
            b = int(random.randrange(len(matingPool)))
            partnerA = matingPool[a]
            partnerB = matingPool[b]
            child = self.dna.crossover(partnerA, partnerB, self.crossoverRate)
            mutatedChild = self.dna.mutate(child, self.mutationRate)
            self.population.append(child)

    def solutionsCount(self, k):
        count = 0
        for i in range(len(self.ranks)):
            if k == self.ranks[i]:
                count += 1
        return count

    def ranking(self, p):
        ranks = []
        value = []
        for i in range(len(p)):
            value.append([p[i][0],p[i][1]])
        for i in range(len(p)):
            ranks.append(2+self.domSolutions(value,i))
        return ranks

    def getPopulationWithValues(self):
        p = []
        for i in range(self.populationSize):
            dist = []
            time = []
            for j in range(len(self.population[i])-1):
                city_a = self.population[i][j]
                city_b = self.population[i][j+1]
                d = self.getDistance(city_a,city_b)
                dist.append(d)
                t = self.getDuration(city_a,city_b)
                time.append(t)
            p.append([sum(dist),sum(time)])
        return p

    def domSolutions(self, val, t):
        rank = 0
        for i in range(len(val)):
            if val[t][0] > val[i][0] and val[t][1] > val[i][1] and t!=i:
                rank += 2
            else:
                if val[t][0] > val[i][0] and t!=i:
                    rank += 1
                else:
                    if val[t][1] > val[i][1] and t!=i:
                        rank += 1
        return rank
    
    def nicheCount(self, p):
        nc = []
        for i in range(len(p)):
            suma = 0
            for j in range(len(p)):
                value = (self.nicheSize - self.euclideanDist(i,j,p)) / self.nicheSize
                if value > 0:
                    suma += value
                else: suma += 0
            nc.append(suma)
        return nc

    def euclideanDist(self, x, y, p):
        suma = 0
        # i - kriterines funkcijos numeris =1 -dist; =2 -time
        for i in range(2):
            suma += ( (p[x][i]-p[y][i]) / (self.findMax(i,p)-self.findMin(i,p)) )**2
        return math.sqrt(suma)

    def findMaxFit(self, f):
        biggest = f[0]
        for i in range(len(f)):
            if f[i] > biggest:
                biggest = f[i]
        return biggest

    def findMax(self, k, p):
        for i in range(len(p)):
            if p[i][k] > self.biggest[k]:
                self.biggest[k] = p[i][k]
        return self.biggest[k]

    def findMin(self, k, p):
        for i in range(len(p)):
            if p[i][k] < self.smallest[k]:
                self.smallest[k] = p[i][k]
        return self.smallest[k]

    def normalizingFitness(self, f1, f2):
        f = []
        for i in range(len(self.ranks)):
            suma = 0
            for j in range(len(self.ranks)):
                suma += f2[i]
            value = round((f2[i] / suma) * f1[i], 2)
            f.append(value)
        return f
    
    def getPopulationFit(self):
        popFit = sum(self.fit)/len(self.fit)*100
        return popFit
    
    def getBest(self):
        max = 0
        index = 0
        for i in range(len(self.fit)):
            if(self.fit[i] > max):
                index = i
                max = self.fit[i]
        return self.population[index]
    
    def getFitiestGeneFit(self):
        max = self.rankRoutes()[0]
        for i in range(1, len(self.population)):
            if(self.rankRoutes()[i] > max):
                max = self.rankRoutes()[i]
        return max
    
    def getFitScore(self):
        return self.fit

    def getBestRouteValues(self, p):
        best = 0
        index = 0
        for i in range(len(self.fit)):
            if best < self.fit[i]:
                best = self.fit[i]
                index = i
            
        return p[index]
    
    def printResults(self, gen, executionTime):
        route = self.getBest()
        bestLength = self.findRouteDistance(route)
        bestTime = self.findRouteDuration(route)
        print("Best route: ", route)
        print("Best route length: ", bestLength)
        print("Best route time: ", bestTime)
        print("Generations: ", gen)
        print("Time: ", executionTime)
        return route

    def findRouteDistance(self, route):
        suma = 0
        for i in range(len(route)-1):
            city_a = route[i]
            city_b = route[i+1]
            d = self.getDistance(city_a,city_b)
            suma += d
        return suma

    def findRouteDuration(self, route):
        suma = 0
        for i in range(len(route)-1):
            city_a = route[i]
            city_b = route[i+1]
            d = self.getDuration(city_a,city_b)
            suma += d
        return suma

    def getMatingPool(self):
        print("\n")
        print("MatingPool = ")
        for i in range(len(self.matingPool)):
            print(self.matingPool[i])
            
    def getPopulation(self):
        print("\n")
        print("POPULATION = ")
        for i in range(len(self.population)):
            print(self.population[i])

class Plot:
    def __init__(self, pop):
        self.pop = pop
    
    def create(self, iterations, val, labelY):
        plt.title('Genetic algorithm')
        plt.plot(iterations, val)
        plt.xlabel('Generations')
        plt.ylabel(labelY)
        plt.grid(True)
        plt.show()

def findNearest(b, g):
    smallest = 10000
    index = 0
    for i in range(0,len(g)):
        if b != g[i]:
            dist = Population.getDistance(Population, b, g[i])
            if dist < smallest:
                smallest = dist
                index = i
    return index

big = 0
small = 1000
def igd(geneticPareto, bruteForcePareto, perfect):
    # inv = 1/perfect
    suma = 0
    for i in range(len(bruteForcePareto)):
        index = findNearest(bruteForcePareto[i], geneticPareto)
        if bruteForcePareto[i] != geneticPareto[index]:
            suma += euclideanDist(bruteForcePareto[i], geneticPareto[index])
        else:
            suma += 0
    return perfect/suma

def euclideanDist(x, y):
        suma = 0
        dist = Population.getDistance(Population, x, y)
        suma += ( dist )**2
        time = Population.getDuration(Population, x, y)
        suma += ( time )**2
        return math.sqrt(suma)

def findMax(dist):
    global big
    if big < dist:
        big = dist
    return big

def findMin(dist):
    global small
    if small > dist:
        small = dist
    return small

def main():
        start = tm.time()
        executionTime = 0
        timeLimit = 20
        mutation = 0.005
        crossover = 1
        populationSize = 200
        generations = 50
        gen = generations+1
        pop = Population(populationSize, mutation, crossover)
        pop.create()
        iterations = []
        d = [] # distances list
        t = [] # durations list
        metrika = []
        brute = ['Vilnius', 'Utena', 'Panevėžys', 'Šiauliai', 'Mažeikiai', 'Klaipėda', 'Kėdainiai', 'Jonava', 'Kaunas', 'Marijampolė', 'Alytus', 'Vilnius']

        while generations > 0:
            fit = 0
            iterations.append(gen-generations)
            fit = pop.fitnessEvaluation(generations)
            p = pop.getPopulationWithValues()
            dist = pop.getBestRouteValues(p)[0]
            dur = pop.getBestRouteValues(p)[1]
            perfectValue = dist + dur
            pareto = pop.getBest()
            igdMetrika = igd(pareto, brute, dist)
            metrika.append(igdMetrika)
            # metrika.append(2-970/dist-12.58/round(dur,2))
            print(str(gen-generations) + " " + str(dist) + " " + str(dur))
            if(generations == 1 or dist == 970):
                pareto = pop.printResults(gen-generations, executionTime)
                break
            else:
                matingPool = pop.naturalSelection()
                pop.reproduction(matingPool)
            generations-=1
            executionTime = (tm.time() - start)
        
        # duration = pop.findRouteDuration(brute)
        # distance = pop.findRouteDistance(brute)
        # perfectValue = distance + duration
        # metrika = igd(pareto, brute, perfectValue)
        # print("igd", metrika)
        for i in range(len(metrika)):
            print(metrika[i])
        plot_Dist = Plot(pop)
        plot_Dist.create(iterations, metrika, "Metrika")
        
if __name__ == "__main__":
        main()


