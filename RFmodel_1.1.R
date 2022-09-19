rm(list=ls())
install.packages("pROC")
install.packages("tidyr")
library(tidyr)
library(plyr)
library(ggplot2)
library(pROC)
library(ISLR)
library(dplyr)
library(rpart)          
library(rpart.plot)
library(randomForest)
library(gbm)
library(MASS)
library(randomForest)
require(randomForest)
set.seed(1)

bank.additional.full <- read.csv("~/Downloads/bank-additional-full.csv", header=TRUE, sep=";")
head(bank.additional.full)
bank <- bank.additional.full[2:41189,]
lit.listy = which((bank.additional.full[,"y"]) == "no")
colnames(bank) <- c("age", "job", "marital", "education", "default","housing","loan","contact","month","day_of_week","duration","campaign","pdays","previous","poutcome","emp.var.rate","cons.price.idx","cons.conf.idx","euribor3m","nr.employed","y")
unknowns = which(apply(bank, 1, function(r) any(r %in% c("unknown"))))
bank <- bank[-unknowns,]

#shows that the unknowns are gone
#str(bank)

bank[,"y"]=ifelse(bank[,"y"]=="yes",1,0)

  #Change them all to NA for imputation
#bank[bank == "unknown"] <- NA

bank$y <- as.integer(bank$y)
bank$y <- as.factor(bank$y)
bank <- droplevels(bank)

# -- the mutations begin here

#str(bank)
# bank[,"default"]=ifelse(bank[,"default"]=="yes",1,0)
# bank[,"housing"]=ifelse(bank[,"housing"]=="yes",1,0)
# bank[,"loan"]=ifelse(bank[,"loan"]=="yes",1,0)

#bank = subset(bank, select=c(age,default,housing,loan,duration,campaign,pdays,previous,poutcome,emp.var.rate,cons.price.idx,cons.conf.idx,euribor3m,nr.employed,resp))

# bank = bank %>% mutate_if(is.factor, as.numeric)
#bank$default <- as.factor(bank$default)
#bank$housing <- as.factor(bank$housing)
#bank$loan <- as.factor(bank$loan)
#bank$poutcome <- as.factor(bank$poutcome)
#bank$y <- as.factor(bank$y)

  #no default housing or loan
  #leading imputation
#bank$resp <- as.numeric(bank$resp)
#bank.imputed <- rfImpute(NA ,resp ~ ., data = bank, iter=2)

# bank = bank %>% mutate_if(is.factor, as.numeric)
#sapply(bank,class)
# -- the mutations and cutouts end here

train <- sample(2:nrow(bank),0.4*nrow(bank))

rf.bank = randomForest(formula = y~., data = bank, ntree= 600 ,subset = train, mtry=6, importance=T)
rf.bank
importance(rf.bank)
#summary(rf.bank)
varImpPlot(rf.bank)
plot(rf.bank)

pred1 = predict(rf.bank, bank[-train,], type = "response", ordered = FALSE)
plot(pred1)
pred1 <- as.numeric(pred1)
confusionM = table(pred1, bank$y[-train])
plot(confusionM)
accuracy = (confusionM[1,1]+confusionM[2,2])/(sum(confusionM))
accuracy
the.roc = roc(response = bank$y[-train], predictor = pred1)
plot.roc(the.roc, axes = TRUE, legacy.axes = FALSE, print.auc=TRUE, auc.polygon=TRUE, max.auc.polygon=TRUE,auc.polygon.col="skyblue", print.thres=TRUE,main='RF2 ROC')
#print.auc=TRUE, auc.polygon=TRUE, grid=c(0.1, 0.2),grid.col=c("green", "red"), max.auc.polygon=TRUE,auc.polygon.col="skyblue", print.thres=TRUE,main='SVM ROC')
confusionM
?randomForest

rf.bank$test

bank[,"y"]=ifelse(bank[,"y"] == 0 ,1,0)
test.err1 = with(bank[-train,], mean( (y-pred1)^2 ))
test.err1

rf.bank$mse
oob.err = 0
test.err = 0
oob.err <- rf.bank$err.rate[nrow(rf.bank$err.rate),1]
oob.err


oob.err[(size-1)*mtry] = rf.bank$mse
pred = predict(rf.bank, bank[-train_boot,])
test.err = with(bank[-train,], mean( (y-pred1)^2 ))


