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
res=es.search(index="logstash-2021.07.01",size=50,body=myquery)
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

print(hashmap)
