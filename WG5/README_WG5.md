# NIH

## Goal

This notebook serves the purpose of creating a dataset by merging publications and projects (US) spanning from 1985 to 2022, sourced from the [RePORTER data](https://reporter.nih.gov/exporter/) web page.

## Issues

These notebooks produce a dataset that is too large (`7 GB`) for direct processing. However, it remains valuable for dataset creation after filtering relevant data from the original dataframes. Column removal is required before merging the original datasets (publications and projects) to eliminate duplicates.

## Notebooks

- `nih_data`: clean csvs
    - `projects.csv`
    - `merge_df2.csv`: link_tables + publications
- `nih_results`: merge pmcids + publications + projects
    - `nih_results-1000.csv`: first 1000 results (entire df: ~ 4M rows - 7 Gb)

## Data

Recreate this folder structure to make the notebook work.

```
 + data
    | pmcids_dois_from_counts_data.txt (pmc ids)
    | results_for_analysis.txt (count_data)
    + raw (zips)
        | link_tables
        | publications 
        | projects 
    + input (csvs)
        | link_tables
        | publications 
        | projects 
    + processing
        | codes.csv
        | link_tables.csv
        | publications.csv 
        | merge_df2.csv (link _tables + publications)
        | projects.csv
    + output
```