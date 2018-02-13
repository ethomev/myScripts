#!/usr/bin/python

import subprocess
import json
import argparse

parser = argparse.ArgumentParser(
    description='Get the average review open time for the specified project this year')

parser.add_argument("-p", "--project",
                    help="the project to get stats for")
parser.add_argument("-o", "--owner",
                    help="the owner to get stats for ")

args = parser.parse_args()

   
query_args_list=["ssh","-p","29418","gerrit.ericsson.se","gerrit","query","--format=JSON","status:merged","after:2018-01-01"]

if args.owner:
    query_args_list.append("owner:"+args.owner)

if args.project:
    query_args_list.append("project:"+args.project)
    
gerrit_query = subprocess.Popen(query_args_list, stdout=subprocess.PIPE)
subprocess.call(["tee", "output"], stdin=gerrit_query.stdout)

file = open('output', "r")

out = "["
for line in file:
   out = out + line + ","

out = out.rstrip(",")
out = out + "]"
parsed_json = json.loads(out)
count = 0
sumTime = 0

for review in parsed_json:
    if review.get("createdOn"):
        created = review['createdOn']
        lastUpdated = review['lastUpdated']
        openTime = (((lastUpdated - created)/60)/60)/24
        print(openTime)
        count = count +1
        sumTime = sumTime + openTime

print("Number of reviews is: "+str(count))
avg = sumTime/count
print("Average is: "+str(avg))

