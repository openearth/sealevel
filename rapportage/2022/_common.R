# example R options set globally

# chunk options set globally

require(acronymsdown)

knitr::opts_chunk$set(
  comment = "#>",
  collapse = TRUE,
  echo = FALSE,
  message = FALSE,
  warning = FALSE,
  out.width = "100%",
  fig.align='center',
  fig.width = 8,
  # cache = TRUE,
  cache.lazy = FALSE
)

screenshot.opts= list(delay = 5)


