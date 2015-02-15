import sys, argparse

from tapp.io.json_validate import valid_json_file

# Parses arguments from command line
def parse_arguments():
  parser = argparse.ArgumentParser(description='TAPP generator', epilog='TAPP Library')

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

  return args
