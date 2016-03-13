#!/usr/local/bin/python

#In this file, it will generate an alert according to the entropy of the data we get.
#entropy will indicate how close the data is, or how far apart the data is. If we get a
#large number of entropy, it means our data is far apart. If we have a small number on 
#entropy, it means our data is close to each other. By my experiment, I set the threshold
#to 0.5, and 0.1. If the entropy is larger than 0.5, it means the data is far apart. If
#the entropy is between 0.1 to 0.5, it means the data is not that far, but not close.
#if the entropy is less than 0.1, we say the data is close to each other.

#import the package we need
#import flask, a web development tool. Flask is a microframework for Python. credits to
#http://flask.pocoo.org/
import flask
#import redis, a data structure server. Redis will give us support so that we can write
#and read data in the real time and at the same time.
import redis
#import collections, it is a high performance container datatypes.
import collections
#import json will help us load the arrival time for every tweet in json format.
#And it will also help us save the time differences in json format.
import json
#numpy is used for large, multi-dimensional arrays and matrices.
import numpy as np

#class flask.Flask. is an application object.
app = flask.Flask(__name__)
#connect to redis, so that we can calculate the average arrival time differences in the
#real time and at the same time when the data is written into redis
conn = redis.Redis()

#Here we will define the way to get the histogram.
def buildHistogram():
	#get the key, which will lead us to find the cities and its referring URL 
	#keys are stored by insert_city.py
    keys = conn.keys()
    #find the referring URLs according to the keys - cities
    values = conn.mget(keys)
    #add the appearances time of each key
    c = collections.Counter(values)
    #sum all the appearances time of the keys together to get the total number of the key 
    #values
    z = sum(c.values())
    #total number divided by the appearances time is the probability, which is the histogram 
    return {k:v/float(z) for k,v in c.items()}
    
#Here we all the buildHistogram function.
h = buildHistogram()
#Here we calculate the entropy and try to know how close our data is.
entropy = -sum([p*np.log(p) for p in h.values()])

#According my experiment, if entropy is larger than 0.5, we say the data is far apart
if entropy > 0.5:
	print 'the data is far apart'
#if the entropy is between 0.1 and 0.5, we say the data is not close and not far apart
if 0.1 <= entropy <= 0.5:
	print 'the data is not close not far apart'
#if the entropy is less than 0.1, we say the data is close
if entropy < 0.1:
	print 'the data is close'