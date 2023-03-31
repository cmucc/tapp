import os, sys, json, argparse
from jsonschema import validate, ValidationError

# Defines a valid JSON input file for argparse
def valid_json_file(filename):
  try:
    infile = open(filename, 'r')
    inData = json.load(infile)
  except IOError as e:
    raise argparse.ArgumentTypeError(e.strerror)
    sys.exit()

  try:
    # XXX use os.path.realpath
    schemaFile = open(os.path.dirname(sys.argv[0])+'/schema.json', 'r')
  except IOError:
    print('Could not load JSON schema file.')
    sys.exit()

  try:
    schema = json.load(schemaFile)
    validate(inData, schema)
  except ValidationError as e:
    print('JSON validation error:\n' + e.message)
    sys.exit()

  return inData
