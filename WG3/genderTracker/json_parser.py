#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import json
import typing 
from pathlib import Path

class JsonParser:

    # CORE_DATA
    PMCID = 'PMCID'
    FIRST_AUTHOR = 'FIRST_AUTHOR'
    LAST_AUTHOR = 'LAST_AUTHOR'
    ASSOCIATED_AUTHORS = 'ASSOCIATED_AUTHORS'
    # FIRST_AUTHOR_NATION
    ## name
    FIRST_AUTHOR_NATION_NAME = 'FIRST_AUTHOR_NATION_NAME'
    FIRST_AUTHOR_NATION_PROBABILITY_NAME = 'FIRST_AUTHOR_COUNTRY_PROBABILITY_NAME'
    FIRST_AUTHOR_NATION_STATUS_NAME = 'FIRST_AUTHOR_NATION_STATUS_NAME'
    ## surname 
    FIRST_AUTHOR_NATION_SURNAME = 'FIRST_AUTHOR_NATION_SURNAME'
    FIRST_AUTHOR_NATION_PROBABILITY_SURNAME = 'FIRST_AUTHOR_COUNTRY_PROBABILITY_SURNAME'
    FIRST_AUTHOR_NATION_STATUS_SURNAME = 'FIRST_AUTHOR_NATION_STATUS_SURNAME'
    # FIRST_AUTHOR_GENDER
    FIRST_AUTHOR_GENDER = 'FIRST_AUTHOR_GENDER'
    FIRST_AUTHOR_GENDER_PROBABILITY = 'FIRST_AUTHOR_GENDER_PROBABILITY'
    FIRST_NAME_GENDER_STATUS = 'FIRST_NAME_GENDER_STATUS'
    FIRST_AUTHOR_SELECTED_NATION_CATEGORY = 'FIRST_AUTHOR_SELECTED_NATION_CATEGORY'

    # LAST_AUTHOR_NATION
    ## name
    LAST_AUTHOR_NATION_NAME = 'LAST_AUTHOR_NATION_NAME'
    LAST_AUTHOR_NATION_PROBABILITY_NAME = 'LAST_AUTHOR_COUNTRY_PROBABILITY_NAME'
    LAST_AUTHOR_NATION_STATUS_NAME = 'LAST_AUTHOR_NATION_STATUS_NAME'
    ## surname
    LAST_AUTHOR_NATION_SURNAME = 'LAST_AUTHOR_NATION_SURNAME'
    LAST_AUTHOR_NATION_PROBABILITY_SURNAME = 'LAST_AUTHOR_COUNTRY_PROBABILITY_SURNAME'
    LAST_AUTHOR_NATION_STATUS_SURNAME = 'LAST_AUTHOR_NATION_STATUS_SURNAME'
    # LAST_AUTHOR_GENDER
    LAST_AUTHOR_GENDER = 'LAST_AUTHOR_GENDER'
    LAST_AUTHOR_PROBABILITY = 'LAST_AUTHOR_PROBABILITY'
    LAST_AUTHOR_GENDER_STATUS = 'LAST_AUTHOR_GENDER_STATUS'
    LAST_AUTHOR_GENDER_PROBABILITY = 'LAST_AUTHOR_GENDER_PROBABILITY'
    LAST_AUTHOR_SELECTED_NATION_CATEGORY = 'LAST_AUTHOR_SELECTED_NATION_CATEGORY'


    def read(json_path: dict) -> dict :
        with open(json_path, 'r', encoding='utf-8') as file:
            return json.load(file)


    def get_authors(json_entries: dict) -> dict:
        """
        Get first and last authors for each project (pmcid)
        ------------------------------------
            :param json_entries: Json project data
        """
        authors_dict = {}
        for entry in json_entries:

            # Transform string to list
            authors_list = json.loads(entry.get('authors', '[]'))
            
            # Check if authors_list is not empty
            if authors_list:
                authors_dict[entry.get('pmcid')] = {
                    'first_author' : authors_list[0].strip(), 
                    'last_author': authors_list[-1].strip(),
                    'status': "PASS"
                }
            else:
                authors_dict[entry.get('pmcid')] = {
                    'first_author' :"", 
                    'last_author': "",
                    'status': "MISSING"
                    }

        return authors_dict


    def is_pmcid_in_csv( csvpath:str, pmcid:str ) -> bool:
        """
        Check if an entry already exists in a CSV file.
        ------------------------------------
            :param csvpath: Path to the CSV file.
            :param entry: The entry (as a dictionary) to check for.
            :return: True if the entry exists in the CSV, False otherwise.
        """
        try:
            with open(csvpath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    if row.get('PMCID') == pmcid:
                        return True
                return False
        except FileNotFoundError:
            return False


    def json2csv( entry:dict,  outfile:str ) -> None:
        """
        Write CSV with data.
        ------------------------------------
            :param entry:    Dict with data
            :param outdir:   Folder where store CSV with results
        """

        # # Final csv file
        # outfile = Path(outdir) / ( 'gender_analysis' + '.csv')

        # # Check information in csv
        # if not JsonParser.is_json_entry_in_csv(outfile, entry):

            # Create and save information in csv
        with open(str(outfile), 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                JsonParser.PMCID,
                JsonParser.FIRST_AUTHOR,
                JsonParser.LAST_AUTHOR,
                JsonParser.ASSOCIATED_AUTHORS,
                JsonParser.FIRST_AUTHOR_NATION_NAME,
                JsonParser.FIRST_AUTHOR_NATION_PROBABILITY_NAME,
                JsonParser.FIRST_AUTHOR_NATION_STATUS_NAME,
                JsonParser.FIRST_AUTHOR_NATION_SURNAME,
                JsonParser.FIRST_AUTHOR_NATION_PROBABILITY_SURNAME,
                JsonParser.FIRST_AUTHOR_NATION_STATUS_SURNAME,
                JsonParser.FIRST_AUTHOR_GENDER,
                JsonParser.FIRST_AUTHOR_GENDER_PROBABILITY,
                JsonParser.FIRST_NAME_GENDER_STATUS,
                JsonParser.FIRST_AUTHOR_SELECTED_NATION_CATEGORY,
                JsonParser.LAST_AUTHOR_NATION_NAME,
                JsonParser.LAST_AUTHOR_NATION_PROBABILITY_NAME,
                JsonParser.LAST_AUTHOR_NATION_STATUS_NAME,
                JsonParser.LAST_AUTHOR_NATION_SURNAME,
                JsonParser.LAST_AUTHOR_NATION_PROBABILITY_SURNAME,
                JsonParser.LAST_AUTHOR_NATION_STATUS_SURNAME,
                JsonParser.LAST_AUTHOR_GENDER,
                JsonParser.LAST_AUTHOR_GENDER_PROBABILITY,
                JsonParser.LAST_AUTHOR_GENDER_STATUS,
                JsonParser.LAST_AUTHOR_SELECTED_NATION_CATEGORY
            ]
            writer = csv.DictWriter(
                csvfile, fieldnames=fieldnames, delimiter=',')
            if  outfile.stat().st_size == 0 :
                writer.writeheader()
            writer.writerow(entry)


