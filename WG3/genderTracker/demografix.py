#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict
from collections import OrderedDict
from pyagify.agify import GenderizeClient, NationalizeClient

class GenderPredictor:


    def format_exceptions( fullname_category: str) -> str:
        """
        """
        # check if name/surnmae is just one letter
        if fullname_category.count(" ") > 1 or "." in fullname_category:
            fullname_category = fullname_category.split(" ")[0]
        
        # check if composed names has several elements joined by -
        if "-"  in fullname_category.replace("‐", "-"):
            fullname_category = fullname_category.replace("‐", "-").split("-")[0]

        return fullname_category

    @staticmethod
    def get_gender ( author_fullname: str, nationality: str, selected_category:str ):
        """
        Predict gender of the name.
        ------------------------------------
            :param author_name:    Author's name
            :param author_surname: Author's surname
            :param nationality:    Author's surname nation

        """
        gender = GenderizeClient()

        AUTHOR_GENDER = {'genderize':{ 'name':{'gender':"", 'gender_score':"", 'gender_status':"PASS"}}}
        gender_author = { author_fullname : AUTHOR_GENDER['genderize'] }


        # Get name and surname and validate 
        try:
            # Check blank spaces
            if author_fullname.count(" ") > 0:
                author_name, author_surname = author_fullname.rsplit(maxsplit=1)
            else:
                raise ValueError("Blank space not found")
            
            # Check length of author_name
            if len(author_name) == 1:
                raise ValueError("Length of author_name is 1")

        except ValueError as e:
            print('\n{}'.format(e))
            gender_author[author_fullname]['name']['country_id'] = ""
            gender_author[author_fullname]['name']['country_score'] = 0.0
            gender_author[author_fullname]['name']['country_status'] = "VALIDATE"
            return gender_author

        # format authors fullname elements (name and surname)
        author_name = GenderPredictor.format_exceptions(author_name) 

        # Gender Name prediction 
        nation = nationality[author_fullname][selected_category]['country_id']
        gender_name = gender.get_raw(author_name, nation)
        gender_author[author_fullname]['name']['gender'] = gender_name['gender'] if gender_name else ""
        gender_author[author_fullname]['name']['gender_score'] = gender_name['probability'] if gender_name else ""

        return  gender_author

    @staticmethod
    def get_nation( author_fullname: str ):
        """
        Predict nation of surname. If fails, use name.
        ------------------------------------------------
            :param author_name:    Author's name
            :param author_surname: Author's surname

        """
        nation = NationalizeClient()

        # Authors nation schema
        AUTHORS_NATION = {
            'nationalize': OrderedDict(
                surname={'country_id': "", 'country_score': "",'country_status': "PASS"},
                name={'country_id': "", 'country_score': "",'country_status': "PASS"}
            )}
        nation_author = { author_fullname : AUTHORS_NATION['nationalize'] }
        

        # Get name and surname and validate 
        try:
            # Check blank spaces
            if author_fullname.count(" ") > 0:
                author_name, author_surname = author_fullname.rsplit(maxsplit=1)
            else:
                raise ValueError("Blank space not found")
            
            # Check length of author_name
            if len(author_name) == 1:
                raise ValueError("Length of author_name is 1")

        except ValueError as e:
            print('\n{}'.format(e))
            for category in ('name', 'surname'):
                nation_author[author_fullname][category]['country_id'] = ""
                nation_author[author_fullname][category]['country_score'] = 0.0
                nation_author[author_fullname][category]['country_status'] = "VALIDATE"
            return nation_author, "surname"


        # format authors fullname elements (name and surname)
        author_name = GenderPredictor.format_exceptions(author_name) 
        author_surname = GenderPredictor.format_exceptions(author_surname)


        # Surname nation prediction
        country_surname = nation.get_raw(author_surname)['country']
        nation_author[author_fullname]['surname']['country_id'] = country_surname[0]['country_id'] if country_surname else ""
        nation_author[author_fullname]['surname']['country_score'] = country_surname[0]['probability'] if country_surname else ""
        
        # Name nation prediction
        country_name = nation.get_raw(author_name)['country']
        nation_author[author_fullname]['name']['country_id'] = country_name[0]['country_id'] if country_name else ""
        nation_author[author_fullname]['name']['country_score'] = country_name[0]['probability'] if country_name else  0.0
        
        return  nation_author, 'surname' if country_surname else 'name'


