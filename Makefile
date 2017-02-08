TALKS_DATA=data/2017-02_S17-talks.json
FLYER_DATA=data/2016-09_F16-flyer.json

OUTPUT_DIR=output/spring17
WEB_DIR=/afs/club.cc.cmu.edu/www/talks/spring17
# When publishing, ensure .htaccess redirects the main talks directory to here


all:	talks flyer ${OUTPUT_DIR}

talks:	talks_poster talks_web
talks_poster:	assets
	python -m tapp.talks.svg_gen -i ${TALKS_DATA} -o ${OUTPUT_DIR}/talks-poster.svg
	python -m tapp.talks.svg_gen -i ${TALKS_DATA} -o ${OUTPUT_DIR}/talks-poster-grayscale.svg -g
talks_web:
	python -m tapp.talks.ics_gen -i ${TALKS_DATA} -o ${OUTPUT_DIR}/ccst.ics
	python -m tapp.talks.php_gen -i ${TALKS_DATA} -o ${OUTPUT_DIR}/index.php
	chmod +x ${OUTPUT_DIR}/index.php

flyer:	assets
	python -m tapp.flyer.svg_gen -i ${FLYER_DATA} -o ${OUTPUT_DIR}/flyer.svg


# Publish to web
publish:	all
	mkdir -p ${WEB_DIR}
	rsync -rpE ${OUTPUT_DIR}/ ${WEB_DIR}/


# Assets such as logos and images
assets:
	mkdir -p ${OUTPUT_DIR}/assets
	cp -a logos/cmucc/2015logo_light.svg ${OUTPUT_DIR}/assets/cmucc_logo_2015_light.svg
	cp -a logos/cmucc/2015logo_dark.svg ${OUTPUT_DIR}/assets/cmucc_logo_2015_dark.svg
	cp -a logos/cmucc/cmucc_qr.svg ${OUTPUT_DIR}/assets/cmucc_qr.svg
	cp -a logos/sponsors/green-hills/GHS_Logo_Provided.svg ${OUTPUT_DIR}/assets/ghs_logo.svg

${OUTPUT_DIR}:
	mkdir -p ${OUTPUT_DIR}


clean:
	rm -rf ${OUTPUT_DIR}


.PHONY:	all talks talks_poster talks_web flyer
.PHONY:	publish
.PHONY:	clean

