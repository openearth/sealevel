require(tidyverse)
require(modelr)
require(ggfortify)
require(jsonlite)
config <- RcppTOML::parseToml("_common/configuration.TOML")

#== Read and prepare data ===================================================

readSeaLevelData <- function(url){
  readr::read_csv(url, comment = "#")
}

readMainStationInfo <- function() {
  jsonlite::read_json("..\\data\\deltares\\main_stations.json") %>%
  purrr::map_df(~ unlist(.[1:15]))
}

readMainStationLocations <- function(){
  read_delim("../data/psmsl/NLstations.csv", 
             delim = ";", escape_double = FALSE, trim_ws = TRUE)
}

addPreviousYearHeight <- function(df){
  df %>%
    dplyr::group_by(station) %>%
    dplyr::mutate(previousYearHeight = height[match(year - 1, year)]) %>%
    dplyr::filter(year > min(year)) %>%
    dplyr::ungroup()
}

addSurgeAnomaly = function(df){
  df %>%
    dplyr::mutate(surge_anomaly = - (`height - surge anomaly` - height))
}

addBreakPoints = function(df){
  df %>%
    dplyr::mutate(from1993 = (year >= 1993) * (year - 1993)) %>%
    dplyr::mutate(from1960_square = (year >= 1960) * (year - 1960) * (year - 1960))
}

selectCols <- function(df){
  df %>%
    tidyr::drop_na(station) %>%
    dplyr::select(
      year, 
      from1960_square,
      from1993,
      epoch,
      height,
      station = name_rws,
      surge_anomaly
    ) %>%
    dplyr::mutate(station = factor(station, levels = config$runparameters$station))
}

read_gtsm_nc <- function(nc = "c:\\Temp\\era5_reanalysis_surge_2023_v1_monthly_mean.nc", stations_selected){
  require(RNetCDF)
  ncf <- RNetCDF::open.nc(nc)
  
  data <- RNetCDF::read.nc(ncf)

  stations <- tibble::tibble(
    gtsmid = data$stations, 
    stationname = data$station_name,
    station_x_coordinate = data$station_x_coordinate,
    station_y_coordinate = data$station_y_coordinate
  )
  
  df <- reshape2::melt(data$surge, value.name = "surge_m") %>%
    dplyr::mutate(
      gtsmid = data$stations[Var2],
      month      = data$month[Var1]
    ) %>%
    dplyr::left_join(stations) %>%
    dplyr::select(-Var1, -Var2) %>%
    dplyr::filter(gtsmid %in% stations_selected)
  
  df
}


read_tidal_components_csv <- function(filesdir = "p:/11202493--systeemrap-grevelingen/1_data/Wadden/ddl/calculated/TA_filtersurge") {
  
  filelist <- list.files(filesdir, pattern = "csv", full.names = T)
  # get names of stations and year from filenames in filelistShort
  filelistShort <- list.files(filesdir, pattern = "csv", full.names = F)
  
  df <- lapply(filelist, function(x) read_csv(x, col_types = cols(), progress = FALSE))
  dfs <- dplyr::bind_rows(df)
  
  names <- tibble(name = str_replace(filelistShort, pattern = "_UTC\\+1.csv", replacement = "")) %>%
    tidyr::separate(name, c("station", "jaar", "component"), sep = "_") %>%
    dplyr::select(-component) %>%
    dplyr::left_join(mainstations_df[,c("ddl_id", "name")], by = c(station = "ddl_id"))
  
  names %>% 
    dplyr::mutate(jaar = as.integer(jaar)) %>%
    dplyr::mutate(data = df)
}



#==== NOT TESTED AT THE MOMENT, THIS IS A CONCEPT ==============

use_gtsm <- function(){
    wind_or_surge_type == "GTSM"
}


check_workflow_wind <- function(wind_or_surge_type){
  if(!wind_or_surge_type %in% config$runparameters$wind_or_surge_types) {
    cat("incorrect wind or surge specification")
  } else
  {
    if(use_gtsm()) {
      cat("Surge correction by GTSM is used")
    } else{
      cat("Wind correction ", wind_or_surge_type, " is used")
    }
  }
}

#==== Model functions ============================================

# linear_model <- function(df){
#     glm(
#       reformulate(
#         c(
#           ifelse(use_gtsm(), config$model_terms$surge_anomaly, config$model_terms$wind_anomaly),
#           config$model_terms$linear_time_term,
#           # config$model_terms$autocorrelation_term,
#           config$model_terms$nodal_term
#         ),
#         config$model_terms$response_term
#       ),
#       family = gaussian(link = "identity"),
#       data = df
#     )
# }

# linear_model <- function(df){
#   glm(
#     height ~ offset(surge_anomaly) + I(year - epoch) + I(cos(2 * pi * (year - epoch)/(18.613))) + I(sin(2 * pi * (year - epoch)/(18.613))),
#     data = df
#   )
# }


linear_model <- function(df){
  if(use_gtsm()){
    lm(
      height ~ offset(surge_anomaly) + 
        I(year - epoch) + 
        I(cos(2 * pi * (year - epoch)/(18.613))) + 
        I(sin(2 * pi * (year - epoch)/(18.613))),
      data = df
    )
  } else {
    lm(
      height ~ wind_anomaly + 
        I(year - epoch) + 
        I(cos(2 * pi * (year - epoch)/(18.613))) + 
        I(sin(2 * pi * (year - epoch)/(18.613))),
      data = df
    )
  }
}


broken_linear_model <- function(df){
  
  if(use_gtsm()){
    lm(
      height ~ offset(surge_anomaly) + 
        I(year - epoch) + 
        from1993 + 
        I(cos(2 * pi * (year - epoch)/(18.613))) + 
        I(sin(2 * pi * (year - epoch)/(18.613))),
      data = df
    )
    
  } else {
    lm(
      height ~ wind_anomaly +
        I(year - epoch) +
        from1993 +
        I(cos(2 * pi * (year - epoch)/(18.613))) +
        I(sin(2 * pi * (year - epoch)/(18.613))),
      data = df
    )
  }
}

## nog aanpassen, zoals hierboven

squared_model <- function(df){
  glm(
    reformulate(
      c(
        ifelse(use_gtsm(), config$model_terms$surge_anomaly, config$model_terms$wind_anomaly),
        config$model_terms$squared_time_term,
        config$model_terms$autocorrelation_term,
        config$model_terms$nodal_term
      ),
      config$model_terms$response_term
    ),
    family = gaussian(link = "identity"),
    data = df
  )
}

broken_squared_model <- function(df){
  glm(
    reformulate(
      c(
        ifelse(use_gtsm(), config$model_terms$surge_anomaly, config$model_terms$wind_anomaly),
        config$model_terms$linear_time_term,
        config$model_terms$broken_quadratic_time_term,
        config$model_terms$autocorrelation_term,
        config$model_terms$nodal_term
      ),
      config$model_terms$response_term
    ),
    family = gaussian(link = "identity"),
    data = df
  )
}


