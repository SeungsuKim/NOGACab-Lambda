#!/usr/bin/env bash

rm darknet.zip
cd env_NOGACab-Lambda/lib/python3.6/site-packages/
zip -r9 ../../../../site-packages.zip .
cd ../../../../
cd darknetmin
zip -r9 ../darknet.zip .
cd ../
mkdir test
cp site-packages.zip test/site-packages.zip
cp darknet.zip test/darknet.zip
rm site-packages.zip
rm darknet.zip
cd test
unzip site-packages.zip
unzip darknet.zip
rm site-packages.zip
rm darknet.zip
chmod 755 darknet
zip -r9 ../darknet.zip .
cd ../
rm -rf test