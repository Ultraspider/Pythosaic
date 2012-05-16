#!/usr/bin/python -u

import os
from optparse import OptionParser
from PIL import Image

def load_samples(pixel_size):
   print("loading samples:"),
   samples = []
   path = 'samples'
   for infile in os.listdir(path):
      im = Image.open(os.path.join(path,infile))
      res = im.resize([1,1], Image.ANTIALIAS)
      twenty = im.resize([pixel_size,pixel_size], Image.ANTIALIAS)
      if res.mode is 'L':
         res = res.convert('RGB')
      col = [ord(x) for x in res.tostring()]
      samples.append([twenty, col])
      print('.'),
   print("Done")
   return samples

def load_image(filename):
   print("reading image..."),
   image = []
   pixels = {}
   f= open(filename, 'rb')
   try:
      pixel = f.read(3)
      while pixel != "":
         if pixel not in pixels.keys():
            pixels[pixel] = [[ord(x) for x in pixel], None]
         image.append(pixel)
         pixel = f.read(3)
   finally:
      f.close()
   print("Done")
   return image, pixels

def matchcolor(samples, pixels):
   pix = dict(pixels)
   iml = list(samples)
   while len(pix) != 0:
      mindiff = None
      for i in pix.keys():
         for j in range(len(iml)):
            r1, g1, b1 = pix[i][0]
            r2, g2, b2 = iml[j][1]
            diff = abs(r1 - r2)*256 + abs(g1-g2)* 256 + abs(b1- b2)* 256
            if mindiff is None or diff < mindiff:
               mindiff = diff
               match = [i, j]

      pixels[match[0]][1] = iml[match[1]][0]
      pix.pop(match[0])
      iml.pop(match[1])


def main():
   usage = "usage: %prog [options] FILE WIDTH"
   parser = OptionParser()
   parser.add_option("-p", "--psize", type='int', dest="pixel_size", help="Size of the small images.", default=20)
   parser.add_option("-o", "--output", type='string', dest="output", help="Output file.", default="out.jpg")

   (options, args) = parser.parse_args()

   filename = args[0]
   image_size = int(args[1])
   pixel_size = options.pixel_size
   outfile = options.output

   dimension = {'x': None, 'y': None}

   image, pixels = load_image(filename)

   dimension['x'] = image_size*pixel_size
   dimension['y'] = (len(image)/image_size)*pixel_size

   buffer = Image.new('RGB', (dimension['x'],dimension['y']))

   samples = load_samples(pixel_size)

   matchcolor(samples, pixels)


   print("assembling and saving output image: %s [%s x %s]" % (outfile, dimension['x'], dimension['y']))
   for i in range(image_size):
      for j in range(len(image)/image_size):
         image_idx = image[i+image_size*j]
         buffer.paste(pixels[image_idx][1],(i*pixel_size, j*pixel_size))

   buffer.save(outfile, "JPEG")

if __name__ == "__main__":
   main()
