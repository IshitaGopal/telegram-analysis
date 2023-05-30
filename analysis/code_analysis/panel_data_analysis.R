# https://www.princeton.edu/~otorres/Panel101R.pdf
# https://stackoverflow.com/questions/28359491/r-plm-time-fixed-effect-model

rm(list=ls())
library(dplyr)
library(foreign)
library(car)
library(plm)
library(lmtest)
library(sandwich)

#######
df <- read.csv("analysis/processed_data/analysis_data/combined_new.csv")
df$date_minsk <- as.Date(df$date_minsk) # convert to date type
df$district_name <- as.factor(df$district_name) # convert to factors

# Check how many observations for each district 
df_summary <- df %>%
  group_by(district_name) %>%
  summarise(n = n_distinct(date_minsk)) 


# Function to create estimate regression model using rhobust standard errors and create summeries
robust_summary <- function(formula, data, cluster_var, time_var) {
  "
  This function takes in the data, regression formula, clustering and time variable
  Converts the data into panel data format
  Runs the panel model with the formula
  Calculates robust standard errors using the vcovHC function with the HC3 estimator
  Calculates the t-stats and p-values for the coefficient estimates using the coeftest function
  "
  pdata <- pdata.frame(data, index=c(cluster_var, time_var))
  model <- plm(formula, data=pdata, model="within", effect = "individual")
  vcov <- vcovHC(model, type="HC3", cluster = "group")
  ct <- coeftest(model, vcov)
  return(ct)
}

# large protest > 1000 participants = 102 protests 
# Binary Repression DV
f1 <- repression_binary ~ lag_log_num_msgs + 
  large_protest_1 + 
  small_protest_1 +
  #focal_day_3 + 
  lag_repression_binary + 
  t_1 + 
  t_2 +
  t_3

m1 <- robust_summary(f1, df, cluster_var="district_name", time_var="date_minsk")

formula2 <- repression_binary ~ lag_log_num_msgs + 
  large_protest + 
  small_protest + 
  focal_day_3 + 
  lag_repression_binary
m2 <- robust_summary(formula2, df, cluster_var="district_name", time_var="date_minsk")

formula3 <- repression_binary ~ lag_log_num_msg_MA3 + 
  large_protest + 
  small_protest + 
  focal_day_3 + 
  lag_repression_binary
m3 <- robust_summary(formula3, df, cluster_var="district_name", time_var="date_minsk")

formula4 <- repression_binary ~ lag_log_num_msg_MA3 + 
  large_protest + 
  small_protest + 
  focal_day_3 + 
  region_protest + 
  country_protest + 
  lag_protest_rollSum5 + 
  lag_region_protest_rollSum5 + 
  lag_country_protest_rollSum5 + 
  lag_repression_binary
m4 <- robust_summary(formula4, df, cluster_var="district_name", time_var="date_minsk")


formula5 <- repression_binary ~ lag_log_num_msg_MA5 + 
  large_protest + 
  small_protest + 
  focal_day_3 + 
  lag_repression_binary
m5 <- robust_summary(formula5, df, cluster_var="district_name", time_var="date_minsk")


formula6 <- repression_binary ~ lag_log_num_msg_MA5 + 
  large_protest + 
  small_protest + 
  focal_day_3 +
  region_protest + 
  country_protest + 
  lag_protest_rollSum5 + 
  lag_region_protest_rollSum5 + 
  lag_country_protest_rollSum5 + 
  lag_repression_binary
m6 <- robust_summary(formula6, df, cluster_var="district_name", time_var="date_minsk")

# Logged Count of Repression DV
formula7 <- log(repression_count+1) ~ lag_log_num_msg_MA3 + 
  large_protest + 
  small_protest + 
  focal_day_3 + 
  region_protest + 
  country_protest + 
  lag_protest_rollSum5 + 
  lag_region_protest_rollSum5 + 
  lag_country_protest_rollSum5 +
  lag_log_repression_count
m7 <- robust_summary(formula7, df, cluster_var="district_name", time_var="date_minsk")

formula8 <- log(repression_count+1) ~ lag_log_num_msg_MA5 + 
  large_protest + 
  small_protest + 
  focal_day_3 + 
  region_protest + 
  country_protest + 
  lag_protest_rollSum5 + 
  lag_region_protest_rollSum5 + 
  lag_country_protest_rollSum5 +
  lag_log_repression_count
m8 <- robust_summary(formula8, df, cluster_var="district_name", time_var="date_minsk")


# Regression Table
covariate_labels = c("Log(Post Vol)$_{district, t-1}$",
                   "Log(3-day MA Post Vol)$_{district, t-1}$",
                   "Log(5-day MA Post Vol)$_{district, t-1}$",
                   "Large Protest$_{district, t}$",
                   "Small Protest$_{district, t}$",
                   "Focal Days (3 day window)$",
                   "Total Protests$_{region, t}$",
                   "Total Protests$_{country, t}$",
                   "Recent Protests$_{district}$",
                   "Recent Protests$_{region}$",
                   "Recent Protests$_{country}$",
                   "Binary DV$_{district, t-1}$",
                   "Log(Count DV)$_{district, t-1}$")

dep_var_labels = c("Binary", 
                   "Binary", 
                   "Binary", 
                   "Binary",
                   "Binary",
                   "Log(Count)",
                   "Log(Count)")


notes <- "All the models include district fixed effects with standard errors clustered at the district level. 
Post Vol = Volume of Telegram posts and these are logged and lagged.
MA=Moving Average.
Large Protest and Small Protest are binary indicators.
Large protests are defined as those where participants were greater than 1000.
Focal Days is a binary variable which is = 1 for Sunday and 2 days before it. 
Recent Protests = Total count of protests in the last 5 days.
"

star <- stargazer::stargazer(m2, m3, m4, m5, m6, m7, m8, 
                     covariate.labels = covariate_labels,
                     column.labels = dep_var_labels,
                     column.sep.width = "0pt",
                     dep.var.labels = "Repression_{t}", 
                     digits = 2,
                     font.size = "small",
                     type="latex",
                     notes =
                     #single.row = TRUE
                     )

note.latex <- notes
star[grepl("Note",star)] <- note.latex
cat (star, sep = "\n")


