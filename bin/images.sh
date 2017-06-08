#!/bin/bash

set -e
for path in "$@"
do
  id=$(echo "$path"|sed -e 's/^cache\/attachment\///' -e 's/\/.*$//')
  dir="image/attachment/$id/"

  suffix=$(echo ${path##*.} | tr '[:upper:]' '[:lower:]')
  doc="$dir/document.$suffix"
  pdf="$dir/document.pdf"

  if [ -d "$dir" ]; then
    continue
  fi

  mkdir -p "$dir"

  case "$suffix" in
  pdf)
    ln -f "$path" "$pdf"
    ;;

  zip)
    continue
    ;;

  *)
    ln -f "$path" "$doc"
    (
      cd $dir
      lowriter --headless --convert-to pdf "document.$suffix"
    )
    ;;
  esac

  pdftoppm -rx 300 -ry 300 -png "$pdf" "$dir/page"
done
