require(tidyverse)
require(modelr)
require(ggfortify)


readSeaLevelData <- function(url){
  read_csv(url, comment = "#")
}

addPreviousYearHeight <- function(df){
  df %>%
    group_by(station) %>%
    mutate(previousYearHeight = height[match(year - 1, year)]) %>%
    filter(year > min(year)) %>%
    ungroup()
}

addSurgeAnomaly = function(df){
  df %>%
    mutate(`surge anomaly` = `height - surge anomaly` - height)
}

addBreakPoints = function(df){
  df %>%
    mutate(from1993 = (year >= 1993) * (year - 1993)) %>%
    mutate(from1960_square = (year >= 1960) * (year - 1960) * (year - 1960))
}

selectCols <- function(df){
  df %>%
    drop_na(station) %>%
    select(
      year, 
      from1960_square,
      from1993,
      previousYearHeight,
      height,
      station = name_rws,
      `surge anomaly`
    )
}

linear_model <- function(df){
  lm(
    reformulate(
      c(
        config$model_terms$surge_anomaly,
        config$model_terms$linear_time_term,
        config$model_terms$autocorrelation_term,
        config$model_terms$nodal_term
      ),
      config$model_terms$response_term
    ),
    data = df
  )
}

broken_linear_model <- function(df){
  lm(
    reformulate(
      c(
        config$model_terms$surge_anomaly,
        config$model_terms$linear_time_term,
        config$model_terms$broken_linear_time_term,
        config$model_terms$autocorrelation_term,
        config$model_terms$nodal_term
      ),
      config$model_terms$ response_term
    ),
    data = df
  )
}

squared_model <- function(df){
  lm(
    reformulate(
      c(
        config$model_terms$surge_anomaly,
        config$model_terms$squared_time_term,
        config$model_terms$autocorrelation_term,
        config$model_terms$nodal_term
      ),
      config$model_terms$response_term
    ),
    data = df
  )
}

broken_squared_model <- function(df){
  lm(
    reformulate(
      c(
        config$model_terms$surge_anomaly,
        config$model_terms$linear_time_term,
        config$model_terms$broken_quadratic_time_term,
        config$model_terms$autocorrelation_term,
        config$model_terms$nodal_term
      ),
      config$model_terms$response_term
    ),
    data = df
  )
}

