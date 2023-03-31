# TAPP
Totally Automated Propaganda Producer

This package contains scripts to be used to produce marketing materials for the
Carnegie Mellon University Computer Club.

A copy of this repository is available to club members at
`/afs/club.cc.cmu.edu/projects/tapp`.
Users can edit the `data` directory and run the scripts as needed.

## Requirements

Before running these scripts, you must [install `pip`](https://pip.pypa.io/en/latest/installation/),
a Python package manager.  If you'd like to keep TAPP's dependencies in their
own virtual environment (or "venv"), separate from the rest of your Python
toolchain, you'll also want the [`python3-venv`
package](https://packages.debian.org/python3-venv) for your operating system.

Then, to create a venv and install all of the necessary modules on your system,
run:

    python3 -m venv .venv/ --prompt tapp
    source .venv/bin/activate
    pip3 install -r requirements.txt

**If you use a venv, make sure to activate it before running any of TAPP's
generators.**

Alternatively, if you don't mind polluting your local user environment:

    pip3 install --user -r requirements.txt

## Produce All the Propaganda!

To produce all of the propaganda for a semester,
check the variables at the top of the `Makefile` and run:

    make

With the proper AFS permissions, the files can be published to the web using:

    make publish

----

# Generating Individual Files

## Talk Series

See data files such as `data/2015-08_F15-talks.json` for input reference.
Use 0 as the `cat` value for weeks without a talk due to holidays, etc.

A `cat` value for each talk is required and relates to how it is colored on the posters;
however, the `categories` array is optional and relates to how the schedule is rendered on the web.
If the `cat` values are not logically contiguous (see Fall 2016 as an example), it is best to dispense with the categories.

### Posters

Usage:

    python3 -m tapp.talks.svg_gen -i foo.json -o bar.svg [-g]

The file `2015logo_light.svg` must be in the same directory as the output file
to display properly.  Additionally, the filename given in the `sponsor_logo`
field must be relative to the output file.

Use `-g` to generate a grayscale version more suitable for mass printing
than the full-color version.  In some browsers, logos may remain in color.

### iCalendar File

Usage:

    python3 -m tapp.talks.ics_gen -i foo.json -o bar.ics

### Webpage

Usage:

    python3 -m tapp.talks.php_gen -i foo.json -o bar.php

## Club Overview Flyers

See data files such as `data/2015-08_F15-flyer.json` for input reference.

Usage:

    python3 -m tapp.flyer.svg_gen -i foo.json -o bar.svg

The files `2015logo_light.svg` and `cmucc_qr.svg` must be in the same directory
as the output file to display properly.

----

# Printing SVGs

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

