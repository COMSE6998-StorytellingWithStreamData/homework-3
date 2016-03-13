Homework 3

In this homework, I explored how to find the distribution of a set of data, find the rate
of the stream, know the distribution of the data, explore the entropy of the distribution, 
which means how close these data are to each other. Further more, I can fine the 
probability of a new message given the stored distributions. 

By exploring the entropy of the distributions, I can clearly know how close the data I 
get and if their relations are becoming closer and closer, or apart. According to my 
experiment, I set a threshold for monitering the changing in entropy.

Finally, I build a webpage to display the distributions that stored in my system.

The API I am using is from USA government. In this API, it will contain user agent, 
country code, known user, global bitly hash, encoding user bitly hash, encoding user login,
short url cname, referring url, long url, timestamp, geo region, geo city name, time zone,
timestamp of time hash and accept language. 
(credits to https://github.com/usagov/1.USA.gov-Data)

In my homework, I mainly focus on the geo-location information, which means the city 
mentioned in the API, and also the referring URL, which means how the users linked to this
data. I care about the city information because I want to know which cities in the United
States is mentioned more often, by knowing that, we can assume that these cities may be
very popular and very active in United States. 

Why I care about the referring URL? Because I want to know what's the source the users are
using to get access to this data information. By exploring that, we can know how popular
this data information is if multi-source web URL linked to the same one data information.
We can also know what is the most popular search engine people are using. We can also
explore people's behavior pattern on using the webpage. Do they usually click google, then
link to the government data information? Do they usually like to jump to the related 
data information from the government website? There are tons of interesting things we can 
explore by using cities and referring URL.

In order to successfully run this homework, first we need to curl the gov webpage, by using 
curl. Then use insert_city.py file to find the key "cities". We will further use this key
to find the distribution, rate, entropy, and probability. Third, please run insert referrer
by city, it will give us the referrer URL. Then run the decrementer.py file, which will
make sure the count won't go infinity. Finally we can run city-bot-api.py file, which will
give us the rate, entropy, distribution and probability. The results can be seen on 
localhost:5000. 

Please double check the redis is connected before you run the code. 