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
  json="$dir/document.json"
  txt="$dir/document.txt"

  mkdir -p "$dir"

  if [ ! -f "$pdf" ] ; then
    case "$suffix" in
    zip)
      echo "$id: skipping ZIP"
      continue
      ;;

    pdf)
      echo "$id: linking PDF"
      ln -f "$path" "$pdf"
      ;;

    *)
      echo "$id: converting to PDF"
      (
        ln -f "$path" "$doc"
        cd $dir
        lowriter --headless --convert-to pdf "document.$suffix"
        rm document.$suffix
      )
      ;;
    esac
  fi

  if ls $dir/page*.png > /dev/null 2>&1 ; then : ; else
    echo "$id: extracting images"
    pdftoppm -l 99 -png "$pdf" "$dir/page"
  fi

  if [ ! -f "$json" ] ; then
    echo "$id: extracting metadata"
    if java -jar cache/tika.jar -j "$path" > "$json" 2> "$dir/tika-json.err" ; then
      rm $dir/tika-json.err
    fi
  fi

  if [ ! -f "$txt" ] ; then
    echo "$id: extracting text"

    # gs -q -sDEVICE=txtwrite -o "$dir/page-%d.txt" "$pdf"
    # pdftotext "$pdf"

    if java -jar cache/tika.jar -t "$path" > "$txt" 2> "$dir/tika-txt.err" ; then
      rm $dir/tika-txt.err
      tmp=/tmp/tika.$$

      # reduce blanks ..
      sed \
        -e 's/[[:space:]]*$//'\
        -e '/^$/N;/^\n$/D' \
        < "$txt" > "$tmp"

      mv "$tmp" "$txt"
    fi
  fi
done
