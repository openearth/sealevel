
# make outline document
require(mindr)

filelist <- list.files(pattern = ".Rmd")

filelist <- c("index.Rmd",
              "01-inleiding.Rmd",
              "06-methoden.Rmd",
              "07-resultaten.Rmd",
              "08-discussie.Rmd",
              "09-conclusies.Rmd",
              "10-references.Rmd",
              "11-appendix.Rmd",
              "04-toepassingen.Rmd",
              "05-metingen.Rmd",
              "03-oorzaken.Rmd")

text <- unlist(lapply(filelist, readLines))
writeLines(text = outline, con = "outline.md")
outline <- mindr::outline(text)


rmarkdown::render(
  input = "outline.md", 
  output_format = "word_document", 
  output_file = "outline.docx", 
    )

mm <- md2mm(
  from = text,
  root = "mindr",
  md_list = FALSE,
  md_braces = FALSE,
  md_bookdown = TRUE,
  md_eq = FALSE,
  md_maxlevel = ""
)

markmap(
  from = mm,
  root = NA,
  input_type = c("auto"),
  md_list = FALSE,
  md_eq = FALSE,
  md_braces = FALSE,
  md_bookdown = FALSE,
  md_maxlevel = "",
  dir_files = TRUE,
  dir_all = TRUE,
  dir_excluded = NA,
  widget_name = NA,
  widget_width = NULL,
  widget_height = NULL,
  widget_elementId = NULL,
  widget_options = markmapOption(preset = "colorful")
)
