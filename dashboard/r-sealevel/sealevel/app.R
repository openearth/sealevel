#
# This is a Shiny web application. You can run the application by clicking
# the 'Run App' button above.
#
# Find out more about building applications with Shiny here:
#
#    http://shiny.rstudio.com/
#

library(shiny)

library(ggplot2)

# Read the sealevel dataset 
library(readr)
sealevel <- read_csv("../dutch-sea-level-monitor-export-2019-09-29.csv", 
                     comment = "#")


# Define UI for application that draws a histogram
ui <- fluidPage(

    # Application title
    titlePanel("Sea-level data"),

    # Sidebar with a slider input for number of bins 
    sidebarLayout(
        sidebarPanel(
            sliderInput("span",
                        "Span:",
                        min = 0.01,
                        max = 1,
                        value = 0.5),
            sliderInput("breakpoint",
                        "Break:",
                        min = 1950,
                        max = 1995,
                        value = 1970)
        ),

        # Show a plot of the generated distribution
        mainPanel(
           plotOutput("trendPlot"),
           plotOutput("breakPlot")
        )
    )
)

# Define server logic required to draw a histogram
server <- function(input, output) {

    output$trendPlot <- renderPlot({
        # generate span based on input
        span <- input$span

        # draw the histogram with the specified number of bins
        fig <- ggplot(sealevel, aes(year, height)) + geom_point() + geom_smooth(span=span)
        print(fig)
    })
    output$breakPlot <- renderPlot({
        # generate breakpoint from ui.R
        breakpoint <- input$breakpoint
        
        covariate <- (sealevel$year > breakpoint)*(sealevel$year - breakpoint)
        
        # draw the histogram with the specified number of bins
        broken <- geom_smooth(method="glm", n=nrow(sealevel), formula=y ~ x + covariate +  1)
        linear <- geom_smooth(method="glm", n=nrow(sealevel), formula=y ~ x + 1, aes(colour='red')) 
        fig <- ggplot(sealevel, aes(year, height)) + geom_point() + broken + linear
        print(fig)
    })    
}

# Run the application 
shinyApp(ui = ui, server = server)
