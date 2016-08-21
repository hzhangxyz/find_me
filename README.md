# FIND_ME

Find_me is optimization software for minimum energy structure **under development**.

## Content

<ul>
  <li>
    <a href=#our-goal>Our Goal</a>
  </li>
  <li>
    <a href=#did-and-test>Did And Test</a>
    <ul>
      <li>
        <a href=#a-wrap-for-vasp>A wrap for VASP</a>
        <ul>
          <li><a href=#a-test>A Test</a></li>
          <li><a href=#instruction-for-poscar>instruction for POSCAR</a></li>
          <li><a href=#attention>Attention</a></li>
        </ul>
      </li>
      <li>
        <a href=#link-with-pso>link with PSO</a>
      </li>
      <li>
        <a href=#link-with-random-search>link with random search</a>
      </li>
      <li>
        <a href=#link-with-spearmint>link with Spearmint</a>
        <ul>
          <li><a href=#code>Code</a></li>
          <li><a href=#test>Test</a></li>
          <li><a href=#attention-1>Attention</a></li>
          <li><a href=#some-test-output>Some Test Output</a></li>
        </ul>
      </li>
    </ul>
  </li>
  <li>
    <a href=#todo>TODO</a>
  </li>
</ul>

## Our Goal

Input element and atoms number, 

via optimization method, and [VASP](http://www.vasp.at/), 

with calculation and optimization, 

it output the global minimum energy structure.

## Did And Test

### A wrap for VASP

As you see in [POSCAR example](https://github.com/zh19970205/find_me/blob/master/test/H2O/POSCAR), 
We define a format to get the true POSCAR for VASP, 
with parser [shared.py](https://github.com/zh19970205/find_me/blob/master/shared.py). 

So we get a python function with structure parameters(positions of atoms) as arguments, 
which call VASP and return energy.

#### A Test

Try:
```
# git clone git@github.com:zh19970205/find_me.git
...
# cd find_me
# ./get_data.sh H2O
# python
...
>>> from shared import get_energy
>>> get_energy([1,1.5,1.2],0,0)
-7.96509304
```

get_data.sh is just a script copying POSCAR, POTCAR, and config.json from test/ to .

POSCAR:
```
H2O
1.00
5       0       0
0       5       0
0       0       5
H       O
2       1
cart
0.00    0.00    0.00
{(a)}   0.00    0.00
{(b)}   {(c)}   0.00
{{
precision       2
vars
a       0.1     2
b       -2      2
c       0.1     2
}}
```

#### instruction for POSCAR

- {...} means this should be replace before calling VASP, and inside it, you can write expression like {(r)*cos(theta)}, this is useful if you know about some symmetry of the structure
- variables should be in (...), for parsing easier
- inside {{...}}, there is some options, eg: precision means decimal places, 
there are some options for random search: cores and times(the totally structure you will calculate is cores*times), 
there are some options for pso: omega, phip, phig.
- after vars, there is variables and its domain

As you see above, {(a)} will be replaced by 1 and {(b)} replaced by 1.5 and {(c)} replaced by 1.2, 
and then python will call VASP and get **the last TOTEN from OUTCAR**.

#### Attention

find_me need VASP **without** mpi, or there will be conflict between mpi in VASP and it in find_me. 
It is general knowledge that parallel program isn't as efficient as serial program. 

![http://cms.mpi.univie.ac.at/vasp/vasp/img49.png](http://cms.mpi.univie.ac.at/vasp/vasp/img49.png)

so we decide to give the parallel chance to optimization method, for its good parallel performance. 

So please compile a version without mpi for VASP and rename it as "vasp_without_mpi" and put it into $PATH

### link with [PSO](https://en.wikipedia.org/wiki/Particle_swarm_optimization)

the code is in [pso_find_me.py](https://github.com/zh19970205/find_me/blob/master/pso_find_me.py), Just for test and contrasts. You can ignore it. 

Try:
```
# ./get_data.sh H2O
```
and set times 3 and cores 3 in POSCAR, and
```
# mpirun -n 3 python pso_find_me.py
[0.6396422576541099, -1.178237412205891, 0.7174609562987219]
-6.90623521
[0.6396422576541099, -1.178237412205891, 0.7174609562987219]
-6.90623521
[0.6396422576541099, -1.178237412205891, 0.7174609562987219]
-6.90623521
[1.0460718276254388, -0.3878937232244988, 0.718089995806529]
-8.21903742
```
it will output parameters and energy of the observed minimum energy structure for each time.

### link with random search

the code is in [surf_energy.py](https://github.com/zh19970205/find_me/blob/master/surf_energy.py), Just for test. You can ignore it. 

Try:
```
# ./get_data.sh H2O
```
and set times 3 and cores 3 in POSCAR, and
```
# mpirun -n 3 python surf_energy.py
[0.5729802365387486, -0.5199666951689141, 1.3634050774944872]
-6.27935381
[0.39566346272656694, -1.682242752146247, 0.4674818456204878]
-1.1084951
[0.13055589978807816, -1.6821267522002494, 0.15910217557314077]
65.58070443
[0.27638633468013285, 1.1741958325033757, 1.359220673768153]
10.30662607
[0.8015793042340994, -1.3107675554786464, 1.2112746779577124]
-7.12601719
[1.1276158144716721, -0.18502400862421853, 1.4800347737040116]
-7.2327105
[1.3406260585320342, 1.426072101772327, 1.1315826861224447]
-9.06377695
[1.172328113256835, 1.4295430294010014, 1.915353771208993]
-5.99833314
[1.8795975781044238, 0.083169635727661, 1.8483449168154649]
-4.2747424
```
it will output parameters and energy for each calculation.

### link with [Spearmint](https://github.com/HIPS/Spearmint)

Spearmint is an implementation of [Bayesian Optimization](https://en.wikipedia.org/wiki/Bayesian_optimization). 
When it work, it play a role as a manager to call function you supply.

#### Code

Spearmint need a config.json([example](https://github.com/zh19970205/find_me/blob/master/test/H2O/config.json)), 
and a python script with main function in it. 

So we just wrap a function for Spearmint over shared.py 
in [spearmint_link.py](https://github.com/zh19970205/find_me/blob/master/spearmint_link.py) 

#### Test

Try:
```
# mkdir ~/var
# mongod --fork --logpath ~/var/mongodb/log --dbpath ~/var/mongodb
# python \</path/to/python/library/directory\>/site-packages/spearmint/main.py .
```
then you will get many 00000***.out in output/
```
# cat output/* | grep Got\ result | sed s/Got\ result\ //
```
then you get the output energy for each step

#### Attention
- Spearmint require pymongo, numpy, scipy and mongdb.

#### Some Test Output

##### H2O(3 param)

The true energy is -14.224 eV, find_me find -14.056 eV.

![H2O](https://raw.githubusercontent.com/zh19970205/find_me/master/images/H2O.bmp)

##### NH3(6 param)

The true energy is -19.246,find_me find -19.259 eV.

![NH3](https://raw.githubusercontent.com/zh19970205/find_me/master/images/NH3.bmp)

##### CH4(9 param)

The true energy is -23.678 eV.

Calculating...

x axis is iteration step and y axis is energy(eV).

As you see, it seems that there are two element during optimization: exploration and exploitation, 
at first exploration has more weight and later exploitation has.
This balance is maintained automatically in Bayesian Optimization.

## TODO

- Useless
  - Compiling Optimization for VASP(Gamma Point Only)
  - Other OM combined with ML?(PSO?)
  - Can Spearmint be separated more with VASP?
  - integrated dft and opt(OK, Think too much)
- To learn about
  - AIRSS?
- Don't Do Repeatly
  - Get info of relaxation in VASP
  - Can WAVECAR be used?
- Don't Do Uselessly
  - Learn to use Spearmint
  - Know about GP and Stochastic Process
  - prior probability with EAM,...(EI/second) ?
  - Set lower precision to accelerate calculation(dynamic, because it may be useful only at first)(Time Complexity)

