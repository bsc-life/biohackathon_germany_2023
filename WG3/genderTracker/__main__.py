#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import typing 
from pathlib import Path
# from .proxy import Proxy
from .json_parser import JsonParser
from collections import OrderedDict
from .demografix import GenderPredictor

NUM_ATTEMPTS = 20

def run ( json_path: str, outfile: str, verbose: bool) -> None:

    # read json 
    json_data = JsonParser.read(json_path)

    # authors: { pmcid: {first_author, last_author, status} }
    data_authors = JsonParser.get_authors(json_data)

    # perdict gender fullnames
    for pmcid, authors in data_authors.items():

        # check if entry is already saved
        if JsonParser.is_pmcid_in_csv( outfile, pmcid ):
            continue

        if (verbose):
            index = 1
            print(f"Gender inference for: {pmcid}", end='', flush=True)

        if authors.get('status') == "PASS":
            # try: 
            ## FIRST AUTHOR
    
            # fist_author: infering  name nation 
            fauthor_nation, fselected_category = GenderPredictor.get_nation(authors.get('first_author'))
            
            # fist_author: infering gender name
            fauthor_gender = GenderPredictor.get_gender(authors.get('first_author'), fauthor_nation, fselected_category)
                
            # LAST AUTHOR

            # last_author: infering name nation 
            lauthor_nation, lselected_category = GenderPredictor.get_nation(authors.get('last_author'))

            # last_author: infering gender name
            lauthor_gender = GenderPredictor.get_gender(authors.get('last_author'), lauthor_nation, lselected_category)


            # define entry
            entry = {
                # CORE_DATA
                JsonParser.PMCID:pmcid,
                JsonParser.FIRST_AUTHOR: authors.get('first_author'),
                JsonParser.LAST_AUTHOR: authors.get('last_author'),
                JsonParser.ASSOCIATED_AUTHORS: authors.get('status'),

                # FIRST_AUTHOR_NATION
                ## name
                JsonParser.FIRST_AUTHOR_NATION_NAME: fauthor_nation.get(authors.get('first_author')).get(fselected_category).get('country_id'),
                JsonParser.FIRST_AUTHOR_NATION_PROBABILITY_NAME: fauthor_nation.get(authors.get('first_author')).get(fselected_category).get('country_score'),
                JsonParser.FIRST_AUTHOR_NATION_STATUS_NAME:fauthor_nation.get(authors.get('first_author')).get(fselected_category).get('country_status'),
                ## surname
                JsonParser.FIRST_AUTHOR_NATION_SURNAME: fauthor_nation.get(authors.get('first_author')).get(fselected_category).get('country_id'),
                JsonParser.FIRST_AUTHOR_NATION_PROBABILITY_SURNAME: fauthor_nation.get(authors.get('first_author')).get(fselected_category).get('country_score'),
                JsonParser.FIRST_AUTHOR_NATION_STATUS_SURNAME:fauthor_nation.get(authors.get('first_author')).get(fselected_category).get('country_status'),
                # FIRST_AUTHOR_GENDER
                JsonParser.FIRST_AUTHOR_GENDER: fauthor_gender.get(authors.get('first_author')).get('name').get('gender'),
                JsonParser.FIRST_AUTHOR_GENDER_PROBABILITY: fauthor_gender.get(authors.get('first_author')).get('name').get('gender_score'),
                JsonParser.FIRST_NAME_GENDER_STATUS: fauthor_gender.get(authors.get('first_author')).get('name').get('gender_status'),
                JsonParser.FIRST_AUTHOR_SELECTED_NATION_CATEGORY: fselected_category,
                
                # LAST_AUTHOR_NATION
                ## name
                JsonParser.LAST_AUTHOR_NATION_NAME: lauthor_nation.get(authors.get('last_author')).get(lselected_category).get('country_id'),
                JsonParser.LAST_AUTHOR_NATION_PROBABILITY_NAME: lauthor_nation.get(authors.get('last_author')).get(lselected_category).get('country_score'),
                JsonParser.LAST_AUTHOR_NATION_STATUS_NAME: lauthor_nation.get(authors.get('last_author')).get(lselected_category).get('country_status'),
                ## surname
                JsonParser.LAST_AUTHOR_NATION_SURNAME: lauthor_nation.get(authors.get('last_author')).get(lselected_category).get('country_id'),
                JsonParser.LAST_AUTHOR_NATION_PROBABILITY_SURNAME: lauthor_nation.get(authors.get('last_author')).get(lselected_category).get('country_score'),
                JsonParser.LAST_AUTHOR_NATION_STATUS_SURNAME: lauthor_nation.get(authors.get('last_author')).get(lselected_category).get('country_status'),
                # LAST_AUTHOR_GENDER
                JsonParser.LAST_AUTHOR_GENDER: lauthor_gender.get(authors.get('last_author')).get('name').get('gender'),
                JsonParser.LAST_AUTHOR_GENDER_PROBABILITY: lauthor_gender.get(authors.get('last_author')).get('name').get('gender_score'),
                JsonParser.LAST_AUTHOR_GENDER_STATUS: lauthor_gender.get(authors.get('last_author')).get('name').get('gender_status'),
                JsonParser.LAST_AUTHOR_SELECTED_NATION_CATEGORY: lselected_category
            }

            if (verbose):
                index += 1
                print(f"\rGender inference for: {pmcid} [OK]")


        else:
            entry = {
                # CORE_DATA
                JsonParser.PMCID:pmcid,
                JsonParser.FIRST_AUTHOR: authors.get('first_author'),
                JsonParser.LAST_AUTHOR: authors.get('last_author'),
                JsonParser.ASSOCIATED_AUTHORS: authors.get('status'),

                # FIRST_AUTHOR_NATION
                ## name
                JsonParser.FIRST_AUTHOR_NATION_NAME: "",
                JsonParser.FIRST_AUTHOR_NATION_PROBABILITY_NAME: 0.0,
                JsonParser.FIRST_AUTHOR_NATION_STATUS_NAME: "MISSING",
                ## surname 
                JsonParser.FIRST_AUTHOR_NATION_SURNAME: "",
                JsonParser.FIRST_AUTHOR_NATION_PROBABILITY_SURNAME: 0.0,
                JsonParser.FIRST_AUTHOR_NATION_STATUS_SURNAME: "MISSING",
                # FIRST_AUTHOR_GENDER
                JsonParser.FIRST_AUTHOR_GENDER: "",
                JsonParser.FIRST_AUTHOR_GENDER_PROBABILITY: 0.0,
                JsonParser.FIRST_NAME_GENDER_STATUS: "MISSING",
                JsonParser.FIRST_AUTHOR_SELECTED_NATION_CATEGORY: "",

                # LAST_AUTHOR_NATION
                ## name
                JsonParser.LAST_AUTHOR_NATION_NAME: "",
                JsonParser.LAST_AUTHOR_NATION_PROBABILITY_NAME: 0.0,
                JsonParser.LAST_AUTHOR_NATION_STATUS_NAME: "MISSING",
                ## surname
                JsonParser.LAST_AUTHOR_NATION_SURNAME: "",
                JsonParser.LAST_AUTHOR_NATION_PROBABILITY_SURNAME: 0.0,
                JsonParser.LAST_AUTHOR_NATION_STATUS_SURNAME: "MISSING",
                # LAST_AUTHOR_GENDER
                JsonParser.LAST_AUTHOR_GENDER: "",
                JsonParser.LAST_AUTHOR_GENDER_PROBABILITY: 0.0,
                JsonParser.LAST_AUTHOR_GENDER_STATUS: "MISSING",
                JsonParser.LAST_AUTHOR_SELECTED_NATION_CATEGORY: ""
            }

            if (verbose):
                index += 1
                print(f"\rGender inference for: {pmcid} [EMPTY]")


        if (verbose):    
            if index % 100 == 0:
                print(f"Checked {index} projects in this run.")

        
        # Write .csv
        JsonParser.json2csv(entry, outfile)
        

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
        # Final csv file
        outfile = Path(outdir) / ( 'gender_analysis' + '.csv')

    if args.verbose:
        print("genderTraker")
        print(f"analyzing json: {args.json}")
        print(f"Output path: {outfile}")


    # Execution
    run ( args.json, outfile, args.verbose )


if __name__ == "__main__":
    main()