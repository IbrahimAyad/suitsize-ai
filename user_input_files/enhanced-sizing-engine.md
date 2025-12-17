# EnhancedSizingEngine - Complete Technical Reference

## Overview

The EnhancedSizingEngine is KCT Menswear's AI-powered suit sizing system that provides accurate size recommendations based on customer measurements. Built on analysis of 3,371 customer records, it achieves 91% accuracy with a 9% return rate (compared to 15% industry average).

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Frontend (React)                                │
│  ┌─────────────────────────────────────────────────────────────────┐   │
│  │  EnhancedSizeGuide.tsx (1,266 lines)                            │   │
│  │  - Circular slider interactions                                  │   │
│  │  - Advanced measurements panel                                   │   │
│  │  - Size history tracking                                         │   │
│  │  - Feedback system                                               │   │
│  └─────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     Edge Functions (Supabase)                            │
│  ┌────────────────────────────┐  ┌────────────────────────────────┐    │
│  │  enhanced-ai-size-bot      │  │  ai-size-bot                   │    │
│  │  (500 lines)               │  │  (212 lines)                   │    │
│  │  - EnhancedSizingEngine    │  │  - Railway API integration     │    │
│  │  - Full sizing algorithm   │  │  - Supabase DB fallback        │    │
│  └────────────────────────────┘  └────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                         Data Sources                                     │
│  ┌────────────────────────────┐  ┌────────────────────────────────┐    │
│  │  Railway API (Primary)      │  │  Supabase Database (Fallback) │    │
│  │  suitsize-ai-production    │  │  simple_size_recommendations   │    │
│  │  .up.railway.app           │  │  table                         │    │
│  └────────────────────────────┘  └────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Core Sizing Matrix

The sizing matrix covers **34 sizes** across 4 length categories:

### Regular Sizes (11 sizes: 34R - 54R)

| Size | Height Range | Weight Range | Chest | Waist | Drop |
|------|-------------|--------------|-------|-------|------|
| 34R | 66-70" | 125-145 lbs | 33-35" | 28-30" | 4-6" |
| 36R | 66-70" | 135-160 lbs | 35-37" | 29-32" | 4-7" |
| 38R | 67-71" | 150-175 lbs | 37-39" | 31-34" | 4-8" |
| 40R | 68-72" | 165-190 lbs | 39-41" | 33-36" | 4-8" |
| 42R | 69-73" | 180-205 lbs | 41-43" | 35-38" | 4-8" |
| 44R | 70-74" | 195-220 lbs | 43-45" | 37-40" | 4-8" |
| 46R | 70-74" | 210-235 lbs | 45-47" | 39-42" | 4-8" |
| 48R | 71-75" | 225-250 lbs | 47-49" | 41-44" | 4-8" |
| 50R | 71-75" | 240-265 lbs | 49-51" | 43-46" | 4-8" |
| 52R | 72-76" | 255-280 lbs | 51-53" | 45-48" | 4-8" |
| 54R | 72-76" | 270-295 lbs | 53-55" | 47-50" | 4-8" |

### Short Sizes (7 sizes: 34S - 46S)

| Size | Height Range | Weight Range | Chest | Waist | Drop |
|------|-------------|--------------|-------|-------|------|
| 34S | 62-66" | 125-145 lbs | 33-35" | 28-30" | 4-6" |
| 36S | 62-66" | 135-160 lbs | 35-37" | 29-32" | 4-7" |
| 38S | 63-67" | 150-175 lbs | 37-39" | 31-34" | 4-8" |
| 40S | 64-68" | 165-190 lbs | 39-41" | 33-36" | 4-8" |
| 42S | 65-69" | 180-205 lbs | 41-43" | 35-38" | 4-8" |
| 44S | 66-70" | 195-220 lbs | 43-45" | 37-40" | 4-8" |
| 46S | 66-70" | 210-235 lbs | 45-47" | 39-42" | 4-8" |

### Long Sizes (7 sizes: 36L - 48L)

| Size | Height Range | Weight Range | Chest | Waist | Drop |
|------|-------------|--------------|-------|-------|------|
| 36L | 74-78" | 135-160 lbs | 35-37" | 29-32" | 4-7" |
| 38L | 75-79" | 150-175 lbs | 37-39" | 31-34" | 4-8" |
| 40L | 76-80" | 165-190 lbs | 39-41" | 33-36" | 4-8" |
| 42L | 77-81" | 180-205 lbs | 41-43" | 35-38" | 4-8" |
| 44L | 78-82" | 195-220 lbs | 43-45" | 37-40" | 4-8" |
| 46L | 78-82" | 210-235 lbs | 45-47" | 39-42" | 4-8" |
| 48L | 79-83" | 225-250 lbs | 47-49" | 41-44" | 4-8" |

### Extra Long Sizes (3 sizes: 40XL - 44XL)

| Size | Height Range | Weight Range | Chest | Waist | Drop |
|------|-------------|--------------|-------|-------|------|
| 40XL | 82-86" | 165-190 lbs | 39-41" | 33-36" | 4-8" |
| 42XL | 83-87" | 180-205 lbs | 41-43" | 35-38" | 4-8" |
| 44XL | 84-88" | 195-220 lbs | 43-45" | 37-40" | 4-8" |

---

## Core Algorithms

### 1. Fast Size Recommendation (Basic Inputs)

Optimized for quick lookups using only height and weight:

```typescript
getFastSizeRecommendation(height: number, weight: number, fitPreference: string, bodyType?: string) {
  const bmi = (weight * 703) / (height * height);
  const inferredBodyType = bodyType || (bmi < 22 ? 'slim' : bmi > 26 ? 'broad' : 'regular');
  
  let recommendedSize = '40R';
  
  if (height < 68) {
    // Short sizes
    recommendedSize = weight < 150 ? '36S' : weight < 170 ? '38S' : weight < 200 ? '40S' : '42S';
  } else if (height > 74) {
    // Long sizes  
    recommendedSize = weight < 150 ? '36L' : weight < 170 ? '38L' : weight < 200 ? '40L' : '42L';
  } else {
    // Regular sizes (68-74 inches)
    recommendedSize = weight < 150 ? '36R' : weight < 180 ? '38R' : weight < 210 ? '40R' : '42R';
  }
  
  return { size: recommendedSize, confidence, ... };
}
```

### 2. Body Type Classification

Multi-factor classification using BMI, drop pattern, and shoulder-to-chest ratio:

```typescript
classifyBodyType(height: number, weight: number, fitPreference: string, advancedMeasurements?: any): string {
  const bmi = (weight * 703) / (height * height);
  const drop = chest - waist;
  const shoulderToChestRatio = shoulders / chest;
  
  // Classification logic
  if (bmi < 20 || drop > 8 || fitPreference === 'slim') return 'slim';
  if (bmi >= 27 && shoulderToChestRatio > 1.15 && drop >= 6) return 'athletic';
  if (bmi > 30 || drop < 4) return 'broad';
  return 'regular';
}
```

**Body Types:**
| Type | Characteristics | Drop Pattern |
|------|----------------|--------------|
| Slim | BMI < 20, narrow shoulders & chest | 8-9" |
| Athletic | V-shaped, broad shoulders, muscular | 6-7" |
| Regular | Balanced proportions | 5-7" |
| Broad | Wide shoulders & chest, larger frame | 3.5-4" |

### 3. Measurement Calculation

Body-type-specific calculations for predicted measurements:

```typescript
calculateMeasurements(height: number, weight: number, bodyType?: string) {
  const bmi = (weight * 703) / (height * height);
  
  // Body-type-specific chest calculations
  switch(bodyType) {
    case 'slim':
      baseChest = 26 + (height - 60) * 0.25;
      chestWeightFactor = (weight - 120) * 0.04;
      break;
    case 'athletic':
      baseChest = 30 + (height - 60) * 0.35;
      chestWeightFactor = (weight - 120) * 0.055;
      break;
    case 'broad':
      baseChest = 32 + (height - 60) * 0.32;
      chestWeightFactor = (weight - 120) * 0.06;
      break;
    default: // regular
      baseChest = 28 + (height - 60) * 0.3;
      chestWeightFactor = (weight - 120) * 0.05;
  }
  
  const chest = baseChest + chestWeightFactor + (bmi - 20) * 0.6;
  
  // Body-type-specific drop patterns
  let drop = 6; // Default
  switch(bodyType) {
    case 'slim': drop = bmi < 18 ? 9 : 8; break;
    case 'athletic': drop = bmi < 25 ? 7 : 6; break;
    case 'broad': drop = bmi > 30 ? 3.5 : 4; break;
    default: drop = bmi < 20 ? 7 : bmi > 28 ? 5 : 6;
  }
  
  return { chest, waist, neck, sleeve, inseam, shoulders, bicep, thigh, calf, drop, bmi };
}
```

### 4. Confidence Scoring

Multi-factor confidence calculation reflecting input quality:

```typescript
calculateConfidence(height, weight, recommendedSize, inputType, bodyType, predictionAccuracy) {
  // Base confidence adjusted for input type
  let confidence = inputType === 'advanced' ? 0.85 : 0.70;
  
  // Apply prediction accuracy for basic inputs
  if (inputType === 'basic' && predictionAccuracy) {
    confidence = confidence * predictionAccuracy;
  }
  
  // Height confidence (+0.1 if within range, -0.015 per inch outside)
  if (height >= sizeData.height[0] && height <= sizeData.height[1]) {
    confidence += 0.1;
  } else {
    confidence -= heightDiff * 0.015;
  }
  
  // Weight confidence (+0.1 if within range, -0.002 per lb outside)
  if (weight >= sizeData.weight[0] && weight <= sizeData.weight[1]) {
    confidence += 0.1;
  } else {
    confidence -= weightDiff * 0.002;
  }
  
  // Body type boost (+0.05 for non-regular)
  if (bodyType && bodyType !== 'regular') {
    confidence += 0.05;
  }
  
  return Math.max(0.4, Math.min(0.95, confidence));
}
```

**Confidence Levels:**
| Level | Score Range | Meaning |
|-------|------------|---------|
| High | > 82% | Strong match to sizing matrix |
| Medium | 68-82% | Good match, minor adjustments may help |
| Low | < 68% | Consider professional fitting |

### 5. Prediction Accuracy Estimation

For basic inputs (height/weight only):

```typescript
estimatePredictionAccuracy(height, weight, bodyType) {
  let accuracy = 0.75; // Base accuracy
  
  // BMI-based adjustments
  const bmi = (weight * 703) / (height * height);
  if (bmi >= 18 && bmi <= 28) accuracy += 0.1;   // Normal range
  if (bmi < 16 || bmi > 35) accuracy -= 0.15;    // Extreme BMI
  
  // Body type provided
  if (bodyType && bodyType !== 'regular') accuracy += 0.08;
  
  // Height-weight correlation
  const expectedWeight = (height - 60) * 5 + 140;
  const weightVariance = Math.abs(weight - expectedWeight) / expectedWeight;
  if (weightVariance < 0.15) accuracy += 0.05;
  if (weightVariance > 0.4) accuracy -= 0.1;
  
  return Math.max(0.6, Math.min(0.9, accuracy));
}
```

### 6. Size Matching Algorithm (Advanced)

Full multi-factor scoring for advanced measurements:

```typescript
getSizeRecommendation(height, weight, fitPreference, advancedMeasurements, bodyType) {
  for (const [size, data] of Object.entries(sizingMatrix)) {
    let score = 0;
    
    // Height scoring (35% weight)
    if (height >= data.height[0] && height <= data.height[1]) {
      score += 0.35;
    } else {
      score += Math.max(0, 0.35 - heightDiff * 0.02);
    }
    
    // Weight scoring (30% weight)
    if (weight >= data.weight[0] && weight <= data.weight[1]) {
      score += 0.30;
    } else {
      score += Math.max(0, 0.30 - weightDiff * 0.002);
    }
    
    // Chest scoring (20% weight)
    if (chest >= data.chest[0] && chest <= data.chest[1]) {
      score += 0.20;
    } else {
      score += Math.max(0, 0.20 - chestDiff * 0.03);
    }
    
    // Drop pattern scoring (15% weight)
    if (drop >= data.drop[0] && drop <= data.drop[1]) {
      score += 0.15;
    } else {
      score += Math.max(0, 0.15 - dropDiff * 0.02);
    }
  }
}
```

**Scoring Weights:**
| Factor | Weight | Rationale |
|--------|--------|-----------|
| Height | 35% | Primary factor for length selection |
| Weight | 30% | Primary factor for chest/waist sizing |
| Chest | 20% | Critical for jacket fit |
| Drop | 15% | Determines silhouette and waist suppression |

### 7. Alteration Recommendations

Generated based on size fit and body type:

```typescript
generateAlterations(height, weight, size, bodyType, advancedMeasurements) {
  const alterations = [];
  
  // Sleeve length
  if (height < sizeData.height[0]) alterations.push('sleeve_shortening');
  else if (height > sizeData.height[1]) alterations.push('sleeve_lengthening');
  
  // Waist suppression for athletic/slim builds
  if (bodyType === 'athletic' || bodyType === 'slim') {
    alterations.push('waist_suppression');
  }
  
  // Always recommend trouser hemming
  alterations.push('trouser_hemming');
  
  // Advanced measurement-based
  if (advancedMeasurements?.shoulders > 48) alterations.push('shoulder_adjustment');
  if (advancedMeasurements?.bicep > 16) alterations.push('sleeve_tapering');
  
  return alterations;
}
```

---

## Edge Functions

### 1. enhanced-ai-size-bot (Primary)

**Path:** `supabase/functions/enhanced-ai-size-bot/index.ts`
**Lines:** 500

**Request:**
```json
{
  "height": 70,
  "weight": 180,
  "fitPreference": "regular",
  "bodyType": "athletic",
  "advancedMeasurements": {
    "chest": 40,
    "waist": 34,
    "neck": 16,
    "sleeve": 34,
    "inseam": 32,
    "shoulders": 18,
    "bicep": 13,
    "thigh": 24,
    "calf": 15
  },
  "aiInsights": {
    "bodyTypeAnalysis": "Mesomorph build",
    "fitPrediction": "Standard fit recommended",
    "riskFactors": [],
    "confidenceFactors": ["Height within range", "Weight optimal"]
  }
}
```

**Response:**
```json
{
  "success": true,
  "recommendation": {
    "size": "40R",
    "confidence": 0.9265,
    "confidenceLevel": "high",
    "bodyType": "regular",
    "alterations": ["sleeve_length", "waist_suppression", "trouser_hemming"],
    "rationale": "Based on your regular build with 70\" height and 180lbs weight...",
    "measurements": {
      "height": 70,
      "weight": 180,
      "chest": 40,
      "waist": 34,
      "drop": 6.0,
      "bmi": 25.8,
      "predictionAccuracy": 0.85
    },
    "algorithm": "Enhanced Sizing Engine v2.1",
    "dataSource": "Customer Data (3,371 records)",
    "inputType": "advanced",
    "recommendationScore": 0.92
  },
  "enhancedFeatures": {
    "realData": true,
    "algorithmVersion": "2.1",
    "customerDataRecords": 3371,
    "advancedMeasurements": true,
    "aiInsights": true,
    "basicInputOptimized": true,
    "bodyTypeSpecific": true,
    "predictionAccuracy": 0.85
  }
}
```

### 2. ai-size-bot (Fallback)

**Path:** `supabase/functions/ai-size-bot/index.ts`
**Lines:** 212

**Fallback Chain:**
1. **Primary:** Railway API (`https://suitsize-ai-production.up.railway.app/api/recommend`)
2. **Fallback:** Supabase `simple_size_recommendations` table

**Request:**
```json
{
  "height": 70,
  "weight": 180,
  "fitPreference": "regular",
  "bodyType": "athletic"
}
```

**Response:**
```json
{
  "size": "40R",
  "confidence": 0.92,
  "confidenceLevel": "high",
  "bodyType": "regular",
  "alterations": [],
  "rationale": "Based on your height (70\") and weight (180 lbs)...",
  "measurements": null,
  "source": "railway",  // or "database" for fallback
  "success": true
}
```

---

## Database Schema

### simple_size_recommendations

Stores pre-computed size recommendations for fast database lookups:

```sql
CREATE TABLE public.simple_size_recommendations (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  height_min INTEGER NOT NULL,
  height_max INTEGER NOT NULL,
  weight_min INTEGER NOT NULL,
  weight_max INTEGER NOT NULL,
  fit_style TEXT NOT NULL,      -- 'slim', 'regular', 'relaxed'
  body_type TEXT NOT NULL,       -- 'athletic', 'regular', 'broad'
  recommended_size TEXT NOT NULL,
  confidence_score NUMERIC(3,2) NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

-- RLS Policies
ALTER TABLE public.simple_size_recommendations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow public read access"
  ON public.simple_size_recommendations
  FOR SELECT
  TO public
  USING (true);
```

**Mapping Functions:**

```typescript
// Fit preference mapping
const fitMapping = {
  'slim': 'slim',
  'regular': 'regular',
  'relaxed': 'relaxed',
  'classic': 'regular',
  'modern': 'slim',
  'comfort': 'relaxed'
};

// Body type mapping
const bodyTypeMapping = {
  'athletic': 'athletic',
  'regular': 'regular',
  'broad': 'broad',
  'average': 'regular',
  'slim': 'athletic',
  'stocky': 'broad'
};
```

### size_history

Stores user size recommendation history for tracking and feedback:

```sql
CREATE TABLE public.size_history (
  id UUID NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id UUID NOT NULL,
  recommended_size TEXT NOT NULL,
  confidence NUMERIC(3,2),
  height_inches INTEGER,
  weight_lbs INTEGER,
  fit_preference TEXT,
  body_type TEXT,
  measurements JSONB,
  ai_insights JSONB,
  feedback TEXT,
  feedback_rating INTEGER,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);
```

---

## Frontend Component

### EnhancedSizeGuide.tsx

**Path:** `src/components/EnhancedSizeGuide.tsx`
**Lines:** 1,266

**Key Features:**

1. **Circular Slider Interactions**
   - Custom radial input for height (60-84") and weight (100-300 lbs)
   - Touch-optimized with snap zones at 0°, 90°, 180°, 270°
   - Ripple effect feedback on interaction

2. **Advanced Measurements Panel**
   - Optional detailed measurements (chest, waist, neck, sleeve, etc.)
   - Boosts confidence score when provided

3. **Size History Tracking**
   - Stores recommendations in `size_history` table
   - Pre-populates with most recent data
   - Shows last 5 recommendations

4. **Feedback System**
   - 5-star rating system
   - Text feedback for improvement
   - Updates size_history record

5. **AI Insights Generation**
   ```typescript
   const aiInsights = {
     bodyTypeAnalysis: analyzeBodyType(height, weight, bmi),
     fitPrediction: generateFitPrediction(bmi, fitPreference, bodyType),
     riskFactors: identifyRiskFactors(bmi, drop, previousSizes),
     confidenceFactors: calculateConfidenceFactors(height, weight, bodyType)
   };
   ```

6. **Local Fallback Calculation**
   - Matches edge function logic exactly
   - 8-second timeout before fallback
   - Uses same height/weight thresholds

**State Management:**
```typescript
const [heightInches, setHeightInches] = useState(70);
const [weightLbs, setWeightLbs] = useState(170);
const [fitPreference, setFitPreference] = useState<'slim' | 'regular' | 'relaxed'>('regular');
const [bodyType, setBodyType] = useState<'athletic' | 'average' | 'broad'>('average');
const [isMetric, setIsMetric] = useState(false);
const [showAdvancedMeasurements, setShowAdvancedMeasurements] = useState(false);
const [advancedMeasurements, setAdvancedMeasurements] = useState({
  chest: 40, waist: 34, neck: 16, sleeve: 34, inseam: 32,
  shoulders: 18, bicep: 13, thigh: 24, calf: 15
});
```

---

## API Reference

### POST /enhanced-ai-size-bot

Primary sizing endpoint with full EnhancedSizingEngine.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| height | number | Yes | Height in inches (60-88) |
| weight | number | Yes | Weight in pounds (100-400) |
| fitPreference | string | No | 'slim', 'regular', 'relaxed' |
| bodyType | string | No | 'athletic', 'average', 'broad' |
| advancedMeasurements | object | No | Detailed body measurements |
| aiInsights | object | No | Pre-computed AI analysis |

### POST /ai-size-bot

Railway API integration with database fallback.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| height | number | Yes | Height in inches |
| weight | number | Yes | Weight in pounds |
| fitPreference | string | No | 'slim', 'regular', 'relaxed' |
| bodyType | string | No | Body type classification |

---

## Performance Metrics

| Metric | Value | Industry Average |
|--------|-------|-----------------|
| Accuracy | 91% | ~75% |
| Confidence Score (avg) | 87% | N/A |
| Return Rate | 9% | 15% |
| Fit Satisfaction | 75% | 60% |
| Response Time | <50ms (fast) / <2s (full) | N/A |
| Timeout | 8 seconds | N/A |

---

## Integration Points

### Railway API (External)

**Endpoint:** `https://suitsize-ai-production.up.railway.app/api/recommend`

```typescript
const response = await fetch(`${ENHANCED_SIZEBOT_API_URL}/api/recommend`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ height, weight, fitPreference, bodyType })
});
```

### Supabase Edge Function Invocation

```typescript
const { data, error } = await supabase.functions.invoke('enhanced-ai-size-bot', {
  body: { height, weight, fitPreference, bodyType, advancedMeasurements, aiInsights }
});
```

### Local Fallback (Frontend)

```typescript
// Matches edge function logic exactly
if (heightInches < 68) {
  recommendedSize = weightLbs < 150 ? '36S' : weightLbs < 170 ? '38S' : weightLbs < 200 ? '40S' : '42S';
} else if (heightInches > 74) {
  recommendedSize = weightLbs < 150 ? '36L' : weightLbs < 170 ? '38L' : weightLbs < 200 ? '40L' : '42L';
} else {
  recommendedSize = weightLbs < 150 ? '36R' : weightLbs < 180 ? '38R' : weightLbs < 210 ? '40R' : '42R';
}
```

---

## File References

| File | Purpose | Lines |
|------|---------|-------|
| `supabase/functions/enhanced-ai-size-bot/index.ts` | Main sizing engine | 500 |
| `supabase/functions/ai-size-bot/index.ts` | Railway + DB fallback | 212 |
| `src/components/EnhancedSizeGuide.tsx` | Frontend component | 1,266 |
| `src/components/ai/CompactSizeGuide.tsx` | Compact variant | ~250 |
| `docs/enhanced-size-bot-readme.md` | Original documentation | 166 |

---

## Version History

| Version | Changes |
|---------|---------|
| v2.1 | Body-type-specific calculations, prediction accuracy, basic input optimization |
| v2.0 | Height/weight prioritization, confidence-based adjustments |
| v1.5 | Multi-factor confidence scoring, edge case detection |
| v1.0 | Initial release with basic height/weight matrix |

---

## Future Enhancements (Planned)

1. **Supabase Fallback for enhanced-ai-size-bot** - Add database fallback to primary edge function
2. **Analytics Dashboard** - Track recommendation accuracy over time
3. **Machine Learning Integration** - Use feedback data to improve predictions
4. **Photo-based Sizing** - Use camera input for measurements
5. **Brand-specific Adjustments** - Account for different brand sizing
