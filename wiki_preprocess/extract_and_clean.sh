#!/bin/sh
set -e

WIKI_DUMP_FILE_IN=$1
WIKI_DUMP_FILE_OUT=${WIKI_DUMP_FILE_IN%%.*}.txt

python wikiextractor/WikiExtractor.py $WIKI_DUMP_FILE_IN --processes 32 -q -o - \
| sed "/^\s*\$/d" \
| grep -v "^<doc id=" \
> $WIKI_DUMP_FILE_OUT