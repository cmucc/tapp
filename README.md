# TAPP
Totally Automated Propaganda Producer

This package contains scripts to be used to produce marketing materials for the CMU Computer Club.

## Talk Series Posters

Usage:

    ./talk_series.py -i foo.json -o bar.svg

See the example `json` file for reference.

The file `2013logo_light.svg` must be in the same directory as the output file to display properly.
Additionally, the filename given in the `sponsor_logo` field must be relative to the output file. 

## Club Overview Flyers

Usage:

    ./overview.py -i foo.json -o bar.svg

See the example `json` file for reference.

The files `2013logo_light.svg` and `cmucc_qr.svg` must be in the same directory as the output file to display properly.
