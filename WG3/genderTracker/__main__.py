#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import os
import re
import time
import json
import typing 
from pathlib import Path
from .json_parser import JsonParser
from .demografix import GenderPredictor



def run ( json_path: str, outdir: str, verbose: bool):
    """
    """

    # read json 
    json_data = JsonParser.read(json_path)

    # authors: { pmcid: {first_author, last_author, status} }
    data_authors = JsonParser.get_authors(json_data)

    # perdict gender fullnames
    
    for pmcid, authors in data_authors.items():

        if authors.get('status') == "PASS":

            ## FIRST AUTHOR
            
            # fist_author: infering  name nation 
            fauthor_nation = GenderPredictor.get_nation(authors.get('first_author'))

            # fist_author: infering gender name
            fauthor_gender = GenderPredictor.get_gender(authors.get('first_author'), fauthor_nation)
        
            
            # LAST AUTHOR

            # last_author: infering name nation 
            lauthor_nation = GenderPredictor.get_nation(authors.get('last_author'))

            # last_author: infering gender name
            lauthor_gender = GenderPredictor.get_gender(authors.get('last_author'), lauthor_nation)


            # define entry
            entry = {
                JsonParser.PMCID:pmcid,
                JsonParser.FIRST_AUTHOR: authors.get('first_author'),
                JsonParser.LAST_AUTHOR: authors.get('last_author'),
                JsonParser.STATUS: authors.get('status'),
                JsonParser.FIRST_AUTHOR_GENDER: fauthor_gender.get(authors.get('first_author')).get('name').get('gender'),
                JsonParser.FIRST_AUTHOR_GENDER_PROBABILITY: fauthor_gender.get(authors.get('first_author')).get('name').get('gender_score'),
                JsonParser.FIRST_NAME_GENDER_STATUS: fauthor_gender.get(authors.get('first_author')).get('name').get('gender_status'),
                JsonParser.FIRST_AUTHOR_NATION: fauthor_nation.get(authors.get('first_author')).get('surname').get('country_id'),
                JsonParser.FIRST_AUTHOR_NATION_PROBABILITY: fauthor_nation.get(authors.get('first_author')).get('surname').get('country_score'),
                JsonParser.FIRST_AUTHOR_NATION_STATUS:fauthor_nation.get(authors.get('first_author')).get('surname').get('country_status'),
                JsonParser.LAST_AUTHOR_GENDER: lauthor_gender.get(authors.get('last_author')).get('name').get('gender'),
                JsonParser.LAST_AUTHOR_GENDER_PROBABILITY: lauthor_gender.get(authors.get('last_author')).get('name').get('gender_score'),
                JsonParser.LAST_AUTHOR_GENDER_STATUS: lauthor_gender.get(authors.get('last_author')).get('name').get('gender_status'),
                JsonParser.LAST_AUTHOR_NATION: lauthor_nation.get(authors.get('last_author')).get('surname').get('country_id'),
                JsonParser.LAST_AUTHOR_NATION_PROBABILITY: lauthor_nation.get(authors.get('last_author')).get('surname').get('country_score'),
                JsonParser.LAST_AUTHOR_NATION_STATUS: lauthor_nation.get(authors.get('last_author')).get('surname').get('country_status')
            }

        else:
            entry = {
                JsonParser.PMCID:pmcid,
                JsonParser.FIRST_AUTHOR: authors.get('first_author'),
                JsonParser.LAST_AUTHOR: authors.get('last_author'),
                JsonParser.STATUS: authors.get('status'),
                JsonParser.FIRST_AUTHOR_GENDER: "",
                JsonParser.FIRST_AUTHOR_GENDER_PROBABILITY: 0.0,
                JsonParser.FIRST_NAME_GENDER_STATUS: "MISSING",
                JsonParser.FIRST_AUTHOR_NATION: "",
                JsonParser.FIRST_AUTHOR_NATION_PROBABILITY: 0.0,
                JsonParser.FIRST_AUTHOR_NATION_STATUS: "MISSING",
                JsonParser.LAST_AUTHOR_GENDER: "",
                JsonParser.LAST_AUTHOR_GENDER_PROBABILITY: 0.0,
                JsonParser.LAST_AUTHOR_GENDER_STATUS: "MISSING",
                JsonParser.LAST_AUTHOR_NATION: "",
                JsonParser.LAST_AUTHOR_NATION_PROBABILITY: 0.0,
                JsonParser.LAST_AUTHOR_NATION_STATUS: "MISSING"
            }
        
        # Write .csv
        JsonParser.json2csv(entry, outdir)
        

def main():

    # CMD Arguments
    parser = argparse.ArgumentParser(
        description='genderTracker is python tool to infer to gender from a fullname')

    parser.add_argument('-j', '--json', type=str, default=None,
                        help='Set jason file with authors entries')

    parser.add_argument('-od', '--outdir', type=str, default=".",
                        help='Set a custom path for the directory where the search .CSV files should be stored.')

    parser.add_argument('-v', '--verbose', type=bool, default=True,
                        help='Verbose mode.')

    args = parser.parse_args()


    if args.json is None:
        print("[ Input Error ] Provide at least one of the following arguments: --json or -j")
        sys.exit()

    if args.outdir is None:
        print("[ Input Error ] Provide at least one of the following arguments: --outdir or -od")
        sys.exit()
    else:
        outdir = Path(args.outdir)
        outdir.mkdir(parents=True,exist_ok=True)

    if args.verbose:
        print("genderTraker")
        print(f"analyzing json: {args.json}")
        print(f"Output path: {args.outdir}")


    # Execution
    run ( args.json, args.outdir, args.verbose )


if __name__ == "__main__":
    main()
    print("""\nWork completed!\n""")