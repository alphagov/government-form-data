#!/bin/bash


find documents/attachment -name \*.png |
while read file
do
  gif=${file%.png}.gif
  convert "$file"  -format gif -thumbnail 50x71 -unsharp 0x.5 "$gif"
done
