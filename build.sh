#!/bin/bash
rm -rf dist/
pyinstaller -c -w -i .\icons\pollen.ico --onefile -n Pollen --add-data configuration.json:configuration.json main.py
chmod +x ./dist/Pollen
cp configuration.json ./dist/
