# url_checker
This code cheks a bunch of domain and find active ones for each categories


In this project I used "URL-categorization-DFE.csv" dataset.

Before using it for crawling or something else, we need to be sure the domain (url) addresses are active.

So this code take all domains and ask them to cloudflare dns "1.1.1.1" and 

if an IP address return from the dns that means it is an active domain so it writes down it to the csv file.
