#!/bin/bash

#
#  tries to build a page and text file for each page in every attachment
#

set -e
cat data/attachment.tsv |
while read attachment filename rest
do
  if [ "$attachment" == "attachment" ] ; then
      continue
  fi

  path=cache/attachment/$attachment/$filename

  suffix=$(echo ${path##*.} | tr '[:upper:]' '[:lower:]')

  dir="documents/attachment/$attachment"
  doc="$dir/document.$suffix"
  pdf="$dir/document.pdf"
  json="$dir/document.json"
  txt="$dir/document.txt"
  valid="$dir/verapdf.xml"

  mkdir -p "$dir"

  if [ ! -f "$pdf" ] ; then
    case "$suffix" in
    zip)
      echo "$attachment: skipping ZIP"
      continue
      ;;

    pdf)
      if [ -s "$pdf" ] ; then
        echo "$attachment: linking PDF"
        ln -f "$path" "$pdf"
      else
        echo "$attachment: skipping missing/empty PDF"
        continue
      fi
      ;;

    *)
      echo "$attachment: converting to PDF"
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
    echo "$attachment: extracting images"
    pdftoppm -l 99 -png "$pdf" "$dir/page"
  fi

  if [ ! -f "$json" ] ; then
    echo "$attachment: extracting metadata"
    if java -jar cache/tika.jar -j "$path" > "$json" 2> "$dir/tika-json.err" ; then
      rm $dir/tika-json.err
    fi
  fi

  if [ ! -f "$txt" ] ; then
    echo "$attachment: extracting text"

    # gs -q -sDEVICE=txtwrite -o "$dir/page-%d.txt" "$pdf"
    # pdftotext "$pdf"

    tmp=$txt.$$
    if java -jar cache/tika.jar -t "$path" > "$tmp" 2> "$dir/tika-txt.err"
    then
      python3 bin/blanks.py < "$tmp" > "$txt"
      rm $dir/tika-txt.err $tmp
    else
      echo "$attachment: tika failed for $path"
      if [ -s $pdf ] ; then
        echo "extracting text from $pdf"
        pdftotext "$pdf" | python3 bin/blanks.py > "$txt"
      fi
    fi
  fi

  if [ ! -f "$valid" ] ; then
    case "$suffix" in
    pdf)
      echo "$attachment: verapdf"
      verapdf "$path" > "$valid" || rm "$valid"
      ;;
   esac
  fi
done
