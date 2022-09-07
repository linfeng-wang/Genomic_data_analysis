library(tidyverse)
library(tmap)    # for static and interactive maps
library(jsonlite)
install.packages("jsonlite")
library(leaflet) # for interactive maps

data()
BOD


ggplot(data = BOD, mapping = aes(x = time, y= demand )) + geom_point()
