library(ggplot2)

# load the data
data <- data.frame(read.csv('../data/out.29.april.2013.csv', header=TRUE))

p <- ggplot(data, aes(ABV, sugar)) + geom_point(aes(colour=factor(pH)), alpha=0.7) + 
    facet_grid(. ~ pH, margins=F) + ggtitle('Drinks by pH level')
ggsave('../graphs/pHs.pdf', width=10, height=5, dpi=72)

p <- ggplot(data, aes(ABV, sugar)) + geom_point(aes(colour=factor(pH)), alpha=0.6) +
    ggtitle('Drinks by pH level')
ggsave('../graphs/ABV_sugar.pdf')
