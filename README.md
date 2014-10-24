# TAPP
Totally Automated Propaganda Producer

This package contains scripts to be used to produce marketing materials for the
CMU Computer Club.

## Requirements

Before running these scripts, you must [install `pip`](https://pip.pypa.io/en/latest/installing.html), a python package manager. Then run:

    pip install --user -r requirements.txt

So that you will have all of the necessary modules installed on your system.

## Talk Series

See data files such as `data/spring2014/talks_series.json` for input reference.
Use 0 as the `cat` value for weeks without a talk due to holidays, etc.

### Posters

Usage:

    ./talk_series/svg-gen.py -i foo.json -o bar.svg

The file `2013logo_light.svg` must be in the same directory as the output file
to display properly.  Additionally, the filename given in the `sponsor_logo`
field must be relative to the output file.

### iCalendar File

Usage:

    ./talk_series/ics-gen.py -i foo.json -o bar.ics

### Webpage

Usage:

    ./talk_series/php-gen.py -i foo.json -o bar.php

## Club Overview Flyers

See data files such as `data/spring2014/overview.json` for input reference.

Usage:

    ./overview/svg-gen.py -i foo.json -o bar.svg

The files `2013logo_light.svg` and `cmucc_qr.svg` must be in the same directory
as the output file to display properly.

## Printing SVGs

Generated SVGs are intended to be viewed and printed from [Google
Chrome](https://www.google.com/chrome/browser/); however, the transcluded logos
can cause issues.  As a workaround, manually remove the `<image>` tags from the
SVG output, and replace them using an SVG editor such as
[Inkscape](http://www.inkscape.org/en/).  Ensure all required fonts are
installed, resize to desired output size, and print.

