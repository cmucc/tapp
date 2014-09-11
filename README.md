# TAPP
Totally Automated Propaganda Producer

This package contains scripts to be used to produce marketing materials for the
CMU Computer Club.

## Talk Series Posters

Usage:

    ./talk_series/svg-gen.py -i foo.json -o bar.svg

See the example `talks_series/example.json` file for reference.

The file `2013logo_light.svg` must be in the same directory as the output file
to display properly.  Additionally, the filename given in the `sponsor_logo`
field must be relative to the output file.

## Club Overview Flyers

Usage:

    ./overview/svg-gen.py -i foo.json -o bar.svg

See the example `overview/example.json` file for reference.

The files `2013logo_light.svg` and `cmucc_qr.svg` must be in the same directory
as the output file to display properly.

## Printing SVGs

Generated SVGs are intended to be viewed and printed from [Google
Chrome](https://www.google.com/chrome/browser/); however, the transcluded logos
can cause issues.  As a workaround, manually remove the `<image>` tags from the
SVG output, and replace them using an SVG editor such as
[Inkscape](http://www.inkscape.org/en/).  Ensure all required fonts are
installed, resize to desired output size, and print.

