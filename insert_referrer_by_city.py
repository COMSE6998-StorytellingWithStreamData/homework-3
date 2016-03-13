#!/usr/local/bin/python

#credits to Columbia University Storytelling with Stream Data Course.

#In this file, we will get the referring URL about each keys - cities. Why I care about 
#the referring URL? Because I want to know what's the source the users are
#using to get access to this data information. By exploring that, we can know how popular
#this data information is if multi-source web URL linked to the same one data information.
#We can also know what is the most popular search engine people are using. We can also
#explore people's behavior pattern on using the webpage. Do they usually click google, then
#link to the government data information? Do they usually like to jump to the related 
#data information from the government website? There are tons of interesting things we can 
#explore by using cities and referring URL.

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
#This module defines a standard interface to break Uniform Resource Locator (URL) strings 
#up in components (addressing scheme, network location, path etc.), to combine the 
#components back into a URL string, and to convert a “relative URL” to an absolute URL 
#given a “base URL.” (credits to https://docs.python.org/2/library/urlparse.html)
import urlparse

#connect to redis, so that we can know the referring URL
#real time and at the same time when the data is written into redis
conn = redis.Redis()

#while true
while 1:
	#we want to read data from redis
    line = sys.stdin.readline()
    #If there is a line in redis, we want to load it
    try:
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
        # then let's just ditch it
        continue

    try:
    #we know that the data we get from load line will have referring URLs.
    #I want to know what's the source the users are using to get access to this data 
    #information. By exploring that, we can know how popular this data information is if 
    #multi-source web URL linked to the same one data information. We can also know what 
    #is the most popular search engine people are using. We can also explore people's 
    #behavior pattern on using the webpage. Do they usually click google, then link to the 
    #government data information? Do they usually like to jump to the related data 
    #information from the government website? There are tons of interesting things we can 
    #explore by using cities and referring URL.
        referrer = d["r"]
    except KeyError:
        # if there is no referrer present in the message
        # then let's just ditch it
        continue

    #if the url is from the gov webpage itself, we will define it as direct
    if referrer == "direct":
        netloc = "direct"
        #if the url is from other outside webpage, we will define it as the source webpage
    else:
        o = urlparse.urlparse(referrer)
        netloc = o.netloc
        
	#When we find a pair, we say we will count it to 1
    conn.hincrby(city, netloc, 1)
    #let's print the city and its referring URL
    print json.dumps({"cy": city, "r": netloc})
    #force clean the cache, since WebSocket only update the output when refresh the cache.
    sys.stdout.flush()