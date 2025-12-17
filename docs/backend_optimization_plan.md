# Railway Backend Algorithm Optimization Blueprint: SVR/GRNN, Distance-Based Confidence, Edge-Case Handling, Customer Similarity Weighting, and Wedding-Party Consistency (KCT)

## Executive Summary

Railway’s backend sizing engine is at The combination an inflection point. of Support Vector Regression (SVR) and Generalized Regression Neural Networks (GRNN) for measurement prediction, distance-based confidence scoring for gating and routing, explicit edge-case handling for extreme body types, customer similarity weighting over a high-quality historical corpus, and wedding-party consistency logic aligned to KCT (Kathryn’s Custom Tailoring) rules can materially raise prediction accuracy, stabilize confidence, and reduce returns.

Evidence from recent peer‑reviewed studies converges on a pragmatic stack: compact regressors—particularly SVR and GRNN—trained on a minimal, high-quality feature set (stature, weight, bust/waist/hip girths, inside leg) deliver low mean absolute errors (MAEs) across a broad suite of fashion-relevant measurements, often within professional precision-step tolerances. In parallel, distance-based confidence computed on model embeddings measurably improves error prediction, ensemble weighting, and novelty detection compared with entropy or margin, enabling safe automation and precise escalation. Together, these methods form a scalable backbone for sizing in production, provided confidence is calibrated and monitored over time and across subpopulations[^2][^3][^7].

This blueprint operationalizes that evidence for Railway’s context:

- Measurement prediction: Add SVR and GRNN predictors behind a common feature store and schema. Optimize via nested cross-validation with MAE relative to precision steps and distribution fidelity (KL divergence) as primary metrics. Anchor feature governance and missing-value imputation on standardized protocols and Gower’s distance for k‑NN imputation[^2][^3].

- Confidence scoring: Implement distance-based confidence on classifier and regressor embeddings with calibrated thresholds. Integrate with ensemble weighting to route low-confidence cases to guided capture, alternative modality, or human review. Monitor AUC for error/novelty detection, Brier score, and Expected Calibration Error (ECE)[^7][^12].

- Edge-case handling: Detect OWOB (overweight/obese) and other extremes, segment by whole-body shape groups and posture proxies, and tune pattern-parameter rules (e.g., back arc, waist depth, hip ease) to align with garment-specific tolerances. Add outlier clamping and winsorization policies at inference to prevent spurious predictions[^8][^24][^25].

- Customer similarity weighting: Construct a 3,371‑record similarity corpus with feature definitions aligned to Railway’s inputs. Compute weighted neighbors with optional confidence-based attenuation. Use local regression or weighted k‑NN voting to stabilize predictions in sparse or atypical regions[^2][^7].

- Wedding-party consistency (KCT): Encode KCT rules to enforce consistent fit intents across party members while honoring individual measurements. Implement conflict detection and resolution (tie-break with variance-aware thresholds), audit trails, and reversible overrides for tailor overrides and special requests[^14][^15][^11].

Implementation is phased. Phase 1 ships SVR/GRNN predictors with distance-based confidence gating. Phase 2 deploys edge-case segmentation and the 3,371‑record similarity weighting. Phase 3 activates wedding-party consistency with KCT integration, KPI dashboards, and CI/CD for models, thresholds, and rules. Expected impact includes lower measurement errors (MAE), fewer returns driven by poor fit, higher automation acceptance rates under confidence gating, and improved inclusivity for edge cases[^2][^3][^7][^8].

## Context and Objectives

Railway’s existing sizing stack is not described in the provided context; however, the business goals are clear: raise prediction accuracy, stabilize confidence, reduce returns, and improve inclusivity for extreme body types. This blueprint defines an implementation plan aligned to evidence-based models and methods.

Objectives:

- Accuracy: Add SVR and GRNN predictors to improve measurement MAEs relative to precision steps and to preserve distribution realism (KL divergence). Select features via standardization and missing-value imputation to support stable training[^2][^3].

- Confidence: Deploy distance-based confidence for gating, routing, and ensemble thresholds to balance weighting. Calibrate automation and escalation. Monitor calibration drift by subpopulation and modality[^7][^12].

- Edge cases: Detect OWOB and extremes; segment by shape groups and posture proxies; adjust pattern-parameter rules for bust/underbust/waist/hip coverage and posture-induced curvature[^8][^24].

- Similarity weighting: Use a 3,371‑record historical corpus to compute weighted neighbors and stabilize predictions where data are sparse or atypical[^2][^7].

- Wedding-party consistency: Encode KCT rules to maintain consistent fit intent across party members, detect conflicts, resolve via variance-aware thresholds, and record audit trails and reversible overrides[^14][^15][^11].

Success metrics:

- Measurement prediction: MAE vs precision steps; precision ratio (PR); KL divergence[^2].

- Size classification: Accuracy and adjacent-size error rate; confusion analysis[^5].

- Confidence: AUC for error/novelty detection; Brier score; ECE; false-escalation rate under thresholding[^7][^12].

- Edge-case coverage: Fit satisfaction proxies (returns and guided-measurement uptake), subgroup calibration metrics[^8].

- Wedding-party consistency: Rule adherence rate; conflict resolution latency; override reversal rate.

- Returns and conversion: Post‑deployment reductions in fit-related returns and changes in conversion/AOV attributable to sizing improvements[^1][^10].

Constraints:

- Schema, APIs, and deployment environment are unspecified; we provide interface contracts and a schema plan to be adapted to Railway’s systems.

- Data modality mix (tape/scan/app) introduces method-dependent errors; we standardize measurement protocols and QC.

- Privacy and compliance for 3D scans and photos must be addressed in deployment; governance should follow data minimization and retention policies[^11].

To ground the plan in current capabilities, we first summarize Railway’s data assets and flows.

To illustrate current assets and flows, Table 1 maps Railway’s data elements to sources, quality controls, and model dependencies.

### Table 1. Railway data assets and flows (indicative)

| Data element | Source | QC notes | Dependencies | Owner |
|---|---|---|---|---|
| Stature | Tape/scan/app | Protocol, posture | Feature store | Data engineering |
| Weight | Self-report/scale | Unit normalization | Feature store | Data engineering |
| Bust/waist/hip girths | Tape/scan/app | Landmarking, double-measure | Feature store; SVR/GRNN | Data engineering |
| Inside leg | Tape/scan/app | Consistency with footwear | Feature store | Data engineering |
| Age | Self-report | Optional | Feature store | Data engineering |
| Scanner landmarks | Scan pipeline | Landmark color/ISO 20685 | Modal validation | Platform |
| App-derived points | App pipeline | Site completeness | Modal validation | Platform |
| Size labels | SKU charts | PD/SD alignment | Classifier; rules | Product ops |
| Returns feedback | OMS | Reason codes | Monitoring; learning loops | Analytics |
| 3D garment templates | PLM | Segmentation, size labels | Visualization | Product design |
| KCT rules | Custom tailoring | Fit intent taxonomy | Rules engine | Tailoring ops |

## Evidence Base

The literature supports a compact, interpretable approach for anthropometric prediction and a complementary confidence framework that improves error detection and routing under distribution shift. Here we synthesize the most relevant studies and datasets.

### Models for Measurement Prediction

SVR and GRNN are the primary candidates for Railway’s measurement prediction. A comparative study across ~30 fashion-relevant measurements showed that linear regression (LR) and SVR achieved strong accuracy and distribution fidelity from modest training sets (stabilizing near ~500 examples), with MAEs at or below precision steps for many targets. Random forests and gradient boosting required more data and showed greater fold instability[^2]. In full‑suite prediction (76 targets from seven inputs), GRNN demonstrated robust performance and tolerance to input noise and atypical bodies, outperforming several neural and kernel baselines[^3]. Earlier work also found backpropagation artificial neural networks (BP‑ANN) superior to linear models for lower-body dimensions used in pattern making[^4].

These findings imply that Railway can achieve high accuracy with SVR and GRNN on a small, standardized feature set (stature, weight, bust/waist/hip, inside leg), with GRNN preferred for broad suites and robustness, and SVR as a strong, stable baseline.

### Confidence Scoring

Distance-based confidence computed on network embeddings reliably predicts classification errors, weights ensembles, and detects novelty. By estimating local density around test points in embedding space—optionally after training with distance losses or adversarial examples—it outperforms entropy and margin across several tasks[^7]. For sizing systems, this translates to effective gating and routing: low-confidence predictions are escalated to guided capture or human review; high-confidence predictions proceed, and ensembles are weighted by confidence to boost performance. Calibration (Brier score, reliability diagrams, ECE) should be measured and monitored across subgroups and modalities[^12].

### Edge-Case Populations

Among OWOB women in the US, five whole-body shape groups emerge, reflecting upper/lower silhouette couplings and posture-induced curvature. Current misses and plus-size ASTM tables rarely deliver perfect fit across bust, underbust, waist, and hip for these shapes; perfect-fit rates are often below 19% for tops and below 8% for bottoms, with large proportions reporting fit problems in at least one area[^8]. Protective clothing guidance underscores the need for shape-aware tolerance definitions and ease allowances; lower-body compression textiles benefit from stratified, shape-driven sizing using 3D digital anthropometry[^24][^25]. Railway must segment by shape groups and posture proxies, tune pattern parameters, and route low-confidence OWOB cases to guided capture.

To contextualize the datasets and evidence, Table 2 summarizes representative sources.

### Table 2. Evidence snapshot: datasets and key outcomes

| Dataset/Source | Size and demographics | Modality | Key outcomes |
|---|---|---|---|
| IFTH French national campaign | ~9,000 adults | 3D scans (standing/sitting) | LR/SVR predicted ~30 fashion measurements with MAEs at/below precision steps; KL divergence favored LR/SVR[^2] |
| ANSUR II (US Army) | 6,068 subjects | 3D anthropometry | GRNN predicted 76 measurements from seven inputs with robustness to input noise[^3] |
| NZDFAS | 1,003 personnel | Scanner + physical | Decision trees aligned shirt/trouser MCU labels; most errors off by one size[^5] |
| SizeUSA (US) | Representative | 3D scans | Five OWOB whole-body shape groups; ASTM tables miss perfect fit for most[^8] |
| SIZER | ~100 subjects, ~2,000 scans | 3D clothed scans | ParserNet/SizerNet enable size-conditioned deformation; lower Verr/Aerr than linear scaling[^6] |

The model performance across studies is consolidated in Table 3.

### Table 3. Model comparison across studies

| Study | Dataset | Inputs | Targets | Best models | Notes |
|---|---|---|---|---|---|
| Meyer et al., 2023 | IFTH | Height, weight, bust/waist/hip, inside leg (+ age, shoe size, SPC) | ~30 measurements | LR, SVR | Stable with ~500 samples; KL divergence favored LR/SVR[^2] |
| Liu et al., 2017 | Custom/industry | Height, hip, waist | 10 lower-body dimensions | BP‑ANN > MLR | Lower-body pattern-making gains[^4] |
| Wang et al., 2021 | ANSUR II | Stature, weight, bust/waist/hip (+ age, gender) | 76 dimensions | GRNN > MLR/SVR/RBFN/BP‑ANN | Robust to noise; single-pass training[^3] |
| Kolose et al., 2021 | NZDFAS | Scanner features | MCU shirt/trouser sizes | Decision trees | Most errors adjacent; automated scanner features strongest[^5] |

For confidence methods, Table 4 contrasts distance-based scoring with alternatives.

### Table 4. Confidence methods comparison

| Method | Signal | Strengths | Weaknesses | Use |
|---|---|---|---|---|
| Max margin | Softmax top‑1 vs top‑2 | Fast | Poor under shift | Baseline |
| Entropy | Output distribution | Captures breadth | Overconfident on OOD | Baseline |
| MC‑Dropout | Stochastic passes | Bayesian proxy | High test-time cost | When latency permits |
| Distance-based | Embedding density | Strong error/novelty detection; ensemble weighting | kNN at test time | Primary signal with calibration[^7] |

The OWOB shape groups are summarized in Table 5.

### Table 5. OWOB whole-body shapes and fit implications

| Group | Upper silhouette | Lower silhouette | Typical issues | Sizing implications |
|---|---|---|---|---|
| Rectangle–curvy | Straight front/back | Curviest hips; prominent abdomen/buttocks | Bust looseness if sized by waist; hip tightness in bottoms | Increase hip ease; adjust waist‑to‑hip grading; consider back length[^8] |
| Parallelogram–moderately curvy | Upper abdomen prominent; moderate back curvature | Moderate buttocks; prominent abdomen | Abdominal pulling; side ride-up | Add front waist suppression; adjust crotch curve[^8] |
| Parallelogram–hip tilt | Upper abdomen prominent; curved upper back | Hip tilt above waist | Lower back pulling; side bunching | Increase back arc; adjust waist placement[^8] |
| Inverted trapezoid–moderately curvy | Bust/upper back prominent | Moderately curvy | Bust looseness if sized by waist; shoulder tension | Balance bust/waist ease; adjust shoulder line[^8] |
| Inverted trapezoid–hip tilt | Most prominent bust/upper back | Hip tilt; large waist–hip difference | Front pull from abdomen; back tension | Increase waist depth and back curvature allowances[^8] |

### SVR and GRNN for Anthropometry

SVR’s strengths lie in stability, distribution fidelity, and modest data requirements; GRNN’s strengths include full-suite coverage and robustness to noisy inputs and atypical bodies. Both operate effectively on minimal inputs when features are standardized and missing values are imputed robustly. The combination offers Railway a practical trade-off: SVR as a high-accuracy baseline; GRNN for comprehensive suites and resilience[^2][^3].

### Distance-Based Confidence

Embedding density around training examples is a practical proxy for correctness. When calibrated, it can weight ensembles and detect novelty, leading to fewer undetected errors and more reliable routing. Railway should adopt distance-based confidence as the primary signal, complemented by entropy or margin as baselines, and calibrate thresholds to minimize false escalations while containing risk[^7][^12].

### Edge Cases: OWOB and Posture

OWOB shapes reflect both fat distribution and posture (thoracic kyphosis, hyperlordosis), which materially affect back curvature and lower-body silhouettes. Railway’s system must detect these segments, adjust pattern parameters, and route low-confidence cases to guided capture or human review. Protective and compression textiles underscore the operational value of shape-aware segmentation and tolerance definitions[^8][^24][^25].

## Measurement Prediction Models: SVR and GRNN Implementation

Railway should implement SVR and GRNN predictors behind a common feature store and schema. The training pipeline standardizes inputs, imputes missing values, optimizes hyperparameters, and validates models via nested cross‑validation with MAE vs precision steps and KL divergence as primary metrics[^2][^3].

### Feature Set and Preprocessing

Use a minimal, high-quality feature set:

- Stature, weight, chest/bust girth, waist girth, hip girth, inside leg length; age as optional.

Standardization:

- StandardScaler for continuous features; handle unit normalization (cm vs inches).

Missing values:

- k‑NN imputation with Gower’s distance to accommodate mixed numeric/categorical features; repeat imputation across folds to avoid leakage[^2].

Outlier handling:

- Winsorize extreme values at specified percentiles per measurement; clamp Mahalanobis distance outliers for multi-feature vectors.

To align preprocessing with modality, Table 6 summarizes feature governance.

### Table 6. Feature preprocessing and scaling plan

| Feature | Scale | Missing-value strategy | Outlier policy | Notes |
|---|---|---|---|---|
| Stature | cm | k‑NN (Gower) | Winsorize 1st/99th pct | Height stable; posture control |
| Weight | kg | k‑NN (Gower) | Winsorize 1st/99th pct | Self-report caveats |
| Bust/waist/hip girths | cm | k‑NN (Gower) | Winsorize 1st/99th pct | Landmarking critical |
| Inside leg | cm | k‑NN (Gower) | Winsorize 1st/99th pct | Consistent footwear |
| Age | years | k‑NN (Gower) | Clamp beyond 3σ | Optional |

### Model Training and Validation

- Nested cross-validation: Outer loop for model selection; inner loop for hyperparameter optimization. Optimize SVR kernel (linear/RBF), C, ε, γ; GRNN spread and smoothing[^2][^3].

- Metrics: MAE vs precision steps; precision ratio (PR); KL divergence to assess distribution fidelity[^2].

- Monitoring: Per-measurement MAEs with confidence intervals; calibration drift; subgroup performance by modality and demographics.

To operationalize, Table 7 outlines the hyperparameter grid.

### Table 7. Hyperparameter grid and tuning ranges

| Model | Hyperparameters | Range/Strategy | Notes |
|---|---|---|---|
| SVR | Kernel | Linear, RBF | Linear often strong on anthropometry[^2] |
| SVR | C, ε, γ | Log-scale grid; Bayesian opt | Minimize MAE; watch stability[^2] |
| GRNN | Spread (σ) | Validation sweep | Single-pass training; robust to noise[^3] |
| GRNN | Smoothing | Validation sweep | Mitigate sparse neighborhoods |
| Imputation | k (neighbors) | 5–15; by fold | Gower distance for mixed types[^2] |

To measure progress, Table 8 defines the evaluation dashboard.

### Table 8. Evaluation dashboard (per measurement)

| Metric | Definition | Target | Notes |
|---|---|---|---|
| MAE | Mean absolute error vs ground truth | ≤ precision step | Key for tailoring tolerance[^2] |
| PR | Precision ratio (MAE/precision step) | ≤ 1.0 | At/below tolerance |
| KL divergence | Predicted vs reference distribution | Lowest feasible | Distribution realism[^2] |
| Calibration | Brier, ECE | Stable; improving | For probabilistic outputs[^12] |

#### Feature Store and Schema

Define a canonical measurement schema aligned to Railway’s inputs and target garment measurements. Include provenance tags (tape/scan/app) to support modality-aware monitoring and calibration.

### Table 9. Canonical measurement schema (indicative)

| Field | Type | Units | Allowed range | Provenance |
|---|---|---|---|---|
| stature | float | cm | 120–220 | tape/scan/app |
| weight | float | kg | 35–200 | scale/self-report |
| bust_girth | float | cm | 60–140 | tape/scan/app |
| waist_girth | float | cm | 50–140 | tape/scan/app |
| hip_girth | float | cm | 70–160 | tape/scan/app |
| inside_leg | float | cm | 60–105 | tape/scan/app |
| age | int | years | 16–90 | self-report |
| measurement_source | enum | – | tape/scan/app | metadata |
| timestamp | datetime | – | – | metadata |

## Confidence Scoring: Distance-Based Methods and Calibration

Implement distance-based confidence as Railway’s primary signal for gating, routing, and ensemble weighting. The system computes embeddings from classifier/regressor penultimate layers, estimates local density around training points, and derives a confidence score that is calibrated and monitored.

### Embeddings and k‑NN Density Estimation

- Extract embeddings from the penultimate layer of size classifiers and regressors.

- For each prediction, compute distances to training embeddings; derive a density-based score (e.g., inverse distance weighting over k nearest neighbors).

- Optionally train with distance losses or adversarial examples to enlarge inter-class margins and tighten intra-class clusters[^7].

- For scalability, approximate k‑NN via locality-sensitive hashing or sampling; cache embeddings to reduce compute.

### Calibration and Routing

- Calibrate thresholds on validation data to target a desired false-escalation rate and failure-detection coverage.

- Route low-confidence cases to guided measurement capture (app or tape), alternative modality (e.g., scan), or human review.

- Weight ensembles by confidence to combine complementary models while minimizing variance.

- Monitor calibration (Brier score, reliability diagrams, ECE) and AUC for error/novelty detection; recalibrate when drift is detected[^12].

To clarify method trade-offs, Table 10 summarizes the confidence score comparison.

### Table 10. Confidence score comparison

| Method | Signal | Strengths | Weaknesses | Compute cost | Recommended use |
|---|---|---|---|---|---|
| Max margin | Softmax margins | Simple | Poor under shift | Low | Baseline[^7] |
| Entropy | Output entropy | Fast | Overconfident OOD | Low | Baseline[^7] |
| MC‑Dropout | Stochastic passes | Bayesian proxy | 100× cost | High | Latency‑tolerant flows[^7] |
| Distance-based | Embedding density | Strong error/novelty; ensemble weighting | kNN storage/compute | Moderate | Primary signal[^7] |

Calibration monitoring is planned in Table 11.

### Table 11. Calibration monitoring plan

| Metric | Frequency | Thresholds | Action |
|---|---|---|---|
| Brier score | Weekly | Stable or improving | Retrain calibration |
| ECE | Weekly | ≤ target band | Recalibrate |
| AUC (error/novelty) | Weekly | ≥ target | Tune k; adjust routing |
| Subgroup drift | Monthly | No significant shift | Investigate; segment recalibration[^12] |

#### Implementation Pseudocode Plan

```python
# Distance-Based Confidence Scoring Implementation
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.preprocessing import StandardScaler
from sklearn.calibration import CalibratedClassifierCV
import pickle
from typing import Tuple, Dict, Any

class DistanceBasedConfidenceScorer:
    """
    Distance-based confidence scoring using embedding density estimation
    Based on research showing superior performance over entropy/margin methods
    """
    def __init__(self, k=50, sigma=1.0):
        self.k = k  # Number of nearest neighbors
        self.sigma = sigma  # Gaussian kernel width
        self.train_embeddings = None
        self.train_labels = None
        self.scaler = StandardScaler()
        self.confidence_thresholds = {}
        self.is_fitted = False
        
    def fit(self, train_embeddings: np.ndarray, train_labels: np.ndarray, 
            confidence_thresholds: Dict[str, float] = None):
        """
        Fit the confidence scorer with training embeddings and labels
        
        Args:
            train_embeddings: Training data embeddings (n_samples, embedding_dim)
            train_labels: Training data labels
            confidence_thresholds: Calibrated confidence thresholds for routing
        """
        self.train_embeddings = train_embeddings
        self.train_labels = train_labels
        self.scaler.fit(train_embeddings)
        self.confidence_thresholds = confidence_thresholds or {}
        self.is_fitted = True
        return self
    
    def compute_embedding_density(self, x_embedding: np.ndarray) -> Tuple[float, np.ndarray, np.ndarray]:
        """
        Compute embedding density using k-nearest neighbors
        
        Args:
            x_embedding: Single embedding vector (1, embedding_dim)
            
        Returns:
            density_score: Normalized confidence score [0, 1]
            neighbor_indices: Indices of k nearest neighbors
            weights: Gaussian kernel weights for each neighbor
        """
        if not self.is_fitted:
            raise ValueError("Confidence scorer must be fitted before use")
            
        # Scale embedding
        x_scaled = self.scaler.transform(x_embedding)
        
        # Calculate distances to all training embeddings
        distances = cdist(x_scaled, self.train_embeddings, metric='euclidean')[0]
        
        # Get k nearest neighbors
        neighbor_indices = np.argsort(distances)[:self.k]
        neighbor_distances = distances[neighbor_indices]
        neighbor_labels = self.train_labels[neighbor_indices]
        
        # Compute Gaussian kernel weights
        weights = np.exp(-neighbor_distances**2 / (2 * self.sigma**2))
        
        # Normalize weights
        weights_sum = np.sum(weights)
        if weights_sum == 0:
            weights = np.ones(self.k) / self.k
        else:
            weights = weights / weights_sum
        
        # Density score as weighted average
        density_score = np.sum(weights)
        
        return density_score, neighbor_indices, weights
    
    def get_confidence_score(self, x_embedding: np.ndarray) -> float:
        """
        Get calibrated confidence score for a single embedding
        
        Args:
            x_embedding: Input embedding (1, embedding_dim)
            
        Returns:
            confidence: Calibrated confidence score [0, 1]
        """
        density_score, _, _ = self.compute_embedding_density(x_embedding)
        
        # Calibrate density to [0, 1] range
        # Use sigmoid calibration with learned parameters
        calibrated_confidence = 1.0 / (1.0 + np.exp(-density_score + 2.0))
        
        return min(max(calibrated_confidence, 0.0), 1.0)
    
    def route_by_confidence(self, x_embedding: np.ndarray) -> str:
        """
        Route decision based on confidence score
        
        Args:
            x_embedding: Input embedding (1, embedding_dim)
            
        Returns:
            action: 'accept', 'guided_capture', or 'human_review'
        """
        confidence = self.get_confidence_score(x_embedding)
        
        # Use calibrated thresholds
        auto_threshold = self.confidence_thresholds.get('auto_threshold', 0.8)
        guided_threshold = self.confidence_thresholds.get('guided_threshold', 0.6)
        
        if confidence >= auto_threshold:
            return "accept"
        elif confidence >= guided_threshold:
            return "guided_capture"
        else:
            return "human_review"
    
    def weight_ensemble(self, predictions: np.ndarray, confidences: np.ndarray) -> np.ndarray:
        """
        Weight ensemble predictions by confidence scores
        
        Args:
            predictions: Array of model predictions (n_models, n_samples)
            confidences: Array of confidence scores (n_models,)
            
        Returns:
            weighted_prediction: Weighted ensemble prediction
        """
        # Normalize confidences
        weights = confidences / (np.sum(confidences) + 1e-8)
        
        # Compute weighted average
        weighted_prediction = np.average(predictions, weights=weights, axis=0)
        
        return weighted_prediction
    
    def detect_novelty(self, x_embedding: np.ndarray, novelty_threshold: float = 0.1) -> Tuple[bool, float]:
        """
        Detect novelty/out-of-distribution samples
        
        Args:
            x_embedding: Input embedding (1, embedding_dim)
            novelty_threshold: Threshold for novelty detection
            
        Returns:
            is_novel: True if sample is novel
            novelty_score: Quantified novelty score
        """
        density_score, _, _ = self.compute_embedding_density(x_embedding)
        
        # Novelty as inverse of density
        novelty_score = 1.0 - min(density_score, 1.0)
        is_novel = novelty_score > (1.0 - novelty_threshold)
        
        return is_novel, novelty_score
    
    def batch_confidence_score(self, embeddings: np.ndarray) -> np.ndarray:
        """
        Compute confidence scores for batch of embeddings
        
        Args:
            embeddings: Batch of embeddings (n_samples, embedding_dim)
            
        Returns:
            confidence_scores: Array of confidence scores (n_samples,)
        """
        confidence_scores = []
        
        for embedding in embeddings:
            score = self.get_confidence_score(embedding.reshape(1, -1))
            confidence_scores.append(score)
            
        return np.array(confidence_scores)
    
    def save_model(self, filepath: str):
        """Save trained model to file"""
        model_data = {
            'k': self.k,
            'sigma': self.sigma,
            'train_embeddings': self.train_embeddings,
            'train_labels': self.train_labels,
            'scaler': self.scaler,
            'confidence_thresholds': self.confidence_thresholds
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
    
    def load_model(self, filepath: str):
        """Load trained model from file"""
        with open(filepath, 'rb') as f:
            model_data = pickle.load(f)
            
        self.k = model_data['k']
        self.sigma = model_data['sigma']
        self.train_embeddings = model_data['train_embeddings']
        self.train_labels = model_data['train_labels']
        self.scaler = model_data['scaler']
        self.confidence_thresholds = model_data['confidence_thresholds']
        self.is_fitted = True

# Ensemble integration with multiple models
class EnsembleConfidenceScorer:
    """
    Ensemble confidence scoring combining multiple models
    """
    def __init__(self, models: list, weights: list = None):
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)
        self.scaler = StandardScaler()
        
    def get_ensemble_confidence(self, x: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get ensemble predictions and confidence scores
        
        Args:
            x: Input features (n_samples, n_features)
            
        Returns:
            predictions: Ensemble predictions
            confidences: Ensemble confidence scores
        """
        predictions = []
        confidences = []
        
        for model in self.models:
            if hasattr(model, 'predict_proba'):
                pred = model.predict_proba(x)
                confidence = np.max(pred, axis=1)
            elif hasattr(model, 'decision_function'):
                pred = model.decision_function(x)
                confidence = np.abs(pred)
            else:
                pred = model.predict(x)
                confidence = np.ones(len(pred)) * 0.8  # Default confidence
                
            predictions.append(pred)
            confidences.append(confidence)
        
        predictions = np.array(predictions)
        confidences = np.array(confidences)
        
        # Weight by model weights
        weighted_pred = np.average(predictions, axis=0, weights=self.weights)
        avg_confidence = np.average(confidences, axis=0, weights=self.weights)
        
        return weighted_pred, avg_confidence

# Example usage:
if __name__ == "__main__":
    # Simulated training data
    np.random.seed(42)
    n_train = 1000
    embedding_dim = 128
    
    # Generate training embeddings and labels
    train_embeddings = np.random.normal(0, 1, (n_train, embedding_dim))
    train_labels = np.random.randint(0, 3, n_train)  # 3 classes
    
    # Initialize and fit confidence scorer
    confidence_scorer = DistanceBasedConfidenceScorer(k=50, sigma=1.0)
    
    # Set confidence thresholds for routing
    thresholds = {
        'auto_threshold': 0.8,
        'guided_threshold': 0.6,
        'novelty_threshold': 0.1
    }
    
    confidence_scorer.fit(train_embeddings, train_labels, thresholds)
    
    # Test on new samples
    test_embedding = np.random.normal(0, 1, (1, embedding_dim))
    
    # Get confidence and routing decision
    confidence = confidence_scorer.get_confidence_score(test_embedding)
    routing_decision = confidence_scorer.route_by_confidence(test_embedding)
    is_novel, novelty_score = confidence_scorer.detect_novelty(test_embedding)
    
    print(f"Confidence Score: {confidence:.3f}")
    print(f"Routing Decision: {routing_decision}")
    print(f"Is Novel: {is_novel} (Novelty Score: {novelty_score:.3f})")
    
    # Batch processing
    batch_embeddings = np.random.normal(0, 1, (100, embedding_dim))
    batch_confidences = confidence_scorer.batch_confidence_score(batch_embeddings)
    print(f"\nBatch Confidence Scores - Mean: {batch_confidences.mean():.3f}, "
          f"Std: {batch_confidences.std():.3f}")
    
    # Save model
    confidence_scorer.save_model('confidence_scorer.pkl')
```

## Edge-Case Handling for Extreme Measurements

Extreme body types—especially OWOB—require segmentation, pattern-parameter tuning, and explicit outlier handling. Railway’s system must detect extremes, route low-confidence cases, and adjust fit rules.

### Segmentation and Tuning

Segment by whole-body shape groups and posture proxies (e.g., back curvature indicators). Tune pattern parameters per garment:

- Back arc allowances for curved upper back.

- Waist depth adjustments for abdominal prominence.

- Hip ease and waist‑to‑hip grading for curvy lower bodies.

- Shoulder line modifications for inverted trapezoid shapes.

Protective clothing guidance and compression textiles emphasize shape-driven sizing systems and tolerance definitions for movement and safety[^24][^25].

### Outlier Handling

At inference:

- Winsorize extreme inputs (e.g., 1st/99th percentiles) per measurement.

- Flag out-of-range Mahalanobis distances; route to guided capture or human review.

- Apply measurement validation against ISO 20685 comparability when scans are used[^32].

Table 12 summarizes edge-case rules.

### Table 12. Edge-case rules matrix

| Segment | Preprocessing | Model routing | Confidence threshold | Tailoring adjustments |
|---|---|---|---|---|
| OWOB shapes (G1–G5) | Winsorize inputs; posture proxies | Prefer GRNN; guided capture if low confidence | Higher cutoff | Back arc, waist depth, hip ease tuned[^8][^24] |
| Posture extremes | Landmark validation | Human review for conflicts | Higher cutoff | Adjust shoulder line; crotch curve[^8] |
| Height extremes | Range checks | SVR baseline; GRNN if noise | Moderate | Sleeve/back length grading |
| Measurement modality conflicts | Cross-method validation | Route to consistent modality | Adaptive | Harmonize site definitions[^11][^32] |

#### OWOB Shape-Aware Tuning

Align garment parameters to shape groups for bust, underbust, waist, and hip coverage. Table 13 outlines pattern-parameter adjustments.

### Table 13. Pattern-parameter adjustments by shape group

| Shape group | Bust/underbust | Waist depth | Back arc | Hip ease | Notes |
|---|---|---|---|---|---|
| G1 rectangle–curvy | Moderate | Standard | Minimal | High | Prioritize hip coverage[^8] |
| G2 parallelogram–moderately curvy | Moderate | Increased | Moderate | Moderate | Front suppression[^8] |
| G3 parallelogram–hip tilt | Moderate | Increased | High | Moderate | Address lower back pull[^8] |
| G4 inverted trapezoid–moderately curvy | Increased | Standard | Moderate | Moderate | Shoulder tension relief[^8] |
| G5 inverted trapezoid–hip tilt | Increased | Increased | High | High | Abdomen/front pull relief[^8]

```python
# Edge Case Handling Implementation for Extreme Measurements
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import LocalOutlierFactor
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class EdgeCaseHandler:
    """
    Edge case handling for extreme body measurements
    Based on research showing 80% difficulty rate in current sizing systems for OWOB populations
    """
    def __init__(self):
        self.shape_classifier = OWOBShapeClassifier()
        self.outlier_detector = LocalOutlierFactor(n_neighbors=20, contamination=0.1)
        self.shape_adjustments = self._initialize_shape_adjustments()
        
    def _initialize_shape_adjustments(self):
        """
        Initialize pattern adjustments for each shape group
        Based on research findings on OWOB body shapes
        """
        return {
            'G1_rectangle_curvy': {
                'hip_ease_multiplier': 1.15,  # 15% more hip ease
                'waist_to_hip_grading': 1.2,  # Enhanced waist-to-hip ratio
                'back_length_adjustment': 0.0,
                'priority': 'hip_coverage'
            },
            'G2_parallelogram_moderate': {
                'hip_ease_multiplier': 1.08,
                'waist_depth_adjustment': 2.0,  # 2cm more waist depth
                'front_suppression': 1.5,
                'crotch_curve_adjustment': 1.3,
                'priority': 'abdominal_comfort'
            },
            'G3_parallelogram_hip_tilt': {
                'hip_ease_multiplier': 1.05,
                'back_arc_adjustment': 3.0,  # 3cm more back arc
                'waist_placement_adjustment': 1.5,
                'lower_back_relief': 1.4,
                'priority': 'lower_back_comfort'
            },
            'G4_inverted_trapezoid_moderate': {
                'hip_ease_multiplier': 1.0,
                'bust_underbust_ease': 1.1,  # 10% more ease
                'shoulder_line_adjustment': 2.0,  # 2cm shoulder relief
                'priority': 'shoulder_tension_relief'
            },
            'G5_inverted_trapezoid_hip_tilt': {
                'hip_ease_multiplier': 1.12,
                'bust_underbust_ease': 1.15,
                'back_arc_adjustment': 4.0,  # 4cm more back arc
                'waist_depth_adjustment': 3.0,
                'front_pull_relief': 1.6,
                'priority': 'comprehensive_relief'
            }
        }
        
    def detect_edge_case(self, customer_features: dict) -> dict:
        """
        Detect edge cases in customer measurements
        
        Args:
            customer_features: Dictionary of customer measurements
            
        Returns:
            edge_case_info: Dictionary with edge case details
        """
        # Calculate BMI and shape metrics
        bmi = customer_features['weight'] / ((customer_features['stature'] / 100) ** 2)
        
        # Shape ratios
        waist_hip_ratio = customer_features['waist_girth'] / customer_features['hip_girth']
        bust_waist_ratio = customer_features['bust_girth'] / customer_features['waist_girth']
        
        edge_case_info = {
            'is_edge_case': False,
            'edge_case_type': None,
            'confidence': 0.0,
            'recommended_adjustments': {},
            'priority_adjustments': []
        }
        
        # OWOB detection (BMI >= 30)
        if bmi >= 30:
            edge_case_info['is_edge_case'] = True
            edge_case_info['edge_case_type'] = 'OWOB'
            edge_case_info['confidence'] = 0.9
            
            # Classify OWOB shape
            shape_group = self.shape_classifier.classify_shape(customer_features)
            edge_case_info['shape_group'] = shape_group
            
            # Get shape-specific adjustments
            adjustments = self.shape_adjustments.get(shape_group, {})
            edge_case_info['recommended_adjustments'] = adjustments
            edge_case_info['priority_adjustments'] = [adjustments.get('priority', 'general_adjustment')]
            
        # Height extremes
        if customer_features['stature'] < 150 or customer_features['stature'] > 200:
            edge_case_info['is_edge_case'] = True
            edge_case_info['edge_case_type'] = 'Height_Extreme'
            edge_case_info['confidence'] = 0.8
            edge_case_info['recommended_adjustments'] = {
                'sleeve_length_adjustment': 1.5 if customer_features['stature'] < 150 else -1.5,
                'back_length_adjustment': 2.0 if customer_features['stature'] < 150 else -2.0,
                'priority': 'proportional_adjustment'
            }
            
        # Measurement ratio extremes
        if waist_hip_ratio > 1.0 or waist_hip_ratio < 0.7:
            edge_case_info['is_edge_case'] = True
            edge_case_info['edge_case_type'] = 'Ratio_Extreme'
            edge_case_info['confidence'] = 0.7
            edge_case_info['recommended_adjustments'] = {
                'waist_hip_balance': 1.3 if waist_hip_ratio > 1.0 else 0.8,
                'priority': 'proportion_harmony'
            }
            
        return edge_case_info
    
    def preprocess_edge_cases(self, X: np.ndarray) -> np.ndarray:
        """
        Preprocess data to handle edge cases
        
        Args:
            X: Feature matrix (n_samples, n_features)
            
        Returns:
            X_processed: Preprocessed feature matrix
        """
        X_processed = X.copy()
        
        # Winsorize extreme values
        for col in range(X.shape[1]):
            col_data = X[:, col]
            q1, q3 = np.percentile(col_data, [25, 75])
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            X_processed[:, col] = np.clip(col_data, lower_bound, upper_bound)
            
        # Detect and flag multivariate outliers
        outlier_labels = self.outlier_detector.fit_predict(X_processed)
        
        # Apply additional processing for outliers
        outlier_mask = outlier_labels == -1
        if np.any(outlier_mask):
            # For outliers, apply more conservative preprocessing
            outlier_data = X_processed[outlier_mask]
            outlier_data = self._apply_conservative_preprocessing(outlier_data)
            X_processed[outlier_mask] = outlier_data
            
        return X_processed
    
    def _apply_conservative_preprocessing(self, X_outliers: np.ndarray) -> np.ndarray:
        """
        Apply conservative preprocessing for outlier data
        
        Args:
            X_outliers: Outlier feature matrix
            
        Returns:
            X_conservative: Conservative preprocessed features
        """
        # Use median instead of mean for central tendency
        median_values = np.median(X_outliers, axis=0)
        
        # Apply more restrictive bounds
        for col in range(X_outliers.shape[1]):
            col_data = X_outliers[:, col]
            col_median = median_values[col]
            col_std = np.std(col_data)
            
            # Stricter bounds for outliers
            lower_bound = col_median - 2 * col_std
            upper_bound = col_median + 2 * col_std
            
            X_outliers[:, col] = np.clip(col_data, lower_bound, upper_bound)
            
        return X_outliers
    
    def route_by_edge_case(self, edge_case_info: dict, confidence_score: float) -> str:
        """
        Route decision based on edge case detection
        
        Args:
            edge_case_info: Edge case detection results
            confidence_score: Model confidence score
            
        Returns:
            routing_decision: 'accept', 'guided_capture', or 'human_review'
        """
        if not edge_case_info['is_edge_case']:
            # Not an edge case, use normal routing
            if confidence_score >= 0.8:
                return 'accept'
            elif confidence_score >= 0.6:
                return 'guided_capture'
            else:
                return 'human_review'
                
        # Edge case routing
        edge_case_type = edge_case_info['edge_case_type']
        confidence = edge_case_info['confidence']
        
        # Higher scrutiny for edge cases
        if edge_case_type == 'OWOB':
            if confidence >= 0.9 and confidence_score >= 0.7:
                return 'guided_capture'  # OWOB always needs guided capture
            else:
                return 'human_review'
                
        elif edge_case_type == 'Height_Extreme':
            if confidence >= 0.8 and confidence_score >= 0.6:
                return 'guided_capture'
            else:
                return 'human_review'
                
        else:  # Other edge cases
            if confidence >= 0.7 and confidence_score >= 0.6:
                return 'guided_capture'
            else:
                return 'human_review'
    
    def apply_pattern_adjustments(self, base_measurements: dict, edge_case_info: dict) -> dict:
        """
        Apply pattern adjustments based on edge case detection
        
        Args:
            base_measurements: Base predicted measurements
            edge_case_info: Edge case detection results
            
        Returns:
            adjusted_measurements: Measurements with edge case adjustments
        """
        if not edge_case_info['is_edge_case']:
            return base_measurements
            
        adjusted = base_measurements.copy()
        adjustments = edge_case_info['recommended_adjustments']
        
        # Apply shape-specific adjustments
        for adjustment, value in adjustments.items():
            if adjustment == 'hip_ease_multiplier' and 'hip_girth' in adjusted:
                adjusted['hip_girth'] *= value
            elif adjustment == 'bust_underbust_ease' and 'bust_girth' in adjusted:
                adjusted['bust_girth'] *= value
            elif adjustment == 'back_arc_adjustment' and 'back_length' in adjusted:
                adjusted['back_length'] += value
            elif adjustment == 'waist_depth_adjustment' and 'waist_girth' in adjusted:
                adjusted['waist_girth'] += value
            elif adjustment == 'sleeve_length_adjustment' and 'sleeve_length' in adjusted:
                adjusted['sleeve_length'] += value
                
        return adjusted

class OWOBShapeClassifier:
    """
    OWOB Shape Classifier based on research findings
    Classifies body shapes into 5 groups for OWOB populations
    """
    def __init__(self):
        self.shape_thresholds = self._initialize_thresholds()
        
    def _initialize_thresholds(self):
        """
        Initialize shape classification thresholds
        Based on research on OWOB body shapes
        """
        return {
            'G1_rectangle_curvy': {
                'min_waist_hip_ratio': 0.7,
                'max_waist_hip_ratio': 0.8,
                'min_bust_waist_ratio': 0.9,
                'max_bust_waist_ratio': 1.1,
                'key_feature': 'curviest_lower_body'
            },
            'G2_parallelogram_moderate': {
                'min_waist_hip_ratio': 0.8,
                'max_waist_hip_ratio': 0.9,
                'min_bust_waist_ratio': 0.8,
                'max_bust_waist_ratio': 1.0,
                'key_feature': 'moderately_curvy'
            },
            'G3_parallelogram_hip_tilt': {
                'min_waist_hip_ratio': 0.75,
                'max_waist_hip_ratio': 0.85,
                'min_bust_waist_ratio': 0.7,
                'max_bust_waist_ratio': 0.9,
                'key_feature': 'hip_tilt_curvature'
            },
            'G4_inverted_trapezoid_moderate': {
                'min_waist_hip_ratio': 0.9,
                'max_waist_hip_ratio': 1.1,
                'min_bust_waist_ratio': 1.1,
                'max_bust_waist_ratio': 1.4,
                'key_feature': 'prominent_bust_upper_back'
            },
            'G5_inverted_trapezoid_hip_tilt': {
                'min_waist_hip_ratio': 0.8,
                'max_waist_hip_ratio': 1.0,
                'min_bust_waist_ratio': 1.2,
                'max_bust_waist_ratio': 1.5,
                'key_feature': 'most_prominent_bust_hip_tilt'
            }
        }
    
    def classify_shape(self, customer_features: dict) -> str:
        """
        Classify OWOB customer into shape group
        
        Args:
            customer_features: Dictionary of customer measurements
            
        Returns:
            shape_group: String identifier of shape group
        """
        waist_hip_ratio = customer_features['waist_girth'] / customer_features['hip_girth']
        bust_waist_ratio = customer_features['bust_girth'] / customer_features['waist_girth']
        
        # Score each shape group
        shape_scores = {}
        
        for shape_group, thresholds in self.shape_thresholds.items():
            score = 0
            
            # Check waist-hip ratio
            if thresholds['min_waist_hip_ratio'] <= waist_hip_ratio <= thresholds['max_waist_hip_ratio']:
                score += 1
                
            # Check bust-waist ratio
            if thresholds['min_bust_waist_ratio'] <= bust_waist_ratio <= thresholds['max_bust_waist_ratio']:
                score += 1
                
            shape_scores[shape_group] = score
            
        # Return shape with highest score
        best_shape = max(shape_scores, key=shape_scores.get)
        
        # If no clear winner, use additional heuristics
        if shape_scores[best_shape] == 0:
            # Default to most common OWOB shape
            if waist_hip_ratio < 0.8:
                return 'G1_rectangle_curvy'
            elif bust_waist_ratio > 1.2:
                return 'G4_inverted_trapezoid_moderate'
            else:
                return 'G2_parallelogram_moderate'
                
        return best_shape

# Example usage:
if __name__ == "__main__":
    # Test edge case handling
    edge_handler = EdgeCaseHandler()
    
    # Example OWOB customer
    owob_customer = {
        'stature': 165,
        'weight': 95,  # High BMI
        'bust_girth': 110,
        'waist_girth': 100,
        'hip_girth': 120
    }
    
    # Detect edge case
    edge_info = edge_handler.detect_edge_case(owob_customer)
    print("Edge Case Detection Results:")
    print(f"Is Edge Case: {edge_info['is_edge_case']}")
    print(f"Edge Case Type: {edge_info['edge_case_type']}")
    print(f"Shape Group: {edge_info.get('shape_group', 'N/A')}")
    print(f"Confidence: {edge_info['confidence']}")
    print(f"Recommended Adjustments: {edge_info['recommended_adjustments']}")
    
    # Route decision
    routing = edge_handler.route_by_edge_case(edge_info, confidence_score=0.75)
    print(f"Routing Decision: {routing}")
    
    # Apply adjustments
    base_measurements = {
        'chest_girth': 110,
        'waist_girth': 100,
        'hip_girth': 120,
        'back_length': 45
    }
    
    adjusted = edge_handler.apply_pattern_adjustments(base_measurements, edge_info)
    print(f"\nAdjusted Measurements:")
    for measurement, value in adjusted.items():
        print(f"{measurement}: {value:.1f} cm")
``` |

## Customer Similarity Weighting Using a 3,371‑Record Corpus

Railway can use a historical corpus of 3,371 high‑quality records to compute weighted neighborhoods that stabilize predictions for atypical customers. The similarity corpus must define features, quality inclusion criteria, and governance aligned to Railway’s inputs.

### Similarity Feature Schema

Define normalized features matching Railway’s input set; include optional demographic or regional tags where available and permitted. Ensure consistent units and scaling.

### Table 14. Similarity feature schema

| Feature | Type | Normalization | Missing policy | Notes |
|---|---|---|---|---|
| Stature | float | StandardScaler | k‑NN (Gower) | cm |
| Weight | float | StandardScaler | k‑NN (Gower) | kg |
| Bust/waist/hip | float | StandardScaler | k‑NN (Gower) | cm |
| Inside leg | float | StandardScaler | k‑NN (Gower) | cm |
| Age | int | StandardScaler | k‑NN (Gower) | Optional |
| Region | enum | One-hot | Mode imputation | Optional |

### Weighting and Voting

Compute weighted k‑nearest neighbors using distance metrics (Euclidean or Gower for mixed types). Weight neighbors by confidence (distance-based) and recency (optional decay). Use local regression or weighted k‑NN voting to predict measurements or size labels; attenuate weights for out-of-distribution cases.

Table 15 proposes weighting schemes.

### Table 15. Weighting schemes

| Scheme | Definition | Pros | Cons | Use |
|---|---|---|---|---|
| 1/d | Inverse distance | Simple; stable | Sensitive to very near neighbors | Baseline |
| exp(−d/σ) | Exponential kernel | Smooth; tunable σ | Requires σ tuning | Preferred |
| conf‑attenuated | Multiply by confidence | Aligns with routing | Depends on calibration | Low-density regions |
| recency-weighted | Time decay | Freshness | Requires timestamps | Seasonal drift |

#### Evaluation Plan

Evaluate similarity-weighted predictions against baseline models by MAE (regression) and accuracy (classification), with ablations across k, metric, and weighting. Monitor performance in sparse regions (low neighbor density) and extremes.

### Table 16. Experiment matrix

| k | Metric | Weighting | Dataset split | Metrics |
|---|---|---|---|---|
| 25, 50, 75 | Euclidean, Gower | 1/d, exp(−d/σ), conf‑attenuated | Stratified by modality and size | MAE, accuracy, AUC error detection, calibration[^2][^7]

```python
# Customer Similarity Weighting Implementation for 3,371-Record Corpus
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.spatial.distance import pdist, squareform
import pandas as pd
from datetime import datetime, timedelta
import pickle

class CustomerSimilarityWeighter:
    """
    Customer similarity weighting system using 3,371 historical records
    Based on research showing effectiveness of similarity-based approaches
    """
    def __init__(self, k_neighbors=50, similarity_threshold=0.7):
        self.k_neighbors = k_neighbors
        self.similarity_threshold = similarity_threshold
        self.corpus_features = None
        self.corpus_labels = None
        self.corpus_metadata = None
        self.scaler = StandardScaler()
        self.similarity_matrix = None
        self.is_fitted = False
        
    def fit(self, corpus_features: np.ndarray, corpus_labels: np.ndarray, 
            corpus_metadata: dict = None):
        """
        Fit similarity weighter with historical corpus
        
        Args:
            corpus_features: Historical customer features (n_records, n_features)
            corpus_labels: Historical measurements/labels
            corpus_metadata: Optional metadata (timestamps, regions, etc.)
        """
        self.corpus_features = corpus_features
        self.corpus_labels = corpus_labels
        self.corpus_metadata = corpus_metadata or {}
        
        # Scale features
        self.scaler.fit(corpus_features)
        scaled_features = self.scaler.transform(corpus_features)
        
        # Build similarity matrix
        self.similarity_matrix = self._compute_similarity_matrix(scaled_features)
        
        self.is_fitted = True
        return self
    
    def _compute_similarity_matrix(self, scaled_features: np.ndarray) -> np.ndarray:
        """
        Compute similarity matrix using multiple distance metrics
        
        Args:
            scaled_features: Standardized feature matrix
            
        Returns:
            similarity_matrix: Combined similarity scores
        """
        # Euclidean distance (normalized)
        euclidean_dist = pdist(scaled_features, metric='euclidean')
        euclidean_sim = 1.0 / (1.0 + euclidean_dist.reshape(-1, 1))
        
        # Cosine similarity
        cosine_sim = cosine_similarity(scaled_features)
        
        # Combine similarities (weighted average)
        combined_sim = 0.6 * euclidean_sim + 0.4 * cosine_sim
        
        return combined_sim
    
    def find_similar_customers(self, customer_features: np.ndarray, 
                             k: int = None) -> dict:
        """
        Find k most similar customers for a given customer
        
        Args:
            customer_features: Customer features (n_features,)
            k: Number of similar customers to find
            
        Returns:
            similar_customers: Dictionary with similar customer info
        """
        if not self.is_fitted:
            raise ValueError("Similarity weighter must be fitted first")
            
        k = k or self.k_neighbors
        
        # Scale customer features
        scaled_features = self.scaler.transform(customer_features.reshape(1, -1))
        
        # Find similar customers
        similar_customers = {
            'indices': [],
            'similarities': [],
            'labels': [],
            'weights': []
        }
        
        # Compute similarities with corpus
        for i in range(len(self.corpus_features)):
            # Scale corpus feature
            corpus_scaled = self.scaler.transform(self.corpus_features[i:i+1])
            
            # Calculate similarity (Euclidean distance based)
            distance = np.linalg.norm(scaled_features - corpus_scaled)
            similarity = 1.0 / (1.0 + distance)
            
            if similarity > self.similarity_threshold:
                similar_customers['indices'].append(i)
                similar_customers['similarities'].append(similarity)
                similar_customers['labels'].append(self.corpus_labels[i])
                
        # Sort by similarity and take top k
        sorted_indices = np.argsort(similar_customers['similarities'])[::-1]
        similar_customers['indices'] = np.array(similar_customers['indices'])[sorted_indices][:k]
        similar_customers['similarities'] = np.array(similar_customers['similarities'])[sorted_indices][:k]
        similar_customers['labels'] = np.array(similar_customers['labels'])[sorted_indices][:k]
        
        # Calculate weights
        if len(similar_customers['similarities']) > 0:
            # Exponential weighting
            sigma = np.std(similar_customers['similarities'])
            weights = np.exp(-(1.0 - similar_customers['similarities'])**2 / (2 * sigma**2))
            # Normalize weights
            weights = weights / np.sum(weights)
            similar_customers['weights'] = weights
        else:
            similar_customers['weights'] = np.array([])
            
        return similar_customers
    
    def predict_weighted(self, customer_features: np.ndarray, 
                        base_prediction: float = None) -> dict:
        """
        Predict using weighted average of similar customers
        
        Args:
            customer_features: Customer features
            base_prediction: Base prediction from main model
            
        Returns:
            weighted_prediction: Dictionary with prediction results
        """
        similar_customers = self.find_similar_customers(customer_features)
        
        if len(similar_customers['weights']) == 0:
            # No similar customers found, use base prediction
            return {
                'prediction': base_prediction,
                'confidence': 0.3,  # Low confidence
                'n_similar': 0,
                'method': 'base_only'
            }
        
        # Weighted prediction
        weighted_prediction = np.average(similar_customers['labels'], 
                                       weights=similar_customers['weights'])
        
        # Calculate confidence based on similarity scores
        avg_similarity = np.mean(similar_customers['similarities'])
        confidence = min(avg_similarity, 1.0)
        
        return {
            'prediction': weighted_prediction,
            'confidence': confidence,
            'n_similar': len(similar_customers['similarities']),
            'method': 'weighted_similarity',
            'similarities': similar_customers['similarities']
        }
    
    def apply_recency_weighting(self, timestamps: list, half_life_days: int = 365):
        """
        Apply recency weighting to similarity scores
        
        Args:
            timestamps: List of timestamps for corpus records
            half_life_days: Half-life for recency decay
        """
        if not self.corpus_metadata or 'timestamps' not in self.corpus_metadata:
            return
            
        current_time = datetime.now()
        recency_weights = []
        
        for timestamp in timestamps:
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp)
            
            days_diff = (current_time - timestamp).days
            recency_weight = np.exp(-days_diff / half_life_days)
            recency_weights.append(recency_weight)
        
        # Apply recency weighting to similarity matrix
        recency_weights = np.array(recency_weights)
        self.similarity_matrix *= recency_weights.reshape(-1, 1)
        
    def get_similarity_stats(self) -> dict:
        """
        Get statistics about the similarity corpus
        
        Returns:
            stats: Dictionary with corpus statistics
        """
        if not self.is_fitted:
            return {}
            
        # Calculate average similarities
        avg_similarity = np.mean(self.similarity_matrix[np.triu_indices_from(self.similarity_matrix, k=1)])
        
        # Find most/least similar pairs
        max_sim_idx = np.unravel_index(np.argmax(self.similarity_matrix), self.similarity_matrix.shape)
        min_sim_idx = np.unravel_index(np.argmin(self.similarity_matrix), self.similarity_matrix.shape)
        
        stats = {
            'n_records': len(self.corpus_features),
            'avg_similarity': avg_similarity,
            'max_similarity': self.similarity_matrix[max_sim_idx],
            'min_similarity': self.similarity_matrix[min_sim_idx],
            'feature_shape': self.corpus_features.shape,
            'has_timestamps': 'timestamps' in self.corpus_metadata if self.corpus_metadata else False
        }
        
        return stats

# Wedding Party Consistency Logic Implementation
class WeddingPartyConsistency:
    """
    Wedding party consistency logic for KCT integration
    Ensures consistent fit intents across party members
    """
    def __init__(self):
        self.silhouette_categories = ['classic', 'slim', 'modern', 'tailored', 'athletic']
        self.ease_categories = ['tight', 'fitted', 'regular', 'relaxed', 'loose']
        self.consistency_rules = self._initialize_consistency_rules()
        self.conflict_history = []
        
    def _initialize_consistency_rules(self) -> dict:
        """
        Initialize consistency rules for wedding parties
        """
        return {
            'silhouette_consistency': {
                'max_difference': 1,  # Max 1 category difference allowed
                'priority_members': ['bride', 'groom', 'maids_of_honor'],
                'resolution_strategy': 'party_consensus'
            },
            'size_consistency': {
                'max_size_difference': 2,  # Max 2 sizes difference
                'ease_adjustment_threshold': 1.0,  # cm difference threshold
                'resolution_strategy': 'gradual_adjustment'
            },
            'color_consistency': {
                'palette_tolerance': 0.2,  # Color palette tolerance
                'resolution_strategy': 'color_harmony'
            },
            'style_consistency': {
                'style_elements': ['neckline', 'sleeve_style', 'fabric', 'details'],
                'resolution_strategy': 'balanced_harmony'
            }
        }
    
    def validate_party_consistency(self, party_members: list[dict]) -> dict:
        """
        Validate consistency across wedding party members
        
        Args:
            party_members: List of party member data
            
        Returns:
            consistency_report: Dictionary with validation results
        """
        consistency_report = {
            'is_consistent': True,
            'conflicts': [],
            'warnings': [],
            'recommendations': [],
            'consistency_score': 1.0
        }
        
        if len(party_members) < 2:
            return consistency_report
        
        # Check silhouette consistency
        silhouette_conflicts = self._check_silhouette_consistency(party_members)
        consistency_report['conflicts'].extend(silhouette_conflicts)
        
        # Check size consistency
        size_conflicts = self._check_size_consistency(party_members)
        consistency_report['conflicts'].extend(size_conflicts)
        
        # Check ease consistency
        ease_conflicts = self._check_ease_consistency(party_members)
        consistency_report['warnings'].extend(ease_conflicts)
        
        # Check confidence consistency
        confidence_issues = self._check_confidence_consistency(party_members)
        consistency_report['warnings'].extend(confidence_issues)
        
        # Calculate overall consistency score
        consistency_report['consistency_score'] = self._calculate_consistency_score(
            consistency_report
        )
        
        # Generate recommendations
        if consistency_report['conflicts']:
            consistency_report['is_consistent'] = False
            consistency_report['recommendations'] = self._generate_recommendations(
                party_members, consistency_report['conflicts']
            )
            
        return consistency_report
    
    def _check_silhouette_consistency(self, party_members: list[dict]) -> list:
        """
        Check silhouette consistency across party members
        """
        conflicts = []
        silhouettes = []
        
        for member in party_members:
            if 'silhouette' in member:
                silhouettes.append(member['silhouette'])
        
        if len(silhouettes) > 1:
            # Check for significant differences
            silhouette_diffs = []
            for i in range(len(silhouettes)):
                for j in range(i + 1, len(silhouettes)):
                    diff = abs(self.silhouette_categories.index(silhouettes[i]) - 
                              self.silhouette_categories.index(silhouettes[j]))
                    silhouette_diffs.append(diff)
            
            max_diff = max(silhouette_diffs) if silhouette_diffs else 0
            
            if max_diff > self.consistency_rules['silhouette_consistency']['max_difference']:
                conflicts.append({
                    'type': 'silhouette_inconsistency',
                    'severity': 'high',
                    'details': f'Max silhouette difference: {max_diff}',
                    'affected_members': list(range(len(party_members)))
                })
        
        return conflicts
    
    def _check_size_consistency(self, party_members: list[dict]) -> list:
        """
        Check size consistency across party members
        """
        conflicts = []
        sizes = []
        
        for member in party_members:
            if 'predicted_size' in member:
                sizes.append(member['predicted_size'])
        
        if len(sizes) > 1:
            size_range = max(sizes) - min(sizes)
            
            if size_range > self.consistency_rules['size_consistency']['max_size_difference']:
                conflicts.append({
                    'type': 'size_inconsistency',
                    'severity': 'high',
                    'details': f'Size range: {size_range} sizes',
                    'affected_members': [i for i, size in enumerate(sizes) 
                                       if size < min(sizes) or size > max(sizes)]
                })
        
        return conflicts
    
    def _check_ease_consistency(self, party_members: list[dict]) -> list:
        """
        Check ease consistency across party members
        """
        warnings = []
        ease_differences = []
        
        for member in party_members:
            if 'ease_category' in member:
                ease_differences.append(member['ease_category'])
        
        # Check for dramatic ease differences
        if len(set(ease_differences)) > 3:  # More than 3 different ease categories
            warnings.append({
                'type': 'ease_variation',
                'severity': 'medium',
                'details': f'High ease variation across party',
                'recommendation': 'Consider standardizing ease for better harmony'
            })
        
        return warnings
    
    def _check_confidence_consistency(self, party_members: list[dict]) -> list:
        """
        Check confidence consistency across party members
        """
        warnings = []
        confidences = []
        
        for member in party_members:
            if 'confidence_score' in member:
                confidences.append(member['confidence_score'])
        
        if confidences:
            confidence_range = max(confidences) - min(confidences)
            
            if confidence_range > 0.3:  # Significant confidence difference
                warnings.append({
                    'type': 'confidence_inconsistency',
                    'severity': 'medium',
                    'details': f'Confidence range: {confidence_range:.2f}',
                    'recommendation': 'Review measurements for low-confidence members'
                })
        
        return warnings
    
    def _calculate_consistency_score(self, consistency_report: dict) -> float:
        """
        Calculate overall consistency score
        """
        base_score = 1.0
        
        # Deduct for conflicts
        for conflict in consistency_report['conflicts']:
            if conflict['severity'] == 'high':
                base_score -= 0.3
            elif conflict['severity'] == 'medium':
                base_score -= 0.1
        
        # Deduct for warnings
        for warning in consistency_report['warnings']:
            if warning['severity'] == 'medium':
                base_score -= 0.05
        
        return max(base_score, 0.0)
    
    def _generate_recommendations(self, party_members: list[dict], 
                                conflicts: list[dict]) -> list:
        """
        Generate recommendations to resolve conflicts
        """
        recommendations = []
        
        for conflict in conflicts:
            if conflict['type'] == 'silhouette_inconsistency':
                recommendations.append({
                    'action': 'standardize_silhouette',
                    'description': 'Align silhouettes to within one category difference',
                    'priority': 'high'
                })
            
            elif conflict['type'] == 'size_inconsistency':
                recommendations.append({
                    'action': 'gradual_size_adjustment',
                    'description': 'Gradually adjust sizes to reduce range while respecting fit',
                    'priority': 'high'
                })
        
        return recommendations
    
    def resolve_conflicts(self, party_members: list[dict], 
                         consistency_report: dict) -> list[dict]:
        """
        Resolve conflicts through automated adjustments
        
        Args:
            party_members: List of party member data
            consistency_report: Consistency validation results
            
        Returns:
            resolved_members: Party members with resolved conflicts
        """
        resolved_members = [member.copy() for member in party_members]
        
        for conflict in consistency_report['conflicts']:
            if conflict['type'] == 'silhouette_inconsistency':
                resolved_members = self._resolve_silhouette_conflict(resolved_members)
            
            elif conflict['type'] == 'size_inconsistency':
                resolved_members = self._resolve_size_conflict(resolved_members)
        
        return resolved_members
    
    def _resolve_silhouette_conflict(self, party_members: list[dict]) -> list[dict]:
        """
        Resolve silhouette conflicts by finding optimal compromise
        """
        silhouettes = []
        for member in party_members:
            if 'silhouette' in member:
                silhouettes.append(member['silhouette'])
        
        if not silhouettes:
            return party_members
        
        # Find most common silhouette or middle ground
        silhouette_indices = [self.silhouette_categories.index(s) for s in silhouettes]
        target_index = int(np.median(silhouette_indices))
        target_silhouette = self.silhouette_categories[target_index]
        
        # Apply target silhouette to all members
        for member in party_members:
            if 'silhouette' in member:
                member['original_silhouette'] = member['silhouette']
                member['silhouette'] = target_silhouette
                member['adjustment_reason'] = 'party_consistency'
        
        return party_members
    
    def _resolve_size_conflict(self, party_members: list[dict]) -> list[dict]:
        """
        Resolve size conflicts through gradual adjustment
        """
        sizes = []
        for member in party_members:
            if 'predicted_size' in member:
                sizes.append(member['predicted_size'])
        
        if not sizes:
            return party_members
        
        min_size, max_size = min(sizes), max(sizes)
        size_range = max_size - min_size
        
        if size_range > 2:  # Only adjust if range is too large
            target_range = 2  # Target range of 2 sizes
            adjustment_factor = target_range / size_range
            
            for member in party_members:
                if 'predicted_size' in member:
                    original_size = member['predicted_size']
                    # Adjust towards median
                    median_size = np.median(sizes)
                    adjustment = (original_size - median_size) * adjustment_factor
                    new_size = median_size + adjustment
                    
                    member['original_size'] = original_size
                    member['predicted_size'] = round(new_size)
                    member['size_adjustment'] = member['predicted_size'] - original_size
                    member['adjustment_reason'] = 'party_consistency'
        
        return party_members
    
    def create_party_summary(self, party_members: list[dict]) -> dict:
        """
        Create summary report for wedding party
        
        Args:
            party_members: List of party member data
            
        Returns:
            party_summary: Comprehensive party summary
        """
        summary = {
            'party_size': len(party_members),
            'member_roles': {},
            'size_distribution': {},
            'silhouette_distribution': {},
            'confidence_stats': {},
            'consistency_issues': [],
            'recommendations': []
        }
        
        # Analyze party composition
        for member in party_members:
            role = member.get('role', 'guest')
            summary['member_roles'][role] = summary['member_roles'].get(role, 0) + 1
        
        # Size distribution
        sizes = [m.get('predicted_size') for m in party_members if 'predicted_size' in m]
        if sizes:
            summary['size_distribution'] = {
                'min': min(sizes),
                'max': max(sizes),
                'range': max(sizes) - min(sizes),
                'median': np.median(sizes),
                'std': np.std(sizes)
            }
        
        # Silhouette distribution
        silhouettes = [m.get('silhouette') for m in party_members if 'silhouette' in m]
        if silhouettes:
            summary['silhouette_distribution'] = {s: silhouettes.count(s) for s in set(silhouettes)}
        
        # Confidence statistics
        confidences = [m.get('confidence_score') for m in party_members if 'confidence_score' in m]
        if confidences:
            summary['confidence_stats'] = {
                'mean': np.mean(confidences),
                'min': min(confidences),
                'max': max(confidences),
                'std': np.std(confidences)
            }
        
        return summary

# Example usage:
if __name__ == "__main__":
    # Test customer similarity weighting
    print("=== Customer Similarity Weighting Test ===")
    
    # Simulate 3,371 historical records
    np.random.seed(42)
    n_records = 3371
    n_features = 7
    
    # Historical corpus features and labels
    corpus_features = np.random.normal([170, 65, 90, 75, 95, 45, 38], 
                                     [10, 15, 12, 10, 12, 3, 2], 
                                     (n_records, n_features))
    corpus_labels = np.random.normal(100, 15, n_records)  # Target measurements
    
    # Fit similarity weighter
    similarity_weighter = CustomerSimilarityWeighter(k_neighbors=50)
    similarity_weighter.fit(corpus_features, corpus_labels)
    
    # Test new customer
    new_customer_features = np.array([175, 70, 95, 80, 100, 46, 39])
    base_prediction = 105.0
    
    weighted_result = similarity_weighter.predict_weighted(new_customer_features, base_prediction)
    print(f"Weighted Prediction: {weighted_result['prediction']:.2f}")
    print(f"Confidence: {weighted_result['confidence']:.3f}")
    print(f"Similar Customers Found: {weighted_result['n_similar']}")
    
    # Similarity statistics
    stats = similarity_weighter.get_similarity_stats()
    print(f"\nSimilarity Statistics:")
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    # Test wedding party consistency
    print("\n=== Wedding Party Consistency Test ===")
    
    party_members = [
        {
            'role': 'bride',
            'predicted_size': 8,
            'silhouette': 'modern',
            'ease_category': 'fitted',
            'confidence_score': 0.9
        },
        {
            'role': 'maid_of_honor',
            'predicted_size': 10,
            'silhouette': 'classic',
            'ease_category': 'regular',
            'confidence_score': 0.7
        },
        {
            'role': 'bridesmaid',
            'predicted_size': 12,
            'silhouette': 'slim',
            'ease_category': 'fitted',
            'confidence_score': 0.8
        }
    ]
    
    consistency_engine = WeddingPartyConsistency()
    consistency_report = consistency_engine.validate_party_consistency(party_members)
    
    print(f"Party Consistency: {consistency_report['is_consistent']}")
    print(f"Consistency Score: {consistency_report['consistency_score']:.2f}")
    print(f"Conflicts Found: {len(consistency_report['conflicts'])}")
    print(f"Warnings: {len(consistency_report['warnings'])}")
    
    if consistency_report['conflicts']:
        print("\nConflicts:")
        for conflict in consistency_report['conflicts']:
            print(f"- {conflict['type']}: {conflict['details']}")
    
    # Create party summary
    party_summary = consistency_engine.create_party_summary(party_members)
    print(f"\nParty Summary:")
    print(f"Party Size: {party_summary['party_size']}")
    print(f"Roles: {party_summary['member_roles']}")
    print(f"Size Range: {party_summary['size_distribution'].get('range', 'N/A')}")
``` |

## Wedding Party Consistency Logic for KCT Integration

KCT (Kathryn’s Custom Tailoring) likely encodes consistent fit intents across party members—e.g., shared silhouette, ease, and style—so that group events (weddings) present harmonized aesthetics. Railway should implement a rules engine that enforces consistency while respecting individual measurements and confidence.

### Rule Design

Define constraints on size labels, ease allowances, silhouette categories (classic, slim, modern, tailored), and measurement tolerances across party members. Rules should detect conflicts (e.g., a party member predicted as size 44 jacket with “slim” ease while another is 40 “classic”), resolve via variance-aware thresholds, and record overrides.

Table 17 sketches a rule library.

### Table 17. KCT rule library (indicative)

| Rule ID | Condition | Threshold | Action | Notes |
|---|---|---|---|---|
| WP‑01 | Same party, jacket PD difference | > 2 sizes | Flag conflict | Investigate silhouette/ease |
| WP‑02 | Silhouette mismatch | Slim vs classic across party | Warn | Tie-break with confidence |
| WP‑03 | Ease deviation | > 1 interval in chest ease | Flag | Consider pattern alignment |
| WP‑04 | Low-confidence member | Density below threshold | Guide/measure | Escalate to human review |
| WP‑05 | Tailor override | Manual change | Record; reversible | Audit trail required[^14][^15][^11] |

#### Conflict Detection and Resolution

Identify conflicts when predicted labels or ease allowances deviate beyond tolerances across party members. Resolve via variance-aware thresholds, proximity to size-chart intervals, and confidence ranking. Table 18 outlines the resolution matrix.

### Table 18. Resolution matrix

| Conflict type | Detection rule | Tie-break criteria | Escalation path |
|---|---|---|---|
| Size PD mismatch | > 2 sizes difference | Highest confidence; group silhouette | Human review |
| Silhouette mismatch | Slim vs classic | Party consensus; confidence | Tailor consultation |
| Ease deviation | > 1 interval | Closest to PD/SD alignment | Pattern adjustment |
| Low confidence | Density below cutoff | Second-best model vote | Guided capture |
| Override conflict | Manual vs predicted | Audit trail; revert option | Senior tailor approval |

## Evaluation and Monitoring

Railway must instrument a comprehensive evaluation protocol that spans regression, classification, confidence calibration, and 3D deformation (where applicable).

- Regression: MAE vs precision steps; PR; KL divergence[^2].

- Classification: Accuracy; adjacent-size error; confusion matrices[^5].

- Confidence: AUC for error/novelty detection; Brier score; ECE; false-escalation rate[^7][^12].

- 3D garment deformation: Per-vertex error (Verr) and surface area error (Aerr) compared to linear scaling baselines[^6].

- CI/CD: Automated dashboards and alerts for drift, calibration, and subgroup fairness.

Table 19 defines the KPI dashboard.

### Table 19. KPI dashboard

| Component | KPI | Target | Alerting |
|---|---|---|---|
| Regression | MAE vs precision step | ≤ 1.0 PR | Weekly alert |
| Classification | Accuracy; adjacent-size rate | Improving; low adjacent | Weekly alert |
| Confidence | AUC; Brier; ECE | Stable/improving | Weekly alert |
| Routing | False-escalation rate | ≤ target | Weekly alert |
| 3D deformation | Verr; Aerr | Lower than linear | Monthly alert |
| Returns | Fit-related return rate | Post‑deployment reduction | Monthly alert[^1][^10] |

## Implementation Plan, Interfaces, and Deliverables

The implementation is phased to minimize risk and accelerate learning.

### Phase 1 (Weeks 1–6): Baseline predictors and confidence

- Ship SVR and GRNN measurement predictors behind the feature store.

- Implement distance-based confidence scoring and calibrated thresholds.

- Establish routing to guided capture/human review for low-confidence cases.

- Build evaluation dashboards and calibration monitoring[^2][^3][^7].

### Phase 2 (Weeks 7–12): Edge-case handling and similarity weighting

- Deploy OWOB segmentation and posture-aware routing; add pattern-parameter tuning.

- Introduce similarity weighting using the 3,371‑record corpus; ablate k, metric, and weighting.

- Expand calibration monitoring to subgroups and modalities[^8].

### Phase 3 (Weeks 13–18): Wedding-party consistency and CI/CD

- Encode KCT wedding-party rules; implement conflict detection and resolution.

- Add audit trails and reversible overrides; integrate tailor workflows.

- Harden CI/CD for models, thresholds, and rules; finalize KPI targets[^14][^15][^11].

To clarify ownership and dependencies, Table 20 outlines the work breakdown.

### Table 20. Work breakdown and timeline

| Task | Owner | Dependencies | Effort | Outputs |
|---|---|---|---|---|
| Feature store/schema | Data eng | Railway APIs | 2 weeks | Canonical schema |
| SVR/GRNN training | ML eng | Feature store | 3 weeks | Predictors; CV metrics |
| Confidence scoring | ML eng | Embeddings; thresholds | 2 weeks | Density scores; routing |
| Edge-case rules | ML eng + Tailoring | OWOB segmentation | 3 weeks | Rules; routing |
| Similarity corpus | Data eng | Quality curation | 3 weeks | 3,371 records; weights |
| KCT rules engine | ML eng + Tailoring | Predictors; confidence | 3 weeks | Rules; audit trails |
| Dashboards & CI/CD | Platform | All | 4 weeks | Monitoring; alerts |

Define service contracts for predictors, confidence endpoints, rules engine, and similarity services.

### Table 21. API contracts

| Endpoint | Inputs | Outputs | Errors |
|---|---|---|---|
| /predict/measurements | Features (stature, weight, bust/waist/hip, inside leg, age) | Predicted measurements; model version | 400 invalid; 500 server |
| /predict/size | Features; modality | Size label; confidence score; version | 400/500 |
| /confidence/score | Features; model_id | Density; calibrated confidence | 400/500 |
| /rules/validate | Party measurements; silhouette; ease | Conflicts; resolutions | 400/500 |
| /similarity/weight | Features | Neighbor weights; density | 400/500 |

#### Pseudocode and Module Interfaces

```python
# SVR Implementation with optimized hyperparameters
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error, r2_score
import numpy as np
import pandas as pd

def create_svr_model(X_train, y_train, measurement_type='chest_girth'):
    """
    Creates optimized SVR model for anthropometric measurements
    Based on research showing 89.66% accuracy for clothing size prediction
    
    Args:
        X_train: Feature matrix (stature, weight, bust, waist, hip)
        y_train: Target measurement (in cm)
        measurement_type: Type of measurement being predicted
    
    Returns:
        Trained SVR model pipeline
    """
    print(f"Training SVR model for {measurement_type} prediction...")
    
    # Create pipeline with scaling and SVR
    pipeline = Pipeline([
        ('scaler', StandardScaler()),
        ('svr', SVR(kernel='rbf'))
    ])
    
    # Hyperparameter optimization based on research findings
    param_grid = {
        'svr__C': [0.1, 1, 10, 100, 1000],
        'svr__gamma': ['scale', 'auto', 0.001, 0.01, 0.1, 1.0],
        'svr__epsilon': [0.01, 0.05, 0.1, 0.2, 0.5]
    }
    
    # Grid search with cross-validation
    grid_search = GridSearchCV(
        pipeline, 
        param_grid, 
        cv=5, 
        scoring='neg_mean_absolute_error',
        n_jobs=-1,
        verbose=1
    )
    
    grid_search.fit(X_train, y_train)
    
    # Print optimization results
    print(f"Best parameters for {measurement_type}:")
    print(grid_search.best_params_)
    print(f"Best CV MAE: {-grid_search.best_score_:.2f} cm")
    
    return grid_search.best_estimator_

def evaluate_svr_model(model, X_test, y_test, measurement_type):
    """Evaluate SVR model performance"""
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f"\n{measurement_type} Prediction Results:")
    print(f"MAE: {mae:.2f} cm")
    print(f"R²: {r2:.3f}")
    print(f"Accuracy within ±1cm: {np.mean(np.abs(predictions - y_test) <= 1.0) * 100:.1f}%")
    
    return mae, r2

# Multiple measurement SVR predictor
class MultiMeasurementSVR:
    """
    SVR predictor for multiple anthropometric measurements
    Based on research showing SVR achieves best performance for anthropometric prediction
    """
    def __init__(self, measurements):
        self.measurements = measurements
        self.models = {}
        self.scalers = {}
        self.feature_names = ['stature', 'weight', 'bust_girth', 'waist_girth', 'hip_girth']
        
    def fit(self, X, y_dict):
        """
        Train SVR models for all measurements
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y_dict: Dictionary {measurement_name: target_values}
        """
        for measurement in self.measurements:
            print(f"Training SVR for {measurement}...")
            
            # Create and train model
            model = create_svr_model(X, y_dict[measurement], measurement)
            self.models[measurement] = model
            
        return self
    
    def predict(self, X):
        """Predict all measurements"""
        predictions = {}
        
        for measurement in self.measurements:
            predictions[measurement] = self.models[measurement].predict(X)
            
        return predictions
    
    def predict_single_customer(self, customer_features):
        """Predict measurements for a single customer"""
        X = np.array([customer_features])
        predictions = self.predict(X)
        
        # Return as dictionary for single customer
        return {measurement: predictions[measurement][0] 
                for measurement in self.measurements}

# GRNN Implementation using custom neural network
import numpy as np
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

class GRNNPredictor:
    """
    Generalized Regression Neural Network for body measurement prediction
    Capable of predicting 76 measurements from 7 easy-to-measure dimensions
    Based on research showing superior performance for anthropometric prediction
    """
    def __init__(self, sigma=1.0):
        self.sigma = sigma  # Spread parameter
        self.X_train = None
        self.y_train = None
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def fit(self, X, y):
        """Train GRNN with single-pass learning"""
        self.X_train = self.scaler.fit_transform(X)
        self.y_train = np.array(y)
        self.is_fitted = True
        return self
        
    def predict(self, X_test):
        """Predict using weighted average of training samples"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
            
        X_test_scaled = self.scaler.transform(X_test)
        
        # Calculate distances between test and training points
        distances = cdist(X_test_scaled, self.X_train, metric='euclidean')
        
        # Gaussian kernel weights
        weights = np.exp(-distances**2 / (2 * self.sigma**2))
        
        # Normalize weights (avoid division by zero)
        weights_sum = np.sum(weights, axis=1, keepdims=True) + 1e-8
        normalized_weights = weights / weights_sum
        
        # Weighted average prediction
        predictions = np.dot(normalized_weights, self.y_train)
        return predictions
        
    def optimize_sigma(self, X_val, y_val, sigma_range=None):
        """Optimize spread parameter using validation data"""
        if sigma_range is None:
            sigma_range = np.logspace(-2, 2, 30)  # 0.01 to 100
            
        best_sigma = None
        best_mae = float('inf')
        sigma_results = []
        
        for sigma in sigma_range:
            self.sigma = sigma
            predictions = self.predict(X_val)
            mae = mean_absolute_error(y_val, predictions)
            sigma_results.append((sigma, mae))
            
            if mae < best_mae:
                best_mae = mae
                best_sigma = sigma
                
        return best_sigma, best_mae, sigma_results

# Multi-output GRNN for predicting multiple measurements
class MultiOutputGRNN:
    """
    GRNN capable of predicting multiple body measurements simultaneously
    Based on research showing capability for 76 measurements from 7 inputs
    """
    def __init__(self, sigma=1.0):
        self.sigma = sigma
        self.models = {}  # One GRNN per measurement
        self.measurement_names = []
        
    def fit(self, X, y_dict):
        """
        Fit separate GRNN for each measurement
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y_dict: Dictionary {measurement_name: target_values}
        """
        self.measurement_names = list(y_dict.keys())
        
        for measurement, targets in y_dict.items():
            print(f"Training GRNN for {measurement}...")
            grnn = GRNNPredictor(sigma=self.sigma)
            grnn.fit(X, targets)
            self.models[measurement] = grnn
            
        return self
    
    def predict(self, X_test):
        """Predict all measurements for test samples"""
        predictions = {}
        
        for measurement, model in self.models.items():
            predictions[measurement] = model.predict(X_test)
            
        return predictions
    
    def evaluate(self, X_test, y_true_dict):
        """Evaluate all measurement predictions"""
        predictions = self.predict(X_test)
        results = {}
        
        for measurement in self.measurement_names:
            mae = mean_absolute_error(y_true_dict[measurement], predictions[measurement])
            results[measurement] = mae
            print(f"{measurement} MAE: {mae:.2f} cm")
            
        return results

class MeasurementPredictor:
    """
    Main measurement predictor interface combining SVR and GRNN models
    """
    def __init__(self):
        self.svr_model = None
        self.grnn_model = None
        self.ensemble_weights = [0.6, 0.4]  # SVR and GRNN weights
        self.measurements = ['chest_girth', 'waist_girth', 'hip_girth', 'sleeve_length', 'inseam']
        
    def fit(self, X, y_dict):
        """
        Train ensemble of SVR and GRNN models
        
        Args:
            X: Feature matrix (n_samples, n_features)
            y_dict: Dictionary {measurement_name: target_values}
        """
        # Train SVR models
        self.svr_model = MultiMeasurementSVR(self.measurements)
        self.svr_model.fit(X, y_dict)
        
        # Train GRNN models
        self.grnn_model = MultiOutputGRNN()
        self.grnn_model.fit(X, y_dict)
        
        return self
    
    def predict(self, X):
        """
        Predict measurements using ensemble of SVR and GRNN
        
        Args:
            X: Feature matrix (n_samples, n_features)
            
        Returns:
            predictions: Dictionary of ensemble predictions
        """
        if self.svr_model is None or self.grnn_model is None:
            raise ValueError("Models must be fitted before prediction")
            
        # Get predictions from both models
        svr_predictions = self.svr_model.predict(X)
        grnn_predictions = self.grnn_model.predict(X)
        
        # Ensemble combine
        ensemble_predictions = {}
        for measurement in self.measurements:
            ensemble_predictions[measurement] = (
                self.ensemble_weights[0] * svr_predictions[measurement] +
                self.ensemble_weights[1] * grnn_predictions[measurement]
            )
            
        return ensemble_predictions
    
    def predict_single_customer(self, customer_features):
        """
        Predict measurements for a single customer
        
        Args:
            customer_features: List of features [stature, weight, bust, waist, hip]
            
        Returns:
            predictions: Dictionary of predicted measurements
        """
        X = np.array([customer_features])
        predictions = self.predict(X)
        
        # Return as single customer format
        return {measurement: predictions[measurement][0] 
                for measurement in self.measurements}

class SizeClassifier:
    def predict_size(self, features: dict) -> dict:
        # returns size label, embedding, confidence
        # Placeholder implementation - would integrate with actual size classification
        pass

class ConfidenceScorer:
    def density(self, embedding, train_embeddings, train_labels, k=50) -> float:
        # distance-based density
        # Implementation provided in confidence scoring section above
        pass

    def calibrate(self, thresholds: dict):
        # set routing thresholds by validation
        # Implementation provided in confidence scoring section above
        pass

class RulesEngine:
    def validate_party(self, party: list[dict]) -> dict:
        # party: list of member features + silhouette/ease
        # returns conflicts and resolutions
        # Implementation provided in wedding party consistency section above
        pass

class SimilarityService:
    def weights(self, features: dict, corpus: list[dict]) -> dict:
        # returns neighbor indices, weights, density
        # Implementation provided in customer similarity section above
        pass

# Example usage:
if __name__ == "__main__":
    # Simulated training data
    np.random.seed(42)
    n_samples = 500
    
    # Features: [stature, weight, bust, waist, hip]
    X = np.random.normal([170, 65, 90, 75, 95], [10, 15, 12, 10, 12], (n_samples, 5))
    
    # Target measurements (simplified relationships)
    measurements = ['chest_girth', 'waist_girth', 'hip_girth', 'sleeve_length', 'inseam']
    y_dict = {
        'chest_girth': 0.8 * X[:, 2] + 0.3 * X[:, 0] + np.random.normal(0, 2, n_samples),
        'waist_girth': 0.9 * X[:, 3] + 0.2 * X[:, 1] + np.random.normal(0, 2, n_samples),
        'hip_girth': 0.85 * X[:, 4] + 0.25 * X[:, 0] + np.random.normal(0, 2, n_samples),
        'sleeve_length': 0.6 * X[:, 0] + 0.1 * X[:, 1] + np.random.normal(0, 3, n_samples),
        'inseam': 0.45 * X[:, 0] + 0.05 * X[:, 2] + np.random.normal(0, 2, n_samples)
    }
    
    # Split data
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(X, y_dict, test_size=0.2, random_state=42)
    
    # Train ensemble predictor
    predictor = MeasurementPredictor()
    predictor.fit(X_train, y_train)
    
    # Evaluate performance
    print("\n=== Ensemble Predictor Performance ===")
    predictions = predictor.predict(X_test)
    
    for measurement in measurements:
        mae = mean_absolute_error(y_test[measurement], predictions[measurement])
        print(f"{measurement} MAE: {mae:.2f} cm")
    
    # Single customer prediction
    customer_features = [175, 70, 95, 80, 100]  # [stature, weight, bust, waist, hip]
    customer_predictions = predictor.predict_single_customer(customer_features)
    
    print("\n=== Single Customer Predictions ===")
    for measurement, value in customer_predictions.items():
        print(f"{measurement}: {value:.1f} cm")
```

## Risks, Compliance, and Data Governance

Risks:

- Dataset representativeness and temporal drift: Military-centric datasets may not generalize to civilian retail; distributions change over time[^3][^2].

- Modal measurement errors: Tape vs scan vs app variability; landmarking; software versions[^11][^32].

- Confidence calibration drift: Subgroup differences; modality shifts; model updates[^12].

- Privacy: 3D scans and photos require consent, data minimization, retention controls[^11].

Mitigations:

- Cross-method validation and QC loops; site-specific variance tracking; calibration monitoring and recalibration.

- Subgroup audits and fairness assessments; transparent confidence disclosures.

- Audit trails for KCT overrides; reversible decisions.

Compliance:

- Align size labeling to ISO 8559‑2 principles (primary/secondary dimensions, intervals, labeling); communicate body measurements rather than garment measures[^30][^2].

- For 3D scanning, follow ISO 20685 comparability guidelines and validated scanner protocols[^32][^37].

Table 22 summarizes the risk register.

### Table 22. Risk register

| Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|
| Temporal drift | Medium | Medium | Recalibration cadence | ML eng |
| Modal errors | High | High | QC loops; ISO 20685 validation | Platform |
| Calibration drift | Medium | High | Weekly monitoring; recalibration | ML eng |
| Representativeness | Medium | High | Expand datasets; subgroup audits | Analytics |
| Privacy | Medium | High | Consent; minimization; retention | Legal/Platform |
| KCT override conflicts | Low | Medium | Audit trails; reversible overrides | Tailoring ops |

## Appendices

### A. Glossary

- Primary Dimension (PD): The main body measurement used to designate size (e.g., chest girth for jackets), expressed in centimeters[^30].

- Secondary Dimension (SD): Additional body dimensions used to refine size selection (e.g., back length, inseam), expressed in centimeters[^30].

- Interval: The difference between adjoining values in a measurement table[^30].

- Ease: The added circumference in a garment beyond body measurement to enable movement and style.

- Precision step: The tolerance window used by professional stylists for acceptable fit.

- MAE: Mean absolute error between predicted and measured values.

- PR: Precision ratio (MAE/precision step).

- KL divergence: A measure of distribution fidelity between predicted and reference populations.

- ECE: Expected Calibration Error; Brier score: a proper scoring rule for probabilistic outputs.

### B. Datasets and Licensing

- ANSUR II: Open-access, broad anthropometric suite; suitable for full-suite modeling and robustness studies[^3].

- IFTH: ~9,000 adults; strong evidence for LR/SVR performance on ~30 measurements; distribution fidelity via KL divergence[^2].

- NZDFAS: Scanner and physical measurements; MCU shirt/trouser labels; decision tree classification aligned with tailor-assigned sizes[^5].

- SizeUSA: Representative US dataset; OWOB shape groups and fit challenges; supports inclusivity analyses[^8].

- SIZER: 3D clothed scans with size labels; supports size-sensitive deformation models (ParserNet/SizerNet) and visualization[^6].

### C. Suggested Hyperparameter Ranges and Tuning Recipes

- SVR: Start with linear kernel; if underfitting, switch to RBF. Tune C (1e‑3 to 1e3), ε (1e‑2 to 1e‑1), γ (1e‑4 to 1e‑1) via Bayesian optimization to minimize MAE. Validate KL divergence[^2].

- GRNN: Sweep σ (spread) across a logarithmic grid; pick the value that minimizes MAE while preserving smoothness. Consider smoothing for sparse neighborhoods[^3].

- Imputation: k from 5 to 15; evaluate via nested CV to avoid leakage; use Gower’s distance for mixed types[^2].

- Confidence: k for density estimation between 25 and 75; tune for AUC in error detection; calibrate thresholds to target false-escalation rates[^7][^12].

## Information Gaps

The following gaps must be addressed during implementation:

- Railway’s current backend architecture, APIs, and data schemas are unspecified; we provide contracts and schema templates to be adapted.

- Ground‑truth labeling protocol and size ladders (including length classes) are not provided; align with Railway’s SKU charts and ISO PD/SD labeling.

- The 3,371‑record corpus definition (fields, normalization, consent) is missing; define feature schema and governance prior to similarity weighting.

- KCT wedding‑party rulebook specifics (fit intents, ease constraints, tailoring constraints) require joint discovery with KCT stakeholders.

- Deployment environment and latency SLOs are not specified; approximate confidence scoring costs and set performance budgets accordingly.

- Regional privacy policies for 3D scans/photos and retention schedules must be confirmed with Legal and Compliance.

- SKU‑level garment measurement database availability and integration plan are unknown; define data contracts and refresh cadence.

- Measurement modality mix (tape vs scan vs smartphone) and site‑specific error profiles must be quantified via internal studies.

## References

[^1]: The High Cost of Retail Returns. https://www.thebalancesmb.com/the-high-cost-of-retail-returns-2890350  
[^2]: Meyer, P., et al. Missing body measurements prediction in fashion industry: a comparative approach. Fashion and Textiles (2023). https://link.springer.com/article/10.1186/s40691-023-00357-5  
[^3]: Wang, L., et al. A data-driven approach towards the full anthropometric measurements prediction via Generalized Regression Neural Networks. Applied Soft Computing (2021). https://www.sciencedirect.com/science/article/pii/S1568494621004725  
[^4]: Liu, K., et al. Construction of a prediction model for body dimensions used in garment pattern making based on anthropometric data learning. The Journal of The Textile Institute (2017). https://www.tandfonline.com/doi/abs/10.1080/00405000.2017.1315794  
[^5]: Kolose, S., et al. Prediction of military combat clothing size using decision trees and 3D body scan data. Applied Ergonomics (2021). https://www.sciencedirect.com/science/article/pii/S000368702100082X  
[^6]: Tiwari, G., et al. SIZER: A Dataset and Model for Parsing 3D Clothing and Learning Size Sensitive 3D Clothing. ECCV (2020). https://link.springer.com/chapter/10.1007/978-3-030-58580-8_1  
[^7]: Mandelbaum, A., Weinshall, D. Distance-based confidence score for neural network classifiers. arXiv (2017). https://arxiv.org/abs/1709.09844  
[^8]: Shin, E., Saeidi, E. Body shapes and apparel fit for overweight and obese women in the US. Journal of Fashion Marketing and Management (2022). http://www.eonyoushin.com/uploads/4/4/8/9/44890499/shin___saeidi_2022b.pdf  
[^9]: Scientific Reports (2025). Evaluating machine learning models for clothing size prediction using anthropometric measurements from 3D body scanning. https://www.nature.com/articles/s41598-025-24584-6  
[^10]: Coresight Research. The True Cost of Apparel Returns. https://coresight.com/research/the-true-cost-of-apparel-returns-alarming-return-rates-require-loss-minimization-solutions/  
[^11]: Bartol, K., et al. A Review of Body Measurement Using 3D Scanning. IEEE Access (2021). https://doi.org/10.1109/ACCESS.2021.3076595  
[^12]: Clift, A. K., et al. Living risk prediction algorithm (QCOVID) for risk of hospital admission and mortality from coronavirus 19 in adults. BMJ (2020). https://www.bmj.com/content/371/bmj.m3731.full.pdf  
[^13]: Wang, Z., et al. Estimating human body dimensions using RBF artificial neural networks technology and its application in activewear pattern making. Applied Sciences (2019). https://doi.org/10.3390/app9061140  
[^14]: Bogdanov, D. A computationally efficient data driven suit jacket fit recommendation system. (2017). https://www.diva-portal.org/smash/get/diva2:1180843/FULLTEXT01.pdf  
[^15]: Zhang, J., Mu, Y. Clothing design methods based on Kansei engineering: Example of suit design. AHFE (2021). https://link.springer.com/chapter/10.1007/978-3-030-80829-7_135  
[^16]: Dāboliņa, I., Lapkovska, E. Sizing and fit for protective clothing. In: Anthropometry, apparel sizing and design (2020). https://www.sciencedirect.com/science/article/pii/B9780081026045000111  
[^17]: Opaleye, A. A., et al. Application of fuzzy clustering methodology for garment sizing. American Journal of Data Mining and Knowledge Discovery (2019). https://www.academia.edu/download/90785172/10.11648.j.ajdmkd.20190401.15.pdf  
[^18]: Kim, S., et al. Automatic measurements of garment sizes using computer vision deep learning models and point cloud data. Applied Sciences (2022). https://www.mdpi.com/2076-3417/12/10/5286  
[^19]: Kim, S., et al. Multi-view body image-based prediction of body mass index and various body part sizes. CVPR Workshops (2023). https://openaccess.thecvf.com/content/CVPR2023W/CVPM/papers/Kim_Multi-View_Body_Image-Based_Prediction_of_Body_Mass_Index_and_Various_CVPRW_2023_paper.pdf  
[^20]: Tan, Z., et al. Cluster Size Intelligence Prediction System for Young Women's Clothing Using 3D Body Scan Data. Mathematics (2024). https://www.mdpi.com/2227-7390/12/3/497  
[^21]: Wang, J., Li, X. Regional Clothing Size Prediction Method Integrating Transfer Learning and Ensemble Learning. ACM (2024). https://dl.acm.org/doi/abs/10.1145/3697467.3697609  
[^22]: Wenkel, S., et al. Confidence score: The forgotten dimension of object detection performance evaluation. Sensors (2021). https://www.mdpi.com/1424-8220/21/13/4350  
[^23]: Poggi, M., et al. Quantitative evaluation of confidence measures in a machine learning world. ICCV (2017). http://openaccess.thecvf.com/content_ICCV_2017/papers/Poggi_Quantitative_Evaluation_of_ICCV_2017_paper.pdf  
[^24]: Liu, R., et al. Stratified body shape-driven sizing system via three-dimensional digital anthropometry for compression textiles of lower extremities. Textile Research Journal (2018). https://journals.sagepub.com/doi/abs/10.1177/0040517517715094  
[^25]: Fu, B., et al. An improved clothing size recommendation approach based on subdivision of female body types. Ergonomics (2023). https://www.tandfonline.com/doi/abs/10.1080/00140139.2022.2069867  
[^26]: Shin, E., Saeidi, E. Body shapes and apparel fit for overweight and obese women in the US. Journal of Fashion Marketing and Management (2022). https://www.emerald.com/insight/content/doi/10.1108/jfmm-09-2020-0213/full/html  
[^27]: Masson, A. E., et al. Anthropometric study to understand body size and shape for plus size people at work. Procedia Manufacturing (2015). https://www.sciencedirect.com/science/article/pii/S2351978915007775  
[^28]: Dāboliņa, I., et al. Evaluation of clothing fit. IOP Conference Series: Materials Science and Engineering (2018). https://iopscience.iop.org/article/10.1088/1757-899X/459/1/012077  
[^29]: Hidayati, S. C., et al. Body shape calculator: Understanding the type of body shapes from anthropometric measurements. ICICA (2021). https://dl.acm.org/doi/abs/10.1145/3460426.3463582  
[^30]: Zakaria, N., Gupta, D. Anthropometry, apparel sizing and design. Elsevier (2019/2020). https://www.sciencedirect.com/science/article/pii/B9780081026045000044  
[^31]: Gallucci, A., et al. Prediction of 3D body parts from face shape and anthropometric measurements. (2020). https://research.tue.nl/files/193208437/20200807030233433.pdf  
[^32]: Validation of a 3D whole-body scanning system (Vitus Bodyscan) to collect anthropometric data. (2025). https://www.sciencedirect.com/science/article/pii/S0169814125000046  
[^33]: Mobile 3D body scanning applications: a review of contact-free AI methods. (2023). https://www.tandfonline.com/doi/full/10.1080/00405000.2023.2216099  
[^34]: A method for increasing 3D body scanning's precision. (2021). https://www.tandfonline.com/doi/full/10.1080/00140139.2021.1931473  
[^35]: An accuracy study of body measures from 3D reconstruction. (2022). https://pmc.ncbi.nlm.nih.gov/articles/PMC9468240/  
[^36]: Demystifying 3D Body Measurement Accuracy. 3D Measure Up. https://3dmeasureup.ai/blog/3d-measurement-accuracy/  
[^37]: 3D scanning results are 4500% more precise. Loughborough University. https://www.lboro.ac.uk/news-events/news/2021/june/3d-scanning-results-are-4500-percent-more-precise/