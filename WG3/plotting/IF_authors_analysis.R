library(dplyr)
library(ggplot2)

# Load the dataset 'vickytable2' from a CSV file with semicolon as the separator
#vickytable2 <- read.table(file.choose(), sep=";", fill=TRUE, header=TRUE)
vickytable2 <- read.table("../inputs/counts_cordis_ratios.csv", sep=",", fill=TRUE, header=TRUE)

# Load the dataset 'maria_table' from a tab-separated text file
#maria_table <- read.table(file.choose(), sep="\t", fill=TRUE, header=TRUE)
maria_table <- read.table("../results/impact_factor/IF_total_journals_cordis.csv", sep="\t", fill=TRUE, header=TRUE, na.strings = c("", " "))

# Assign labels to the 'sexrep' column based on the condition of 'median_agg_ratio'
vickytable2$sexrep[vickytable2$median_agg_ratio > 1] <- "More Males"
vickytable2$sexrep[vickytable2$median_agg_ratio < 1] <- "More Females"
vickytable2$sexrep[vickytable2$median_agg_ratio == 1] <- "Both"

# Merge the datasets 'vickytable2' and 'maria_table' based on the 'pmcid' column
cordis_IF <- merge(vickytable2, maria_table, by="pmcid", all=TRUE)

# Summarize data using dplyr to count, calculate median, and interquartile range (IQR)
summary_data <- cordis_IF %>%
  group_by(sexrep) %>%
  summarise(
    count = n(),
    median = median(impact_factor, na.rm=TRUE),
    IQR = IQR(impact_factor, na.rm=TRUE)
  )

# Display the summary data
print(summary_data)

# Summarize the 'totalcost_cordis' column
summary(cordis_IF$totalcost_cordis)

gg1 <- ggplot(data=cordis_IF, aes(x=impact_factor, y=totalcost_cordis, size=impact_factor, color=sexrep)) +
  geom_point() +
  scale_size(range=c(1, 5)) +
  labs(title="Bubble chart", x="Impact Factor", y="Total Cost") +
  theme_bw()

# Save the ggplot to a file (adjust the file path and format as needed)
ggsave("../results/impact_factor/plots/IF_bubble_chart.png", gg1, width = 8, height = 6)

# Select relevant columns and remove rows with NA values
COND_FUND <- cordis_IF[c("pmcid", "impact_factor", "totalcost_cordis", "sexrep", "median_agg_ratio")]
cond_fund_na <- na.omit(COND_FUND)

# Create another scatter plot with data without NA values
gg2 <- ggplot(data=cond_fund_na, aes(x=impact_factor, y=totalcost_cordis, size=impact_factor, color=sexrep)) +
  geom_point() +
  scale_size(range=c(1, 5)) +
  labs(title="", x="Impact Factor", y="Funding") +
  theme_bw()

# Save the ggplot to a file (adjust the file path and format as needed)
ggsave("../results/impact_factor/plots/IF_scatter_chart.png", gg2, width = 8, height = 6)

# Save the 'COND_FUND' dataset to a CSV file
write.table(COND_FUND, file="../results/impact_factor/IF_funding_ratios.csv", sep="\t")
