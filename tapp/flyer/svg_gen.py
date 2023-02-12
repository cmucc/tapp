#! /usr/bin/env python

# tapp/flyer/svg_gen.py
# Generator for club overview flyer
# Part of the TAPP library
# Copyright 2014 Sam Gruber <scgruber@club.cc.cmu.edu>

import datetime

from tapp.io.command_line import CliParser
from tapp.io.json_validate import valid_json_file

# Top-level function
def generate_SVG():
  parser = CliParser('Overview flyer (SVG) generator')
  parser.requireFileIO()

  args = parser.parse()
  inData, outFile = args.infile, args.outfile
  outData = render_SVG(inData)
  outFile.write(outData + '\n')

# Converts the data into an SVG
def render_SVG(data):
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

  # Font definitions and styles
  output += '<defs>\n'
  output += '  <style type="text/css">@import url(http://fonts.googleapis.com/css?family=Open+Sans:300,400,700);</style>\n'
  output += '  <style type="text/css">@import url(http://fonts.googleapis.com/css?family=Open+Sans+Condensed:700);</style>\n'
  output += '  <style type="text/css">@import url(http://fonts.googleapis.com/css?family=Inconsolata:700);</style>\n'
  output += '  <style type="text/css">\n'
  output += '    .subtitle { font-family: \'Open Sans\', sans-serif; fill: %s; font-size: 16px; font-weight: 300; }\n' %(pal['white'])
  output += '    .meetings { font-family: \'Open Sans Condensed\', sans-serif; fill: %s; font-size: 13px; font-weight: 700; }\n' %(pal['white'])
  output += '    .heading { font-family: \'Open Sans Condensed\', sans-serif; fill: %s; font-size: 36px; font-weight: 700; }\n' %(pal['gray'])
  output += '    .body { font-family: \'Open Sans\', sans-serif; fill: %s; font-size: 16px; font-weight: 400; letter-spacing: -0.5px; }\n' %(pal['black'])
  output += '    .bold-body { font-family: \'Open Sans\', sans-serif; fill: %s; font-size: 16px; font-weight: 700; letter-spacing: -0.5px; }\n' %(pal['black'])
  output += '    .bracket {font-family: \'Open Sans Condensed\', sans-serif; fill: %s; font-size: 20px; font-weight: 700; }\n' %(pal['gray'])
  output += '    .link { font-family: \'Inconsolata\', sans-serif; fill: %s; font-size: 26px; font-weight: 700; }\n' %(pal['gray'])
  output += '  </style>\n'
  output += '</defs>\n'

  # Header
  output += '<g>\n'
  output += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />\n' \
    %(MARGIN, MARGIN, DOCUMENT_WIDTH-(MARGIN*2), 108, pal['red'])
  LOGO_FILE = 'assets/cmucc_logo_2015_light.svg'
  output += '<image x="%d" y="%d" width="%d" height="%d" xlink:href="%s" />\n' \
    %(MARGIN+12, MARGIN+12, 342, 90, LOGO_FILE)

  # Meetings
  output += '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />\n' \
    %(DOCUMENT_WIDTH-MARGIN-12-144, MARGIN+12, 144, 108-(12*2), pal['gray'])
  (m1l1, m1l2) = make_meeting(data['meetings'][0])
  output += '<text x="%d" y="%d" class="meetings">' %(DOCUMENT_WIDTH-MARGIN-150, MARGIN+30)
  output += m1l1
  output += '</text>\n'
  output += '<text x="%d" y="%d" class="meetings">' %(DOCUMENT_WIDTH-MARGIN-150, MARGIN+45)
  output += m1l2
  output += '</text>\n'
  (m2l1, m2l2) = make_meeting(data['meetings'][1])
  output += '<text x="%d" y="%d" class="meetings">' %(DOCUMENT_WIDTH-MARGIN-150, MARGIN+69)
  output += m2l1
  output += '</text>\n'
  output += '<text x="%d" y="%d" class="meetings">' %(DOCUMENT_WIDTH-MARGIN-150, MARGIN+84)
  output += m2l2
  output += '</text>\n'
  output += '</g>\n'

  def red_bar(yPosition):
    return '<rect x="%d" y="%d" width="%d" height="%d" fill="%s" />\n' \
      %(MARGIN, yPosition, DOCUMENT_WIDTH-(MARGIN*2), 3, pal['red'])

  # Services
  output += '<text x="%d" y="%d" class="heading">' %(MARGIN, MARGIN+150)
  output += 'We Create &amp; Run Services'
  output += '</text>'
  output += red_bar(MARGIN+156)
  output += '<text x="%d" y="%d" class="body">' %(MARGIN, MARGIN+180)
  output += 'Computer Club hacks on projects used at CMU and around the world:'
  output += '</text>\n'
  for idx in range(0,6):
    if idx % 2 == 0:
      xPosition = MARGIN+12
    else:
      xPosition = ((DOCUMENT_WIDTH+MARGIN)/2) + 12
    yPosition = MARGIN + 204 + (idx/2)*24
    output += '<text x="%d" y="%d" class="bold-body">' %(xPosition, yPosition)
    output += '- ' + data['services'][idx]
    output += '</text>\n'

  # Events
  output += '<text x="%d" y="%d" class="heading">' %(MARGIN, MARGIN+306)
  output += 'We Also Host Events'
  output += '</text>\n'
  output += red_bar(MARGIN+312)
  for idx in range(0,3):
    xPosition = MARGIN + 12
    yPosition = MARGIN + 336 + (idx*24)
    output += '<text x="%d" y="%d" class="body">' %(xPosition, yPosition)
    output += '<tspan class="bold-body">- ' + data['events'][idx]['name'] + '</tspan>'
    output += ': ' + data['events'][idx]['blurb']
    output += '</text>\n'
    output += '<text x="%d" y="%d" class="bracket" text-anchor="end">' \
      %(DOCUMENT_WIDTH - xPosition, yPosition)
    output += ']'
    output += '</text>\n'
    output += '<text x="%d" y="%d" class="bracket" text-anchor="start">' \
      %(DOCUMENT_WIDTH - xPosition - 72, yPosition)
    output += '['
    output += '</text>\n'
    output += '<text x="%d" y="%d" class="body" text-anchor="middle">' \
      %(DOCUMENT_WIDTH - xPosition - 36, yPosition)
    output += data['events'][idx]['when']
    output += '</text>\n'

  # Toys
  output += '<text x="%d" y="%d" class="heading">' %(MARGIN, MARGIN+438)
  output += 'And We Have Cool Toys'
  output += '</text>\n'
  output += red_bar(MARGIN+444)
  output += '<text x="%d" y="%d" class="body">' %(MARGIN, MARGIN+468)
  output += 'Members have access to our internal services:'
  output += '</text>\n'
  for idx in range(0,3):
    xPosition = MARGIN + 12
    yPosition = MARGIN + 492 + (idx*24)
    output += '<text x="%d" y="%d" class="body">' %(xPosition, yPosition)
    output += '<tspan class="bold-body">- ' + data['toys'][idx]['name'] + '</tspan>'
    output += ': ' + data['toys'][idx]['blurb']
    output += '</text>\n'

  # QR
  QR_FILE = 'assets/cmucc_qr.svg'
  output += '<image x="%d" y="%d" width="%d" height="%d" xlink:href="%s" />\n' \
    %(DOCUMENT_WIDTH-MARGIN-144, DOCUMENT_HEIGHT-MARGIN-144, 144, 144, QR_FILE)
  # QR_WIDTH = 144
  # QR_HEIGHT = 144
  # QR_X = DOCUMENT_WIDTH-MARGIN-QR_WIDTH
  # QR_Y = DOCUMENT_HEIGHT-MARGIN-QR_HEIGHT
  # output += f'<foreignObject x="{QR_X}" y="{QR_Y}" width="{QR_WIDTH}" height="{QR_HEIGHT}">\n'
  # output += f'  <body>\n'
  # output += f'    <img src={QR_FILE}\n'
  # output += f'     type="image/svg+xml" width="{QR_WIDTH}px" height="{QR_HEIGHT}px">'
  # output += f'  </body>\n'
  # output += f'</foreignObject>'

  # Links
  output += '<g>\n'
  for idx in range(0,4):
    xPosition = MARGIN + 12
    yPosition = DOCUMENT_HEIGHT-MARGIN-144+18+(41*idx)
    output += '<text x="%d" y="%d" class="link">' %(xPosition, yPosition)
    output += data['links'][idx]
    output += '</text>\n'
  output += '</g>\n'

  output += '</svg>'
  return output

def make_meeting(mtg):
  line1 = mtg['name'] + ' (' + mtg['location'] +')'
  time = datetime.datetime.strptime(mtg['time'], '%H:%M')
  line2 = mtg['day'] + 's @ ' + time.strftime('%I:%M %p').lstrip('0')
  return (line1, line2)

# Invoke top-level function
if __name__ == '__main__':
  generate_SVG()
