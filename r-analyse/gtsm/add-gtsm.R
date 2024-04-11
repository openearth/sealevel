require(jsonlite)
require(ncdf4)
require(tidyverse)
require(scales)

# todo:
# make more generic. 
# year as parameter
# update last years data
# write to generic file (no year in filename)

#== read station information =================================

mainstations <- jsonlite::read_json("..\\data\\deltares\\main_stations.json")
mainstations_df <- map_df(mainstations, ~ unlist(.[1:15])) %>%
  mutate(gtsm_id_2023 = as.numeric(gtsm_id_2023))

source("_common/functions.R")

selectedstations = mainstations_df$gtsm_id_2023

#===== read test NetCDF for 2023 =============================

gtsm_2024 <- read_gtsm_nc(
  nc = "c:\\Temp\\era5_reanalysis_surge_2023_v1_monthly_mean.nc", 
  stations_selected = selectedstations
  ) %>%
  arrange(gtsmid, month) %>%
  left_join(mainstations_df, by = c(gtsmid = "gtsm_id_2023"))

gtsm_2024 %>% distinct(id, gtsm_id, gtsmid, stationname, name)
range(gtsm_2024$month)
range(gtsm_2024$surge_m)

#========== visual checks ===============================

ggplot(gtsm_2024, aes(month, surge_m)) +
  geom_path(aes(color = name, group = name), size = 1, alpha = 1) +
  theme_minimal()
  
require(leaflet)
leaflet(gtsm_2024) %>%
  addTiles() %>%
  addCircleMarkers(
    lng = ~station_x_coordinate, 
    lat = ~station_y_coordinate, 
    label = ~name, 
    labelOptions = labelOptions(noHide = TRUE)
  )

#======== calculate yearly averages (weigthed) ===============================

gtsm_2024_monthly_add <- gtsm_2024 %>%
  mutate(
    t = as.Date(paste("2023", str_pad(as.character(month), 2, "left", "0"), "01", sep = "-")),
    psmsl_id = as.numeric(psmsl_id)
  ) %>% 
  select(
    t,
    name,
    psmsl_id,
    ddl_id,
    latitude = station_y_coordinate,
    longitude = station_x_coordinate,
    station_name = stationname,
    surge = surge_m
  )  %>%
  bind_rows(
    group_by(., t) %>%
      summarise(
        surge = mean(surge),
        latitude = 52.1551995,
        longitude = 5.3850577,
        station_name = "Dutch mean"
      ) %>%
      mutate(
        name = "NL",
        ddl_id = "NL"
      )
  )


gtsm_2024_annual_add <- gtsm_2024 %>% 
  mutate(
    date = as.Date(paste("2023", str_pad(as.character(month), 2, "left", "0"), "01", sep = "-")),
    year = year(date),
    daysInMonth = lubridate::days_in_month(date)
    ) %>% 
  group_by(name, ddl_id, gtsmid, year) %>%
  summarise(
    yearly_weighted_mean_surge_m = weighted.mean(surge_m, daysInMonth)
  ) %>%
  ungroup() %>%
  mutate(
    t = as.Date(paste(year, "01", "01", sep = "-"))
  ) %>%
  select(
    t,
    name,
    ddl_id,
    surge = yearly_weighted_mean_surge_m
  ) %>% 
  bind_rows(
      group_by(., t) %>%
      summarise(
        surge = mean(surge)
        ) %>%
      mutate(
        name = "NL",
        ddl_id = "NL"
      )
  )

#==== add to existing gtsm file =============================================

gtsm_2023_annual <- read_csv("../data/deltares/gtsm/gtsm_surge_annual_mean_main_stations_2023.csv")
gtsm_2023_monthly <- read_csv("../data/deltares/gtsm/gtsm_surge_monthly_mean_main_stations_2023.csv")

gtsm_2024_annual <- bind_rows(gtsm_2023_annual, gtsm_2024_annual_add)
gtsm_2024_monthly <- bind_rows(gtsm_2023_monthly, gtsm_2024_monthly_add)

#==== check =================================================================

gtsm_2024_annual %>%
  filter(name !="NL") %>%
  ggplot(aes(t, surge)) +
  geom_line(aes(color = name), linewidth = 1) +
  scale_x_date(breaks = scales::breaks_pretty(10), date_labels = "%Y")

save_file_name_annual <- "../data/deltares/gtsm/gtsm_surge_annual_mean_main_stations_2024.csv"
metadata_gtsm_2024_annual <- c("# generated with r-analyse/gtsm/add-gtsm.R", 
                                "# contains gtsm surge output per year")
# not implemented, but metadata can be added above the csv table
write_lines(
  metadata_gtsm_2024_annual, 
  save_file_name_annual, 
)
write.table(
  gtsm_2024_annual,
  save_file_name_annual, 
  append = T,
  sep = ","
)





gtsm_2024_monthly %>%
  filter(name !="NL") %>%
  ggplot(aes(t, surge)) +
  geom_line(aes(color = name), linewidth = 1) +
  scale_x_date(breaks = scales::breaks_pretty(20), minor_breaks = "1 year", date_labels = "%Y")

save_file_name_monthly <- "../data/deltares/gtsm/gtsm_surge_monthly_mean_main_stations_2024.csv"
metadata_gtsm_2024_monthly <- c("# generated with r-analyse/gtsm/add-gtsm.R", 
                               "# contains gtsm surge output per month")
# not implemented, but metadata can be added above the csv table
write_lines(
  metadata_gtsm_2024_monthly, 
  save_file_name_monthly, 
)
write.table(
  gtsm_2024_monthly,
  save_file_name_monthly, 
  append = T,
  sep = ","
)






