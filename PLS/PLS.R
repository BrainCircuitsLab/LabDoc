library(PTCA4CATA)
library(TExPosition)
library(TInPosition)
library(data4PCCAR)
library(ExPosition)
library(InPosition)
library(ggplot2)
library(readxl)
library(psych)
# source("functions.R")
library(gridExtra)
library(ggplotify)
library(grid)
library(knitr)
library(pheatmap)

# Read the dataset
file_path <- "/Users/yilewang/workspaces/data4project/prediction_project/v2_prediction4tables/v3_table1.xlsx"
table <- as.data.frame(read_excel(file_path, sheet = "Amp1", skip = 1))
# exclude the last four columns
table <- table[, 1:(ncol(table) - 4)]
# reindex table
rownames(table) <- 1:nrow(table)
# groups definition
levels(table$group) <- c("SNC","NC","MCI","AD")

# manually setting color design
m.color.design <- as.matrix(colnames(table))
# Each block
ignition.table <- table[3:24]
m.color.design[3:24] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))
tvb_para.table <- table[25:29]
m.color.design[25:29] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))
# for regular main table
SimFreq.table <- table[30:37]
m.color.design[30:37] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))

##########################################
# the color of participants
ob.color.design <- as.matrix(rownames(table))
# ob.color.design[1:10] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))
# ob.color.design[11:23] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))

# ob.color.design <- as.matrix(rownames(table))
ob.color.design[1:10] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))
ob.color.design[11:26] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))
ob.color.design[27:61] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))
ob.color.design[62:74] <- prettyGraphsColorSelection(starting.color = sample(1:170, 1))


##########################################
start_col <- 3
end_col <- ncol(table)

# ALL
pls.data1 <- table[3:24]
pls.data2 <- table[25:37]

# SNC
# pls.data1 <- table[ 1:10 ,3:24]
# pls.data2 <- table[1:10, 25:37]

# NC
# pls.data1 <- table[ 11:26 ,3:24]
# pls.data2 <- table[11:26, 25:37]

# MCI
# pls.data1 <- table[ 27:61 ,3:24]
# pls.data2 <- table[27:61, 25:37]

# AD
# pls.data1 <- table[ 62:74 ,3:24]
# pls.data2 <- table[62:74, 25:37]

res.PLS <- tepPLS(DATA1 = pls.data1, 
                  scale1 = "SS1", 
                  center1 = FALSE, 
                  DATA2 = pls.data2, 
                  scale2 = "SS1",
                  center2 = FALSE, 
                  DESIGN = table$group, 
                  graphs = FALSE)

fii <- res.PLS$TExPosition.Data$fii
eigs <- res.PLS$TExPosition.Data$eigs
tau <- res.PLS$TExPosition.Data$t
fs <- res.PLS$TExPosition.Data$fi
cj <- res.PLS$TExPosition.Data$cj
ci <- res.PLS$TExPosition.Data$ci
fj <-res.PLS$TExPosition.Data$fj
lx <- res.PLS$TExPosition.Data$lx
ly <- res.PLS$TExPosition.Data$ly
p.pls <- res.PLS$TExPosition.Data$pdq$p
q.pls <- res.PLS$TExPosition.Data$pdq$q
t <- res.PLS$TExPosition.Data$t

hm.pls <- pheatmap(mat=cor(pls.data1, pls.data2), 
                   cluster_rows = FALSE, display_numbers = TRUE, 
                   cluster_cols = FALSE, breaks=seq(-0.7, 0.7, length.out=101))

nIter <- 1000
resPerm4PLSC <- perm4PLSC(pls.data1, pls.data2, nIter = nIter)

plot.scree(eigs, resPerm4PLSC$pEigenvalues)
eigs.permu <- resPerm4PLSC$permEigenvalues
plot.permutation(eigs.permu, eigs)

rownames(lx) <- table$caseid
rownames(ly) <- table$caseid
plot.lv(DESIGN=table$group, lx, ly, d=1)
