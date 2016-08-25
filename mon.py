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
to_print += '</pre><img src=%s-%02d-mon.png width=100%%></img>\n<pre style="font-size:150%%">'%(name,node)
data=map(float,sp.check_output(
    r"./en.py -n 1000 -rc",
    shell=True).replace(":","").split())
to_print += "Minimum Energy is\t:\t%f\n\nCONTCAR\t\t\t:\n"%min(data)
min_poscar = int(data[data.index(min(data))-1])
to_print += "</pre><pre>%s</pre><pre style='font-size:150%%'>\nPlot\t\t\t:\n</pre>"%sp.check_output(r"cd try_%d;cat CONTCAR"%min_poscar,shell=True)

d = r"""
<script type="text/javascript" src="three.js"></script>
<script type="text/javascript">
var scene = null;
var camera = null;
var renderer = null;
var light = null;

var mesh = null;
var meshes = [];
var id = null;

function init() {
renderer = new THREE.WebGLRenderer({
canvas: document.getElementById('mainCanvas')
});
renderer.setClearColor(0x000000);
scene = new THREE.Scene();

light = new THREE.PointLight( 0xFFFFFF );
light.position.set(10,2,2);
scene.add( light );

//camera = new THREE.OrthographicCamera(-2, 2, 2, -2);
camera = new THREE.PerspectiveCamera()
camera.position.set(1, 0.5, 0);
camera.lookAt(new THREE.Vector3(0, 0, 0));
scene.add(camera);

proto_mesh = new THREE.Mesh(new THREE.SphereGeometry(0.03, 16, 16), new THREE.MeshLambertMaterial({
color: 0x00ff00
}));

//HERE

/*
{[(
m%d = proto_mesh.clone()
m%d.position.set(%f,%f,%f);
scene.add(m%d);
meshes.push(m%d);
)]}
*/

id = setInterval(draw, 20);
}

function draw() {
meshes.forEach((m)=>{
m.position.applyEuler(new THREE.Euler(0,0.01,0,"XYZ"))
});
//camera.position.applyEuler(new THREE.Euler(0,0,0.01,"XYZ"))
//light.position.applyEuler(new THREE.Euler(0,0,0.01,"XYZ"))
//camera.lookAt(new THREE.Vector3(0, 0, 0));
renderer.render(scene, camera);
}
</script>

<canvas id="mainCanvas" width="500px" height="500px" ></canvas>
<script>
init()
</script>
</body>
</html>
"""

start_pos = d.find("{[(")+3
end_pos = d.find(")]}")
proto = d[start_pos:end_pos]+"\n\n"

with open("try_%d/CONTCAR"%min_poscar,"r")  as f:
    contcar = f.read()

direct = contcar.find("Direct")+6
pos_end = contcar.find("\n \n")

pos = contcar[direct:pos_end]
pos_d = pos.split()

data = []
for i in range(len(pos_d)/6):
    data.append(map(float,pos_d[i*6:i*6+3]))

for i in range(len(data)):
    for j in range(3):
        if data[i][j] < -0.5:
            data[i][j] += 1
        if data[i][j] > 0.5:
            data[i][j] -= 1

to_replace = ""

for i in range(len(data)):
    to_replace += proto%(i,i,data[i][0],data[i][1],data[i][2],i,i)

to_save = d.replace("//HERE",to_replace)

to_print += to_save
with open("%s/%s-%02d-mon.html"%(www,name,node),"w") as f:
    f.write(to_print)
