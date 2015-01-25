#! /usr/bin/env python

# talk_series/ics-gen.py
# Generator for talk series iCalendar file
# Part of the TAPP library
# Copyright 2014 Tim Parenti <tparenti@club.cc.cmu.edu>

import os, sys, getopt, json, datetime, argparse
from jsonschema import validate, ValidationError

import icalendar
from icalendar import *

# Top-level function
def generate_ICS():
  inData, outFile = parse_arguments()
  outData = render_ICS(inData)
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
  parser = argparse.ArgumentParser(description='Generator for talk series iCalendar file',
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

# Converts the data into an ICS
def render_ICS(data):
    cal = Calendar()

    # Header for calendar
    header = [
            ['version', 2.0],
            ['calscale', 'GREGORIAN'],
            ['method', 'PUBLISH'],
            ['x-wr-calname', 'CMU Computer Club ' + data['name'] + ' Talks Series'],
            ['x-wr-timezone', 'America/New_York'],
            ['x-wr-caldesc',
                data['url'] + '\n\n' +
                data['ical_desc'] + '\n\n' +
                'Sponsored by ' + data['sponsor']['name'] + '\n' +
                data['sponsor']['url']
            ],
    ]
    for item in header:
        cal.add(item[0], item[1])

    # Timezone settings
    tz = Timezone()
    tz_settings = [
            ['tzid', 'America/New_York'],
            ['x-lic-location', 'America/New_York'],
    ]
    for item in tz_settings:
        tz.add(item[0], item[1])

    # Timezone Daylight
    tz_d = TimezoneDaylight()
    tz_d_settings = [
            ['tzname', 'EDT'],
            ['tzoffsetfrom', datetime.timedelta(hours=-5)],
            ['tzoffsetto', datetime.timedelta(hours=-4)],
            ['dtstart', datetime.datetime(1970, 3, 8, 2, 0, 0)],
            ['rrule', {'freq': 'yearly', 'bymonth': 3, 'byday': '2su'}],
    ]
    for item in tz_d_settings:
        tz_d.add(item[0], item[1])
    tz.add_component(tz_d)

    # Timezone Standard
    tz_s = TimezoneStandard()
    tz_s_settings = [
            ['tzname', 'EST'],
            ['tzoffsetfrom', datetime.timedelta(hours=-4)],
            ['tzoffsetto', datetime.timedelta(hours=-5)],
            ['dtstart', datetime.datetime(1970, 11, 1, 2, 0, 0)],
            ['rrule', {'freq': 'yearly', 'bymonth': 11, 'byday': '1su'}],
    ]
    for item in tz_s_settings:
        tz_s.add(item[0], item[1])
    tz.add_component(tz_s)

    cal.add_component(tz)

    # Manufacture dates
    startDate = datetime.datetime.strptime(data['first_date'], '%Y-%m-%d')
    startTime = datetime.datetime.strptime(data['start_time'], '%H:%M').time()
    endTime = datetime.datetime.strptime(data['end_time'], '%H:%M').time()
    dates = disperse_dates(startDate, len(data['talks']))

    # Create individual events
    for idx in range(0, len(dates)):
        if not data['talks'][idx]['cat'] == 0:
            event = Event()
            event_settings = [
                ['uid', 'talks-series-' + dates[idx].strftime("%Y-%m-%d") + '@club.cc.cmu.edu'],
                ['dtstart', datetime.datetime.combine(dates[idx], startTime)],
                ['dtend', datetime.datetime.combine(dates[idx], endTime)],
                ['summary', 'CMUCC Talk: ' + data['talks'][idx]['title']],
                ['location', data['location']],
                ['description',
                        data['talks'][idx]['desc'] + '\n\n' +
                        'Part of the CMU Computer Club ' + data['name'] + ' Talks Series\n' +
                        data['url'] + '\n\n' +
                        'Sponsored by ' + data['sponsor']['name'] + '\n' +
                        data['sponsor']['url']
                ],
                ['sequence', 0],
                ['status', 'CONFIRMED'],
                ['transp', 'OPAQUE'],
            ]
            for item in event_settings:
                event.add(item[0], item[1])
            cal.add_component(event)

    return cal.to_ical()


def disperse_dates(startDate, numEvents):
  step = datetime.timedelta(days=7)
  dates = [startDate]
  for idx in range(1, numEvents):
    startDate += step
    dates += [startDate]
  return dates

def wrap_line(line, n, sep):
  split_line = [line[i:i+n] for i in range(0, len(line), n)]
  joined_line = sep.join(split_line)
  return joined_line

# Invoke top-level function
if __name__ == '__main__':
  generate_ICS()
