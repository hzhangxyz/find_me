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
direc = "."
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
d = sp.check_output(r"cd %s;./en.py -cn 10000"%direc,
                     shell=True)
data=map(float,d.split())
to_print += "Sampled Structure Number is \t:\t%d\n"%len(data)
d = sp.check_output(r"cd %s;./en.py -n 10000"%direc,
                     shell=True)
data=map(float,d.split())
to_print += "Mongodb Structure Number is \t:\t%d\n"%int(
    sp.check_output("mongo cu%02d/spearmint "
                    "--eval 'db.%s.jobs.find().size()'"
                    " | tail -n 1"%(node,name),shell=True))
to_print += "Totaled Structure Number is \t:\t%d\n"%len(data)
to_print += "Current Processes Number is \t:\t%d\n"%int(
    sp.check_output("ssh cu%02d ps -A"
                    "|grep vasp_with"
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
fig.savefig('/home/hzhang/cod/%s-mon.png'%name)
to_print += '</pre><img src=%s-mon.png width=100%%></img>\n'%name
with open("%s/%s-mon.html"%(www,name),"w") as f:
    f.write(to_print)
