#!/usr/local/bin/python

#credits to Columbia University Storytelling with Stream Data Course.

#Please curl https://github.com/usagov/1.USA.gov-Data when using this one

#In this file, we will get the key information from gov website. We define the key information
#as the cities mentioned in the gov web. The key is very important since we will use the 
#key as an indicator to calculate the rate, referring, distribution, and entropy.

#import the package we need
#import json will help us load the arrival time for every tweet in json format.
#And it will also help us save the time differences in json format.
import json
#stdout is used for display the results in the terminal
import sys
#import redis, a data structure server. Redis will give us support so that we can write
#and read data in the real time and at the same time.
import redis
#import time will help us record the time
import time

#connect to redis, so that we can know the referring URL
#real time and at the same time when the data is written into redis
conn = redis.Redis()

#while true
while 1:
	#we want to read data from redis
    line = sys.stdin.readline()
    try:
    #If there is a line in redis, we want to load it
        d = json.loads(line)
    except ValueError:
        # sometimes we get an empty line, so just skip it
        continue

    try:
    #we know that the data we get from load line will have the keyword city. That's what
    #we cared.
    #By using this geo-location information, which means the city mentioned in the API, 
    #and also the referring URL, which means how the users linked to this data. I care 
    #about the city information because I want to know which cities in the United
    #States is mentioned more often, by knowing that, we can assume that these cities may be
    #very popular and very active in United States. 
        city = d["cy"]
    except KeyError:
        # if there is no city present in the message
        # then store a "null" city
        city = "null"

	#let's find the arrival time this information we get
    t = str(time.time())
    #set the key to hold the arrival time and cities for 120 seconds
    conn.setex(t, city, 120)
    #let's print the time 
    print json.dumps({"t":t, "cy":city})
    #force clean the cache, since WebSocket only update the output when refresh the cache.
    sys.stdout.flush()