library(GGally)
library(ggplot2)#library("ggplot2", lib.loc="~/R/win-library/3.4")
library(reshape)
#library(devtools)
#install_github("ggbiplot", "vqv")
library(ggfortify)
library(ggbiplot)
library(factoextra)

#detach("package:ggbiplot", unload=TRUE)
#library(ggbiplot)

#Reading data
data<-read.csv("data/Data_beats.csv",header=TRUE,sep=",")
rownames(data)<-data$Beat
data=data[,2:length(data[1,])]
data[is.na(data)]<-0

#Perform PCA
data.pca<-prcomp(data,center=TRUE,scale. = TRUE)
#Loadings(Rotation) for each variable.
#From these we can check which original variables influence the most in each PC(principal component)
#Usually, we are interested in PC1 and PC2
#5 most positive and 5 most negatives for each PC
print(data.pca)

#Plot of variances associated with each PC
plot(data.pca,type="l")

#Importance of components (how much variance is explained by each component)
summary(data.pca)


#Plotting only observations
autoplot(data.pca)+
  labs(title="Observations factor map")+
  theme(plot.title = element_text(hjust = 0.5)) #Center title

#Plotting only variables
g3 <- ggbiplot(data.pca, obs.scale = 1, var.scale = 1, alpha=0, 
               circle = TRUE, varname.size = 4)+
  theme(legend.direction = 'horizontal', 
        legend.position = 'top')+
 # xlim(-5,5)+
  labs(title="Variables factor map")+
  theme(plot.title = element_text(hjust = 0.5)) #Center title
print(g3)






#Biplot ()
g4 <- ggbiplot(data.pca, obs.scale = 1, var.scale = 1, ellipse = TRUE, 
               circle = FALSE,varname.size = 4)+
  scale_color_discrete(name = '')+
  theme(legend.direction = 'horizontal', 
        legend.position = 'top')+
  #xlim(-5.5,10)+ylim(-4.5,4)+
  labs(title="Biplot of variables and observations")+
  theme(plot.title = element_text(hjust = 0.5)) #Center title
print(g4)

#Saving observations projected into PC1 and PC2
proj_data<-data.pca$x[,1:3]
rownames(proj_data)<-rownames(data)

#Determining The Optimal Number Of Clusters
#Elbow, Silhouhette and Gap statistic methods
# Elbow method
fviz_nbclust(proj_data, kmeans, method = "wss") +
  #geom_vline(xintercept = 3, linetype = 2)+
  labs(subtitle = "Elbow method")
# Silhouette method
fviz_nbclust(proj_data, kmeans, method = "silhouette")+
  labs(subtitle = "Silhouette method")
# Gap statistic
# nboot = 50 to keep the function speedy. 
# recommended value: nboot= 500 for your analysis.
# Use verbose = FALSE to hide computing progression.
set.seed(123)
fviz_nbclust(proj_data, kmeans, nstart = 25,  method = "gap_stat", nboot = 50)+
  labs(subtitle = "Gap statistic method")

autoplot(kmeans(proj_data, centers=4,iter.max=100), data = proj_data,label=TRUE)+
  labs(title="Observations factor map colored by cluster \n( kmeans, k = 7 )")+
  theme(plot.title = element_text(hjust = 0.5))#+ #Center title
  #xlim(-0.3,0.6)

cluster3d_4=kmeans(proj_data, centers=4,iter.max=100)
cluster3d_4=cluster3d_4$cluster

#3D plots
library(rgl)
plot3d(data.pca$x[,1:3],col=cluster3d_4)
text3d(data.pca$x[,1:3],texts=toString(rownames(data.pca)))
plot3d(data.pca$rotation[,1:3])
text3d(data.pca$rotation[,1:3], texts=rownames(data.pca$rotation), col="red")
coords <- NULL
for (i in 1:nrow(data.pca$rotation)) {
  coords <- rbind(coords, rbind(c(0,0,0),data.pca$rotation[i,1:3]))
}
lines3d(coords, col="red", lwd=4)


#DBSCAN clustering
library(dbscan)
kNNdistplot(proj_data, k = 4)
abline(h=1.5, col = "red", lty=2)
clusters_dbscan <- dbscan(proj_data, eps = 1.5, minPts = 5)
pairs(proj_data,col=clusters_dbscan$cluster+1L)



