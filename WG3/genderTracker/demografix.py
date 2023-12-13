#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Dict
from pyagify.agify import GenderizeClient, NationalizeClient

class GenderPredictor:

    def get_gender ( author_fullname: str, nationality: str ) -> Dict[str,Dict[str,str]]:
        """
        Predict gender of the name.
        ------------------------------------
            :param author_name:    Author's name
            :param author_surname: Author's surname
            :param nationality:    Author's surname nation

        """
        AUTHOR_GENDER = {'genderize':{ 'name':{'gender':"", 'gender_score':"", 'gender_status':"PASS"}}}

        gender = GenderizeClient()
        gender_author = { author_fullname : AUTHOR_GENDER['genderize'] }
        
        # Check blank spaces
        if author_fullname.count(" ") > 0:
            author_name, author_surname = author_fullname.rsplit(maxsplit=1)
        else:
            gender_author[author_fullname]['name']['country_id'] = ""
            gender_author[author_fullname]['name']['gender_score'] = 0.0
            gender_author[author_fullname]['name']['gender_status'] = "VALIDATE"
            return gender_author

        # Exceptions
        if author_fullname.count(" ") > 1:
            author_name = author_name.split(" ")[0]

        if "-"  in author_name.replace("‐", "-"):
            author_name = author_name.replace("‐", "-").split("-")[0]
        
        # if "." in author_name.replace(".", "."):
        #     author_name = author_name.replace(".", ".").split(".")[0]

        if len(author_name) == 1:
            gender_author[author_fullname]['name']['gender'] = ""
            gender_author[author_fullname]['name']['gender_score'] = 0.0
            gender_author[author_fullname]['name']['gender_status'] = "VALIDATE"
            return gender_author

        # Gender prediction 
        if author_fullname and author_name:
            nation = nationality[author_fullname]
            gender_author[author_fullname]['name']['gender'] = gender.get_raw(author_name, nation['surname']['country_id'])['gender']
            gender_author[author_fullname]['name']['gender_score'] = gender.get_raw(author_name, nation['surname']['country_id'])['probability']
        else:
            gender_author[author_fullname]['name']['gender'] = ""
            gender_author[author_fullname]['name']['gender_score'] = 0.0
            

        return  gender_author


    def get_nation( author_fullname: str ) -> Dict[str,Dict[str,str]]:
        """
        Predict nation of surname. If fails, use name.
        ------------------------------------------------
            :param author_name:    Author's name
            :param author_surname: Author's surname

        """
        AUTHORS_NATION = {'nationalize':{'surname':{'country_id':"",'country_score':"", 'country_status':"PASS"}}}

        nation = NationalizeClient()
        nation_author = { author_fullname : AUTHORS_NATION['nationalize'] }

        # Check blank spaces
        if author_fullname.count(" ") > 0:
            author_name, author_surname = author_fullname.rsplit(maxsplit=1)
        else:
            nation_author[author_fullname]['surname']['country_id'] = ""
            nation_author[author_fullname]['surname']['country_score'] = 0.0
            nation_author[author_fullname]['surname']['country_status'] = "VALIDATE"
        
        # Exceptions
        if author_fullname.count(" ") > 1:
            author_name = author_name.split(" ")[0]

        if "-"  in author_surname.replace("‐", "-"):
            author_surname = author_surname.replace("‐", "-").split("-")[0]

        # Nation prediction
        if author_fullname and author_surname:
            try:
                country = nation.get_raw(author_surname)['country']
                nation_author[author_fullname]['surname']['country_id'] = country[0]['country_id'] 
                nation_author[author_fullname]['surname']['country_score'] = country[0]['probability'] 
            
            except IndexError:
                country = nation.get_raw(author_name)['country']
                nation_author[author_fullname]['surname']['country_id'] = country[0]['country_id'] if country else ""
                nation_author[author_fullname]['surname']['country_score'] = country[0]['probability'] if country else  0.0

        if author_fullname and author_name:
                country = nation.get_raw(author_name)['country']
                nation_author[author_fullname]['surname']['country_id'] = country[0]['country_id'] if country else ""
                nation_author[author_fullname]['surname']['country_score'] = country[0]['probability'] if country else 0.0

        return nation_author