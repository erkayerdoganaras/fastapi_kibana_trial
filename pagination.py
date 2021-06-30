#Trial Codes for PAgination only

res= es.search(index="logstash-2021.06.26",scroll='2m',size=10,body=query_body)
counter=0
sid=res["_scroll_id"]
scroll_size=res["hits"]["total"]
scroll_size=scroll_size["value"]

while(scroll_size>0 and counter<400):
    page=es.scroll(scroll_id=sid,scroll="10m")
    sid=page["_scroll_id"]
    scroll_size=len(page["hits"]["hits"])
    counter+=1

print("total :{}".format(counter))
