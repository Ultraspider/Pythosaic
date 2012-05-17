Python program to transform a picture into a mosaic of smaller pictures.

Work in progress

Usage: mosaic.py [options] FILE

Options:
  -h, --help            show this help message and exit
  -p PIXEL_SIZE, --psize=PIXEL_SIZE
                        Size of the small images.
  -o OUTPUT, --output=OUTPUT
                        Output file.
  -d, --dither          Use dithering instead of adaptive palette
  -r RAW_WIDTH, --raw_width=RAW_WIDTH
                        width of raw file if input file is a raw RGB image
  -c COLCOUNT, --col_count=COLCOUNT
                        Color count for color reduction, Default: 32

if using -r, file must be a raw RGB (3 bytes per pixel) image prepared with another software like ImageMagick's convert:
convert -resize 20% picture.jpg -depth 8 -colors 32 rgb:rpicture
adapt the above to your liking, see convert manual for info about parameters
Note: -d and -c are ineffective when -r is used as the raw image is used without further processing.

RAW_WIDTH is the width of the raw file = (original image width)*(resize parameters of convert)

Samples (pictures that will compose the mosaic) have to be put in <working directory>/samples/

