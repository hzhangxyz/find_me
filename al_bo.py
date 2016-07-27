#!/usr/bin/env python
with open("output","r") as out_file:
    data=out_file.read()
data="[%s]"%data.replace("\n",",")
data=[[i["point"], i["value"]] for i in eval(data)]
to_count=[i[0] for i in data]
