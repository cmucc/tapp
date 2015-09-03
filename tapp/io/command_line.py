import sys, argparse

from tapp.io.json_validate import valid_json_file

class CliParser():
  parser = argparse.ArgumentParser()

  def __init__(self, description):
    self.parser = argparse.ArgumentParser(description=description)

  def requireFileIO(self):
    self.parser.add_argument('-i', '--infile', dest='infile', metavar='inputfile', help='input file name, omit option to read from stdin', type=valid_json_file, default=sys.stdin, required=True)
    self.parser.add_argument('-o', '--outfile', dest='outfile', metavar='outputfile', help='output file name, omit option to write to stdout', type=argparse.FileType('w'), default=sys.stdout, required=True)

  def option(self, *args, **kwargs):
    self.parser.add_argument(*args, **kwargs)

  def parse(self):
    args = self.parser.parse_args()

    # Workaround instead of lazy-evaluating default argparse arguments:
    if args.infile == sys.stdin:
      args.infile = json.load(sys.stdin)

    return args

