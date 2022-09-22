library(tidyverse)
library(languageserver)
library(httpgd)
library(tmap)    # for static and interactive maps
library(jsonlite)
library(leaflet) # for interactive maps
Sys.setenv("DISPLAY"=":0.0")
Sys.getenv(c("DISPLAY"))

cars <- c(1, 3, 6, 4, 9)
plot(cars)


print(cars)

ggplot(cars, aes(x=cars, y=cars))+geom_point()

data <- data.frame(x=rnorm(30))
 
# Basic plot with title
ggplot( data=data, aes(x=x)) + 
  geom_histogram(fill="skyblue", alpha=0.5, bins=10) +
  ggtitle("A blue Histogram") +
  theme_minimal()

head(iris)

ggplot(iris, aes(x=Sepal.Length, y=Sepal.Width)) + 
    geom_point()
