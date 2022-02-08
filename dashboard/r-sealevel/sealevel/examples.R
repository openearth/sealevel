
library(readr)
library(dplyr)

url <- "~/src/sealevel/data/deltares/results/dutch-sea-level-monitor-export-2020-11-25.csv"

deltares_df <- read_csv(url, comment = "#")

url <- "~/src/sealevel/data/knmi/cmip5/SeaLevelPerc_KNMI14.csv"

knmi_df <- read_csv(url, comment = "#")



ggplot() + geom_line(data=knmi_median_df, mapping=aes(time, perc_ts, colour=scenario))

# merge with percentiles
knmi_perc10_df <- knmi_df %>% filter(percentiles==10) %>% select(time, scenario, proc, perc_ts) %>%  rename(perc_ts_10=perc_ts)
knmi_perc50_df <- knmi_df %>% filter(percentiles==50) %>% select(time, scenario, proc, perc_ts) %>%  rename(perc_ts_50=perc_ts)
knmi_perc90_df <- knmi_df %>% filter(percentiles==90) %>% select(time, scenario, proc, perc_ts) %>%  rename(perc_ts_90=perc_ts)
knmi_perc_df <- merge(merge(knmi_perc10_df, knmi_perc50_df), knmi_perc90_df) %>% filter(proc=="Total")

fig <- (ggplot() 
  + geom_line(data=knmi_perc_df, mapping=aes(time, perc_ts_50, colour=scenario)) 
  + geom_ribbon(data=knmi_perc_df, mapping=aes(x=time, ymin=perc_ts_10, ymax=perc_ts_90, colour=scenario, fill=scenario), alpha=0.1)
)
