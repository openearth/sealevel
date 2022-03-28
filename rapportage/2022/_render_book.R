## rendering naar een of meerdere van de onderstaande formats

# recommended latex distribution
# install.packages("tinytex")
# tinytex::install_tinytex()  # install TinyTeX

require(rmarkdown)
require(bookdown)

file.remove("_main.Rmd")
file.remove("_main.md")

# Fedors bibliography synchroniseren wanneer nodig.
# download.file("https://raw.githubusercontent.com/SiggyF/bibliography/master/bibliography.bib", destfile = "bib/bibliography.bib")
# # convert refs
# require(RefManageR)
# refs <- RefManageR::ReadBib("bib/bibliography.bib", .Encoding = 'utf-8', check = 'error')
# RefManageR::WriteBib(refs, file = "bib/bibliography_adapted.bib", biblatex = T)
# 


# gitbook formatted html pages (gebruikt op testpagina)

bookdown::render_book(file.path("index.Rmd"), output_dir = "docs",
                      output_format = NULL, 
                      new_session = F)

# standard pdf
# options(tinytex.verbose = TRUE)
# file.remove("_main.md")
# bookdown::render_book("index.Rmd", output_format = bookdown::pdf_book(),
#                       new_session = T, clean_envir = T)

# Veel voorkomende fouten
# Figuurlabels (label in code block) mogen geen underscore (_) bevatten bij rendering naar pdf
# Dubbele labels mogen niet (door hele document, alle hoofdstukken)
# Tufte output laat maar 2 niveau's toe (chapters # en sections ##)
# gebruik geen \\ als directory afscheiding. Gaat niet goed van latex naar pdf