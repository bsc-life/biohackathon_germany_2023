#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys
import time
import typing 
from pathlib import Path
# from .proxy import Proxy
from .json_parser import JsonParser
from .demografix import GenderPredictor

NUM_ATTEMPTS = 20

def run ( json_path: str, outfile: str, verbose: bool) -> None:

    # read json 
    json_data = JsonParser.read(json_path)

    # authors: { pmcid: {first_author, last_author, status} }
    data_authors = JsonParser.get_authors(json_data)

    # perdict gender fullnames
    for pmcid, authors in data_authors.items():
        attempt = 0
        
        # check if entry is already saved
        if JsonParser.is_pmcid_in_csv( outfile, pmcid ):
            continue

        if (verbose):
            index = 1
            print(f"Gender inference for: {pmcid}", end='', flush=True)

        if authors.get('status') == "PASS":
            try:

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


            except Exception as e:
                print('\n{}'.format(e))
                print(
                    '[ Query Error ] There was a problem infering gender/nation for {pmcid}. Attempt {}/{}'.format(attempt + 1, NUM_ATTEMPTS))
                attempt = attempt + 1

                while True:
                    # Stop the run to change the proxy
                    inp = input('An unexpected problem has occurred or you have reached the limit of requests specified by the library.' 
                            'Please, continue the execution and if the error persists, use a vpn to change the IP or open a pull request to fix the problem if this persist.'
                            'Press Enter to continue the analysis or type "exit" to stop and exit....')
                    if inp.strip().lower() == "exit":
                        sys.exit()

                    elif not inp.strip():
                        print("Wait 10 seconds...")
                        time.sleep(10)
                        break  # Break the inner while loop and continue with the next attempt
                    else:
                        print("Invalid input. Please press Enter or type 'exit'.")
            
                if attempt == NUM_ATTEMPTS:
                    sys.exit("Disconnected!")
            #         # If connection fails because of the proxy, try to find and connect a new one
            #         print(' '.join("[ Connection Error ]: Connecting to a new proxy. This process can takes times. \
            #                                         Retrying in 15 seconds once we find a new proxy.".split()))
            #         Proxy.set_new_proxy()
            #     else:
            #         break
            # else:, end='', flush=True
            #     raise ConnectionError('[ Critical Error ] Too many failed attempts at scraping Google Scholar. Please run the program again.')

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

            if (verbose):
                index += 1
                print(f"\rGender inference for: {pmcid} [OK]")


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
        outfile = Path(outdir) / ( 'gender_analysis1' + '.csv')

    if args.verbose:
        print("genderTraker")
        print(f"analyzing json: {args.json}")
        print(f"Output path: {outfile}")


    # Execution
    run ( args.json, outfile, args.verbose )


if __name__ == "__main__":
    main()