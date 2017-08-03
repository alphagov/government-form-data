#!/bin/bash

echo "attachment	page-number	colours"
find documents/attachment -name page-*.png |
  while read file
  do
    attachment=$(echo "$file" | sed -e 's/^.*attachment\/\([0-9]*\)\/.*$/\1/')
    pageno=$(echo "$file" | sed -e 's/^.*page-0*\([0-9][0-9]*\).png/\1/')
    colours=$(convert $file +dither -colors 5 -unique-colors -define histogram:unique-colors=true -format "%c" histogram:info: 2> /dev/null |
      sed -e 's/^.*#\([0-9A-F]*\).*$/\1;/' |
      tr -d '\n' |
      sed -e 's/;$//')
    echo "$attachment	$pageno	$colours"
  done
