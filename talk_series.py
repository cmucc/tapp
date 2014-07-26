#! /usr/bin/env python

# talk_series.py
# Generator for talk series posters
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
    print 'talk_series.py -i <inputfilename> -o <outputfilename>'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'test.py -i <inputfilename> -o <outputfilename>'
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

  if not isinstance(data, dict):
    print 'Parse Error: Input must be JSON object.'
    failed = True

  if not 'name' in data:
    print 'Parse Error: Talk series must have name.'
    failed = True
  elif not isinstance(data['name'], unicode):
    print 'Parse Error: name must be string.'
    failed = True

  if not 'first_date' in data:
    print 'Parse Error: Talk series must have first_date.'
    failed = True
  elif not isinstance(data['first_date'], unicode):
    print 'Parse Error: first_date must be datestring.'
    failed = True
  try:
    dummydate = datetime.datetime.strptime(data['first_date'], '%d-%m-%Y')
  except ValueError:
    print 'Parse Error: first_date must match format %d-%m-%Y.'
    failed = True

  if not 'location' in data:
    print 'Parse Error: Talk series must have location.'
    failed = True
  elif not isinstance(data['location'], unicode):
    print 'Parse Error: location must be string.'
    failed = True

  if not 'talks' in data:
    print 'Parse Error: Talk series must have talks.'
    failed = True
  elif not isinstance(data['talks'], list):
    print 'Parse Error: talks must be list.'
    failed = True
  elif len(data['talks']) < 2:
    print 'Parse Error: talks must have length > 1'
    failed = True
  else:
    for talk in data['talks']:
      if not 'title' in talk:
        print 'Parse Error: talk must have title.'
        failed = True
      elif not isinstance(talk['title'], unicode):
        print 'Parse Error: title must be string.'
        failed = True
      if not 'cat' in talk:
        print 'Parse Error: talk must have cat.'
        failed = True
      elif not isinstance(talk['cat'], int):
        print 'Parse Error: cat must be integer.'
        failed = True

  if failed:
    sys.exit()

# Converts the data into an SVG
def render(data):
  # Color palette
  pal = { 'bg':  '#3a3a3c',
          'em':  '#ffec82',
          'reg': '#a5afa4',
          'blk': '#1f1f1f',
          'cat': ['#a5afa4', '#fec24d', '#f598ab', '#70ceec', '#a5ce43'] }

  # Manufacture start date object
  startDate = datetime.datetime.strptime(data['first_date'], '%d-%m-%Y')
  startTime = datetime.datetime.strptime(data['start_time'], '%H:%M')
  endTime = datetime.datetime.strptime(data['end_time'], '%H:%M')

  output = '<?xml version="1.0"?>\n'
  output += '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1224 792">\n'

  # Font definitions
  output += '<defs>\n'
  output += '  <style type="text/css">@import url(http://fonts.googleapis.com/css?family=Open+Sans:400,600);</style>\n'
  output += '  <style type="text/css">@import url(http://fonts.googleapis.com/css?family=Open+Sans+Condensed:700);</style>\n'
  output += '</defs>\n'

  # Background
  output += '<rect x="0" y="0" width="1224" height="792" fill="'+pal['bg']+'" />\n'

  # Series Name
  output += '<text x="436" y="396" fill="'+pal['em']+'" font-family="\'Open Sans Condensed\', sans-serif" font-weight="700" font-size="40" text-anchor="end">'
  output += data['name'] + ' Talk Series'
  output += '</text>\n'

  # Day of Week
  output += '<text x="396" y="432" fill="'+pal['reg']+'" font-family="\'Open Sans\', sans-serif" font-size="18" text-anchor="end">'
  output += startDate.strftime('%A') + 's'
  output += '</text>\n'

  # Location
  output += '<text x="396" y="456" fill="'+pal['reg']+'" font-family="\'Open Sans\', sans-serif" font-size="18" text-anchor="end">'
  output += data['location']
  output += '</text>\n'

  # Time
  output += '<text x="396" y="480" fill="'+pal['reg']+'" font-family="\'Open Sans\', sans-serif" font-size="18" text-anchor="end">'
  output += time_range_str(startTime.time(), endTime.time())
  output += '</text>\n'

  # Lay out schedule
  SCHEDULE_X = 492
  SCHEDULE_Y = 72
  SCHEDULE_WIDTH = 648
  SCHEDULE_HEIGHT = 576
  LINE_HEIGHT = 32
  heights = disperse_heights(SCHEDULE_Y, SCHEDULE_HEIGHT, len(data['talks']), LINE_HEIGHT)
  dates = disperse_dates(startDate, len(data['talks']))
  for idx in range(0, len(heights)):
    output += '<g>'
    # Date
    output += '<rect x="%d" y="%d" width="72" height="%d" fill="%s" />' %(SCHEDULE_X, heights[idx], LINE_HEIGHT, pal['cat'][data['talks'][idx]['cat']])
    output += '<text x="%d" y="%d" fill="%s" font-family="\'Open Sans\', sans-serif" font-size="16" font-weight="600" text-anchor="middle">' %(SCHEDULE_X+36, heights[idx]+22, pal['blk'])
    output += dates[idx].strftime("%b %d").upper()
    output += '</text>'
    # Title
    output += '<text x="%d" y="%d" fill="%s" font-family="\'Open Sans Condensed\', sans-serif" font-weight="700" font-size="28" text-anchor="start">' %(SCHEDULE_X+98, heights[idx]+28, pal['cat'][data['talks'][idx]['cat']])
    output += data['talks'][idx]['title']
    output += '</text>'
    output += '</g>'
    output += '\n'

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

# Invoke main as top-level function
if __name__ == '__main__':
  main(sys.argv[1:])