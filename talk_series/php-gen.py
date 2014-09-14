#! /usr/bin/env python

# talk_series/php-gen.py
# Generator for talk series PHP webpage
# Part of the TAPP library
# Copyright 2014 Tim Parenti <tparenti@club.cc.cmu.edu>

import sys, getopt, json, datetime

# Top-level function, parses arguments
def main(argv):
  inFileName = ''
  outFileName = ''
  try:
    opts, args = getopt.getopt(argv, 'hi:o:', ['infile=','outfile='])
  except getopt.GetoptError:
    print 'talk_series/php-gen.py -i <inputfilename> -o <outputfilename>'
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-h':
      print 'talk_series/php-gen.py -i <inputfilename> -o <outputfilename>'
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

  outIcs = render(inData)

  outFile.write(outIcs)
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
    dummydate = datetime.datetime.strptime(data['first_date'], '%Y-%m-%d')
  except ValueError:
    print 'Parse Error: first_date must match format %Y-%m-%d.'
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

# Converts the data into a PHP webpage
def render(data):
  # Manufacture start date object
  startDate = datetime.datetime.strptime(data['first_date'], '%Y-%m-%d')
  startTime = datetime.datetime.strptime(data['start_time'], '%H:%M')
  endTime = datetime.datetime.strptime(data['end_time'], '%H:%M')

  # Preamble
  output = (
    '<?php include(\'../../header.php\'); ?>\n'
    '<div>\n'
    '<div id="onecol">\n'
    '  <div class="cbox">\n'
    '  <div class="section-tag">' + data['name'].upper() + ' TALK SERIES</div>\n'
    '    ' + data['web_desc'] + '\n'
    '    <p>\n'
    '      These talks will take place every <b>' + startDate.strftime('%A') + '</b> starting at <b>' + startTime.time().strftime('%I:%M %p').lstrip('0') + '</b> in <b>' + data['location'] + '</b> throughout the semester.\n'
    '    </p>\n'
    '    <p>\n'
    '      Sponsored by <a href="' + data['sponsor']['url'] + '" target="_blank">' + data['sponsor']['name'] + '</a>.\n'
    '      ' + data['sponsor']['desc'] + '\n'
    '    </p>\n'
    # Leave the .cbox div open, to be closed by category generator.
  )

  # Create categories and events
  categories = data['categories']
  dates = disperse_dates(startDate, len(data['talks']))
  previousCat = -1
  for idx in range(0, len(dates)):
    cat = data['talks'][idx]['cat']
    if not cat == 0:
      # Create a new section if the category has changed.
      # NOTE: It's possible to use talk categories out-of-order. TODO: Avoid this.
      if not cat == previousCat:
        output += (
          '  </div>\n' # Close previous .cbox div
          '  <div class="narrowpad"></div>\n'
          '  <div class="cbox">\n'
          '    <div class="section-tag">' + data['categories'][cat-1].upper() + '</div>\n'
        )
        previousCat = cat
      # Otherwise, just separate this from the one above.
      else:
        output += '    <hr/>\n'
      # List the event.
      output += (
        '    <div class="date-future">' + dates[idx].strftime("%b %d") + '</div>\n'
        '    <h1>' + data['talks'][idx]['title'] + '</h1>\n'
        '    <p>' + data['talks'][idx]['desc'] + '</p>\n'
      )

  # Postamble
  output += (
    '  </div>\n' # Close the last .cbox div
    '</div>\n'
    '<?php include(\'../../footer.php\'); ?>\n'
  )

  return output

def disperse_dates(startDate, numEvents):
  step = datetime.timedelta(days=7)
  dates = [startDate]
  for idx in range(1, numEvents):
    startDate += step
    dates += [startDate]
  return dates

# Invoke main as top-level function
if __name__ == '__main__':
  main(sys.argv[1:])
