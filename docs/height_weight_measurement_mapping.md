# Height/Weight to Suit Measurement Mapping for Short Suits (34S–50S)

## Executive Summary

Short suits exist to correct a persistent problem in ready-to-wear suiting: jacket and sleeve proportions that are scaled to an “average” or taller frame, leaving shorter men with sleeves that stack at the wrist, jackets that hang past the optimal break, and pants with excessive rise and inseam. A systematic mapping from height and weight to suit measurements for short lengths (34S–50S) is therefore valuable both as a pre-fit heuristic and as a baseline for algorithmic sizing. This report assembles the necessary anthropometric foundations, translates them into practical mapping, and proposes a validation framework to improve prediction accuracy.

Four findings anchor the approach:

- Jacket length categories correlate with height bands. Retail guidance consistently associates Short (S) lengths with approximately 5'4"–5'7", Regular (R) with 5'7.5"–5'11", Long (L) with 5'11.5"–6'2.5", and X-Long (XL) with 6'3" and up. Within Short, manufacturers’ charts show meaningful chest, shoulder, sleeve, and length differences that must be reconciled to a coherent size roll for 34S–50S.[^1][^4][^5][^12]

- Height and weight alone are insufficient to guarantee fit. Body type—operationalized here via frame size (small, medium, large) and shape descriptors (slim/rectangle, regular/trapezoid, broad/inverted triangle, athletic)—modulates the relationships among chest, shoulder breadth, waist, and sleeve length. Frame-size methods based on elbow breadth percentiles or the “HAT” model (height vs. biacromial + bitrochanter width) provide pragmatic adjustments to chest/shoulder predictions; shape-aware heuristics then guide waist and sleeve trade-offs.[^13][^14][^8]

- Manufacturer charts exhibit inter-brand variance. A consolidated Short suit table reveals systematic differences in how brands allocate chest ranges, shoulder widths, sleeve lengths, and jacket lengths across the same nominal size. This variance necessitates brand-specific calibration and a conservative approach when generalizing height/weight recommendations.[^4][^5][^12]

- Predictive modeling must go beyond linear bivariate rules. While early sizing systems used height and weight bivariate tables, modern evidence supports more expressive models—gradient boosting for measurement prediction (R² ≈ 0.647 on key dimensions) and machine learning classifiers for size assignment from 3D-scan features—combined with fit-loss minimization and shape-aware constraints.[^9][^10][^18]

What practitioners can do immediately:

- Use height bands to assign length category (Short vs. Regular vs. Long), then use height/weight to triangulate a first chest size. Apply frame-size adjustments (elbow breadth or HAT) to refine chest/shoulder estimates, and shape-aware heuristics to adjust waist and sleeve. Always plan for minimal alterations to correct sleeve break and jacket waist suppression.[^1][^14][^8]

Where data gaps persist:

- Public, multi-brand 3D body-scan data for men under 5'7" are limited; manufacturer size charts are proprietary; and mapping ease (the difference between body and garment measurements) varies by brand and style. We propose a validation plan—stratified by height, weight, and body type; measured via 3D scans; evaluated using fit-loss metrics—to iteratively improve predictions and publish brand-calibrated matrices.[^9][^10]

The report proceeds from anthropometric foundations to a consolidated short-suit table, a height/weight-to-size mapping, modeling approaches, body-type adjustments, edge-case considerations, and a validation plan.

[^1]: Suit Sizes & Size Chart - Mens Style Guide - Macy’s.  
[^4]: Men’s Suits Size Chart (Cloudfront hosted PDF).  
[^5]: Men’s Suit Sizing Chart - Aerostich.  
[^12]: Size Charts | Suit, Tuxedo & Accessory Measurements - SuitShop.  
[^9]: Anthropometric measurements and size chart development using ISO 8559-1 and ASTM D5585-10.  
[^10]: Evaluating machine learning models for clothing size prediction using anthropometric measurements from 3D body scanning.  
[^14]: Body Frame Measures and Perceptions of Frame Size and Weight (Frisancho-based methods).  
[^8]: Anthropometry, Apparel Sizing and Design (Gupta & Zakaria, 2014).  
[^18]: Predicting t-shirt size from height and weight (NHANES-based modeling approach).



## Anthropometric Foundations: Body Proportions Relevant to Short Suits

Suit fit depends on the interaction of linear dimensions (heights and lengths) and breadth/girth dimensions (shoulder breadth, chest girth, waist girth). For short suits, the controlling lengths are stature, shoulder height, shoulder–elbow length, shoulder–waist length (omphalion), and sleeve length, while the controlling breadths/girths are biacromial breadth, chest girth, and waist girth. Robust measurement protocols—consistent landmarking, posture, and tape tension—are essential to minimize error and ensure reproducibility.[^7]

Two traditions inform sizing system design. Classical bivariate systems used height and weight to group bodies, often with limited success. Contemporary practice identifies control dimensions—key measures that drive pattern blocks and sizing bands—then builds classification and prediction around them.[^8] Multivariate statistics (principal component analysis), clustering, and modern machine learning have superseded simplistic bivariate tables, especially when 3D-scan data are available.[^8][^9][^10]

### Key Dimensions and Control Dimensions

In men's suiting, the jacket number conventionally corresponds to chest girth (in inches). Shoulder and sleeve proportions, as well as jacket body length, must scale coherently with chest and with the wearer’s stature and limb lengths. For prediction and grading, a practical control set is:

- Stature (overall height)
- Shoulder height (acromion)
- Shoulder–elbow length
- Shoulder–waist length (omphalion)
- Biacromial breadth (shoulder width)
- Chest girth (at the fullest point)
- Waist girth (natural waist)

The goal is not to predict every anthropometric dimension, but to predict those that drive garment fit and aesthetics (chest, shoulders, sleeve) while respecting length proportions for short frames.[^8][^7]

### Proportional Relationships and Percentiles

Because short suits target men at the lower end of the stature distribution, percentiles for relevant linear measures guide expectations for sleeve and jacket-body length. The 2016 NCSU anthropometric tables provide detailed male percentiles for several lengths relevant to suiting:

- Shoulder height (standing): mean ≈ 144.25 cm (56.79 in); 5th ≈ 133.78 cm (52.67 in); 95th ≈ 153.17 cm (60.30 in).
- Shoulder–elbow length: mean ≈ 36.90 cm (14.53 in); 5th ≈ 34.02 cm (13.39 in); 95th ≈ 39.88 cm (15.70 in).
- Shoulder–waist length (omphalion): mean ≈ 38.37 cm (15.11 in); 5th ≈ 34.27 cm (13.49 in); 95th ≈ 42.72 cm (16.82 in).[^3][^2]

To illustrate the distributions relevant to short suits, the following table summarizes selected male percentiles from NCSU (converted to inches). These are the controlling lengths that underpin jacket sleeve and body-length decisions.

Table 1. Selected male percentiles (inches) for controlling lengths (NCSU 2016)

| Measure                          | Mean | 5th  | 25th | 50th | 75th | 95th |
|----------------------------------|------|------|------|------|------|------|
| Shoulder height (standing)       | 56.79| 52.67| 54.89| 56.42| 58.01| 60.30|
| Shoulder–elbow length            | 14.53| 13.39| 14.05| 14.52| 15.00| 15.70|
| Shoulder–waist length (omphalion)| 15.11| 13.49| 14.42| 15.08| 15.76| 16.82|

Interpreting Table 1: the 5th percentile shoulder–elbow length (~13.4 in) and shoulder–waist length (~13.5 in) indicate that a non-trivial share of men will require shorter sleeve and body-length scaling than an “average” (50th percentile) pattern provides. These differences accumulate: a shorter shoulder–elbow length calls for a shorter sleeve, and a shorter shoulder–waist length calls for a shorter jacket body to maintain proper waist suppression and break. When combined with stature bands for Short suits (see below), these percentiles explain why off-the-rack regular-length suits commonly present as “long” on shorter men.[^3][^2]

To visualize the underlying distributions, Figures 1–3 plot representative percentile profiles for the key lengths used in short-suit mapping.

![Shoulder height percentile distribution (NCSU Anthropometric Data)](.pdf_temp/viewrange_chunk_5_21_25_1765987197/images/6kf162.jpg)

![Shoulder–elbow length distribution (NCSU Anthropometric Data)](.pdf_temp/viewrange_chunk_1_1_5_1765987195/images/up8ijl.jpg)

![Shoulder–waist length (omphalion) distribution (NCSU Anthropometric Data)](.pdf_temp/viewrange_chunk_1_1_5_1765987195/images/h2vffq.jpg)

These distributions underscore two practical points. First, limb- and torso-length variation at a given stature is meaningful; thus, height alone cannot capture the adjustments needed for short suits. Second, a size system that accounts for control dimensions (shoulder–elbow, shoulder–waist, biacromial breadth) can reduce systematic misfit in the short population while preserving aesthetics (e.g., proper sleeve break, jacket waist suppression, and break at the trouser).[^3][^2][^7][^8]



## Suit Sizing Standards and Short Suit Specifications (34S–50S)

The sizing convention in men’s suits pairs a numeric chest size (e.g., 40) with a lettered length category: Short (S), Regular (R), Long (L), and sometimes X-Long (XL). The number approximates the wearer’s chest circumference in inches, while the letter indicates jacket and sleeve length proportions. Retailer guidance converges on the following height bands for length categories:

Table 2. Height bands vs. jacket length categories

| Height Range     | Jacket Length |
|------------------|---------------|
| 5'4"–5'7"        | Short (S)     |
| 5'7.5"–5'11"     | Regular (R)   |
| 5'11.5"–6'2.5"   | Long (L)      |
| 6'3" and up      | X-Long (XL)   |

These bands are consistent with department store guidance and are mirrored across multiple brands, confirming Short as the default starting point for men at or below approximately 5'7" (with individual variation).[^1][^16][^5][^11]

Within the Short category, manufacturers publish chest, shoulder, sleeve, and length ranges that define the size roll. While the sizes share the same nominal chest number, Short jackets differ from their Regular counterparts by shorter sleeves and bodies; in some brands, shoulder breadth and chest ranges are also adjusted. A consolidated view across three sources reveals both commonalities and brand-specific variance:

Table 3. Consolidated Short suit specifications (selected fields)

| Size | Chest (in) | Shoulder (in) | Sleeve (in) | Jacket Length (in) | Height Band (in) | Weight (lbs) |
|------|------------|----------------|-------------|---------------------|------------------|--------------|
| 34S  | 32–34      | 17.75          | 30.0        | 32.0                | 5'6"–5'9"        | 110–120      |
| 36S  | 33–35      | 18.00          | 30.0        | 32.0                | 5'6"–5'9"        | 120–130      |
| 38S  | 36–38      | 18.75          | 30.5        | 30.5                | 5'8"–5'11"       | 145–155      |
| 40S  | 38–40      | 19.25          | 33.0        | 31.0                | 5'8"–5'11"       | 160–170      |
| 42S  | 40–42      | 19.75          | 33.0        | 31.0                | 5'10"–6'1"       | 180–190      |
| 44S  | 42–44      | 20.25          | 34.0        | 31.0                | 5'10"–6'1"       | 200–210      |
| 46S  | 44–46      | 20.75          | 34.0        | 31.5                | 6'0"–6'3"        | 210–220      |
| 48S  | 48–50      | 21.75          | 35.0        | 31.75               | 6'1"–6'5"        | 240–260      |
| 50S  | 48–50      | 21.75          | 35.0        | 31.75               | 6'1"–6'5"        | 240–260      |

Notes: Values consolidate a multi-brand chart; specific fields vary by source and brand. For 36S, one source lists sleeve 32" and length 30". Shoulder widths for 38S–48S are not specified in one source; where missing, values are carried from the corresponding Regular where helpful for orientation. Always consult the brand’s own chart before use.[^4][^5]

Even from this consolidated view, three patterns matter for short suits:

- Sleeve length shortens in S vs. R within the same chest size. This directly addresses the shorter shoulder–elbow lengths observed in anthropometric distributions.

- Jacket bodies shorten in S. Maintaining proportional jacket length on shorter statures improves visual balance (waist suppression, trouser break).

- Chest and shoulder breadth ranges shift modestly across brands. This variation, along with style ease, is the primary driver of inter-brand fit differences and underscores why height/weight-to-size mapping must be brand-calibrated.[^4][^5][^12]



## Height/Weight Ranges that Typically Fit Each Short Suit Size (34S–50S)

Retailer and manufacturer charts rarely provide a single mapping from height and weight to size; instead, they show ranges for height and weight alongside chest, shoulder, sleeve, and length. This reflects the reality that two men with the same height and weight can have different shapes (shoulders, chest, waist). Nonetheless, these ranges are a practical starting point for initial sizing.

Table 4 synthesizes height/weight bands that typically correspond to each Short size, anchored in the consolidated short-suit table (Table 3) and adjusted with height-band guidance for Short jackets.

Table 4. Short suit mapping by height and weight (starting point)

| Size | Typical Height Range | Typical Weight Range | Anchors and Notes |
|------|----------------------|----------------------|-------------------|
| 34S  | 5'3"–5'6"            | 110–125              | At the lower end of the stature distribution; prioritize sleeve shortening and higher waist suppression. |
| 36S  | 5'4"–5'7"            | 120–135              | Core Short band; aligns with Macy’s Short height band. |
| 38S  | 5'6"–5'9"            | 135–155              | Overlaps with lower end of Regular heights in some charts; use sleeve length to discriminate. |
| 40S  | 5'7"–5'10"           | 155–175              | Some brands push 40S up to ~5'11"; use sleeve/body lengths to confirm category. |
| 42S  | 5'8"–5'11"           | 175–195              | Higher variance across brands; expect shoulder breadth to increase. |
| 44S  | 5'9"–6'0"            | 195–215              | Upper Short boundary; some wearers may prefer Regular length depending on limb proportions. |
| 46S  | 5'10"–6'1"           | 210–230              | Transitional to Regular; check jacket body length and sleeve break carefully. |
| 48S  | 6'0"–6'3"            | 235–265              | Many brands show similar 48S/50S entries; frame and waist guidance become decisive. |
| 50S  | 6'1"–6'3"            | 250–275              | Highest Short; consider Long if sleeve and body lengths feel constrained. |

These bands draw on the consolidated short-suit table and mainstream height bands (Table 2). They should be interpreted as starting points, not absolutes. For borderline cases—e.g., a wearer near 5'11" who could fit either 40S or 40R—prioritize sleeve length and jacket body proportion to decide between Short and Regular. In practice, if a 40R sleeve is more comfortable at the desired break, the wearer may prefer Regular despite being within a Short height band; such cases are common near the band boundaries and do not invalidate the mapping, they simply highlight where anthropometric variability requires human judgment.[^4][^1][^6]



## Mathematical Models for Predicting Suit Measurements from Height/Weight

Historically, apparel sizing relied on bivariate tables of height and weight. While intuitive, these tables underperform because they do not account for shape variability (e.g., shoulder breadth vs. waist girth). Modern sizing systems identify control dimensions, reduce dimensionality (e.g., via principal component analysis), and either predict measurements directly or classify sizes using learned decision boundaries. Two modern model families are most relevant: (i) regression and gradient boosting for predicting continuous measurements (chest, shoulder, sleeve), and (ii) classification for size assignment (34S, 36S, …, 50S) with or without sub-size cuts (slim/regular/broad).

Table 5 compares model options and inputs.

Table 5. Model family comparison for short-suit sizing

| Model family                  | Inputs                                | Outputs                                  | Strengths                                           | Limitations                                          | Reported performance (illustrative) |
|------------------------------|---------------------------------------|------------------------------------------|-----------------------------------------------------|------------------------------------------------------|-------------------------------------|
| Linear regression             | Height, weight                         | Chest, shoulder, sleeve, jacket length   | Simple, interpretable                               | Misses shape interactions                            | Baseline; often insufficient        |
| Gradient boosting regression  | Height, weight, selected frame indices | Chest, shoulder, sleeve, jacket length   | Captures non-linearities; strong on tabular data    | Needs feature engineering (frame/shape proxies)       | R² ≈ 0.647 (key dimensions)[^9]     |
| ML classifiers (RF/GBM/NN)    | 3D-scan features or robust anthropometrics | Size class (e.g., 40S), fit preference   | Directly optimizes size accuracy; integrates style  | Requires richer inputs; black-box if not careful      | Promising in 3D-scan settings[^10]  |
| Hybrid (regression + rules)   | Predicted measurements + shape heuristics | Final size and cut                       | Aligns with tailoring practice; explainable         | Rule maintenance across brands                        | Good practical results              |

A practical pipeline for short suits:

1) Predict key measurements from height/weight plus frame/shape proxies (e.g., elbow breadth percentiles, HAT width sum).  
2) Map predicted chest to a nominal size (34–50) and predicted shoulder–elbow to sleeve length.  
3) Apply shape-aware heuristics (e.g., inverted triangle → broader shoulders/ chest, narrower waist) to select between cuts (slim/regular/broad) and adjust waist and ease allowances.  
4) Evaluate with fit-loss metrics and iterate.[^8][^9][^10][^14]

Table 6 lists the input features with evidence on predictive power.

Table 6. Input features for measurement prediction and expected contribution

| Feature                                | Expected contribution to prediction | Rationale and evidence |
|----------------------------------------|-------------------------------------|------------------------|
| Height                                 | High for sleeve and jacket length   | Strong driver of linear dimensions; part of control set in PCA-based systems.[^8] |
| Weight                                 | Medium–high for chest and waist     | Weight correlates with girths; primary feature for missing-measurement imputation.[^18] |
| Elbow breadth percentile (frame)       | Medium for shoulder/chest breadth   | Frame size indicator; percentiles define small/medium/large frames.[^14] |
| HAT width sum (biacromial + bitrochanter) | Medium for shoulder/hip balance   | Captures width independent of stature; used in frame-size modeling.[^14] |
| 3D-scan girths/widths (if available)   | High for all target measurements    | ML models trained on scan features show strong performance in size prediction.[^10] |

These inputs are grounded in standards and practice: ISO 8559-1 and ASTM D5585-10 outline measurement selection and definitions; PCA and clustering inform control dimensions and size-roll design; and gradient boosting has demonstrated improved accuracy over linear models for anthropometric prediction in apparel contexts.[^9][^8][^7]

### Feature Engineering and Data Requirements

When full 3D scans are unavailable, frame indices and shape proxies become essential:

- Frame size via elbow breadth percentiles (Frisancho): small (<15th), medium (15th–85th), large (>85th). This yields an interpretable, population-referenced proxy for skeletal breadth.[^14]

- HAT model: regress height against the sum of biacromial and bitrochanter diameters; classify small/medium/large around ±1 SD from the regression line. Provides a two-dimensional frame concept (linear + width).[^14]

- Shape descriptors: triangle (waist/hips > shoulders), inverted triangle (shoulders/chest > waist), trapezoid (balanced, athletic), rectangle (linear). These are used not as rigid categories but as adjustments to predicted chest, shoulder, and waist—e.g., inverted triangle → add breadth to shoulders/chest, subtract ease at waist.[^8]

Data quality and measurement protocol matter. CDC’s anthropometry manual provides standardized procedures for landmarking and measuring (e.g., elbow breadth, waist girth), which help reduce error variance and improve model reliability.[^7]



## Body Types and Their Effect on Measurements (Slim, Regular, Broad, Athletic)

Retailers commonly offer cuts labeled slim, regular (sometimes “modern”), and broad (sometimes “classic” or “relaxed”). These cuts reflect different ease allowances and distribution of room through the chest, waist, and hips. On shorter frames, the impact is magnified: even small absolute misalignments in shoulder width or sleeve length are visually obvious.

Table 7. Body type characteristics and suit measurement implications

| Body type (descriptor) | Typical characteristics                                 | Implication for suit measurements                                 |
|------------------------|----------------------------------------------------------|--------------------------------------------------------------------|
| Slim / Rectangle       | Shoulders, chest, waist, hips similar; lower body fat   | Favor slim cuts; moderate shoulder padding to broaden; slim trousers to avoid excess fabric. |
| Regular / Trapezoid    | Balanced shoulders and waist; muscular but not bulky    | Regular cut with moderate ease; works well with classic lapels.    |
| Broad / Inverted triangle | Broad shoulders/chest; narrower waist                | Choose broader cuts; avoid extra padding; balance with slightly roomier trousers. |
| Oval                   | Fuller midsection; shoulders may be narrower than waist | Classic/relaxed fits; higher rise and more waist ease; structured shoulder to frame the torso. |

These descriptors echo industry practice: broad/inverted triangle shapes benefit from cuts with more upper-body room and balanced lapels; slim/rectangle shapes benefit from slimmer trousers and structured shoulders to create the illusion of width; and oval shapes require more room through the midsection with a suppressed visual emphasis on the waist.[^13][^8]

Frame size (small/medium/large) complements these shape categories by modulating skeletal breadth. A medium-frame rectangle may have the same stature and weight as a medium-frame inverted triangle, yet require a different shoulder and chest allowance. Frame indices (elbow breadth percentiles or HAT) thus provide an objective anchor for otherwise subjective cut recommendations.[^14]



## Edge Cases and Special Considerations for Short Suits

Boundary conditions arise near height-band transitions and among atypical proportions. Addressing them proactively reduces alteration costs and returns.

Table 8. Edge-case patterns and recommended adjustments

| Edge case                                                | Diagnostic cue                                      | Recommended adjustment                                        |
|----------------------------------------------------------|-----------------------------------------------------|----------------------------------------------------------------|
| Long torso, short limbs                                  | Shoulder–elbow below 5th percentile; shoulder–waist near 50th–75th | Prioritize shorter sleeve; slightly longer jacket body may be acceptable. |
| Short torso, long arms                                   | Shoulder–elbow above 75th; shoulder–waist below 25th | Favor Regular sleeve length even if height suggests Short; moderate jacket body. |
| Broad shoulders with narrow waist (inverted triangle)    | HAT width sum high; elbow breadth >85th percentile  | Broader chest/shoulder allowance; slimmer waist suppression; choose regular/broad cut. |
| High waist-hip differential (triangle)                   | Waist girth >> chest; hip breadth above average     | Classic/relaxed cuts; higher rise; suppress waist less aggressively. |
| Borderline height (e.g., 5'7.5") near S/R boundary       | Height falls in overlap                             | Choose by sleeve comfort: if 40R sleeve breaks naturally vs. 40S bunching, prefer 40R. |
| High BMI with short stature                              | Weight high for height band                          | Prioritize comfort ease; expect larger waist adjustments; avoid overly slim cuts. |

In all cases, minimal alterations typically include: sleeve shortening (or slight lengthening), waist suppression adjustments, and trouser hemming and rise tweaks. The key is to respect the wearer’s proportional signal (limb vs. torso) while maintaining the suit’s visual hierarchy (shoulder line, lapel width, jacket break).[^14][^8][^1]



## Validation and Fit-Assessment Plan

A sizing system earns its value by minimizing fit loss—the difference between predicted body measurements and the garment’s finished dimensions—while meeting consumer preferences for ease and silhouette. We propose a three-part validation framework.

- Fit-loss minimization. Following recent apparel research, compute the deviation between predicted anthropometric measurements and the target garment’s corresponding dimensions. Use mean squared error (MSE) and related metrics to track performance; iterate model features and rules to reduce overall fit loss.[^9]

- Accuracy and preference evaluation. For size classification (34S–50S), track classification accuracy and top-2 accuracy. Where possible, measure consumer satisfaction with ease and silhouette using Likert scales; compare across body types to ensure no systematic disadvantage (e.g., inverted triangle wearers receiving consistently poor shoulder fit).[^10]

- Protocol and data quality. Use standardized measurement procedures and trained staff to collect anthropometric inputs. If 3D body scans are available, incorporate automated feature extraction to improve measurement accuracy and reduce manual error. Where scans are unavailable, record frame indices (elbow breadth, HAT width sum) alongside height and weight to preserve shape information.[^7][^10]

Table 9. Validation metrics and target thresholds

| Metric                                 | Target (initial)                  | Rationale                                   |
|----------------------------------------|-----------------------------------|---------------------------------------------|
| Regression MSE (chest/shoulder/sleeve) | ≤ baseline linear model           | Ensure non-linear models outperform basics. |
| Classification accuracy (size + cut)   | ≥ 75% top-1; ≥ 90% top-2          | Consumer-grade utility with room to improve.|
| Fit-loss reduction vs. baseline        | ≥ 20% reduction                   | Meaningful improvement in practical fit.    |
| Consumer satisfaction (silhouette/ease)| ≥ 4.0/5.0 average                 | Experience parity with off-the-rack fits.   |

A pragmatic approach is to A/B test the mapping in a retail setting: offer the algorithmic recommendation as a starting point and measure alteration incidence and customer satisfaction relative to business-as-usual selection. Iterations incorporate fit-loss analysis and feedback loops to recalibrate size bands and shape rules.[^9][^10]



## Implementation Guide: From Height/Weight to Suit Measurements

Step-by-step procedure for short suits (34S–50S):

1) Confirm length category by height. If the wearer is within 5'4"–5'7", start with Short; if borderline (e.g., 5'7.5"), compare Short vs. Regular sleeve and jacket body preferences.  
2) Use height and weight to propose an initial chest size (e.g., 40S). Consult the brand’s own chart for chest, shoulder, sleeve, and length ranges.  
3) Adjust for frame size. If elbow breadth is below the 15th percentile, consider moving toward the lower end of the chest range and narrowing shoulder; if above the 85th percentile, consider the upper end. Apply HAT width sum similarly to reconcile shoulder vs. hip balance.  
4) Adjust for body type. Inverted triangle (broad shoulders/chest) → favor regular or broad cuts; rectangle (linear) → slim cuts may work; triangle (waist/hips fuller) → classic/relaxed fits.  
5) Validate sleeve and jacket body. Confirm that the sleeve breaks at the desired point and that the jacket body hits at a flattering length with appropriate waist suppression.  
6) Plan alterations. Common short-suit adjustments: sleeve shortening, waist suppression tuning, trouser hemming and cuff (if any), and occasional small body-length changes.  
7) Log outcomes. Record the chosen size, cut, anthropometric inputs, and alterations to feed continuous improvement.

Table 10 provides a compact algorithm checklist.

Table 10. Decision checklist for sizing short suits

| Step | Decision cue                                   | Action                                                                |
|------|------------------------------------------------|-----------------------------------------------------------------------|
| 1    | Height 5'4"–5'7"                               | Choose Short length category                                          |
| 2    | Height/weight near band center                 | Select mid-range chest within size                                    |
| 3    | Elbow breadth percentile (small vs. large)     | Adjust chest/shoulder up or down within size                          |
| 4    | HAT width sum (narrow vs. broad)               | Adjust shoulder/chest vs. waist balance                               |
| 5    | Shape: inverted triangle vs. rectangle         | Choose broad or slim cut; adjust ease                                 |
| 6    | Sleeve break preference                        | Final sleeve length decision (alter if needed)                        |
| 7    | Trouser break and rise                         | Set hem and rise; anticipate minor adjustments                        |
| 8    | Outcome log                                   | Record inputs, outputs, alterations for model iteration               |

This procedure is intentionally explainable and tailor-friendly. It preserves the speed benefits of height/weight-based pre-selection while acknowledging that final fit is a joint function of anthropometry and wearer preference.[^1][^4][^14][^13][^8]



## Data Sources and Limitations

This report triangulates across standards (ISO 8559-1; ASTM D5585-10), comprehensive anthropometric summaries (NCSU 2016 tables), peer-reviewed research on modeling approaches (gradient boosting; 3D-scan ML), and commercial size charts that operationalize length categories and size rolls. The consolidation of Short suit specs (Table 3) relied on three public charts; although they are directionally consistent, their ranges differ in chest allocations, shoulder widths, and sleeve lengths, which is typical of proprietary brand grading.[^9][^3][^2][^4][^5][^12]

Key limitations and information gaps:

- There is no comprehensive, public, multi-brand 3D-scan dataset specific to men under 5'7" in the sources reviewed; access to such data would materially improve shape-aware prediction.  
- Manufacturer proprietary grading rules and ease allowances vary by brand and style and are not public; the consolidated short-suit table should be treated as indicative, not definitive.  
- A direct height/weight-to-size mapping for 34S–50S requires brand-specific calibration; the ranges here are starting points.  
- Numeric tie-ins between ASTM/ISO control dimensions and commercial Short suit grading are not fully documented in public sources.  
- Consumer preference data for ease and silhouette across body types are scarce in the public domain.

Future data collection should prioritize 3D scans of short-stature men, brand-by-brand size-roll sampling, and consumer fit studies stratified by body type and frame size. This will support publishing brand-calibrated height/weight matrices and refining predictive models.[^10]



## Appendix: Consolidated Data Tables

Table A1. Short suits (34S–50S) consolidated measurements and ranges

| Size | Chest (in) | Shoulder (in) | Sleeve (in) | Jacket Length (in) | Height (in) | Weight (lbs) |
|------|------------|----------------|-------------|---------------------|-------------|--------------|
| 34S  | 32–34      | 17.75          | 30.0        | 32.0                | 5'6"–5'9"   | 110–120      |
| 36S  | 33–35      | 18.00          | 30.0–32.0   | 30.0–32.0           | 5'6"–5'9"   | 120–130      |
| 38S  | 36–38      | 18.75          | 30.5        | 30.5                | 5'8"–5'11"  | 145–155      |
| 40S  | 38–40      | 19.25          | 33.0        | 31.0                | 5'8"–5'11"  | 160–170      |
| 42S  | 40–42      | 19.75          | 33.0        | 31.0                | 5'10"–6'1"  | 180–190      |
| 44S  | 42–44      | 20.25          | 34.0        | 31.0                | 5'10"–6'1"  | 200–210      |
| 46S  | 44–46      | 20.75          | 34.0        | 31.5                | 6'0"–6'3"   | 210–220      |
| 48S  | 48–50      | 21.75          | 35.0        | 31.75               | 6'1"–6'5"   | 240–260      |
| 50S  | 48–50      | 21.75          | 35.0        | 31.75               | 6'1"–6'5"   | 240–260      |

Source: Consolidated from multi-brand charts. Shoulder and sleeve ranges vary by brand; consult the specific brand’s size chart before purchase.[^4][^5]

Table A2. Selected male anthropometric percentiles (inches) for controlling lengths

| Measure                          | Mean | 5th  | 25th | 50th | 75th | 95th |
|----------------------------------|------|------|------|------|------|------|
| Shoulder height (standing)       | 56.79| 52.67| 54.89| 56.42| 58.01| 60.30|
| Shoulder–elbow length            | 14.53| 13.39| 14.05| 14.52| 15.00| 15.70|
| Shoulder–waist length (omphalion)| 15.11| 13.49| 14.42| 15.08| 15.76| 16.82|

Source: NCSU Anthropometric Detailed Data Tables (2016).[^3]

Table A3. Height bands and typical corresponding Short sizes (illustrative)

| Height band  | Typical Short sizes (illustrative weight bands) |
|--------------|-----------------------------------------------|
| 5'4"–5'5"    | 34S (110–125 lbs)                             |
| 5'5"–5'6"    | 36S (120–135 lbs)                             |
| 5'6"–5'8"    | 38S (135–155 lbs)                             |
| 5'8"–5'10"   | 40S (155–175 lbs)                             |
| 5'9"–5'11"   | 42S (175–195 lbs)                             |
| 5'10"–6'0"   | 44S (195–215 lbs)                             |
| 5'11"–6'1"   | 46S (210–230 lbs)                             |
| 6'0"–6'2"    | 48S (235–265 lbs)                             |
| 6'2"–6'3"    | 50S (250–275 lbs)                             |

Notes: These are indicative bands for initial sizing. Borderline cases should be resolved by sleeve/jacket body preference and minimal alterations.[^1][^4][^6]

Table A4. Frame-size classification options (summary)

| Method                     | Measurement(s)                         | Classification rule                               |
|---------------------------|----------------------------------------|---------------------------------------------------|
| Elbow breadth percentiles | Elbow breadth                          | Small <15th; Medium 15th–85th; Large >85th       |
| HAT frame model           | Height; biacromial + bitrochanter sum  | Small/Medium/Large around regression ±1 SD        |
| Wrist ratio (historical)  | Height:wrist circumference ratio       | Population-defined r ranges for small/medium/large|

Sources: Frisancho-based methods and HAT model; see Body Frame Measures literature for full derivations and instrument details.[^14]



## References

[^1]: Suit Sizes & Size Chart - Mens Style Guide - Macy’s. https://www.macys.com/ce/mens-style-guide/suit-sizes-chart  
[^2]: Anthropometric Data for U.S. Adults (Summary Table, 2020) - NCSU Ergocenter. https://ergocenter.ncsu.edu/wp-content/uploads/sites/18/2020/07/Anthropometry-Summary-Table-2020.pdf  
[^3]: Anthropometric Detailed Data Tables (2016) - NCSU Ergocenter. https://multisite.eos.ncsu.edu/www-ergocenter-ncsu-edu/wp-content/uploads/sites/18/2016/06/Anthropometric-Detailed-Data-Tables.pdf  
[^4]: Men’s Suits Size Chart (Cloudfront hosted PDF). https://d3gqasl9vmjfd8.cloudfront.net/b71054dc-4c26-4afc-bbb1-6c4681318852.pdf  
[^5]: Men’s Suit Sizing Chart - Aerostich. https://www.aerostich.com/pages/mens-suit-sizing-chart  
[^6]: Clothing Fit Guide for Short Men | Peter Manning NYC. https://petermanningnyc.com/pages/fit-guide  
[^7]: Body Measurements (Anthropometry) Manual - CDC NHANES III. https://wwwn.cdc.gov/nchs/data/nhanes3/manuals/anthro.pdf  
[^8]: Anthropometry, Apparel Sizing and Design (Gupta & Zakaria, 2014). https://ftp.idu.ac.id/wp-content/uploads/ebook/ip/BUKU%20ANTROPOMETRI/Anthropometry,%20apparel%20sizing%20and%20design.pdf  
[^9]: Contribution to the research of Anthropometric measurements and size chart development (ISO 8559-1, ASTM D5585-10). https://www.sciencedirect.com/science/article/pii/S2590291125003067  
[^10]: Evaluating machine learning models for clothing size prediction using anthropometric measurements from 3D body scanning. https://www.nature.com/articles/s41598-025-24584-6  
[^11]: Men’s Suit Size Chart - Hockerty. https://www.hockerty.com/en-us/blog/suit-size-chart  
[^12]: Size Charts | Suit, Tuxedo & Accessory Measurements - SuitShop. https://suitshop.com/size-charts/  
[^13]: Male Body Types: Get to Know Them and Dress for Your Best Look - Hockerty. https://www.hockerty.com/en-us/blog/male-body-types  
[^14]: Body Frame Measures and Perceptions of Frame Size and Weight (Frisancho-based methods). https://vtechworks.lib.vt.edu/bitstream/handle/10919/45772/LD5655.V855_1987.M476.pdf  
[^15]: Suit size based on height and weight (blog guidance) - Suits99. https://www.suits99.com/blogs/news/suit-size-based-on-height-and-weight  
[^16]: Men’s suits & sportcoats: find your fit & how to measure - Nordstrom (PDF). https://www.nordstrom.com/sizeguides/1456_sizeguide.pdf  
[^17]: Size Chart - Men’s Suiting - Kenneth Cole. https://www.kennethcole.com/pages/size-chart-mens-suiting  
[^18]: Predicting t-shirt size from height and weight (NHANES-based modeling approach). https://tylerburleigh.com/blog/2019/09/27/