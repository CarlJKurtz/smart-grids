#!/bin/sh

mkdir -p dist/dmg

rm -r dist/dmg/*

cp -r 'dist/SmartGrids.app' dist/dmg

test -f 'dist/SmartGrids.dmg' && rm 'dist/SmartGrids.dmg'
create-dmg \
  --volname 'SmartGrids' \
  --volicon 'assets/SmartGrids_Icon.png' \
  --window-pos 200 120 \
  --window-size 600 300 \
  --icon-size 100 \
  --icon 'SmartGrids.app' 175 120 \
  --hide-extension 'SmartGrids.app' \
  --app-drop-link 425 120 \
  'dist/SmartGrids.dmg' \
  'dist/dmg/'
