Missing body measurements prediction 
in fashion industry: a comparative approach
Philippe Meyer1  , Babiga Birregah1, Pierre Beauseroy1, Edith Grall1 and Audrey Lauxerrois2 
Introduction
In the design of clothing, many measurements of the human body are required to obtain 
garments adapted to human morphologies. Some of these dimensions, such as the 
height or the waist girth, are said to be easy-to-measure since it is possible to get them 
easily oneself with a tape measure by finding the associated key body points. However, 
other dimensions are difficult to obtain without the help of a professional stylist. Among 
them we can cite for example the back width and length which are requested to the man -
ufacture of men’s shirts. Moreover, even with a professional measurement, we can find 
ourselves faced with errors due to the variability of measurements between stylists.Abstract 
The use of artificial intelligence to predict body dimensions rather than measuring 
them by stylists or 3D scanners permits to obtain easily all measurements of individual 
consumers and can consequently reduce costs of population survey campaigns. In 
this paper, we have compared several models of machine learning to predict about 30 
measurements used in fashion industry to construct clothes from 6 easy-to-measure 
body dimensions and demographic information. The four types of models we have 
studied are linear regressions, random forests, gradient boosting trees and support 
vector regressions. To construct and train them we have used anthropometric meas-
urements of 9000 adult individuals of the French population collected by the French 
Institute of Textiles and Clothing (IFTH) during a national measurement campaign col-
lected between 2003 and 2005. We have analyzed the model prediction performance 
in terms of individual and global predictions as well as the effect of the training dataset 
size and the importance of the input features. The linear and the support vector regres-
sions have given the best results with respect to evaluation metrics, predicted distribu-
tions and have required less training data than tree-based models. It turns out that the 
weight and height have been the most important input features for the models 
considered while the hip girth has been the less important among the input measure -
ments. Since the set of body dimensions used in fashion industry and the morphol-
ogy depend on the gender, we have decided to treat men and women separately 
and to compare them.
Keywords: Artificial intelligence, Machine learning, Fashion and apparel industry, 
Anthropometric measurement, Sizing systemOpen Access
© The Author(s) 2023. Open Access  This article is licensed under a Creative Commons Attribution 4.0 International License, which permits 
use, sharing, adaptation, distribution and reproduction in any medium or format, as long as you give appropriate credit to the original 
author(s) and the source, provide a link to the Creative Commons licence, and indicate if changes were made. The images or other third 
party material in this article are included in the article’s Creative Commons licence, unless indicated otherwise in a credit line to the mate -
rial. If material is not included in the article’s Creative Commons licence and your intended use is not permitted by statutory regulation or 
exceeds the permitted use, you will need to obtain permission directly from the copyright holder. To view a copy of this licence, visit http://  
creat iveco mmons. org/ licen ses/ by/4. 0/.RESEARCHMeyer  et al. Fashion and Textiles           (2023) 10:37  
https://doi.org/10.1186/s40691-023-00357-5Fashion and Textiles
Correspondence:   
philippe.meyer@utt.fr
1 Computer Science and Digital 
Society Laboratory (LIST3N), 
Université de Technologie de 
Troyes, Troyes, France
2 French Institute of Textiles 
and Clothing, Troyes, France

Page 2 of 17 Meyer et al. Fashion and Textiles           (2023) 10:37 
The 3D scanning devices have been used by the textile industry to minimize errors 
with manual measurements and to reduce their acquisition time. In general, 3D scan -
ning model the human body in the form of a mesh made up of points and triangles. 
Software such as Anthroscan from Human Solutions or 3D Measurement Software from 
ProtoTech Solutions permit to extract up to 200 measurements of the human body from 
a mesh. This extraction is usually performed by using computational geometry together 
with landmarks placed on the subject body before the acquisition (Lu and Wang 2008) 
or more recently with deep learning-based methods (Kaashki et al. 2021). For a compre -
hensive survey about 3D scanning technologies and the associated processing stages one 
can read (Bartol et al. 2021).
On the other hand, Smartphone scanning applications have been developed in order 
to extract measurements. The principle is to position the device in front of the person so 
that the phone camera collects pictures of the individual for the extraction. The technol -
ogies generally involved use computer vision, plane geometry (Hung et al. 2004), artifi -
cial intelligence (Ashmawi et al. 2019; de Souza et al. 2020) and permit the user to obtain 
its body measurements in a limited number.
The ever-increasing development of artificial intelligence in recent years has allowed 
its application to many fields of the fashion and apparel industry. These methods include 
machine learning, decision support system, expert system, optimization, image recogni -
tion and vision and have given interesting results to the apparel manufacturing, apparel 
design, distribution and fabric production. Exhaustive reviews of the impact of these 
techniques to this specific range of applications can be consulted in Guo et al. (2011) and 
Giri et al. (2019).
The aim of this paper is to apply artificial intelligence methods to facilitate the extrac -
tion of measurements and to accurately predict full-body anthropometric measurements 
from a subset of easy-to-measure dimensions. Our approach is particularly interest -
ing to allow all measurements of individual consumers to be obtained from measure -
ments taken by themselves as well as to consequently reduce costs of population survey 
campaigns.
The extraction of the individual customer body dimensions is helpful nowadays where 
the internet shopping for clothes has become increasingly popular, especially since the 
pandemic crisis. In practice, the user can measure some of its body dimensions and 
deduce all of them with the help of artificial intelligence. Thus, he can buy on online 
clothing stores by filling in the measures in order to obtain clothes adapted as best as 
possible to its morphology.
On the other hand, since there is a substantial variation in body measurements 
between people, the usual method to provide accurate sizing charts of a population for 
the garment pattern making is to survey a representative sample of the target popula -
tion. These surveys generally include general information about the clothing habits and 
the demographic characteristics of the individual surveyed together with the measure of 
its body sizes by stylists or by scanning them with 3D scanning devices. The implemen -
tation of such campaigns can therefore require many professionals as well as advanced 
technology deployed across a territory or a country and is consequently very expensive. 
Thus, the prediction of full-body anthropometric measurements can help to reduce sig -
nificantly the complexity of the process of the survey and its costs. The idea is to collect 

Page 3 of 17
 Meyer et al. Fashion and Textiles           (2023) 10:37 
 
only some of the easy-to-measure key body dimensions and recover all of them with 
artificial intelligence. In these conditions, the survey can be conducted online where 
respondents measure themselves with a tape or a scanning application even in pandemic 
situations.
In this paper, we have used and compared different machine learning models to deduce 
all the necessary body dimensions for making all type of clothing (36 for women, 31 for 
men) from 6 easy-to-measure body dimensions, such as the height or the waist girth and 
demographic information. The machine learning models we have used are linear regres -
sions, random forests, gradient boosting trees and support vector regressions. We have 
computed and compared their accuracies in terms of individual and global predictions. 
Moreover, we have studied the influence of the training dataset size and the importance 
of the input features in the model performance. To train and test our methods, we have 
used a database of 9000 adult individuals surveyed by French Institute of Textiles and 
Clothing (IFTH) during a national measurement campaign between 2003 and 2005 with 
the help of 3D scanning device from Human Solutions coupled with Anthroscan and 
professional stylists.
The paper is organized as follows. In “ General scheme” section we present the gen -
eral scheme of our work. The dataset and its preprocessing are presented in “ Anthropo -
metric data and preprocessing ” section and the models, their evaluation metrics and the 
associated hyperparameters tuning in “Models, evaluation metrics and hyperparameters 
tuning ” section. The “Results” section reports the results about the comparison of the 
performance of the models, the influence of the training dataset size and the importance 
of the input features. We discuss and interpret these results in “Discussion ” and we con -
clude in “ Conclusion ” section.
The estimation of body measurements is intrinsically related to the study of propor -
tions of the human body and is not only a problem considered within the framework of 
the textile industry. The beginnings of this old subject can be found in the work of the 
roman architect of the first century BC Vitruvius in the first chapter titled “On Sym -
metry: In Temples And In The Human Body” of the book III of its treatise “De Archi -
tectura” and its considerable influence on the architects and artists of the Renaissance.
The first modern statistical studies in this direction have been made by Rollet in 
1892 (Rollet 1892) and Pearson in 1899 (Pearson 1899) by the estimation of the human 
height from its long bone lengths. This question also arises in the health sector and 
has been particularly studied for the health of elderly people, where the measurements 
can become difficult to measure because of the position required or the deformations 
of the skeleton. Chumea and other researchers have used several linear regressions to 
predict the height and/or the weight from the easy-to-measure knee height in Chumlea 
et al. (1985) or Chumlea and Guo (1992) using the National Health Examination Survey 
(NHES) database (Gordon and Miller 1964).
Afterward, the development of artificial intelligence encouraged many researchers 
to apply machine learning models to this problem. The analysis of correlation of body 
dimensions shows that there are important linear dependencies between them. Thus, 
in the literature, several studies have been conducted using linear machine learning 
models. For example in Indah et al. (2016), Indah et al. estimated 35 measurements 
of a small dataset of 45 elderly Javanese from age and body mass index by linear 

Page 4 of 17 Meyer et al. Fashion and Textiles           (2023) 10:37 
regression models. The sex, height, weight and foot size have been predicted from 
22 hand related features from linear and logistic regression by Miguel-Hurtado et al. 
(2016).
The ever-increasing interest of the application of deep learning in industrial prob -
lems led to several research studies applying artificial neural networks to apparel 
industry problems. Liu et al. (2017) exposed that back propagation neural networks 
is accurate and stable in the prediction of 10 lower body dimensions from the height, 
hip and waist girths. Wang et al. (2019) showed that this type of neural network can 
be outperformed by radial basis function artificial neural networks. They deduced 8 
measurements from 4 easy-to-measure dimensions and studied the effect of the vol -
ume of the training dataset initially composed of 180 samples. In Wang et al. (2021), 
generalized regression neural networks have been used to predict 76 body measure -
ments from 7 easy-to-measure dimensions with the Anthropometric Survey of US 
Army Personnel (ANSUR) II dataset (Gordon et al. 2014).
In order to take into account linear and non-linear aspects of body dimensions, Liu 
et al. (2014) used a combination of multiple linear regression and radial basis function 
network models to predict 60 body dimensions from 8 feature parameters. Similarly 
(Chan et al. 2005; AP et al. 2003) studied the relationship between men’s tailor-made 
shirt pattern parameters and body parameters with multiple linear regression and 
artificial neural networks. Rativa et  al. (2018) compared several machine learning 
regression models (support vector regression, Gaussian process and artificial neu -
ral network) to estimate the height and the weight from different groups of anthro -
pometric measurements on the National Health and Nutrition Examination Survey 
(NHANES) III (NCHS 1994) and the ANSUR datasets (Gordon et al. 1989).
Methods
In this section we explain our approach to estimate body dimensions from a set of 
easy-to-measure measurements.
General scheme
The institute IFTH has identified in collaboration with several modelers 36 (respectively 
31) measurements for women (respectively men) that are needed for garment pattern 
making. These measurements are given in Table  1 together with precision steps and 
associated units. The precision step of a measurement is defined as the acceptable error 
in measuring a measurement by a professional stylist. Among them, we have chosen 
the six key easy-to-measure body dimensions which are the height, weight, chest/bust, 
waist and hip girths and inside leg length as input features, see Fig.  1. They have the 
particularity that they can be measured alone with a tape measure or with a scan appli -
cation installed on a Smartphone. Additionally to these dimensions, we have included 
two demographic information, the age and the socioprofessional category, and the shoe 
size of the individual. Then, four types of machine learning algorithms have been trained 
and tested on a dataset of a French national measurement campaign to predict the 30 
(respectively 25) remaining measurements for women (respectively men).

Page 5 of 17
 Meyer et al. Fashion and Textiles           (2023) 10:37 
 
Anthropometric data and preprocessing
In this paper we have used a dataset composed of individuals of the French popula -
tion collected by the institute IFTH in a national measurement campaign between 
2003 and 2005 by using 3D scanners. Each person is thus represented by standing and 
sitting meshes composed of around 400k vertices and 800k triangles. The software 
Anthroscan has been used to extract around 90 body measurements for each position. 
Hence, about 180 measurements have been collected per individual together with Table 1 Measurements used in fashion industry according to the modelers of the French Institute 
of Textiles and Clothing (IFTH)
Measurements used in fashion industry for men and women Precision step Unit
Chest/bust girth 1 cm
Waist girth 1 cm
High hip girth 1 cm
Hip girth 1 cm
Thigh girth 0.5 cm
Knee girth 0.5 cm
Calf girth 0.5 cm
Ankle girth 0.5 cm
Chest/bust width 0.5 cm
Back width 0.5 cm
Head girth 0.5 cm
Neck girth 0.5 cm
Neck base girth (suprasternal) 0.5 cm
Upper arm girth 0.5 cm
Wrist girth 0.5 cm
Shoulder length (acromia—7th cervical vertebra) 1 cm
Length of scye 1 cm
Body rise 1 cm
Back length (7th cervical-waist) 1 cm
Left shoulder slope (acromiale-neck base) 1 cm
Waist height 1 cm
7th cervical height 1 cm
Inside leg length 1 cm
Waist-knee height 1 cm
Knee-ground height 1 cm
Left arm length (acromia-wrist) 1 cm
Head height (vertex-7th cervical) 1 cm
Front lower trunk length 1 cm
Back lower trunk length 1 cm
Height 1 cm
Weight 1 kg
Additional measurements used in fashion industry for women Precision step Unit
Underbust girth 1 cm
Bustpoint length (neck base-bustpoint) 1 cm
Bustpoint-waist length 1 cm
Bustpoints breadth 0.5 cm
Left waist side length-ground 1 cm

Page 6 of 17 Meyer et al. Fashion and Textiles           (2023) 10:37 
some additional manual measures taken by professional stylists and demographic 
information such as the gender or the education level and clothing size habits.
This campaign has been made in 37 different locations in France to represent correctly 
the target population. The sample collected of size 11 500 is aged from 5 to 70 years. In 
this work we have restricted the sample to the 9000 adults composed of 5000 women 
and 4000 men. Missing values in measurement features have been filled using a k-near -
est neighbors algorithm with the Gower’s distance (Gower 1971). The continuous input 
variables have all been standardized. The socioprofessional categorical nominal variable 
is a statistical nomenclature to classify professions of the French population created by 
the National Institute of Statistics and Economic Studies (Insee). It defines seven groups 
(managers, students, employees, farmers/merchants, laborers, inactives and retirees) 
and it has been encoded by a one-hot-encoding forgetting one category (farmers/mer -
chant) to avoid multicollinearity issues.
Models, evaluation metrics and hyperparameters tuning
In this section we present the machine learning models used in this paper, the evalua -
tion metrics considered and how we have chosen the associated hyperparameters. The 
models that have been compared for our regression tasks are linear regression models 
(LR), random forest models (RF), gradient boosting tree models (GB) and support vector 
regression models (SVR).
The random forest is an ensemble machine learning algorithm based on the use of 
combination of multiple decision trees trained in parallel on randomly extracted subsets 
of the dataset. This algorithm can be used to solve regression problems by averaging the 
predictions of decision trees. Random forests are usually used on large datasets and have 
much better performance and fewer overfitting issues than decision trees. However, they 
can have a high training time and are difficult to interpret (Ho 1995).
Gradient boosting trees is also an ensemble learning algorithm that can be used in 
regression and which is based on decision trees. This time, the trees are trained itera -
tively by eliminating the errors of the previous trees. This model is generally more accu -
rate than random forests but unfortunately once again hard to interpret (Breiman 1997).
The important idea behind support vector machine models is to map the dataset 
into high-dimensional space where it is easier to perform regression analysis. To this 
end kernel functions are used and permit non-linear analysis. These models are robust 
Fig. 1 The 6 easy-to-measure key body measurements

Page 7 of 17
 Meyer et al. Fashion and Textiles           (2023) 10:37 
 
prediction methods and produce significant accuracy than models based on decision 
trees with less computation time (Cortes and Vapnik 1995).
To evaluate the prediction accuracy of the models, we have used the average mean 
absolute error (MAE) defined by
where x=(x1,...,xn) and y=(y1,...,yn) are n-dimensional vectors, and we have eval -
uated it between the real test values y and the predicted values x by a model. This metric 
has been used to be compared with the precision steps given in Table  1. The precision 
ratio PR of a measurement is defined to be the ratio between the MAE associated to the 
best model and the precision step of the measurement, that is to say:
where y is a measurement of Table  1, PS(y) is its precision step, ˆm is a trained model 
where m∈models  , Xtest is the input test matrix and ytest is the real test values.
The machine learning algorithms considered in this work have a wide range of hyper -
parameters with significant effects on the performances of models that we have tuned 
with bayesian optimization methods. This method comes from global optimization the -
ory (Mockus et al. 1978) and is applicable to the problem of minimizing a scalar-valued 
function which is costly to evaluate. This approach has been applied to solve machine 
learning problems where the function is an evaluation metric of a model. This optimi -
zation method has better results and is much faster than the grid and random search 
cross-validations.
Hence we have used bayesian optimization to tune hyperparameters of the RF, GB and 
SVR models by minimizing the evaluation metric MAE. The hyperparameters that we 
have considered to tune the RF and GB models are the number and the maximum depth 
of trees, the minimum number of samples required to split an internal node and to be at 
a leaf node. For the SVR model the hyperparameters tuned are the kernel function, its 
coefficient γ , the regularization parameter and the epsilon-tube in which no penalty is 
associated in the training loss function.
Results
Model prediction performance
We have trained the machine learning models considered in “Models, evaluation met -
rics and hyperparameters tuning ” to estimate each key measurement used in fashion 
industry (see Table  1) from our input features separating men from women. To this 
end we have split the dataset into two sets, one set to train the algorithms and another 
set to test the algorithms, following a 70–30% division. The resulting evaluation scores 
comparing the test values and the predicted values on the test set sorted in descending (1)MAE (x,y)=1
n/summationdisplay
i
(2) PR(y)=min
m∈models/parenleftbig
MAE (ytest,ˆm(X test))/parenrightbig
PS(y)

Page 8 of 17 Meyer et al. Fashion and Textiles           (2023) 10:37 
order with respect to the precision ratios are given in Tables  2 and 3 for women and men 
respectively.
The hyperparameters tuned for the models by the bayesian optimization are not 
much affected by gender. For both the RF and GB models, except for the maximum 
depth of trees, the average of the hyperparameters obtained are similar. We have 
obtained on average 550 trees, and 6 minimum of samples required to split an inter -
nal node and to be at a leaf node. However the maximum depth of trees is on average 
14 for the RF models while 5 for the GB models. The tuning of the hyperparameters of 
the SVR models give on average 58 for the regularization parameter, 0.72 for the epsi -
lon-tube and 10.64 for the γ coefficient. The linear, sigmoid and radial basis function Table 2 Prediction performance metrics of the measurements used in fashion industry for the 
women dataset
Measurement LR RF GB SVR Best model Best 
model 
MAEPrecision ratio
Left shoulder slope (acromiale-neck base) 3.41 3.44 3.46 3.42 LR 3.41 3.41
Thigh girth 1.66 1.64 1.63 1.65 GB 1.63 3.27
Neck base girth (suprasternal) 1.46 1.48 1.49 1.46 SVR 1.46 2.92
Chest/bust width 1.38 1.38 1.39 1.38 SVR 1.38 2.76
Calf girth 1.23 1.30 1.27 1.23 SVR 1.23 2.46
Knee girth 1.23 1.27 1.27 1.23 SVR 1.23 2.45
High hip girth 2.35 2.38 2.57 2.35 SVR 2.35 2.35
Upper arm girth 1.20 1.15 1.24 1.19 RF 1.15 2.31
Head girth 1.13 1.15 1.18 1.12 SVR 1.12 2.25
Neck girth 1.10 1.14 1.21 1.09 SVR 1.09 2.19
Shoulder length (acromia—7th cervical 
vertebra)2.18 2.20 2.22 2.18 LR 2.18 2.18
Ankle girth 1.06 1.08 1.14 1.07 LR 1.06 2.13
Underbust girth 1.92 1.90 1.89 1.91 GB 1.89 1.89
Wrist girth 0.80 0.81 0.81 0.80 SVR 0.80 1.60
Bustpoint-waist length 1.51 1.54 1.54 1.51 SVR 1.51 1.51
Left arm length (acromia-wrist) 1.37 1.43 1.39 1.37 SVR 1.37 1.37
Bustpoint length (neck base-bustpoint) 1.34 1.34 1.35 1.34 LR 1.34 1.34
Back length (7th cervical-waist) 1.31 1.36 1.42 1.30 SVR 1.30 1.30
Back lower trunk length 1.27 1.33 1.27 1.27 LR 1.27 1.27
Bustpoints breadth 0.59 0.60 0.60 0.58 SVR 0.58 1.16
Left waist side length-ground 1.13 1.23 1.18 1.13 SVR 1.13 1.13
Waist height 1.10 1.22 1.17 1.11 LR 1.10 1.10
Body rise 1.08 1.16 1.11 1.07 SVR 1.07 1.07
Front lower trunk length 1.02 1.08 1.11 1.02 SVR 1.02 1.02
Waist-knee height 1.01 1.09 1.03 1.01 LR 1.01 1.01
7th cervical height 0.91 0.95 0.99 0.91 LR 0.91 0.91
Head height (vertex-7th cervical) 0.90 0.96 0.93 0.90 SVR 0.90 0.90
Length of scye 0.71 0.72 0.72 0.71 LR 0.71 0.71
Knee-ground height 0.61 0.63 0.64 0.61 SVR 0.61 0.61
Back width 0.02 0.01 0.00 0.02 GB 0.00 0.01

Page 9 of 17
 Meyer et al. Fashion and Textiles           (2023) 10:37 
 
kernels have also been compared and for every measurement and both genders the 
linear kernel has the best performance.
Comparison of model prediction distributions
The objective of this work was to make individual predictions as well as to update past 
sizing systems. To this end we were not only interested into average model prediction 
performances, but also into the distributions of the values predicted by models. In this 
section we have computed and compared the Kullback–Leibler (KL) divergence (Kull -
back and Leibler 1951) of the density estimations between the real values of the test set 
and the predicted values by our models for each measurement.
For two distributions p=(pk) and q=(qk) , the KL divergence (or relative entropy) 
d(p, q) is defined by
(3)d(p,q)=/summationdisplay
kpklog/parenleftBigpk
qk/parenrightBig
.Table 3 Prediction performance metrics of the measurements used in fashion industry for the men 
dataset
Measurement LR RF GB SVR Best model Best 
model 
MAEPrecision ratio
Left shoulder slope (acromiale-neck base) 3.37 3.41 3.54 3.37 SVR 3.37 3.37
Neck base girth (suprasternal) 1.67 1.68 1.74 1.66 LR 1.66 3.31
Thigh girth 1.58 1.50 1.52 1.49 SVR 1.49 2.97
Neck girth 1.26 1.32 1.30 1.25 SVR 1.25 2.49
Calf girth 1.26 1.30 1.36 1.24 SVR 1.24 2.48
Shoulder length (acromia—7th cervical 
vertebra)2.44 2.51 2.69 2.44 SVR 2.44 2.44
Head girth 1.16 1.17 1.16 1.16 SVR 1.16 2.30
Upper arm girth 1.18 1.13 1.17 1.18 RF 1.13 2.27
Ankle girth 1.11 1.13 1.29 1.11 SVR 1.11 2.21
Chest/Bust width 1.09 1.13 1.21 1.09 SVR 1.09 2.18
High hip girth 2.14 2.16 2.13 2.13 GB 2.13 2.13
Knee girth 1.05 1.08 1.08 1.05 SVR 1.05 2.10
Wrist girth 0.87 0.88 0.90 0.87 SVR 0.87 1.73
Left arm length (acromia-wrist) 1.62 1.67 1.80 1.62 LR 1.62 1.62
Back lower trunk length 1.50 1.56 1.58 1.49 SVR 1.49 1.49
Back length (7th cervical-waist) 1.45 1.51 1.50 1.45 LR 1.45 1.45
Waist height 1.31 1.34 1.41 1.31 SVR 1.31 1.31
Body rise 1.31 1.37 1.39 1.30 SVR 1.30 1.30
Front lower trunk length 1.21 1.26 1.35 1.21 SVR 1.21 1.21
Waist-knee height 1.17 1.19 1.25 1.16 SVR 1.16 1.16
7th cervical height 0.96 1.06 1.09 0.96 SVR 0.96 0.96
Head height (vertex-7th cervical) 0.97 0.98 1.03 0.94 SVR 0.94 0.94
Knee-ground height 0.67 0.70 0.74 0.67 SVR 0.67 0.67
Length of scye 0.41 0.42 0.42 0.41 LR 0.41 0.41
Back width 0.03 0.02 0.01 0.03 GB 0.01 0.01

Page 10 of 17 Meyer et al. Fashion and Textiles           (2023) 10:37 
This statistical distance is used in probability and information theories to measure the 
difference between probability distributions and quantifies which model best respects 
the expected distribution although it is non-symmetric and doesn’t satisfy to the triangle 
inequality.
In Table  4 we have summarized for each measurement and both gender which model 
has the lowest KL divergence compared to the distribution of the test set. Again, for 
almost all measurements LR and SVR models are better than RF and GB models.
The effect of the training dataset size
Since the training dataset is one of the key factors that can affect the performance 
of our models, various training datasets with increasing sizes were established in 
order to investigate the effects. For each training dataset, the data were extracted 
Table 4 Models with lowest KL divergence from the expected distribution sorted by lowest 
divergence
Measurement Women Men
Lowest KL 
divergenceModel Lowest KL 
divergenceModel
Left shoulder slope (acromiale-neck base) 0.0238 LR 0.0191 RF
Bustpoint-waist length 0.0066 SVR – –
Shoulder length (acromia—7th cervical vertebra) 0.0027 LR 0.0024 LR
Wrist girth 0.0020 LR 0.0018 LR
Bustpoint length (neck base-bustpoint) 0.0018 LR – –
Ankle girth 0.0017 SVR 0.0014 LR
Upper arm girth 0.0016 RF 0.0012 RF
Head height (vertex-7th cervical) 0.0013 SVR 0.0012 LR
Length of scye 0.0013 LR 0.0003 LR
Chest/Bust width 0.0012 SVR 0.0006 SVR
Body rise 0.0012 SVR 0.0016 SVR
Neck base girth (suprasternal) 0.0010 LR 0.0010 SVR
Calf girth 0.0010 SVR 0.0009 SVR
Neck girth 0.0010 SVR 0.0009 LR
Back length (7th cervical-waist) 0.0009 LR 0.0009 LR
Knee girth 0.0009 LR 0.0007 LR
Back lower trunk length 0.0008 LR 0.0009 SVR
Bustpoints breadth 0.0008 SVR – –
Front lower trunk length 0.0008 SVR 0.0009 SVR
Thigh girth 0.0007 RF 0.0006 GB
High hip girth 0.0005 RF 0.0004 LR
Left arm length (acromia-wrist) 0.0005 LR 0.0006 SVR
Underbust girth 0.0005 SVR – –
Head girth 0.0004 SVR 0.0003 LR
Waist-knee height 0.0003 SVR 0.0003 LR
Knee-ground height 0.0002 SVR 0.0002 LR
Left waist side length-ground 0.0001 SVR – –
Waist height 0.0001 LR 0.0001 LR
7th cervical height 0.0000 LR 0.0000 LR
Back width 0.0000 GB 0.0000 LR

Page 11 of 17
 Meyer et al. Fashion and Textiles           (2023) 10:37 
 
randomly from the remaining data in the dataset. Then our 4 models have been 
trained with bayesian optimization hyperparameter tuning and tested on these sub -
sets. To illustrate this in Fig.  2 we have shown it for the measurement waist-knee 
height for women which is a well-estimated measurement.
Features importance
The permutation feature importance measures the importance of the input features 
of a model by calculating the increase in the model’s prediction error after ran -
domly shuffling the feature. A feature is said to be important if permuting its values 
increases the model error. This notion was introduced in Breiman (2001) for random 
forests and in Fisher et al. (2019) for a general model.
We now explain how to calculate the permutation feature importance. For a 
trained model ˆm where m∈models  , the input test matrix Xtest , a column feature j  in 
Xtest and the target test feature ytest:
• We compute the error metric MAE (ytest ,ˆm(Xtest));
• We define the matrix Xtest ,perm  to be the matrix Xtest where the column feature j 
has been randomly permuted;
• We compute the associated error metric MAE (ytest ,ˆm(Xtest ,perm ));
• We calculate the permutation feature importance FIj of j by 
In Table  5 we have presented the means of permutation feature importances along 
all measurements for all models and in Table  6 we have counted the number of 
measurements where each feature is the most important.(4) FIj=MAE (ytest ,ˆm(X test))−MAE (ytest ,ˆm(X test ,perm )).
Fig. 2 MAE of the models trained by datasets with various sizes for the waist-knee height measurement for 
women. LR: linear regression. RF: random forest. GB: gradient boosting. SVR: support vector regression

Page 12 of 17 Meyer et al. Fashion and Textiles           (2023) 10:37 
Discussion
We have obtained that, for both genders, all measurements are estimated with a MAE 
and a precision ratio smaller than 3.6 and that models have similar performances. Meas -
urements can have different prediction accuracies depending on the gender, for example 
the knee girth has a precision ratio of 2.45 for women and 2.10 for men. For both gen -
ders, the five same measurements have a precision ratio less than 1 and almost exactly 
in the same order, these measurements are given in Fig.  3. The three least well estimated 
measurements are the same for women and men and are given in Fig.  3. One can see 
that neck measurements are not easily obtainable by our models. We have got that the Table 5 Table of means of permutation feature importances for all measurements and both 
genders
SPC Socio-Professional CategoryInput feature Women Men
LR RF GB SVR LR RF GB SVR
Height 0.613 0.542 0.551 0.568 0.761 0.653 0.641 0.661
Weight 0.722 0.549 0.571 0.620 0.689 0.490 0.497 0.540
Chest/bust girth 0.514 0.490 0.488 0.492 0.342 0.310 0.305 0.316
Waist girth 0.549 0.450 0.480 0.502 0.391 0.344 0.338 0.352
Hip girth 0.267 0.254 0.254 0.258 0.176 0.167 0.167 0.171
Inside leg length 0.477 0.375 0.376 0.403 0.438 0.340 0.331 0.360
Age 0.044 0.039 0.040 0.042 0.042 0.037 0.038 0.038
Shoe size 0.012 0.009 0.011 0.011 0.018 0.013 0.015 0.015
SPC_manager 0.004 0.002 0.002 0.002 0.007 0.004 0.003 0.004
SPC_student 0.009 0.005 0.004 0.005 0.004 0.002 0.002 0.003
SPC_employee 0.006 0.003 0.002 0.003 0.003 0.001 0.001 0.002
SPC_inactive 0.002 0.001 0.001 0.001 0.001 0.001 0.001 0.001
SPC_laborer 0.003 0.002 0.002 0.002 0.004 0.003 0.002 0.003
SPC_retiree 0.004 0.002 0.001 0.002 0.004 0.002 0.001 0.002
Table 6 Count table of permutation feature importances for all measurements and both genders
SPC Socio-Professional CategoryInput feature Women Men
LR RF GB SVR LR RF GB SVR
Height 7 6 7 5 8 7 5 7
Weight 11 10 9 11 10 9 11 10
Chest/bust girth 6 5 6 6 4 4 4 4
Waist girth 2 4 4 3 1 2 1 1
Hip girth 0 1 0 0 0 1 0 0
Inside leg length 4 3 4 5 2 2 3 3
Age 0 1 0 0 0 0 1 0
Shoe size 0 0 0 0 0 0 0 0
SPC_manager 0 0 0 0 0 0 0 0
SPC_student 0 0 0 0 0 0 0 0
SPC_employee 0 0 0 0 0 0 0 0
SPC_inactive 0 0 0 0 0 0 0 0
SPC_laborer 0 0 0 0 0 0 0 0
SPC_retiree 0 0 0 0 0 0 0 0

Page 13 of 17
 Meyer et al. Fashion and Textiles           (2023) 10:37 
 
average MAE is between 1.25 and 1.4% for each model and that the predictions for 
women are slightly better than for men. The linear and the support vector regressions 
have an average MAE between 1.25 and 1.3% and are therefore better than the models 
based on decision trees which have an average MAE between 1.3 and 1.4%. For almost 
all measurements LR and SVR models are better than RF and GB models.
The computation of KL divergences in our case have corroborated the previous discus -
sion and the results of “Model prediction performance” section since we have obtained 
Fig. 3 The five best estimated measurements by the models for both genders in figures (a) to (e). The three 
least well estimated measurements by the models for both genders in figures (f–h) and the fourth least well 
estimated measurement for women (respectively men) in figure (i) (respectively (j))
Fig. 4 Boxplots and density estimations of the predicted values by the models compared to the real 
test values of the bustpoint-waist length for women. LR: linear regression. RF: random forest. GB: gradient 
boosting. SVR: support vector regression

Page 14 of 17 Meyer et al. Fashion and Textiles           (2023) 10:37 
that the LR and SVR models have better distributions than the RF and GB models. We 
note that this time the men have slightly better results than women contrary to results 
with the metric MAE. To illustrate this we have shown in Fig.  4 the boxplots and the 
density estimations of the predicted values by the models compared to the real test 
values of the bustpoint-waist length for women which is one of the less well estimated 
measurements.
Moreover, the effect of the training dataset size is almost always the same for both gen -
ders and all measurements. One can see that the LR and SVR models rapidly have good 
results with an important stability while the RF and GB models need a more important 
dataset size and have rather unstable results. This instability is certainly due to the fact 
that these two models have a part of randomness in their construction and learning. For 
the LR and SVR models, it turns out that to obtain good results we have needed a data -
set of size approximately 500. One of the only measurements having a different behavior 
by evaluating its model prediction performance metric along different training dataset 
sizes is the upper arm girth. This particularity is more pronounced for the men dataset 
where we have that the RF model has better result than the LR and SVR models and con -
tinue to improve without stabilization, see Fig. 5.
We have also studied the evolution of the KL divergence of the density estimations 
between the real values of the test set and the predicted values by our models when 
increasing the size of the training datasets and the results are very similar to the evolu -
tion of the MAE.
It turns out that, even if the weight and height have the most influence for both 
sexes, the weight is the most important input feature for women while the height 
is the most important feature for men. The inside leg length, the chest/bust, waist 
and hip girths have more influence for women than for men. It is shared for both 
genders and all models that the inside leg length, the chest/bust and waist girths are 
more important than the hip girth. It is interesting to note that the only measure -
ment for which the hip girth is the most important feature is the thigh girth for the 
RF model and both sexes and that this measurement has the particularity to be not 
Fig. 5 MAE of the models trained by datasets with various sizes for the upper arm girth measurement for 
men. LR: linear regression. RF: random forest. GB: gradient boosting. SVR: support vector regression

Page 15 of 17
 Meyer et al. Fashion and Textiles           (2023) 10:37 
 
well estimated in terms of evaluation metrics (see Tables  2 and 3 ) while having good 
distribution results (see Table  4). The age, the shoe size and the socioprofessional cat -
egory don’t have much importance. We also see that the LR model is less stable than 
the other ones with respect to the variation of the inputs while tree based models are 
more resistant.
The only measurement for which the age is the most important input feature is 
the left shoulder slope (acromiale-neck base) for the model RF (respectively GB) for 
women (respectively men) and is the most difficult measurement to predict for both 
genders (see Tables 2 , 3 and 4 ).
Conclusions
In this article, we have compared linear regressions, random forests, gradient boost -
ing trees and support vector regressions to predict about thirty measurements used 
in fashion industry to construct clothes from 6 easy-to-measure body dimensions and 
demographic information. Our work shows that for both genders the models have 
good prediction accuracies and distributions. More precisely, the average MAE per 
model is less than 1.4 and is slightly better for women than for men, while the KL 
divergences between test values and predicted values in the test set are inferior to 
0.03 and are slightly better for men than for women. The results suggest to use lin -
ear and support vector regressions to estimate body dimensions. These models have 
better MAE and distribution results, they generally need only 500 samples to be cor -
rectly trained and are more stable than tree-based models. It turns out that girth 
measurements are more difficult to estimate than height measurements. The study 
of the importance of the input features indicates that for both genders, the clothing 
habits and the demographic characteristics are not important and that the weight and 
height have the most influence for the models considered while the hip girth is the 
less important among the input measurements. This result is positive since it is much 
easier to measure its weight and height rather than the hip girth which is often con -
fused with the high hip girth. Actually we have that the weight is the most important 
feature for women while the height is the most important feature for men. It is shown 
in the literature that artificial neural networks have efficient results to predict body 
dimensions. Hence, future research can be conducted to compare the models used in 
this work with deep learning models and study their individual and global prediction 
results and the influence of the input features and training dataset size.
Abbreviations
GB  Gradient boosting
IFTH  French Institute of Textiles and Clothing
KL  Kullback–Leibler
LR  Linear regression
MAE  Mean absolute error
PR  Precision ratio
PS  Precision step
RF  Random forest
SVR  Support vector regression
UTT   Université de Technologie de Troyes
Acknowledgements
Not applicable.

Page 16 of 17 Meyer et al. Fashion and Textiles           (2023) 10:37 
Authors’ contributions
PM coded the algorithmic parts and wrote the original draft. AL transmitted and analyzed the dataset and the list of 
measurements used in fashion industry. BB, AL, PB, EG conceptualized the approach and the methodology. BB, PB, EG 
supervised the theoretical parts. All authors read and approved the final manuscript.
Funding
This work was supported by Labcom-DiTeX, a joint research group in Textile Data Innovation between Institut Français 
du Textile et de l’Habillement (IFTH) and Université de Technologie de Troyes (UTT).
Availability of data and materials
This research was conducted under the approval and supervision of the scientific board of IFTH protocols regarding 
the GDPR requirements and the ethical issue including consent to participate in the CNM (Campagne Nationale de 
Mensuration) 2003.
Declarations
Competing interests
The authors declare that they have no competing interests.
Received: 6 March 2023   Accepted: 12 August 2023
References
AP , C., Fan, J., & Yu, W. (2003). Men’s shirt pattern design part ii: Prediction of pattern parameters from 3d body measure -
ments. Sen’I Gakkaishi, 59(8), 328–333.  https:// doi. org/ 10. 2115/ fiber. 59. 328.
Ashmawi, S., Alharbi, M., Almaghrabi, A., & Alhothali, A. (2019). Fitme: Body measurement estimations using machine 
learning method. Procedia Computer Science, 163, 209–217. https:// doi. org/ 10. 1016/j. procs. 2019. 12. 102.
Bartol, K., Bojanić, D., Petković, T., & Pribanić, T. (2021). A review of body measurement using 3d scanning. IEEE Access, 9, 
67281–67301. https:// doi. org/ 10. 1109/ ACCESS. 2021. 30765 95.
Breiman, L. (1997). Arcing the edge. Technical report, Technical Report 486, Statistics Department, University of California, 
Berkeley CA. 94720.
Breiman, L. (2001). Random forests. Machine Learning, 45(1), 5–32. https:// doi. org/ 10. 1023/A: 10109 33404 324.
Chan, A., Fan, J., & Yu, W. (2005). Prediction of men’s shirt pattern based on 3d body measurements. International Journal 
of Clothing Science and Technology, 17(2), 100–108. https:// doi. org/ 10. 1108/ 09556 22051 05812 45.
Chumlea, W. C., & Guo, S. (1992). Equations for predicting stature in white and black elderly individuals. Journal of Geron-
tology, 47(6), M197–M203. https:// doi. org/ 10. 1093/ geronj/ 47.6. m197.
Chumlea, W. C., Roche, A. F., & Steinbaugh, M. L. (1985). Estimating stature from knee height for persons 60 to 90 years of 
age. Journal of the American Geriatrics Society, 33(2), 116–120.https:// doi. org/ 10. 1111/j. 1532- 5415. 1985. tb022 76.x.
Cortes, C., & Vapnik, V. (1995). Support-vector networks. Machine Learning, 20(3), 273–297. https:// doi. org/ 10. 1007/ BF009 
94018.
de Souza, J. W. M., Holanda, G. B., Ivo, R. F., Alves, S. S. A., da Silva, S. P . P ., Nunes, V. X., Loureiro, L. L., Dias-Silva, C. H., & 
Rebouças Filho, P . P . (2020). Predicting body measures from 2d images using convolutional neural networks. In 2020 
International Joint Conference on Neural Networks (IJCNN) (pp 1–6). https:// doi. org/ 10. 1109/ IJCNN 48605. 2020. 92073 
30
Fisher, A., Rudin, C., & Dominici, F. (2019). All models are wrong, but many are useful: Learning a variable’s importance by 
studying an entire class of prediction models simultaneously. Journal of Machine Learning Research, 20(177), 1–81. 
https:// doi. org/ 10. 48550/ arXiv. 1801. 01489.
Giri, C., Jain, S., Zeng, X., & Bruniaux, P . (2019). A detailed review of artificial intelligence applied in the fashion and apparel 
industry. IEEE Access, 7, 95376–95396. https:// doi. org/ 10. 1109/ ACCESS. 2019. 29289 79
Gordon, C. C., Blackwell, C. L., Bradtmiller, B., Parham, J. L., Barrientos, P ., Paquette, S. P ., Corner, B. D., Carson, J. M., Venezia, 
J. C., Rockwell, B. M., et al. (2014). 2012 anthropometric survey of us army personnel: Methods and summary statistics. 
Army Natick Soldier Research Development and Engineering Center MA. Technical report.
Gordon, C. C., Churchill, T., Clauser, C. E., Bradtmiller, B., & McConville, J. T. (1989). Anthropometric survey of us army person-
nel: Methods and summary statistics 1988. Yellow Springs OH: Anthropology Research Project Inc. Technical report.
Gordon, T. & Miller, H. W. (1964). Cycle I of the Health Examination Survey: Sample and Response, United States, 1960-62. 
Number 1. US Department of Health, Education, and Welfare, Public Health Service.
Gower, J. C. (1971). A general coefficient of similarity and some of its properties. Biometrics, 27, 857–871. https:// doi. org/ 
10. 2307/ 25288 23
Guo, Z., Wong, W. K., Leung, S., & Li, M. (2011). Applications of artificial intelligence in the apparel industry: A review. Textile 
Research Journal, 81(18), 1871–1892. https:// doi. org/ 10. 1177/ 00405 17511 411968.
Ho, T. K. (1995). Random decision forests. In Proceedings of 3rd international conference on document analysis and recogni-
tion, IEEE, Canada, 1, 278–282. https:// doi. org/ 10. 1109/ ICDAR. 1995. 598994.
Hung, P .C.-Y., Witana, C. P ., & Goonetilleke, R. S. (2004). Anthropometric measurements from photographic images. Com -
puting Systems, 29(764–769), 3.
Indah, P ., Sari, A. D., Suryoputro, M. R., & Purnomo, H. (2016). Prediction of elderly anthropometric dimension based on 
age, gender, origin, and body mass index. IOP Conference Series: Materials Science and Engineering, Indonesia, 105(1), 
Article 012024.  https:// doi. org/ 10. 1088/ 1757- 899X/ 105/1/ 012024.

Page 17 of 17
 Meyer et al. Fashion and Textiles           (2023) 10:37 
 
Kaashki, N. N., Hu, P ., & Munteanu, A. (2021). Deep learning-based automated extraction of anthropometric measure -
ments from a single 3-d scan. IEEE Transactions on Instrumentation and Measurement, 70, 1–14. https:// doi. org/ 10. 
1109/ TIM. 2021. 31061 26.
Kullback, S., & Leibler, R. A. (1951). On information and sufficiency. The Annals of Mathematical Statistics, 22(1), 79–86. 
https:// doi. org/ 10. 1214/ aoms/ 11777 29694
Liu, K., Wang, J., Kamalha, E., Li, V., & Zeng, X. (2017). Construction of a prediction model for body dimensions used in gar -
ment pattern making based on anthropometric data learning. The Journal of the Textile Institute, 108(12), 2107–2114. 
https:// doi. org/ 10. 1080/ 00405 000. 2017. 13157 94
Liu, Z., Li, J., Chen, G., & Lu, G. (2014). Predicting detailed body sizes by feature parameters. International Journal of Clothing 
Science and Technology, 26(2), 118–130. https:// doi. org/ 10. 1108/ IJCST- 02- 2013- 0009
Lu, J.-M., & Wang, M.-J.J. (2008). Automated anthropometric data collection using 3d whole body scanners. Expert Systems 
with Applications, 35(1–2), 407–414. https:// doi. org/ 10. 1016/j. eswa. 2007. 07. 008.
Miguel-Hurtado, O., Guest, R., Stevenage, S. V., Neil, G. J., & Black, S. (2016). Comparing machine learning classifiers and 
linear/logistic regression to explore the relationship between hand dimensions and demographic characteristics. 
PLoS ONE, 11(11), Article e0165521. https:// doi. org/ 10. 1371/ journ al. pone. 01655 21.
Mockus, J., Tiesis, V., & Zilinskas, A. (1978). The application of bayesian methods for seeking the extremum. Towards Global 
Optimization, 2(117–129), 2.
NCHS (1994). Plan and operation of the Third National Health and Nutrition Examination Survey, 1988–94. DHHS publication. 
U.S. Department of Health and Human Services, Public Health Service, Centers for Disease Control and Prevention, 
National Center for Health Statistics.
Pearson, K. (1899). IV. Mathematical contributions to the theory of evolution.-V. On the reconstruction of the stature of 
prehistoric races. Philosophical Transactions of the Royal Society of London. Series A, Containing Papers of a Mathemati-
cal or Physical Character, 192, 169–244.  https:// doi. org/ 10. 1098/ rsta. 1899. 0004
Rativa, D., Fernandes, B. J., & Roque, A. (2018). Height and weight estimation from anthropometric measurements using 
machine learning regressions. IEEE Journal of Translational Engineering in Health and Medicine, 6, 1–9.  https:// doi. org/ 
10. 1109/ JTEHM. 2018. 27979 83
Rollet, E. (1892). Détermination de la taille d’après les os longs des membres. Publications de la Société Linnéenne de Lyon, 
11(1), 163–178. (Included in a thematic issue: 1892). https:// doi. org/ 10. 3406/ linly. 1892. 16376
Wang, L., Lee, T. J., Bavendiek, J., & Eckstein, L. (2021). A data-driven approach towards the full anthropometric measure -
ments prediction via generalized regression neural networks. Applied Soft Computing, 109, Article 107551. https:// 
doi. org/ 10. 1016/j. asoc. 2021. 107551.
Wang, Z., Wang, J., Xing, Y., Yang, Y., & Liu, K. (2019). Estimating human body dimensions using RBF artificial neural net -
works technology and its application in activewear pattern making. Applied Science, 9(6), Article 1140.  https:// doi. 
org/ 10. 3390/ app90 61140.
Publisher’s Note
Springer Nature remains neutral with regard to jurisdictional claims in published maps and institutional affiliations.
Philippe Meyer is a Postdoctoral Researcher in the Computer Science and Digital Society Laboratory at 
the Université de Technologie de Troyes in France. His work focuses on the applications of Mathematics, 
Machine Learning and Topological Data Analysis.
Babiga Birregah is an Associate Professor at the Université de Technologie de Troyes in France. His work 
in the Computer Science and Digital Society Laboratory is focused on Big Data Analytics and Artificial Intel-
ligence with several application fields.
Pierre Beauseroy is a full Professor at the Université de Technologie de Troyes in France. His work focuses 
on Machine Learning, Detection and Regression applied to different types of systems, with a particular 
interest in systems that are difficult to characterize due to noise, limited expertise, or non-stationarity of 
behavior.
Edith Grall‑Maës is an Associate Professor in the LIST3N (Computer Science and Digital Society) Labora-
tory at the Université de Technologie de Troyes in France. Her research interests include signal and data 
analysis and supervised/unsupervised learning decision models.
Audrey Lauxerrois is an expert in the Research and Development department of the French Institute of 
Textiles and Clothing. Her activities are focused in particular on morphology applied to fashion professions, 
processing and analysis of the database of the French National Measurement Campaign.