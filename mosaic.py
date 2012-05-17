#!/usr/bin/python -u

import os
from optparse import OptionParser
from PIL import Image
import scipy
import scipy.misc
import scipy.cluster

def load_samples(pixel_size):
   print("loading samples:"),
   samples = []
   NUM_CLUSTERS = 3
   path = 'samples'

   for infile in os.listdir(path):
      sample = Image.open(os.path.join(path,infile))
      if sample.mode is not 'RGB':
         sample = sample.convert('RGB')
      
      resized_sample = sample.resize([pixel_size,pixel_size], Image.ANTIALIAS)
      
      res = sample.resize([1,1], Image.ANTIALIAS) #used to approximate the dominant color of the image
      col = [ord(x) for x in res.tostring()]

#     ar = scipy.misc.fromimage(sample.resize([100,100]))
#     shape = ar.shape
#     ar = ar.reshape(scipy.product(shape[:2]), shape[2])

#     codes, dist = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)

#     vecs, dist = scipy.cluster.vq.vq(ar, codes)         # assign codes
#     counts, bins = scipy.histogram(vecs, len(codes))    # count occurrences

#     index_max = scipy.argmax(counts)                    # find most frequent
#     peak = codes[index_max]

#      col = peak

      samples.append([resized_sample, col])
      print('.'),
   print("Done")
   return samples

def load_image(filename, colcount, dither):
   print("reading image..."),
   image = []
   pixels = {}
   im = Image.open(filename)
   size = im.size
   im = im.resize([size[0]/5, size[1]/5], Image.ANTIALIAS)
   
   if im.mode is not 'RGB':
      im = im.convert('RGB')
   if dither:
      im = im.convert("P", colors=colcount)
   else:
      im = im.convert("P", palette=Image.ADAPTIVE, colors=colcount)
   im = im.convert('RGB')
   
   im_raw = im.tostring()
   for i in range(0, len(im_raw), 3):
      pixel = im_raw[i]+im_raw[i+1]+im_raw[i+2]
      if pixel not in pixels.keys():
         pixels[pixel] = [[ord(x) for x in pixel], None]
      image.append(pixel)
   print("Done")
   return image, pixels, im.size

def load_raw(filename, raw_width):
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
   size = [raw_width,len(image)/raw_width]
   print("Done")
   return image, pixels, size

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
   usage = "usage: %prog [options] FILE"
   parser = OptionParser(usage=usage)
   parser.add_option("-p", "--psize", type='int', dest="pixel_size", help="Size of the small images.", default=20)
   parser.add_option("-o", "--output", type='string', dest="output", help="Output file.", default="out.jpg")
   parser.add_option("-d", "--dither", action='store_true', dest="dither", help="Use dithering instead of adaptive palette", default=False)
   parser.add_option("-r", "--raw_width", type='int', dest="raw_width", help="width of raw file if input file is a raw RGB image", default=None)
   parser.add_option("-c", "--col_count", type='int', dest="colcount", help="Color count for color reduction, Default: 32", default=32)

   (options, args) = parser.parse_args()

   filename = args[0]
   pixel_size = options.pixel_size
   outfile = options.output
   dither = options.dither
   colcount = options.colcount
   raw_width = options.raw_width

   dimension = {'x': None, 'y': None}

   if raw_width:
      image, pixels, size = load_raw(filename, raw_width)
   else:
      image, pixels, size = load_image(filename, colcount, dither)

   dimension['x'] = size[0]
   dimension['y'] = size[1]

   buffer = Image.new('RGB', (dimension['x'] * pixel_size, dimension['y']*pixel_size))

   samples = load_samples(pixel_size)

   matchcolor(samples, pixels)

   print("assembling and saving output image: %s [%s x %s]" % (outfile, dimension['x']*pixel_size, 
                                                                        dimension['y']*pixel_size))

   for i in range(dimension['x']):
      for j in range(dimension['y']):
         image_idx = image[i+dimension['x']*j]
         buffer.paste(pixels[image_idx][1],(i*pixel_size, j*pixel_size))

   buffer.save(outfile, "JPEG")

if __name__ == "__main__":
   main()
