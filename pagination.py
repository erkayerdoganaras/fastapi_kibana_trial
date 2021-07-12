#Trial Codes for PAgination only

res= es.search(index="logstash-2021.07.01",scroll='1m',size=1700,body=myquery) #Size can change due to query

sid=res["_scroll_id"]
scroll_size=res["hits"]["total"]
scroll_size=scroll_size["value"]
for i in res["hits"]["hits"]:
    print(i)
print(res["_scroll_id"])


counter=0 
while(scroll_size>0):
    page=es.scroll(scroll_id=sid,scroll="2m")
    sid=page["_scroll_id"]
    scroll_size=len(page["hits"]["hits"])
    counter+=1

print("total :{}".format(counter))




#PAGINATION METOT2
res=es.search(index="logstash-2021.07.01",size=100,body=myquery,from_=0)
data=res["hits"]["hits"]
hashmap={}
step=1
for i in range(len(data)):
    if i==0:
        hashmap[i] = data[0:step]
    else:
        startIndex = step * i
        EndIndex =  ((i+1) * (step))
        sample = data[startIndex:EndIndex]
        hashmap[i] = sample
for i in hashmap:
    print(hashmap[i])

print(type(hashmap))



#PAGINATION METOT3(FROM SIZE)
query_trial={
    "from":0,
    "size":100,
    "query": {
    "bool": {
      "must":
        {
          "match_phrase": {
            "kubernetes.namespace_name": {           #this part can change
              "query": "kube-system"
            }
          }
        },
      "filter": [
        {
          "match_all": {}
        }
      ],
      "should": [],
      "must_not": []
    }
  }
        }
#index would change
res=es.search(index="logstash-2021.07.01",body=query_trial,size=100)
data=res["hits"]["hits"]
data2=res["hits"]["total"]
for i in data:
    print(i)
    
    
    
    
    
    
#Have a look at this
{
  "index": {
    "max_result_window": 10000000
  }
}

#Look at this too
https://kb.objectrocket.com/elasticsearch/elasticsearch-and-scroll-in-python-953
https://gist.github.com/hmldd/44d12d3a61a8d8077a3091c4ff7b9307
