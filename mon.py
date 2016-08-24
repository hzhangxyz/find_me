#!/usr/bin/env python
import subprocess as sp
import sys
from optparse import OptionParser
parser = OptionParser()
parser.add_option("-N","--name",dest="name",help="name of the material")
parser.add_option("-n","--node",dest="node",help="nodes that is running its mongodb")
parser.add_option("-w","--www",dest="www",help="web directory",default="/home/hzhang/cod")
(opt,args)=parser.parse_args()
name = opt.name
node = int(opt.node)
www = opt.www
to_print = r"""<body style='padding:5%'>
<h1>Monitor</h1>
<pre style='font-size:150%'>
<script>
var r=new XMLHttpRequest();
r.open('GET',location.href,false);
r.send();
document.write('The Current Time is\t\t:\t');
document.write(r.getResponseHeader('Date'));
document.write('\n')
document.write('Report Generated at\t\t:\t')
document.write(r.getResponseHeader('Last-Modified'))
document.write('\n')
</script>
"""
d = sp.check_output(r"./en.py -cn 10000",
                     shell=True)
data=map(float,d.split())
to_print += "Sampled Structure Number is \t:\t%d\n"%len(data)
d = sp.check_output(r"./en.py -n 10000",
                     shell=True)
data=map(float,d.split())
to_print += "Mongodb Structure Number is \t:\t%d\n"%int(
    sp.check_output("mongo cu%02d/spearmint "
                    "--eval 'db.%s.jobs.find().size()'"
                    " | tail -n 1"%(node,name),shell=True))
to_print += "Totaled Structure Number is \t:\t%d\n"%len(data)
to_print += "Current Processes Number is \t:\t%d\n"%int(
    sp.check_output("ssh cu%02d ps -A"
                    "|grep vasp"
                    "|wc -l"%node,
                    shell=True))
import matplotlib as mpl
mpl.use('Agg')
from matplotlib import pyplot as plt
fig,axes=plt.subplots()
axes.scatter(range(len(data)),data,color="#00ff00",s=1)
axes.patch.set_facecolor('#000000')
axes.set_ylim([-40,5])
axes.set_xlim([-10,len(data)+10])
fig.set_size_inches(10, 7)
fig.savefig('/home/hzhang/cod/%s-%02d-mon.png'%(name,node))
to_print += '</pre><img src=%s-%02d-mon.png width=100%%></img>\n<pre>'%(name,node)
try:
    data=map(float,sp.check_output(
        r"./en.py -n 1000 -rc",
        shell=True).replace(":","").split())
    to_print += "Minimum Energy is\t:\t%f\n\nCONTCAR\t:\n\n"%min(data)
    to_print += sp.check_output(r"cd try_%d;cat CONTCAR"%int(data[data.index(min(data))-1]),shell=True)
except:
    pass
with open("%s/%s-%02d-mon.html"%(www,name,node),"w") as f:
    f.write(to_print)
