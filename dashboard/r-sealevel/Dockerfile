FROM trestletech/plumber
MAINTAINER Fedor Baart <fedor.baart@deltares.nl>
RUN R -e 'install.packages(c("ggplot2", "readr"))'
WORKDIR /app
CMD ["/app/plumber.R"]
