require(MASS)
library(caTools)
library(datasets)
str(iris)
set.seed(1)
subset(iris, Species == "versicolor")[1:50,]
subset(iris, Species == "virginica")[1:50,]
versicolor <- subset(iris, Species == "versicolor")
virginica <- subset(iris, Species == "virginica")
new_iris = rbind(versicolor, virginica)
versicolor_test <- versicolor[1:10,1:4]
virginica_test <- virginica[1:10,1:4]
versicolor_training <- versicolor[11:50,1:4]
virginica_training <- virginica[11:50,1:4]
as.factor(new_iris$Sepal.Length)
as.factor(new_iris$Sepal.Width)

summary(versicolor_training)
summary(virginica_training)
rA <- lda(formula = Species ~ ., data = new_iris)
rB <- lda(Species ~ ., data = new_iris, subset = {versicolor_training$virginica_training})
train = c(51:60,101:110)
plda = predict(object = rA, newdata = new_iris[-train,])
confusionMatrix(plda,versicolor_training$virgininca_training)

new_iris$large = ifelse(new_iris$Petal.Length >= 4.7, 1, 0)
glm.fit <- glm(large ~ Sepal.Width + Sepal.Length, data = new_iris, family = binomial(link="logit"))
summary(glm.fit)

new_iris$large = ifelse(new_iris$Petal.Length >= 4.7, 1, 0)
glm.fit <- glm(large ~ Sepal.Length, data = new_iris, family = binomial)
summary(glm.fit)


