#!/bin/sh
killall mongod -9
rm ~/var/mongodb/* -rf
mongod --fork --logpath ~/var/mongodb/log --dbpath ~/var/mongodb

source activate spearmint
python ~/envs/spearmint/lib/python2.7/site-packages/spearmint/main.py .
source deactivate
