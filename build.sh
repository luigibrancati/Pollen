#!/bin/bash
pyinstaller -c -w -i .\icons\pollen.ico --onefile -n Pollen main.py
chmod +x ./dist/Pollen
mkdir temp
cp ./dist/Pollen ./temp/
cp configuration.json ./temp/
cp LEGGIMI.txt ./temp/
cd ./temp && tar -zcvf ../releases/Pollen_ubuntu_20-04.tar.gz . && cd -
rm -rf ./temp
rm -rf ./dist
rm -rf ./build