Distance-based Conﬁdence Score for Neural Network Classiﬁers
Amit Mandelbaum Daphna Weinshall
School of Computer Science and Engineering
Hebrew University of Jerusalem, IsraelSchool of Computer Science and Engineering
Hebrew University of Jerusalem, Israel
Abstract
The reliable measurement of conﬁdence in
classiﬁers’ predictions is very important for
many applications, and is therefore an im-
portant part of classiﬁer design. Yet, al-
though deep learning has received tremen-
dous attention in recent years, not much
progress has been made in quantifying the
prediction conﬁdence of neural network classi-
ﬁers. Bayesian models oﬀer a mathematically
grounded framework to reason about model
uncertainty, butusuallycomewithprohibitive
computational costs. In this paper we pro-
pose a simple, scalable method to achieve a
reliable conﬁdence score, based on the data
embedding derived from the penultimate layer
of the network. We investigate two ways to
achieve desirable embeddings, by using either
a distance-based loss or Adversarial Train-
ing. We then test the beneﬁts of our method
when used for classiﬁcation error prediction,
weighting an ensemble of classiﬁers, and nov-
elty detection. In all tasks we show signiﬁcant
improvement over traditional, commonly used
conﬁdence scores.
1 Introduction
Classiﬁcation conﬁdence scores are designed to mea-
sure the accuracy of the model when predicting class
assignment (rather than the uncertainty inherent in the
data). Most generative classiﬁcation models are proba-
bilistic in nature, and therefore provide such conﬁdence
scores directly. Most discriminative models, on the
other hand, do not have direct access to the probability
of each prediction. Instead, related non-probabilisticscores are used as proxies, as for example the margin
in SVM classiﬁers.
When trying to evaluate the conﬁdence of neural net-
work (NN) classiﬁers, a number of scores are commonly
used. One is the strength of the most activated output
unit followed by softmax normalization, or the closely
related ratio between the activities of the strongest
and second strongest units. Another is the (negative)
entropy of the output units, which is minimal when
all units are equally probable. Often, however, these
scores do not provide a reliable measure of conﬁdence.
Why is it important to reliably measure prediction con-
ﬁdence? In various contexts such as medical diagnosis
and decision support systems, it is important to know
the prediction conﬁdence in order to decide how to act
upon it. For example, if the conﬁdence in a certain
prediction is too low, the involvement of a human ex-
pert in the decision process may be called for. Another
important aspect of real world applications is the abil-
ity to recognize samples that do not belong to any of
the known classes, which can also be improved with a
reliable conﬁdence score. But even irrespective of the
application context, reliable prediction conﬁdence can
be used to boost the classiﬁer performance via such
methods as self-training or ensemble classiﬁcation. In
this context a better conﬁdence score can improve the
ﬁnal performance of the classiﬁer. The derivation of a
good conﬁdence score should therefore be part of the
classiﬁer’s design, as important as any other component
of classiﬁers’ design.
In order to derive a reliable conﬁdence score for NN
classiﬁers, we focus our attention on an empirical obser-
vation concerning neural networks trained for classiﬁca-
tion, which have been shown to demonstrate in parallel
useful embedding properties. Speciﬁcally, a common
practice these days is to treat one of the upstream
layers of a pre-trained network as a representation (or
embedding) layer. This layer activation is then used for
representing similar objects and train simpler classiﬁers
(such as SVM, or shallower NNs) to perform diﬀerent
tasks, related but not identical to the original task the
network had been trained on.arXiv:1709.09844v1  [cs.AI]  28 Sep 2017

Distance-based Conﬁdence Score for Neural Network Classiﬁers
In computer vision such embeddings are commonly
obtained by training a deep network on the recognition
of a very large database (typically ImageNet (Deng
et al., 2009)). These embeddings have been shown to
provide better semantic representations of images (as
compared to more traditional image features) in a num-
ber of related tasks, including the classiﬁcation of small
datasets (Sharif Razavian et al., 2014), image annota-
tion (Donahue et al., 2015) and structured predictions
(Hu et al., 2016). Given this semantic representation,
one can compute a natural multi-class probability dis-
tribution as described in Section 2.1, by estimating
local density in the embedding space. This estimated
density can be used to assign a conﬁdence score to each
test point, using its likelihood to belong to the assigned
class.
We note, however, that the commonly used embedding
discussed above is associated with a network trained
for classiﬁcation only, which may impede its suitability
to measure conﬁdence reliably. In fact, when train-
ing neural networks, metric learning is often used to
achievedesirableembeddings(e.g., Westonetal.(2012);
Schroﬀ et al. (2015); Hoﬀer & Ailon (2015); Tadmor
et al. (2016)). Since our goal is to improve the prob-
abilistic interpretation of the embedding, which is es-
sentially based on local point density estimation (or
the distance between points), we may wish to modify
the loss function and add a term which penalizes for
the violation of pairwise constraints as in Hadsell et al.
(2006). Our experiments show that the modiﬁed net-
work indeed produces a better conﬁdence score, with
comparable classiﬁcation performance. Surprisingly,
while not directly designed for this purpose, we show
that networks which are trained with adversarial ex-
amples following the Adversarial Training paradigm
(Szegedy et al., 2013; Goodfellow et al., 2014), also
provide a suitable embedding for the new conﬁdence
score.
Our ﬁrst contribution, therefore, is a new prediction
conﬁdence score which is based on local density esti-
mation in the embedding space of the neural network.
This score can be computed for every network, but in
order for this score to achieve superior performance, it
is necessary to slightly change the training procedure.
In our second contribution we show that suitable em-
bedding can be achieved by either augmenting the loss
function of the trained network with a term which pe-
nalizes for distance-based similarity loss (as in Eq. (2)
below), or by using Adversarial Training. The impor-
tance of the latter contribution is two fold: Firstly, we
are the ﬁrst to show that the density of image embed-
dings is improved with indirect Adversarial Training
perturbations, in addition to the improved word em-
bedding quality shown in Miyato et al. (2016) by directAdversarial Training perturbations. Secondly, we show
in Section 3 that Adversarial Training improves the
results while imposing a much lighter burden of hyper-
parameters to tune as compared to the distance-based
loss.
The new conﬁdence score is evaluated in comparison
to other scores, using the following tasks: (i) Perfor-
mance in the binary classiﬁcation task of identifying
each class prediction as correct or incorrect (see Sec-
tion 2.1). (ii) Training an ensemble of NN classiﬁers,
where each classiﬁer’s prediction is weighted by the
new conﬁdence score (see Section 2.4). (iii) Novelty
detection, where conﬁdence is used to predict whether
a test point belongs to one of the known classes from
the train set (see Section 2.5).
The empirical evaluation of our method is described
in Section 3, using a few datasets and diﬀerent net-
work architectures which have been used in previous
work when using these speciﬁc datasets. Our method
achieves signiﬁcant improvement in all 3 tasks. When
compared with a more recent method which had been
shown to improve traditional measures of classiﬁcation
conﬁdence - MC dropout (Gal & Ghahramani, 2015),
our distance-based score achieves better results while
also maintaining lower computational costs.
Prior Work
The Bayesian approach seeks to compute a posterior
distribution over the parameters of the neural network
which is used to estimate prediction uncertainty, as in
MacKay (1992) and Neal (2012). However, Bayesian
neural networks are not always practical to implement,
and the computational cost involved it typically high.
In accordance, in a method which is referred to below
asMC-Dropout , Gal & Ghahramani (2015) proposed
to use dropout during test time as a Bayesian approxi-
mation of the neural network, providing a cheap proxy
to Bayesian Neural Networks. Lakshminarayanan et al.
(2016) proposed to use Adversarial Training to improve
the uncertainty measure of the entropy score of the
neural network.
Still, the most basic and one of the most common
conﬁdence scores for neural networks can be derived
from the strength of the most activated output unit, or
ratheritsnormalizedversion(alsocalled softmax output
ormax margin ). A conﬁdence score that handles better
a situation where there is no one class which is most
probable, is the (negative) entropy of the normalized
network’s output. Zaragoza & d’Alché Buc (1998)
compared these scores, as well as some more complex
ones (e.g. Tibshirani (1996)), demonstrating somewhat
surprisingly the empirical superiority of the two most
basic methods described in the previous paragraph.

Amit Mandelbaum, Daphna Weinshall
Ensembles of models have been used to improve the
overall performance of the ﬁnal classiﬁer (see reviews
in Dietterich (2000) and Li et al. (2017)). There are
many ways to train an ensemble, such as boosting or
bagging. There are also many ways to integrate the
predictions of the classiﬁers in the ensemble, including
the average prediction or voting discussed by Bauer
& Kohavi (1999). Some ensemble methods use the
conﬁdence score to either weight the predictions of the
diﬀerent classiﬁers (average weighting) or for conﬁdence
voting.
Novelty detection, where the task is to determine
whether a test point belongs to a known class label
or not, is another problem which becomes more rele-
vant with the ever increasing availability of very large
datasets, see reviews in Markou & Singh (2003), Pi-
mentel et al. (2014) and the recent work in Vinokurov
& Weinshall (2016). This task is also highly relevant
in real world applications, where the classiﬁer is usu-
ally exposed to many samples which do not belong to
a known class. Note that novelty detection is quite
diﬀerent from the learning of classes with no examples,
as in zero shot learning (Palatucci et al., 2009).
2 New Conﬁdence Score
We propose next a new conﬁdence score. We then
discuss how it can be used to boost classiﬁcation per-
formance with ensemble methods, or when dealing with
novelty detection.
2.1 New Conﬁdence Score for Neural
Network Classiﬁers
Our conﬁdence score is based on the estimation of local
density as induced by the network, when points are
represented using the eﬀective embedding created by
the trained network in one of its upstream layers. Local
density at a point is estimated based on the Euclidean
distance in the embedded space between the point and
itsknearest neighbors in the training set.
Speciﬁcally, let f(x)denote the embedding of xas
deﬁned by the trained neural network classiﬁer. Let
A(x) =fxj
traingk
j=1denote the set of k-nearest neigh-
bors ofxin the training set, based on the Euclidean
distance in the embedded space, and let fyjgk
j=1denote
the corresponding class labels of the points in A(x). A
probability space is constructed (as is customary) by
assuming that the likelihood that two points belong to
the same class is proportional to the exponential of the
negative Euclidean distance between them. In accor-
dance, the local probability that a point xbelongs to
classcis proportional to the probability that it belongs
to the same class as the subset of points in A(x)thatbelong to class c.
Based on this local probability, the conﬁdence score
D(x)for the assignment of point xto class ^yis deﬁned
as follows:
D(x) =Pk
j=1;yj=^ye jjf(x) f(xj
train)jj2
Pk
j=1e jjf(x) f(xj
train)jj2(1)
D(x)is a score between 0 to 1, which is monotonically
related to the local density of similarly labeled train
points in the neighborhood of x. Henceforth (1) is
referred to as Distance score .1We note here that while
intuitively it might be beneﬁcial to add a scaling factor
to the distance in (1), such as the mean distance, we
found it to have a deteriorating eﬀect, in line with
related work such as Salakhutdinov & Hinton (2007).
Two ways to achieve eﬀective embedding: As
mentioned is Section 1, in order to achieve an eﬀective
embedding it helps to modify the training procedure of
the neural network classiﬁer. The simplest modiﬁcation
augments the network’s loss function during training
with an additional term. The resulting loss function is
a linear combination of two terms, one for classiﬁcation
denotedLclass(X;Y), and another pairwise loss for
the embedding denoted Ldist(X;Y). This is deﬁned as
follows:
L(X;Y) =Lclass(X;Y) +Ldist(X;Y)(2)
Ldist(X;Y) =1
PPX
p=1Ldist(xp1;xp2)
whereLdist(xi;xj)is deﬁned as
(
jjf(xi) f(xj)jj2 ifyi=yj
maxf0;(m jjf(xi) f(xj)jj2)gifyi6=yj
A desirable embedding can also be achieved by Ad-
versarial Training, using the fast gradient method sug-
gested in Goodfellow et al. (2014). In this method,
given an input xwith target y, and a neural network
with parameters , adversarial examples are generated
using:
x0=x+ sign (5xLclass(;x;y )) (3)
In each step an adversarial example is generated for
each pointxin the batch and the current parameters
of the network, and classiﬁcation loss is minimized for
both the regular and adversarial examples. Although
originally designed to improve robustness, this method
1Related measures of density, such as a count of the
"correct" neighbors or the inverse of the distance, behave
similarly and perform comparably.

Distance-based Conﬁdence Score for Neural Network Classiﬁers
seems to improve the network’s embedding for the pur-
pose of density estimation, possibly because along the
way it increases the distance between pairs of adjacent
points with diﬀerent labels.
Implementation details: In (2)Ldistis deﬁned by
all pairs of points, denoted (xp1;xp2). For each training
minibatch, thissetissampledwithnoreplacementfrom
the training points in the minibatch, with half as many
pairs as the size of the minibatch. In our experiments,
Lclass(X;Y)is the regular cross entropy loss. We note
here that we also tried distance-based loss functions
which do not limit the distance between points of the
same class to be exactly 0 (such as those in Hoﬀer
& Ailon (2015) and Tadmor et al. (2016)). However,
those functions produced worse results, especially when
the dataset had many classes. Finally we note that we
have tried using the distance-based loss and adversarial
training together while training the network, but this
has also produced worse results.
2.2 Alternative conﬁdence scores
Given a trained network, two measure are usually used
to evaluate classiﬁcation conﬁdence:
Max margin: the maximal activation, after normal-
ization, in the output layer of the network.
Entropy: the (negative) entropy of the activations in
the output layer of the network.
As noted above, the empirical study in Zaragoza &
d’Alché Buc (1998) showed that these two measures
are typically as good as any other existing method for
the evaluation of classiﬁcation conﬁdence.
Two recent methods have been shown to improve the re-
liability of the conﬁdence score based on Entropy: MC-
Dropout (Gal & Ghahramani, 2015) and Adversarial
Training (Lakshminarayanan et al., 2016; Goodfellow
et al., 2014). In terms of computational cost, adversar-
ial training can increase (and sometimes double) the
training time, due to the computation of additional
gradients and the addition of the adversarial examples
to the training set. MC-Dropout, on the other hand,
does not change the training time but increases the test
time by orders of magnitude (typically 100-fold). Both
methods are complementary to our approach, in that
they focus on modiﬁcations to the actual computation
of the network during either train or test time. After
all is done, they both evaluate conﬁdence using the
Entropy score. As we show in our experiments, adver-
sarial training combined with our proposed conﬁdence
score improves the ﬁnal results signiﬁcantly.2.3 Our method: computational analysis
Unlike the two methods described above, MC-Dropout
andAdversarial Training , our distance-based conﬁ-
dence score takes an existing network and computes
a new conﬁdence score from the network’s embedding
and output activation. It can use any network, with
or without adversarial training or MC dropout. If the
loss function of the network is suitably augmented (see
discussion above), empirical results in Section 3 show
that our score always improves results over the Entropy
score of the given network.
Train and test computational complexity: Con-
sidering the distance-based loss, Tadmor et al. (2016)
showed that computing distances during the training
of neural networks have negligible eﬀect on training
time. Alternatively, when using adversarial training,
additional computational cost is incurred as mentioned
above, while on the other hand fewer hyper parame-
ters are left for tuning. During test time, our method
requires carrying over the embeddings of the train-
ing data and also the computation of the knearest
neighbors for each sample.
Nearest neighbor classiﬁcation has been studied exten-
sively in the past 50 years, and consequently there are
many methods to perform either precise or approxi-
matek-nn with reduced time and space complexity (see
Gunadi (2011) for a recent empirical comparison of the
main methods). In our experiments, while using either
Condensed Nearest Neighbours (Hart, 1968) or Density
Preserving Sampling (Budka & Gabrys, 2013), we were
able to reduce the memory requirements of the train set
to5%of its original size without aﬀecting performance.
At this point the additional storage required for the
nearest neighbor step was much smaller than the size
of the networks used for classiﬁcation, and the increase
in space complexity became insigniﬁcant.
With regards to time complexity, recent studies have
shown how modern GPU’s can be used to speed up
nearest neighbor computation by orders of magnitude
(Garcia et al., 2008; Areﬁn et al., 2012). Hyvönen
et al. (2015) also showed that k-nn approximation with
99% recall can be accomplished 10-100 times faster as
compared to precise k-nn.
Combining such reductions in both space and time, we
note that even for a very large dataset, including for
example 1M images embedded in a 1K dimensional
space, the computation complexity of the knearest
neighbors for each test sample requires at most 5M
ﬂoating-point operations. This is comparable and even
muchfasterthanasingleforwardrunofthistestsample
through a modern, relatively small, ResNets (He et al.,
2016) with 2-30M parameters. Thus, our method scales

Amit Mandelbaum, Daphna Weinshall
well even for very large datasets.
2.4 Ensembles of Classiﬁers
There are many ways to deﬁne ensembles of classiﬁers,
and diﬀerent ways to put them together. Here we focus
on ensembles which are obtained when using diﬀerent
trainingparameterswithasingletrainingmethod. This
speciﬁcally means that we train several neural networks
using random initialization of the network parameters,
along with random shuﬄing of the train points.
Henceforth Regular Networks will refer to networks
that were trained only for classiﬁcation with the reg-
ular cross-entropy loss, Distance Networks will refer
to networks that were trained with the loss function
deﬁned in (2), and AT Networks will refer to networks
that were trained with adversarial examples as deﬁned
in (3).
Ensemble methods diﬀer in how they weigh the predic-
tions of diﬀerent classiﬁers in the ensemble. A number
of options are in common use (see Li et al. (2017)
for a recent review), and in accordance are used for
comparison in the experimental evaluation section: 1)
softmax average, 2) simple voting, 3) weighted softmax
average (where each softmax vector is multiplied by
its related prediction conﬁdence score), 4) conﬁdence
voting (where the most conﬁdent network getsn
2votes),
and 5) dictator voting (the decision of the most con-
ﬁdent network prevails). We evaluate methods 3 5
with weights deﬁned by either the Entropy score or the
Distance score deﬁned in (1).
2.5 Novelty Detection
Novelty detection seeks to identify points in the test set
which belong to classes not present in the train set. To
evaluate performance in this task we train a network
with a known benchmark dataset, while augmenting
the test set with test points from another dataset that
includes diﬀerent classes. Each conﬁdence score is used
to diﬀerentiate between known and unknown samples.
This is a binary classiﬁcation task, and therefore we
can evaluate performance using ROC curves.
3 Experimental Evaluation
In this section we empirically evaluate the beneﬁts of
our proposed approach, comparing the performance
of the new conﬁdence score with alternative existing
scores in the 3 diﬀerent tasks described above.
3.1 Experimental Settings
For evaluation we used 3 data sets: CIFAR-100
(Krizhevsky & Hinton, 2009), STL-10 (Coates et al.,2010) ( 3232version) and SVHN (Netzer et al., 2011).
In all cases, as is commonly done, the data was pre-
processed using global contrast normalization and ZCA
whitening. No other method of data augmentation was
used for CIFAR-100 and SVHN, while for SVHN we
also did not use the additional ˜500K labeled images2.
For STL-10, on the other hand, cropping and ﬂipping
were used for STL-10 to check the robustness of our
method to heavy data augmentation.
In our experiments, all networks used ELU (Clevert
et al., 2015) for non-linear activation. For CIFAR-100
and STL-10 we used the network suggested in Clevert
et al. (2015) with the following architecture:
C(192;5))P(2))C(192;1))C(240;3))
P(2))C(240;1))C(260;3))P(2))
C(260;1))C(280;2))P(2))C(280;1))
C(300;2))P(2))C(300;1))FC(100)
C(n;k)denotes a convolution layer with nkernels of
sizekkand stride 1. P(k)denotes a max-pooling
layer with window size kkand stride 2, and FC(n)
denotes a fully connected layer with noutput units. For
STL-10 the last layer was replaced by FC(10). During
training (only) we applied dropout (Srivastava et al.,
2014)beforeeachmaxpoolinglayer(excludingtheﬁrst)
and after the last convolution, with the corresponding
drop probabilities of [0:1;0:2;0:3;0:4;0:5].
With the SVHN dataset we used the following archi-
tecture:
C(32;3))C(32;3))C(32;3))P(2))
C(64;3))C(64;3))C(64;3))P(2))
C(128;3))C(128;3))C(128;3))P(2))
FC(128))FC(10)
For the networks trained with distance loss, for each
batch, we randomly picked pairs of points so that at
least 20% of the batch included pairs of points from
the same class. The margin min (2) was set to 25 in
all cases, and the parameter in (2) was set to 0.2.
The rest of the training parameters can be found in the
supplementary material. For the distance score we ob-
served that the number of knearest neighbors could be
set to the maximum value, which is the number of sam-
ples in each class in the train data. We also observed
that smaller numbers (even k= 50) often worked as
2Note that reported results denoted as "state-of-the-art"
for these datasets often involve heavy augmentation. In our
study, in order to be able to do the exhaustive comparisons
described below, we opted for the un-augmented scenario
as more ﬂexible and yet informative enough for the purpose
of comparison between diﬀerent methods. Therefore our
numerical results should be compared to empirical studies
which used similar un-augmented settings . We speciﬁcally
selected commonly used architectures that achieve good
performance, close to the results of modern ResNets, and
yet ﬂexible enough for extensive evaluations.

Distance-based Conﬁdence Score for Neural Network Classiﬁers
Table 1: AUC Results of Correct Classiﬁcation.
Conf.
ScoreCIFAR-100
(Classiﬁer acccuracy: 60%)STL-10
(Classiﬁer acccuracy: 70.5%)SVHN
(Accuracy: 93.5%)
Reg. Dist. AT MCD Reg. Dist. AT MCD Reg. Dist. AT
Margin 0.828 0.834 0.844 0.836 0.804 0.775 0.812 0.804 0.904 0.896 0.909
Entropy 0.833 0.837 0.851 0.833 0.806 0.786 0.816 0.810 0.916 0.907 0.918
Distance 0.7890.853 0.843 0.726 0.798 0.824 0.863 0.6710.9160.925 0.925
Table 1, legend. Leftmost column: MarginandEntropy denote the commonly used conﬁdence scores described in
Section 2.2. Distance denotes our proposed method described in Section 2.1. Second line: Reg.denotes networks trained
with the entropy loss, Dist.denotes networks trained with the distance loss deﬁned in (2), ATdenotes networks trained
with adversarial training as deﬁned in (3), and MCDdenotes MC-Dropout when applied to networks normally trained
with the entropy loss. Since the network trained for SVHN was trained without dropout, MCDwas not applicable.
Table 2: AUC Results of Correct classiﬁcation - Ensemble of 2 Networks.
Conﬁdence
ScoreCIFAR-100 STL-10 SVHN
Reg. Dist. AT Reg. Dist. AT Reg. Dist. AT
Max margin 0.840 0.846 0.856 0.802 0.792 0.814 0.909 0.901 0.911
Entropy 0.844 0.839 0.857 0.807 0.798 0.816 0.918 0.912 0.920
Distance (1) 0.775 0.863 0.862 0.815 0.834 0.866 0.916 0.924 0.926
Distance (2) 0.876 0.872 0.879 0.833 0.832 0.859 0.9180.929 0.927
Table 2, legend. Notations are similar to those described in the legend of Table 1, with one distinction: Distance (1) now
denotes the regular architecture where the distance score is computed independently for each network in the pair using its
own embedding, while Distance (2) denotes the hybrid architecture where one network in the pair is ﬁxed to be a Distance
network, and its embedding is used to compute the distance score for the prediction of the second network in the pair.
well. In general, the results reported below are not
sensitive to the speciﬁc values of the hyper-parameters
as listed above; we observed only minor changes when
changing the values of k;and the margin m.
MC-Dropout: asproposedinGal&Ghahramani(2015),
we used MC dropout in the following manner. We
trained each network as usual, but computed the pre-
dictions while using dropout during test. This was
repeated 100 times for each test example, and the
average activation was delivered as output.
Adversarial Training: we used (3) following Goodfellow
et al. (2014), ﬁxing = 0:1in all the experiments.
3.2 Error Prediction of Multi-class Labels
We ﬁrst compare the performance of our conﬁdence
score in the binary task of evaluating whether the net-
work’s predicted classiﬁcation label is correct or not.
While our results are independent of the actual accu-
racy, we note that the accuracy is comparable to those
achieved with ResNets when not using augmentation
for CIFAR-100 or when using only the regular training
data for SVHN (see Huang et al. (2016) for example).
Performance in this binary task is evaluated using ROC
curves computed separately for each conﬁdence score.Results on all three datasets can be seen in Table 1. In
all cases our proposed distance score, when computed
on a suitably trained network, achieves signiﬁcant im-
provement over the alternative scores, even when those
are enhanced by using either Adversarial Training or
MC-Dropout.
To further test our distance score we evaluate perfor-
mance over an ensemble of two networks. Results are
shown in Table 2. Here too, the distance score achieves
signiﬁcant improvement over all other methods. We
also note that the diﬀerence between the distance score
computedover Distance networks andtheentropyscore
computed over adversarially trained networks, is now
much higher as compared to this diﬀerence when using
only one network. As we show in Section 3.3, adversar-
ial training typically leads to a decreased performance
when using an ensemble of networks and relying only
on the entropy score (probably due to a decrease in vari-
ance among the classiﬁers). This observation further
supports the added value of our proposed conﬁdence
score.
As a ﬁnal note, we also used a hybrid architecture using
a matched pair of one classiﬁcation network (of any
kind) and a second Distance network . The embedding
deﬁned by the Distance network is used to compute
the distance score for the predictions of the ﬁrst clas-
siﬁcation network. Surprisingly, this method achieves

Amit Mandelbaum, Daphna Weinshall
Figure 1: Accuracy when using an ensemble of networks with CIFAR-100 (top left), STL-10 (top right) and
SVNH (bottom). The X-axis denotes the number of networks in the ensemble. Absolute accuracy (marked on
the leftY-axis) is shown for the 2 most successful ensemble methods among all the methods we had evaluated
(blue and yellow solid lines, see text), and 2 methods which did not use our distance score including the best
performing method in this set (red dotted line, denoted baseline). Diﬀerences in accuracy between the two top
performers and the top baseline method are shown using a bar plot (marked on the right Y-axis), with standard
deviation of the diﬀerence over (at least) 5 repetitions.
the best results in both CIFAR-100 and SVHN while
being comparable to the best result in STL-10. This
method is used later in Section 3.3 to improve accuracy
when running an ensemble of networks. Further inves-
tigation of this phenomenon lies beyond of the scope
of the current study.
3.3 Ensemble Methods
In order to evaluate the improvement in performance
when using our conﬁdence score to direct the integra-
tion of classiﬁers in an ensemble, we used a few common
ways to deﬁne the integration procedure, and a few
ways to construct the ensemble itself. In all compar-
isons the number of networks in the ensemble remained
ﬁxed atn. Our experiments included the following
ensemble compositions: (a) nregular networks , (b)n
distance networks , (c)nAT (Adversarially Trained)
networks , and (d-f) nnetworks such thatn
2networks
belong to one kind of networks ( regular,distance or
AT) and the remainingn
2networks belong to another
kind, spanning all 3 combinations.As described in Section 2.4, the predictions of classiﬁers
in an ensemble can be integrated using diﬀerent criteria.
In general we found that all the methods which did not
use our distance score (1), including methods which
used any of the other conﬁdence score for prediction
weighting, performed less well than a simple average
of the softmax activation (method 1 in Section 2.4).
Otherwise the best performance was obtained when
using a weighted average (method 3 in Section 2.4)
with weights deﬁned by our distance score (1). With
variants (d-f) we also checked two options of obtaining
the distance score: (i) Each network deﬁned its own
conﬁdence score; (ii) in light of the advantage demon-
strated by hybrid networks as shown in Section 3.2
and for each pair of networks from diﬀerent kinds, the
distance score for both was computed while using the
embedding of only one of networks in the pair. MC-
Dropout was not used in this section due to its high
computational cost.
While our experiments included all variants and all
weighting options, only 4 cases are shown in the fol-
lowing description of the results in order to improve

Distance-based Conﬁdence Score for Neural Network Classiﬁers
readability: 1) the combination achieving best perfor-
mance; 2) the combination achieving best performance
when not using adversarial training (as ATentails
additional computational load at train time); 3) the
ensemble variant achieving best performance without
using the distance score (baseline), 4) ensemble average
when using adversarial training without distance score.
Additional results for most of the other conditions we
tested can be found in the supplementary material. To
gain a better statistical signiﬁcance, each experiment
was repeated at least 5 times, with no overlap between
the networks.
CIFAR-100 and STL-10: Fig. 1 shows the ensem-
ble accuracy for the methods mentioned above when
using these datasets. It can be clearly seen that weight-
ing predictions based on the distance score from (1)
improves results signiﬁcantly. The best results are
achieved when combining Distance Networks andAd-
versarial Networks , with signiﬁcant improvement over
an ensemble of only one kind of networks (not shown
in the graph). Still, we note importantly that the dis-
tance score is used to weight bothkind of networks.
Since Adversarial Training is not always applicable
due to its computational cost at train time, we show
that the combination of Distance networks andRegular
networks can also lead to signiﬁcant improvement in
performance when using the distance score and the
hybrid architecture described in Section 3.2. Finally
we note that Adversarial networks alone achieve very
poor results when using the original ensemble aver-
age, further demonstrating the value of the distance
score in improving the performance of an ensemble of
Adversarial networks alone.
SVHN: Results for this dataset are also shown in Fig.1.
While not as signiﬁcant as those in the other datasets
(partly due to the high initial accuracy), they are still
consistent with them, demonstrating again the power
and robustness of the distance score.
3.4 Novelty Detection
Finally, we compare the performance of the diﬀerent
conﬁdence scores in the task of novelty detection. In
this task the conﬁdence score is used to decide another
binary classiﬁcation problem: does the test example be-
long to the set of classes the networks had been trained
on, or rather to some unknown class? Performance in
this binary classiﬁcation task is evaluated using the
corresponding ROC curve of each conﬁdence score.
Weusedtwocontriveddatasetstoevaluateperformance
in this task, following the experimental construction
suggested in Lakshminarayanan et al. (2016). In the
ﬁrst experiment, we trained the network on the STL-10
dataset, and then tested it on both STL-10 and SVHN
test sets. In the second experiment we switched be-tween the datasets (and changed the trained network)
making SVHN the known dataset and STL-10 the
novel one. The task requires to discriminate between
the known and the novel datasets. For comparison we
computed novelty, as one often does, with a one-class
SVM classiﬁer while using the same embeddings. Nov-
elty thus computed showed much poorer performance,
possibly because this dataset involves many classes
(one class SVM is typically used with a single class),
and therefore these results are not included here.
Table 3: AUC Results for Novelty Detection.
Conﬁde.
ScoreSTL-10/SVHN SVHN/STL-10
Reg. Dist. AT Reg. Dist. AT
Max
Margin.808 .849 .860 .912 .922 .985
Entropy .810 .857 .870 .917 .933 .992
Distance .798 .870 .901.904 .934 .996
Table 3, legend. Left: STL-10 (known) and SVHN (novel).
Right: SVHN (known) and STL-10 (novel).
Results are shown in Table 3. Adversarial training,
which was designed to handle this sort of challenge,
is not surprisingly the best performer. Nevertheless,
we see that our proposed conﬁdence score improves
the results even further, again demonstrating its added
value.
4 Conclusions
We proposed a new conﬁdence score for multi-class
neural network classiﬁers. The method we proposed
to compute this score is scalable, simple to implement,
and can ﬁt any kind of neural network. This method
is diﬀerent from other commonly used methods as it is
based on measuring the point density in the eﬀective
embedding space of the network, thus providing a more
coherent statistical measure for the distribution of the
network’s predictions.
We also showed that suitable embeddings can be
achieved by using either a distance-based loss or, some-
what unexpectedly, Adversarial Training. We demon-
strated the superiority of the new score in a number
of tasks. Those tasks were evaluated using a number
of diﬀerent datasets and with task-appropriate net-
work architectures. In all tasks our proposed method
achieved the best results when compared to traditional
conﬁdence scores.
References
Areﬁn, Ahmed Shamsul, Riveros, Carlos, Berretta,
Regina, and Moscato, Pablo. Gpu-fs-k nn: A soft-

Amit Mandelbaum, Daphna Weinshall
ware tool for fast and scalable k nn computation
using gpus. PloS one , 7(8):e44000, 2012.
Bauer, Eric and Kohavi, Ron. An empirical comparison
ofvotingclassiﬁcationalgorithms: Bagging, boosting,
and variants. Machine learning , 36(1-2):105–139,
1999.
Budka, Marcin and Gabrys, Bogdan. Density-
preserving sampling: robust and eﬃcient alternative
to cross-validation for error estimation. IEEE trans-
actions on neural networks and learning systems , 24
(1):22–34, 2013.
Clevert, Djork-Arné, Unterthiner, Thomas, andHochre-
iter, Sepp. Fast and accurate deep network learning
by exponential linear units (elus). arXiv preprint
arXiv:1511.07289 , 2015.
Coates, Adam, Lee, Honglak, and Ng, Andrew Y. An
analysis of single-layer networks in unsupervised fea-
ture learning. Ann Arbor , 1001(48109):2, 2010.
Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., and
Fei-Fei, L. ImageNet: A Large-Scale Hierarchical
Image Database. In CVPR09 , 2009.
Dietterich, Thomas G. Ensemble methods in machine
learning. In International workshop on multiple clas-
siﬁer systems , pp. 1–15. Springer, 2000.
Donahue, Jeﬀrey, Anne Hendricks, Lisa, Guadarrama,
Sergio, Rohrbach, Marcus, Venugopalan, Subhashini,
Saenko, Kate, and Darrell, Trevor. Long-term re-
current convolutional networks for visual recognition
and description. In Proceedings of the IEEE confer-
ence on computer vision and pattern recognition , pp.
2625–2634, 2015.
Gal, Yarin and Ghahramani, Zoubin. Dropout as
a bayesian approximation: Representing model
uncertainty in deep learning. arXiv preprint
arXiv:1506.02142 , 2, 2015.
Garcia, Vincent, Debreuve, Eric, and Barlaud, Michel.
Fast k nearest neighbor search using gpu. In Com-
puter Vision and Pattern Recognition Workshops,
2008. CVPRW’08. IEEE Computer Society Confer-
ence on, pp. 1–6. IEEE, 2008.
Goodfellow, Ian J, Shlens, Jonathon, and Szegedy,
Christian. Explaining and harnessing adversarial
examples. arXiv preprint arXiv:1412.6572 , 2014.
Gunadi, Hendra. Comparing nearest neighbor algo-
rithms in high-dimensional space. 2011.
Hadsell, Raia, Chopra, Sumit, and LeCun, Yann. Di-
mensionality reduction by learning an invariant map-
ping. In Computer vision and pattern recognition,
2006 IEEE computer society conference on , volume 2,
pp. 1735–1742. IEEE, 2006.Hart, Peter. The condensed nearest neighbor rule
(corresp.). IEEE transactions on information theory ,
14(3):515–516, 1968.
He, Kaiming, Zhang, Xiangyu, Ren, Shaoqing, andSun,
Jian. Deep residual learning for image recognition.
InProceedings of the IEEE conference on computer
vision and pattern recognition , pp. 770–778, 2016.
Hoﬀer, Elad and Ailon, Nir. Deep metric learning
using triplet network. In International Workshop
on Similarity-Based Pattern Recognition , pp. 84–92.
Springer, 2015.
Hu, Hexiang, Zhou, Guang-Tong, Deng, Zhiwei, Liao,
Zicheng, and Mori, Greg. Learning structured infer-
ence neural networks with label relations. In Proceed-
ings of the IEEE Conference on Computer Vision
and Pattern Recognition , pp. 2960–2968, 2016.
Huang, Gao, Sun, Yu, Liu, Zhuang, Sedra, Daniel, and
Weinberger, Kilian Q. Deep networks with stochastic
depth. In European Conference on Computer Vision ,
pp. 646–661. Springer, 2016.
Hyvönen, Ville, Pitkänen, Teemu, Tasoulis, Sotiris,
Jääsaari, Elias, Tuomainen, Risto, Wang, Liang,
Corander, Jukka, and Roos, Teemu. Fast k-nn search.
arXiv preprint arXiv:1509.06957 , 2015.
Krizhevsky, Alex and Hinton, Geoﬀrey. Learning mul-
tiple layers of features from tiny images. 2009.
Lakshminarayanan, Balaji, Pritzel, Alexander, and
Blundell, Charles. Simple and scalable predictive
uncertainty estimation using deep ensembles. arXiv
preprint arXiv:1612.01474 , 2016.
Li, Hui, Wang, Xuesong, and Ding, Shifei. Research
and development of neural network ensembles: a
survey.Artiﬁcial Intelligence Review , pp. 1–25, 2017.
MacKay, David JC. Bayesian methods for adaptive
models. PhD thesis, California Institute of Technol-
ogy, 1992.
Markou, Markos and Singh, Sameer. Novelty detection:
a review—part 2:: neural network based approaches.
83(12):2499–2521, 2003.
Miyato, Takeru, Dai, Andrew M, and Goodfellow, Ian.
Adversarial training methods for semi-supervised
text classiﬁcation. arXiv preprint arXiv:1605.07725 ,
2016.
Neal, Radford M. Bayesian learning for neural net-
works, volume 118. Springer Science & Business
Media, 2012.
Netzer, Yuval, Wang, Tao, Coates, Adam, Bissacco,
Alessandro, Wu, Bo, and Ng, Andrew Y. Reading
digits in natural images with unsupervised feature
learning. In NIPS workshop on deep learning and
unsupervised feature learning , volume 2011, pp. 5,
2011.

Distance-based Conﬁdence Score for Neural Network Classiﬁers
Palatucci, Mark, Pomerleau, Dean, Hinton, Geoﬀrey E,
and Mitchell, Tom M. Zero-shot learning with seman-
tic output codes. In Advances in neural information
processing systems , pp. 1410–1418, 2009.
Pimentel, Marco AF, Clifton, David A, Clifton, Lei,
andTarassenko, Lionel. Areviewofnoveltydetection.
Signal Processing , 99:215–249, 2014.
Salakhutdinov, Ruslan and Hinton, Geoﬀrey E. Learn-
ing a nonlinear embedding by preserving class neigh-
bourhood structure. In AISTATS , volume 11, 2007.
Schroﬀ, Florian, Kalenichenko, Dmitry, and Philbin,
James. Facenet: A uniﬁed embedding for face recog-
nition and clustering. In Proceedings of the IEEE
Conference on Computer Vision and Pattern Recog-
nition, pp. 815–823, 2015.
Sharif Razavian, Ali, Azizpour, Hossein, Sullivan,
Josephine, and Carlsson, Stefan. Cnn features oﬀ-
the-shelf: an astounding baseline for recognition. In
Proceedings of the IEEE Conference on Computer
Vision and Pattern Recognition Workshops , pp. 806–
813, 2014.
Srivastava, Nitish, Hinton, Geoﬀrey E, Krizhevsky,
Alex, Sutskever, Ilya, and Salakhutdinov, Ruslan.
Dropout: a simple way to prevent neural networks
from overﬁtting. Journal of Machine Learning Re-
search, 15(1):1929–1958, 2014.
Szegedy, Christian, Zaremba, Wojciech, Sutskever, Ilya,
Bruna, Joan, Erhan, Dumitru, Goodfellow, Ian, and
Fergus, Rob. Intriguingpropertiesofneuralnetworks.
arXiv preprint arXiv:1312.6199 , 2013.
Tadmor, Oren, Rosenwein, Tal, Shalev-Shwartz, Shai,
Wexler, Yonatan, and Shashua, Amnon. Learning
a metric embedding for face recognition using the
multibatch method. In Advances In Neural Informa-
tion Processing Systems , pp. 1388–1389, 2016.
Tibshirani, Robert. A comparison of some error esti-
mates for neural network models. Neural Computa-
tion, 8(1):152–163, 1996.
Vinokurov, Nomi and Weinshall, Daphna. Novelty
detection in multiclass scenarios with incomplete
set of class labels. arXiv preprint arXiv:1604.06242 ,
2016.
Weston, Jason, Ratle, Frédéric, Mobahi, Hossein, and
Collobert, Ronan. Deep learning via semi-supervised
embedding. In Neural Networks: Tricks of the Trade ,
pp. 639–655. Springer, 2012.
Zaragoza, Hugo and d’Alché Buc, Florence. Conﬁdence
measures for neural network classiﬁers. In Proceed-
ings of the Seventh Int. Conf. Information Processing
and Management of Uncertainty in Knowlegde Based
Systems, 1998.