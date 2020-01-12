#!/bin/bash

mkdir -p data

wget http://www.robots.ox.ac.uk/~vgg/data/pets/data/images.tar.gz
tar xf images.tar.gz -C data
rm images.tar.gz

wget http://www.robots.ox.ac.uk/~vgg/data/pets/data/annotations.tar.gz
tar xf annotations.tar.gz -C data annotations/xmls
rm annotations.tar.gz

mkdir -p pretrained
wget -O pretrained/darknet53.weights https://pjreddie.com/media/files/darknet53.conv.74
python keras-yolo3/convert.py -w keras-yolo3/darknet53.cfg pretrained/darknet53.weights pretrained/darknet53.h5
