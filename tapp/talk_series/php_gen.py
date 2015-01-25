#! /usr/bin/env python

# talk_series/php-gen.py
# Generator for talk series PHP webpage
# Part of the TAPP library
# Copyright 2014 Tim Parenti <tparenti@club.cc.cmu.edu>

import os, sys, getopt, json, datetime, argparse
from jsonschema import validate, ValidationError

# Top-level function
def generate_PHP():
  inData, outFile = parse_arguments()
  outData = render_PHP(inData)
  outFile.write(outData + '\n')

# Defines a valid json input file for argparse
def valid_json_file(filename):
  try:
    infile = open(filename, 'r')
    inData = json.load(infile)
  except IOError as e:
    raise argparse.ArgumentTypeError(e.strerror)
    sys.exit()

  try:
    schemaFile = open(os.path.dirname(sys.argv[0])+'/schema.json', 'r') # XXX use os.path.realpath
  except IOError:
    print 'Could not load JSON schema file.'
    sys.exit()

  try:
    schema = json.load(schemaFile)
    validate(inData, schema)
  except ValidationError as e:
    print 'JSON validation error:\n' + e.message
    sys.exit()

  return inData

# Parses arguments from command line
def parse_arguments():
  parser = argparse.ArgumentParser(description='Generator for talk series PHP webpage',
                                   epilog='TAPP Library')

  arguments = [
  ['-i', '--infile', 'inputfile', 'input file name, omit option to read from stdin', valid_json_file, sys.stdin],
  ['-o', '--outfile', 'outputfile', 'output file name, omit option to write to stdout', argparse.FileType('w'), sys.stdout],
  ]

  for item in arguments:
    parser.add_argument(item[0], item[1], metavar=item[2], help=item[3], type=item[4], default=item[5])

  args = parser.parse_args()
  # Workaround instead of lazy-evaluating default argparse arguments:
  if args.infile == sys.stdin:
    args.infile = json.load(sys.stdin)
  return args.infile, args.outfile

# Converts the data into a PHP webpage
def render_PHP(data):
  # Manufacture start date object
  startDate = datetime.datetime.strptime(data['first_date'], '%Y-%m-%d')
  startTime = datetime.datetime.strptime(data['start_time'], '%H:%M')
  endTime = datetime.datetime.strptime(data['end_time'], '%H:%M')

  # Preamble
  output = (
    '<?php include(\'../../header.php\'); ?>\n'
    '<?php date_default_timezone_set("America/New_York"); ?>\n'
    '<base href="/talks/' + data['slug'] + '/" />\n'
    '<div>\n'
    '<div id="onecol">\n'
    '  <div class="cbox">\n'
    '  <div class="section-tag">' + data['name'].upper() + ' TALK SERIES</div>\n'
    '    ' + data['web_desc'] + '\n'
    '    <p>\n'
    '      These talks will take place every <b>' + startDate.strftime('%A') + '</b> starting at <b>' + startTime.time().strftime('%I:%M %p').lstrip('0') + '</b> in <b>' + data['location'] + '</b> throughout the semester.\n'
    '    </p>\n'
    '    <p>\n'
    '    This schedule is also available as an <a href="ccst.ics">iCalendar file</a> which is compatible with all calendaring software.\n'
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
        '    <div class="' + date_style_call(dates[idx]) + '">\n'
        '      <time datetime="' + dates[idx].strftime('%Y-%m-%d') + 'T' + startTime.time().strftime('%H:%M:%S') + '">' + dates[idx].strftime("%b %d") + '</time>\n'
        '    </div>\n'
        '    <h1>' + notes_link_call(data['talks'][idx]['title'], data['talks'][idx]['notes']) + '</h1>\n'
        '    <p>' + data['talks'][idx]['desc'] + '</p>\n'
      )

  # Postamble
  output += (
    '  </div>\n' # Close the last .cbox div
    '</div>\n'
    '<?php include(\'../../footer.php\'); ?>\n'
  )

  # PHP date styling function
  output += (
    '\n'
    '<?php\n'
    '  function dateStyle($date) {\n'
    # Extract dates of actual talks
    '    $dates = array(' + ', '.join([dates[idx].strftime('"%Y-%m-%d"') for idx in range(len(dates)) if not data['talks'][idx]['cat'] == 0]) + ');\n'
    '    $today = date("Y-m-d");\n'
    '    \n'
    '    foreach ($dates as $d) {\n'
    '      if ($d >= $today) {\n'
    '        $next = $d;\n'
    '        break;\n'
    '      }\n'
    '    }\n'
    '    \n'
    '    if ($date < $today) {\n'
    '      $class = "date-past";\n'
    '    }\n'
    '    elseif (isset($next) && $date == $next) {\n'
    '      $class = "date-next";\n'
    '    }\n'
    '    else {\n'
    '      $class = "date-future";\n'
    '    }\n'
    '    return $class;'
    '  }\n'
    '?>\n'
  )

  # PHP notes linking function
  output += (
    '\n'
    '<?php\n'
    '  function notesLink($title, $path) {\n'
    '    if (file_exists($path)) {\n'
    '      return "<a href=\\"".$path."\\">".$title."</a>";\n'
    '    }\n'
    '    else {\n'
    '      return $title;\n'
    '    }\n'
    '  }\n'
    '?>\n'
  )

  return output

def disperse_dates(startDate, numEvents):
  step = datetime.timedelta(days=7)
  dates = [startDate]
  for idx in range(1, numEvents):
    startDate += step
    dates += [startDate]
  return dates

def date_style_call(date):
  return '<?php echo dateStyle("' + date.strftime("%Y-%m-%d") + '"); ?>'

def notes_link_call(title, path):
  return '<?php echo notesLink("' + title + '", "' + path + '"); ?>'

# Invoke top-level function
if __name__ == '__main__':
  generate_PHP()
