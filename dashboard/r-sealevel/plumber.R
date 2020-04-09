#
# This is a Plumber API. You can run the API by clicking
# the 'Run API' button above.
#
# Find out more about building APIs with Plumber here:
#
#    https://www.rplumber.io/
#

library(plumber)
library(ggplot2)

# Read the sealevel dataset 
library(readr)
sealevel <- read_csv("dutch-sea-level-monitor-export-2019-09-29.csv", 
                     comment = "#")

#* @apiTitle Plumber Example API

#* Echo back the input
#* @param msg The message to echo
#* @get /echo
function(msg = "") {
    list(msg = paste0("The message is: '", msg, "'"))
}

#* Plot a histogram
#* @png
#* @get /plot
function() {
    rand <- rnorm(100)
    hist(rand)
}

#* Return the sum of two numbers
#* @param a The first number to add
#* @param b The second number to add
#* @serializer unboxedJSON
#* @post /sum
function(a, b) {
    list(result=as.numeric(a) + as.numeric(b))
}


#* Return a plot of all sea-level measurements
#* @png
#* @get /chart
function() {
  fig <- ggplot(sealevel, aes(year, height)) + geom_point() 
  fig <- fig + geom_smooth()
  # you need to print it, to return it.
  print(fig)
}

#* Return  the sea-level trend
#* @serializer unboxedJSON
#* @post /fit
function() {
  fit <- lm(height ~ year + 1,  sealevel)
  fit$coefficients
}

#* Return a broken linear trend
#* @serializer unboxedJSON
#* @param breakpoint The year of the breakpoint
#* @post /fit/break
function(breakpoint) {
  breakpoint <- as.numeric(breakpoint)
  # compute a covariate for the trend after the breakpoint
  covariate <- (sealevel$year > breakpoint)*(sealevel$year - breakpoint)
  fit <- lm(height ~ year + covariate + 1,  sealevel)
  fit$coefficients
}

