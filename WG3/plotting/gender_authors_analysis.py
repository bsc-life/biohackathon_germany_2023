import os
import sys
import pandas as pd
import seaborn as sns
from pathlib import Path
import matplotlib.pyplot as plt

GENDER_DATA = sys.argv[1]
COUNTAS_DATA = sys.argv[2]
VERBOSE = True
class GenderData:

    def __init__(self, file):
        self.file = file

    def read(self):
        return pd.read_csv(self.file)

class CountsData:

    def __init__(self, file):
        self.file = file

    def read(self):
        df = pd.read_csv(self.file)
        df.columns = df.columns.str.upper()
        return df

class StatisticalAnalyzer:

    @staticmethod
    def describe_data(df):
        """Prints basic information and statistics about the DataFrame."""
        print(df.info())
        print(df.describe())

    @staticmethod
    def get_percentages(df, colname):
        """ """
        return df[colname].value_counts(normalize=True) * 100

    @staticmethod
    def get_gender_zeros(df, colname):
        return df.loc[df[colname] == 0.0][['ASSOCIATED_AUTHORS', colname]]

class Plots:

    @staticmethod
    def pieplot(percentage, titlename, save_path=None):
        plt.pie(percentage, labels=list(percentage.index), autopct='%.0f%%')
        plt.title(f"Distribution of {titlename}")
        plt.legend()

        if save_path:
            plt.savefig(save_path + "_pieplot.png")
            plt.savefig(save_path + "_pieplot.pdf")
        else:
            plt.show()

    @staticmethod
    def histplot():
        pass

    @staticmethod
    def barplot(df, x_col, y_col, title, xlabel, ylabel, save_path=None):
        sns.set(style="whitegrid")
        plt.figure(figsize=(10, 6))
        sns.barplot(x=x_col, y=y_col, data=df)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        if save_path:
            plt.savefig(save_path + "_barplot.png")
            plt.savefig(save_path + "_barplot.pdf")
        else:
            plt.show()

    @staticmethod
    def countplot(df, x_col, title, xlabel, ylabel, save_path=None):
        plt.figure(figsize=(8, 6))
        sns.countplot(x=x_col, data=df)
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        if save_path:
            plt.savefig(save_path + "_countplot.png")
            plt.savefig(save_path + "_countplot.pdf")
        else:
            plt.show()


    @staticmethod
    def bar_chart(categories, values, title, xlabel, ylabel, save_path=None):
        plt.figure(figsize=(10, 6))
        plt.bar(categories, values, color=['blue', 'pink'])
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        
        if save_path:
            plt.savefig(save_path + "_bar_chart.png")
            plt.savefig(save_path + "_bar_chart.pdf")
        else:
            plt.show()

def main():

    # read csvs

    # read gender inferences
    gender_cordis = GenderData(GENDER_DATA)
    gender_data = gender_cordis.read()
    
    # read counts_ration
    counts_cordis = CountsData(COUNTAS_DATA)
    counts_data = counts_cordis.read()
    counts_data = counts_data[[
                        'PMCID',
                        'TOTALCOST_CORDIS', 
                        'MAX_N_RATIO', 
                        'MAX_PERC_RATIO',
                        'MEDIAN_N_FEM', 
                        'MEDIAN_PERC_FEM', 
                        'MEDIAN_N_MALE', 
                        'MEDIAN_PERC_MALE',
                        'MEDIAN_N_RATIO', 
                        'MEDIAN_PERC_RATIO', 
                        'MAX_AGG_RATIO',
                        'MEDIAN_AGG_RATIO'
                    ]]


    # Apply statistics
    analyzer = StatisticalAnalyzer()
    gender_summary = analyzer.describe_data(gender_data)
    counts_summary = analyzer.describe_data(counts_data)

    if(VERBOSE):
        print(gender_summary)
        print(counts_summary)

    # Get percentages from the status of the query
    status_percentages = analyzer.get_percentages(gender_data, 'ASSOCIATED_AUTHORS')
    Plots.pieplot(
        status_percentages,
        'ASSOCIATED_AUTHORS',
        save_path='../results/gender/plots/associated_authors'
    )

    # combined data
    data = pd.merge(gender_data, counts_data, on='PMCID', how='inner')

    # Remove Missings
    data_without_missings = data.loc[data['ASSOCIATED_AUTHORS'] != 'MISSING']
    print(f"Percentage of entries without missings: {len(data_without_missings)} / {len(data)} ({(len(data_without_missings) / len(data)) * 100:.2f})%")
    print(f"Total entries for the next statistics: {len(data_without_missings)}")

    # Plot
    Plots.countplot(
        data_without_missings,
        'ASSOCIATED_AUTHORS',
        'Number of Entries without Missing Values',
        'Associated Authors Category',
        'Count',
        save_path='../results/gender/plots/data_without_missings'
    )

    # Not detected gender entries in firts authors
    fauthor_gender_zeros = analyzer.get_gender_zeros(data_without_missings, 'FIRST_AUTHOR_GENDER_PROBABILITY')
    print(f"Percentage of not detected gender in first authors: {len(fauthor_gender_zeros)} / {len(data_without_missings)} ({(len(fauthor_gender_zeros) / len(data_without_missings)) * 100:.2f})%")

    # Plot
    Plots.countplot(
        fauthor_gender_zeros,
        'FIRST_AUTHOR_GENDER_PROBABILITY',
        'Undetected Gender in First Authors',
        'Gender',
        'Count',
        save_path='../results/gender/plots/fauthor_gender_zeros'
    )

    # Not detected gender entries in last authors
    lauthor_gender_zeros = analyzer.get_gender_zeros(data_without_missings, 'LAST_AUTHOR_GENDER_PROBABILITY')
    print(f"Percentage of not detected gender in last authors: {len(lauthor_gender_zeros)} / {len(data_without_missings)} ({(len(lauthor_gender_zeros) / len(data_without_missings)) * 100:.2f})%")

    # Plot
    Plots.countplot(
        lauthor_gender_zeros,
        'LAST_AUTHOR_GENDER_PROBABILITY',
        'Undetected Gender in Last Authors',
        'Gender',
        'Count',
        save_path='../results/gender/plots/lauthor_gender_zeros'
    )

    # Remove 0.0 in gender probability (NAN gender) in first authors
    first_authors_ok = data_without_missings.loc[data_without_missings['FIRST_AUTHOR_GENDER_PROBABILITY'] != 0.0]
    print(f"Total firts authors without missings and not NaN gender: {len(first_authors_ok)}")
    
    # Plot
    Plots.countplot(
        first_authors_ok,
        'FIRST_AUTHOR_GENDER',
        'Gender without 0.0 Probability in First Authors',
        'Gender',
        'Count',
        save_path='../results/gender/plots/first_authors'
    )

    fauthors_counts = first_authors_ok['FIRST_AUTHOR_GENDER'].value_counts().to_dict()
    fmales_percentage = (fauthors_counts.get('male', 0) / sum(fauthors_counts.values())) * 100
    ffemales_percentage = (fauthors_counts.get('female', 0) / sum(fauthors_counts.values())) * 100
    print(f"First Authors: Percentage of males: {fauthors_counts['male']} / {sum(fauthors_counts.values())} ({(fauthors_counts['male']/sum(fauthors_counts.values())*100):.2f}%)")
    print(f"First Authors: Percentage of females: {fauthors_counts['female']} / {sum(fauthors_counts.values())} ({(fauthors_counts['female']/sum(fauthors_counts.values())*100):.2f}%)")

    Plots.bar_chart(
        ['Male', 'Female'],
        [fmales_percentage, ffemales_percentage],
        'Percentage of Genders among First Authors',
        'Gender',
        'Percentage',
        save_path='../results/gender/plots/fauthors_counts'
    )


    # Remove 0.0 in gender probability (NAN gender) in last authors
    last_authors_ok = data_without_missings.loc[data_without_missings['LAST_AUTHOR_GENDER_PROBABILITY'] != 0.0]
    print(f"Total lasts authors without missings and not NaN gender: {len(last_authors_ok)}")
    
    # Plot
    Plots.countplot(
        last_authors_ok,
        'LAST_AUTHOR_GENDER',
        'Gender without 0.0 Probability in Last Authors',
        'Gender',
        'Count',
        save_path='../results/gender/plots/last_authors'
    )

    lauthors_counts = last_authors_ok['LAST_AUTHOR_GENDER'].value_counts().to_dict()
    lmales_percentage = (lauthors_counts.get('male', 0) / sum(lauthors_counts.values())) * 100
    lfemales_percentage = (lauthors_counts.get('female', 0) / sum(lauthors_counts.values())) * 100
    print(f"Last Authors: Percentage of males: {lauthors_counts['male']} / {sum(lauthors_counts.values())} ({(lauthors_counts['male']/sum(lauthors_counts.values())*100):.2f}%)")
    print(f"Last Authors: Percentage of females: {lauthors_counts['female']} / {sum(lauthors_counts.values())} ({(lauthors_counts['female']/sum(lauthors_counts.values())*100):.2f}%)")

    # Plot
    Plots.bar_chart(
        ['Male', 'Female'],
        [lmales_percentage, lfemales_percentage],
        'Percentage of Genders among Last Authors',
        'Gender',
        'Percentage',
        save_path='../results/gender/plots/lauthors_counts'
    )


    # Funding analysis by gender of first author
    Plots.barplot(
        data,
        'FIRST_AUTHOR_GENDER',
        'TOTALCOST_CORDIS',
        'Funding by Gender of First Author',
        'Gender of First Author',
        'Total Funding (TOTALCOST_CORDIS)',
        save_path='../results/gender/plots/fauthors_founding'

    )

    # Funding analysis by gender of last author
    Plots.barplot(
        data,
        'LAST_AUTHOR_GENDER',
        'TOTALCOST_CORDIS',
        'Funding by Gender of Last Author',
        'Gender of Last Author',
        'Total Funding (TOTALCOST_CORDIS)',
        save_path='../results/gender/plots/lauthors_founding'
    )


if __name__ == "__main__":
    main()

