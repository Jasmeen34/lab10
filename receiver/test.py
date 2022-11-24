import connexion
from connexion import NoContent
import json 
import datetime

lst = []
with open("event.json", "r+") as fh:
   data = json.load(fh)
   
   for i in data:
         lst.append(i)
         print(len(lst))
        