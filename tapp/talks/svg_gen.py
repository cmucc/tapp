#! /usr/bin/env python

# tapp/talks/svg_gen.py
# Generator for talk series posters
# Part of the TAPP library
#
# Copyright 2014-2015
# Sam Gruber <scgruber@club.cc.cmu.edu>
# Tim Parenti <tparenti@club.cc.cmu.edu>

import datetime

from tapp.io.command_line import parse_arguments
from tapp.io.json_validate import valid_json_file

# Top-level function
def generate_SVG():
  args = parse_arguments('Talk series poster (SVG) generator')
  inData, outFile = args.infile, args.outfile
  outData = render_SVG(inData)
  outFile.write(outData + '\n')

# Converts the data into an SVG
def render_SVG(data):
  # Color palette
  pal = { 'bg':  '#3f3a3c',
          'em':  '#ffea7f',
          'reg': '#a5afa4',
          'blk': '#1f1f1f',
          'cat': ['#a5afa4', '#fec24d', '#f598ab', '#70ceec', '#a5ce43', '#fe824d']
          # (grey), yellow, pink, blue, green, orange
  }

  # Manufacture start date object
  startDate = datetime.datetime.strptime(data['first_date'], '%Y-%m-%d')
  startTime = datetime.datetime.strptime(data['start_time'], '%H:%M')
  endTime = datetime.datetime.strptime(data['end_time'], '%H:%M')

  # Preamble
  output = '<?xml version="1.0"?>\n'
  output += '<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 1224 792">\n'

  # Font definitions
  if (len(data['talks']) > 10):
    BLOCK_HEIGHT = 32
  else:
    # Use a larger size if there are fewer talks
    BLOCK_HEIGHT = 40
  BLOCK_WIDTH = BLOCK_HEIGHT*2.25
  TITLE_SIZE = BLOCK_HEIGHT

  output += '<defs>\n'
  output += '  <style type="text/css">@import url(http://fonts.googleapis.com/css?family=Open+Sans:400,600);</style>\n'
  output += '  <style type="text/css">@import url(http://fonts.googleapis.com/css?family=Open+Sans+Condensed:700);</style>\n'
  output += '  <style type="text/css">\n'
  output += '    .series-title { font-family: \'Open Sans Condensed\', sans-serif; font-size: 40px; font-weight: 700; }\n'
  output += '    .when-and-where { font-family: \'Open Sans\', sans-serif; font-size: 18px; }\n'
  output += '    .website { font-family: \'Open Sans\', sans-serif; font-size: 24px; }\n'
  output += '    .sponsored-by { font-family: \'Open Sans\', sans-serif; font-size: 18px; }\n'
  output += '    .talk-date { font-family: \'Open Sans\', sans-serif; font-size: %fpx; font-weight: 600; }\n' %(BLOCK_HEIGHT*0.5)
  output += '    .talk-title { font-family: \'Open Sans Condensed\', sans-serif; font-size: %fpx; font-weight: 700; }\n' %(TITLE_SIZE)
  output += '  </style>\n'
  output += '</defs>\n'

  # Background
  DOCUMENT_WIDTH = 1224
  DOCUMENT_HEIGHT = 792
  MARGIN = 72
  output += '<rect x="0" y="0" width="%f" height="%f" fill="%s" />\n' %(DOCUMENT_WIDTH, DOCUMENT_HEIGHT, pal['bg'])

  # CMUCC Logo
  LOGO_WIDTH = 475
  LOGO_HEIGHT = 125
  LOGO_MARGIN = 20
  LOGO_SCALE = 0.7
  LOGO_FILE = '2015logo_light.svg'
  output += '<image x="%f" y="%f" width="%f" height="%f" xlink:href="%s"/>\n' %(436-((LOGO_WIDTH-LOGO_MARGIN)*LOGO_SCALE), 360-(LOGO_HEIGHT*LOGO_SCALE), (LOGO_WIDTH*LOGO_SCALE), (LOGO_HEIGHT*LOGO_SCALE), LOGO_FILE)

  # Series Name
  output += '<text x="436" y="396" fill="'+pal['em']+'" class="series-title" text-anchor="end">'
  output += data['name'] + ' Talk Series'
  output += '</text>\n'

  # Day of Week
  output += '<text x="396" y="432" fill="'+pal['reg']+'" class="when-and-where" text-anchor="end">'
  output += startDate.strftime('%A') + 's'
  output += '</text>\n'

  # Location
  output += '<text x="396" y="456" fill="'+pal['reg']+'" class="when-and-where" text-anchor="end">'
  output += data['location']
  output += '</text>\n'

  # Time
  output += '<text x="396" y="480" fill="'+pal['reg']+'" class="when-and-where" text-anchor="end">'
  output += time_range_str(startTime.time(), endTime.time())
  output += '</text>\n'

  # Website
  output += '<text x="%f" y="%f" fill="%s" class="website" text-anchor="end">' %(396, DOCUMENT_HEIGHT - MARGIN - 144, pal['em'])
  output += data['url']
  output += '</text>\n'

  # Sponsor
  SPONSOR_WIDTH = 144
  SPONSOR_HEIGHT = 108
  output += '<text x="%f" y="%f" fill="%s" class="sponsored-by" text-anchor="end">' %(396 - SPONSOR_WIDTH, DOCUMENT_HEIGHT - MARGIN - data['sponsor']['logo_svg-gen_height_offset'], pal['reg'])
  output += 'Sponsored by'
  output += '</text>\n'
  output += '<image x="%f" y="%f" width="%f" height="%f" xlink:href="%s" />\n' %(396 - SPONSOR_WIDTH, DOCUMENT_HEIGHT - MARGIN - SPONSOR_HEIGHT, SPONSOR_WIDTH, SPONSOR_HEIGHT, data['sponsor']['logo'])

  # Lay out schedule
  SCHEDULE_X = 492
  SCHEDULE_Y = MARGIN
  SCHEDULE_WIDTH = 648
  SCHEDULE_HEIGHT = DOCUMENT_HEIGHT - (MARGIN * 2)

  heights = disperse_heights(SCHEDULE_Y, SCHEDULE_HEIGHT, len(data['talks']), BLOCK_HEIGHT)
  dates = disperse_dates(startDate, len(data['talks']))
  for idx in range(0, len(heights)):
    output += '<g>\n'
    # Date
    output += '<rect x="%f" y="%f" width="%f" height="%f" fill="%s" />\n' %(SCHEDULE_X, heights[idx], BLOCK_WIDTH, BLOCK_HEIGHT, pal['cat'][data['talks'][idx]['cat']])
    output += '<text x="%f" y="%f" fill="%s" class="talk-date" text-anchor="middle">' %(SCHEDULE_X+(BLOCK_WIDTH/2), heights[idx]+(BLOCK_HEIGHT/2)+6, pal['blk'])
    output += dates[idx].strftime("%b %d").upper()
    output += '</text>\n'
    # Title
    output += '<text x="%f" y="%f" fill="%s" class="talk-title" text-anchor="start">' %(SCHEDULE_X+BLOCK_WIDTH+26, heights[idx]+(BLOCK_HEIGHT/2)+12, pal['cat'][data['talks'][idx]['cat']])
    output += data['talks'][idx]['title']
    output += '</text>\n'
    output += '</g>\n'

  output += '</svg>'
  return output

def time_range_str(start, end):
  if (start.hour < 12) != (end.hour < 12):
    startM = choose(start.hour < 12,'AM','PM')
    endM = choose(end.hour < 12,'AM','PM')
    # Different AM/PM
    return start.strftime('%I:%M %p').lstrip('0') + ' - ' + end.strftime('%I:%M %p').lstrip('0')
  else:
    return start.strftime('%I:%M').lstrip('0') + ' - ' + end.strftime('%I:%M %p').lstrip('0')

def disperse_heights(initialOffset, totalHeight, numEvents, lineHeight):
  totalSpace = (totalHeight*1.0) - (numEvents * lineHeight)
  step = (totalSpace/(numEvents-1)) + lineHeight
  heights = []
  for idx in range(0,numEvents):
    heights += [initialOffset + (idx * step)]
  return heights

def disperse_dates(startDate, numEvents):
  step = datetime.timedelta(days=7)
  dates = [startDate]
  for idx in range(1, numEvents):
    startDate += step
    dates += [startDate]
  return dates

def choose(cond, t, f):
  if cond:
    return t
  else:
    return f

# Invoke top-level function
if __name__ == '__main__':
  generate_SVG()
