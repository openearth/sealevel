
# from config TOML

config <- RcppTOML::parseToml("_common/configuration.TOML")

rmarkdown::render(
  "sealevelmonitor.Rmd", 
  params = list(
    wind_or_surge_type = config$runparameters$wind_or_surge_types,
    station = config$runparameters$stations,
    modeltype = config$runparameters$modeltypes
  )
)


# User defined
rmarkdown::render(
  "sealevelmonitor.Rmd", 
  params = list(
    wind_or_surge_type = "GTSM",
    station = c( "Vlissingen"),
    modeltype = "linear"
  )
)

