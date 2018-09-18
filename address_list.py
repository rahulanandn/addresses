import requests
from lxml import html
import json
import pandas as pd

import string
import os

from flask import Flask, request,  make_response
app = Flask(__name__)

@app.route("/", methods=['post'])
def index():
    pincode = request.get_json()['result']['parameters']['pincode']
    print(pincode)
    r = requests.get("https://secureorder.bt.com/consumerProducts/v1/addressSearch.do?postcode=%s&house=&format=json" % (pincode))
    r = r.json()
    offers = {'messages':[]}


    if 'addresses' not in r:
        offers['messages'].append({'platform':'facebook', 'type': 0, 'speech': 'No addreses found.'})
        response = make_response(json.dumps(offers))
        response.headers['Content-Type'] = 'text/plain'
        return response        


    for i in r['addresses']:
        
        SubBuildingName = i['SubBuildingName']
        BuildingName = i['BuildingName']
        BuildingNumber = i['BuildingNumber']  
        ThoroughfareName = i['ThoroughfareName']
        PostTown = i['PostTown']
        Postalcode = i['Postalcode']
        
        #my_response = (SubBuildingName,BuildingName,BuildingNumber,ThoroughfareName,PostTown,Postalcode)   # Tupple
        #my_response = list(filter(None, my_response))
        #my_response.remove('')
        #set(my_response)
        
        my_response = "%s %s %s %s %s %s" %(SubBuildingName, BuildingName, BuildingNumber, ThoroughfareName, PostTown, Postalcode)


        # Card
        offers['messages'].append({'buttons':[{'postback':'https://www.google.com/','text':'Select'}],'platform':'facebook', 'type': 1, 'title': my_response})
        

        # Simple message
        
        #offers['messages'].append({'platform':'facebook', 'type': 0, 'speech': my_response})
        
        # Quick Reply
        #offers['messages'].append({'replies':[my_response],'platform':'facebook', 'type': 2, 'title': my_response})


        # Basic card
        #offers['messages'].append({'buttons':[{"openUrlAction":'https://www.google.com/','title':'Select'}],'platform':'facebook', 'type': 'basic_card', 'title': my_response})


        #break
        
        # print(type(my_response))

    
        #my_json = json.dumps({'speech':my_response}, indent=4)
        #response = make_response(my_json)
        #response.headers['Content-Type'] = 'text/plain'

#     test_response = """




#     """

    #my_test_response = make_response(json.loads(test_response))
    #print(my_test_response)
    print(json.dumps(offers))
    response = make_response(json.dumps(offers))
    response.headers['Content-Type'] = 'text/plain'
    return response
    
        #my_json = json.dumps({'speech':add_full}, indent=4)
        #response = make_response(add_full)
        #response.headers['Content-Type'] = 'text/plain'
    

if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')




  
