#Make cubic polynomials 

library(dplyr)

#######
df <- read.csv("analysis/processed_data/analysis_data/combined_new.csv")
df$date_minsk <- as.Date(df$date_minsk) # convert to date type

# Create cubic polynomial of time to account for downward trend in data 
date_unique <- unique(df$date_minsk)
time_df <- data.frame(date_minsk = (date_unique))%>%
  arrange(date_minsk)
time_df$t_1 <- 1:dim(time_df)[1]
time_df$t_2 <- (time_df$t_1) ^ 2
time_df$t_3 <- (time_df$t_1) ^ 3

# Merge this into the data
df <- df %>% 
  left_join(time_df, by = "date_minsk")

write.csv(df, file="analysis/processed_data/analysis_data/combined_new.csv", row.names = FALSE)

