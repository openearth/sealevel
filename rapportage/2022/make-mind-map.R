
# make outline document
require(mindr)

filelist <- list.files(pattern = ".Rmd")

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
