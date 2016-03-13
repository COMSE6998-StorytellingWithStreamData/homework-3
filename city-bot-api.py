#!/usr/local/bin/python

#credits to Columbia University Storytelling with Stream Data Course.

#In this file, we will generate the APIs for rate, entropy, distribution, and probability.
#This file is so important, that the results will be shown on localhost:5000.

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

#This one will help us show the rate on localhost:5000 by typing localhost:5000/rate
@app.route("/rate")
#define rate
def rate():
	#call the build Histogram function
	h = buildHistogram()
	#The rate equals the total data we get divided by the time interval
	rate = len(h)/2.0
	#show the rate on the webpage
	return json.dumps(rate)        
    

#This one will help us show the histogram of each cities we get        
@app.route("/")
#define histogram
def histogram():
	#call the build Histogram function
    h = buildHistogram()
    #show the histogram on the webpage
    return json.dumps(h)

#This one will help us show the entropy      
@app.route("/entropy")
#define entropy
def entropy():
	#call the build Histogram function
    h = buildHistogram()
    #calculate entropy by the following function
    return json.dumps(-sum([p*np.log(p) for p in h.values()])) 

#This one will help us show the probabilities of each cities we get    
@app.route("/probability")
#define probability
def probability():
	#find the city called mountain view
    city = flask.request.args.get('city', 'Mountain View')
    #fine the referer from www.google.com
    ref = flask.request.args.get('referrer', 'www.google.com')
    # get the distribution for the city
    print city
    #put it in the redis
    d = conn.hgetall(city)
    # get the count for the referrer
    try:
    	#get the referring
      c = d[ref]
    except KeyError:
    	#output the city, probability and referring URL
    	#if the key is error, the probability is zero.
      return json.dumps({
        "city": city, 
        "prob": 0,
        "referrer": ref
      })
    # get the normalising constant
    z = sum([float(v) for v in d.values()])
    #output the city, probability and referring URL
    #if the key is not error, calculate the probability
    return json.dumps({
      "city": city, 
      "prob": float(c)/z,
      "referrer": ref
      })

#the main function
if __name__ == "__main__":
    app.debug = True
    app.run()