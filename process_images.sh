#!/usr/bin/env bash
#
# 2400 x 1600 ; https://flothemes.com/flothemes-image-sizes/
# https://www.smashingmagazine.com/2015/06/efficient-image-resizing-with-imagemagick/

for IMG_F in data/*.jpg; do
    WIDTH=$(exiftool "$IMG_F" -ImageWidth | cut -d ":" -f 2 | tr -d "[:blank:]")
    HEIGHT=$(exiftool "$IMG_F" -ImageHeight | cut -d ":" -f 2 | tr -d "[:blank:]")
    if (( WIDTH > HEIGHT )); then
        if (( WIDTH >= 2400 )); then
            NEWSIZE="2400"
        else
            NEWSIZE=$WIDTH
        fi
    else
        if (( HEIGHT >= 1600 )); then
            NEWSIZE="x1600"
        else
            NEWSIZE="x${HEIGHT}"
        fi
    fi
    echo "$IMG_F -- $NEWSIZE original $WIDTH x $HEIGHT"
    convert "$IMG_F" -filter Triangle -define filter:support=2 -thumbnail "$NEWSIZE" \
        -unsharp 0.25x0.25+8+0.065 -dither None -posterize 136 -quality 82 \
        -define jpeg:fancy-upsampling=off -define png:compression-filter=5 \
        -define png:compression-level=9 -define png:compression-strategy=1 \
        -define png:exclude-chunk=all -interlace none -colorspace sRGB -strip \
        "${IMG_F//normalized/optimized}"
done
