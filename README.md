# TAPP
Totally Automated Propaganda Producer

This package contains scripts to be used to produce marketing materials for the
CMU Computer Club.

## Requirements

Before running these scripts, you must [install `pip`](https://pip.pypa.io/en/latest/installing.html),
a Python package manager.  Then, to install all of the necessary modules on your system, run:

    pip install --user -r requirements.txt

## Talk Series

See data files such as `data/spring2014/talks_series.json` for input reference.
Use 0 as the `cat` value for weeks without a talk due to holidays, etc.

### Posters

Usage:

    python -m tapp.talk_series.svg_gen -i foo.json -o bar.svg
    python -m tapp.talk_series.svg_gen_short -i foo.json -o bar.svg

The file `2013logo_light.svg` must be in the same directory as the output file
to display properly.  Additionally, the filename given in the `sponsor_logo`
field must be relative to the output file.

The "short" generator generates a poster suitable for a shorter series of talks
(on the order of 7), as opposed to the normal 15.

### iCalendar File

Usage:

    python -m tapp.talk_series.ics_gen -i foo.json -o bar.ics

### Webpage

Usage:

    python -m tapp.talk_series.php_gen -i foo.json -o bar.php

## Club Overview Flyers

See data files such as `data/spring2014/overview.json` for input reference.

Usage:

    python -m tapp.overview.svg_gen -i foo.json -o bar.svg

The files `2013logo_light.svg` and `cmucc_qr.svg` must be in the same directory
as the output file to display properly.

## Printing SVGs

Generated SVGs are intended to be viewed and printed from [Google
Chrome](https://www.google.com/chrome/browser/).  Talk Series posters are best
printed to tabloid (17"x11") paper, landscape orientation, with margins set to
0.25" on the left and right, 0.2" on top, and 0" on bottom.  Club Overview
flyers are best printed to letter (8.5"x11") paper, portrait orientation, with
the "minimum margins" setting.  **For the most consistent results, print to a
PDF.**

In some cases, when attempting to open the SVGs in other tools, the transcluded logos
can cause issues.  As a workaround, manually remove the `<image>` tags from the
SVG output, and replace them using an SVG editor such as
[Inkscape](http://www.inkscape.org/en/).  Ensure all required fonts are
installed, resize to desired output size, and print.

