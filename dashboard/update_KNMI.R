
# read and extract projection data. 
# This version of the data is corrected for reference period
# see 

require(tidync)
require(tidyverse)

datadir <- "../../data/knmi/knmi21/"
list.files(datadir)

# run below code when updating data
# if (updateData) {
scen = c("ssp126", "ssp245", "ssp585")
# scen = scen[1]
scenarios <- list()
for(scen in scen){
  con <- file.path(datadir, paste0("SeaLevelPerc_KNMIsignal_BiasCorr_NoWind_",scen,".nc"))
  df <- tidync::tidync(con, "perc_ts") %>% hyper_tibble()
  scenarios[[scen]] <- df
  rm(df)
}

knmi_df <- data.table::rbindlist(scenarios, use.names = TRUE, idcol = "scenario") %>%
  mutate(perc_ts = perc_ts)                        # everything in mm
rm(scenarios)

save(knmi_df, file =  file.path("../../data/knmi/knmi21", "knmi_df21.Rdata"))
knmi_df %>%
  filter(percentiles %in% c(5, 50, 95)) %>%
  write_csv(file = file.path("../../data/knmi/knmi21", "knmi_21_5_50_95.csv"))
# }





datadir <- "../../data/knmi/knmi22/projections_all_contrib"
list.files(datadir)

# run below code when updating data
# if (updateData) {
  scen = c("ssp126", "ssp245", "ssp585")
  # scen = scen[1]
  scenarios <- list()
  for(scen in scen){
    con <- file.path(datadir, paste0("KNMIsignal_BiasCorr_NoWind_",scen,"_ref_1995_2014.nc"))
    df <- tidync::tidync(con, "perc_ts") %>% hyper_tibble()
    scenarios[[scen]] <- df
    rm(df)
  }
  
  knmi_df <- data.table::rbindlist(scenarios, use.names = TRUE, idcol = "scenario") %>%
    mutate(perc_ts = perc_ts)                        # everything in mm
  rm(scenarios)
  
  save(knmi_df, file =  file.path("../../data/knmi/knmi22", "knmi_df22.Rdata"))
  knmi_df %>%
    filter(percentiles %in% c(5, 50, 95)) %>%
  write_csv(file = file.path("../../data/knmi/knmi22", "knmi_22_5_50_95.csv"))
# }


