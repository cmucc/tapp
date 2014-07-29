#! /usr/bin/env python

# overview.py
# Generator for overview posters
# Part of the TAPP library
# Copyright 2014 Sam Gruber <scgruber@club.cc.cmu.edu>

import sys, getopt, json, datetime

# Top-level function, parses arguments
def main(argv):
  inFileName = ''
  outFileName = ''
  try:
    opts, args = getopt.getopt(argv, 'hi:o:', ['infile=','outfile='])
  except getopt.GetoptError:
    print 'overview.py -i <inputfilename> -o <outputfilename>'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'overview.py -i <inputfilename> -o <outputfilename>'
      sys.exit()
    elif opt in ('-i','--infile'):
      inFileName = arg
    elif opt in ('-o','--outfile'):
      outFileName = arg

  if inFileName == '':
    inFile = sys.stdin
  else:
    try:
      inFile = open(inFileName, 'r')
    except IOError:
      print 'Input filename not valid.'
      sys.exit()

  if outFileName == '':
    outFile = sys.stdout
  else:
    try:
      outFile = open(outFileName, 'w')
    except IOError:
      print 'Output filename not valid.'
      sys.exit()

  inData = json.load(inFile)

  validate(inData)

  outSvg = render(inData)

  outFile.write(outSvg)
  outFile.write('\n')

# Checks that data is a properly-formatted input to the generator
def validate(data):
  failed = False

  if failed:
    sys.exit()

# Converts the data into an SVG
def render(data):
  output = ''

  DOCUMENT_WIDTH = 612
  DOCUMENT_HEIGHT = 792
  MARGIN = 36

  # Color palette
  pal = {
    'red' : '#9c1b20',
    'gray' : '#413f42',
    'white' : '#ffffff',
    'black' : '#231f20' }

  # Preamble
  output += '<?xml version="1.0"?>\n'
  output += '<svg xmlns="http://www.w3.org/2000/svg" '
  output += 'xmlns:xlink="http://www.w3.org/1999/xlink" '
  output += 'viewBox="0 0 612 792">\n'

  # Header
  output += '<g>\n'
  output += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />\n' \
    %(MARGIN, MARGIN, DOCUMENT_WIDTH-(MARGIN*2), 108, pal['red'])
  output += '</g>\n'

  output += '</svg>'
  return output

# Invoke main as top-level function
if __name__ == '__main__':
  main(sys.argv[1:])