
rmarkdown::render(
  "sealevelmonitor.Rmd", 
  params = list(
    wind_or_surge_type = "GTSM",
    station = c( "Netherlands (without Delfzijl)"),
    modeltype = "linear"
  )
)

