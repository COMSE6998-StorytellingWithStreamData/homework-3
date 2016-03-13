#!/usr/local/bin/python

#credits to Columbia University Storytelling with Stream Data Course.

# Run the decrementer.py file, which will make sure the count won't go infinity.

#import the package we need
#import redis, a data structure server. Redis will give us support so that we can write
#and read data in the real time and at the same time.
import redis
#import time will help us record the time
import time
#import json will help us load the arrival time for every tweet in json format.
#And it will also help us save the time differences in json format.
import json
#stdout is used for display the results in the terminal
import sys

#connect to redis, so that we can know the referring URL
#real time and at the same time when the data is written into redis
conn = redis.Redis()

while True:
	#from radis, get the key cities value
    cities = conn.keys()
	
	#city is the the hashtable, we will need to find the appearances time by getting city
    for city in cities:
    	#If city is not empty, we will get the city value, which contains the appearances
    	#time
        try:

            d = conn.hgetall(city)
            
			#if we find the referring, we want to know the appearances time
            for ref in d:
            	#if the appearances time is larger than 1
                if int(d[ref]) > 1:
            		#we want to reduce the appearances time by 1 since we don't want to 
            		#overflow the appearances time
            		
            		#first give the appearances time to count
                    count = int(d[ref])
                    #then count reduce by 1
                    count -= 1
                    #let the new appearances time equals to the count
                    d[ref] = str(count)

			#Now combine the city and referring together
            conn.hmset(city,d)
        except:
            pass

	#Set a sleep time to 2 seconds, which means we will do this decrement every 2 seconds
    time.sleep(2)

