Here are the code and results for WG3.

# WG3: GENER ATURHOS INFERENCE (FIRST AND LAST) AND IMPACT FACTOR

# genderTracker

Execution for all counts (directory: "cd ./WG3"):
`python -m genderTracker -j results_for_analysis.json -od results -v True`

Execution for CORDIS (directory: "cd ./WG3"):
`python -m genderTracker -j results_for_analysis_CORDIS.json -od results -v True`

# IFTracker

Execution for all counts (directory: "cd ./WG3"):
`python get_IF_journal.py pmcid_journals.csv `

# Plotting

Execution gender authors (directory: "cd ./WG3/plotting"):
`python gender_authors_analysis.py ../results/gender/gender_analysis.csv ../inputs/gender/counts_cordis_ratios.csv`

Execution impact factor (directory: "cd ./WG3/plotting"):
`Rscript IF_authors_analysis.R`
