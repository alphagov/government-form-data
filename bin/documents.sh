#!/bin/bash

#
#  tries to build a page and text file for each page in every attachment
#

set -e
find cache/attachment -type f |
while read path
do
  id=$(echo "$path"|sed -e 's/^cache\/attachment\///' -e 's/\/.*$//')
  dir="documents/attachment/$id"

  suffix=$(echo ${path##*.} | tr '[:upper:]' '[:lower:]')
  doc="$dir/document.$suffix"
  pdf="$dir/document.pdf"

  mkdir -p "$dir"

  if [ ! -f "$pdf" ]; then
    case "$suffix" in
    pdf)
      # no need to convert PDFs
      ln -f "$path" "$pdf"
      ;;

    zip)
      echo "$id: skipping ZIP"
      continue
      ;;

    *)
      echo "$id: converting to PDF"
      ln -f "$path" "$doc"
      (
        cd $dir
        lowriter --headless --convert-to pdf "document.$suffix"
      )
      rm "$doc"
      ;;
    esac
  fi

  if ls $dir/page*.png > /dev/null 2>&1
  then
    :
  else
    echo "$id: extracting images"
    pdftoppm -rx 300 -ry 300 -png "$pdf" "$dir/page"
    mogrify -resize 50% $dir/page-*.png
  fi

  if ls $dir/document.txt > /dev/null 2>&1
  then
    :
  else
    echo "$id: extracting text"
    # gs -q -sDEVICE=txtwrite -o "$dir/page-%d.txt" "$pdf"
    pdftotext "$pdf"
  fi

done
