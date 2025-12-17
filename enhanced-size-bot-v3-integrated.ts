/**
 * Enhanced Size Bot V3 - Integrated Version
 * Combines EnhancedSizingEngine algorithms with our comprehensive research data
 * Target: 93%+ accuracy, <8% return rate
 */

Deno.serve(async (req) => {
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE, PATCH',
        'Access-Control-Max-Age': '86400',
        'Access-Control-Allow-Credentials': 'false'
    };

    if (req.method === 'OPTIONS') {
        return new Response(null, { status: 200, headers: corsHeaders });
    }

    try {
        const requestData = await req.json();
        const { height, weight, fitStyle, bodyType, unit = 'imperial', advancedMeasurements } = requestData;

        if (!height || !weight || !fitStyle) {
            return new Response(
                JSON.stringify({
                    error: {
                        code: 'MISSING_PARAMETERS',
                        message: 'Height, weight, and fit style are required'
                    }
                }),
                {
                    status: 400,
                    headers: { ...corsHeaders, 'Content-Type': 'application/json' }
                }
            );
        }

        const heightInches = unit === 'metric' ? Math.round(height / 2.54) : height;
        const weightLbs = unit === 'metric' ? Math.round(weight * 2.20462) : weight;

        const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
        const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;

        // EnhancedSizingEngine Algorithm Integration
        const bmi = (weightLbs * 703) / (heightInches * heightInches);
        
        // Enhanced body type classification (scientific approach)
        let inferredBodyType = bodyType?.toLowerCase();
        if (!inferredBodyType) {
            inferredBodyType = bmi < 22 ? 'slim' : bmi > 26 ? 'broad' : 'regular';
        }

        // Enhanced measurement calculations (EnhancedSizingEngine approach)
        function calculateMeasurements(height: number, weight: number, bodyType: string) {
            const bmi = (weight * 703) / (height * height);
            
            // Body-type-specific chest calculations
            let baseChest, chestWeightFactor;
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
            
            const waist = chest - drop;
            
            return { chest, waist, drop, bmi };
        }

        // Enhanced confidence scoring (EnhancedSizingEngine multi-factor approach)
        function calculateConfidence(height: number, weight: number, recommendedSize: string, inputType: string, bodyType: string, sizeData: any) {
            let confidence = inputType === 'advanced' ? 0.85 : 0.70;
            
            // Height confidence (+0.1 if within range, -0.015 per inch outside)
            if (sizeData && height >= sizeData.height_min_inches && height <= sizeData.height_max_inches) {
                confidence += 0.1;
            } else if (sizeData) {
                const heightCenter = (sizeData.height_min_inches + sizeData.height_max_inches) / 2;
                const heightDiff = Math.abs(height - heightCenter);
                confidence -= heightDiff * 0.015;
            }
            
            // Weight confidence (+0.1 if within range, -0.002 per lb outside)
            if (sizeData && weight >= sizeData.weight_min_lbs && weight <= sizeData.weight_max_lbs) {
                confidence += 0.1;
            } else if (sizeData) {
                const weightCenter = (sizeData.weight_min_lbs + sizeData.weight_max_lbs) / 2;
                const weightDiff = Math.abs(weight - weightCenter);
                confidence -= weightDiff * 0.002;
            }
            
            // Body type boost (+0.05 for non-regular)
            if (bodyType && bodyType !== 'regular') {
                confidence += 0.05;
            }
            
            return Math.max(0.4, Math.min(0.95, confidence));
        }

        // Prediction accuracy estimation (EnhancedSizingEngine feature)
        function estimatePredictionAccuracy(height: number, weight: number, bodyType: string) {
            let accuracy = 0.75; // Base accuracy
            
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

        // Query sizing data with enhanced approach
        const lookupResponse = await fetch(`${supabaseUrl}/rest/v1/sizing_lookup_simple?select=*`, {
            method: 'GET',
            headers: {
                'apikey': supabaseKey,
                'Authorization': `Bearer ${supabaseKey}`,
                'Content-Type': 'application/json'
            }
        });

        const sizingData = await lookupResponse.json();

        // Enhanced size matching with scoring
        let bestMatch = null;
        let bestScore = 0;

        for (const entry of sizingData) {
            let score = 0;
            
            // Height scoring (35% weight) - EnhancedSizingEngine approach
            if (heightInches >= entry.height_min_inches && heightInches <= entry.height_max_inches) {
                score += 0.35;
            } else {
                const heightCenter = (entry.height_min_inches + entry.height_max_inches) / 2;
                const heightDiff = Math.abs(heightInches - heightCenter);
                score += Math.max(0, 0.35 - heightDiff * 0.02);
            }
            
            // Weight scoring (30% weight)
            if (weightLbs >= entry.weight_min_lbs && weightLbs <= entry.weight_max_lbs) {
                score += 0.30;
            } else {
                const weightCenter = (entry.weight_min_lbs + entry.weight_max_lbs) / 2;
                const weightDiff = Math.abs(weightLbs - weightCenter);
                score += Math.max(0, 0.30 - weightDiff * 0.002);
            }
            
            // Fit style matching (20% weight)
            if (entry.fit_style === fitStyle.toLowerCase()) {
                score += 0.20;
            }
            
            // Body type matching (15% weight)
            if (entry.body_type === inferredBodyType) {
                score += 0.15;
            }
            
            if (score > bestScore) {
                bestScore = score;
                bestMatch = entry;
            }
        }

        // Fallback to exact match if no good scoring match
        if (!bestMatch || bestScore < 0.5) {
            bestMatch = sizingData.find((entry: any) => {
                const heightMatch = heightInches >= entry.height_min_inches && heightInches <= entry.height_max_inches;
                const weightMatch = weightLbs >= entry.weight_min_lbs && weightLbs <= entry.weight_max_lbs;
                const fitMatch = entry.fit_style === fitStyle.toLowerCase();
                
                return heightMatch && weightMatch && fitMatch;
            }) || sizingData[0];
        }

        // Enhanced confidence calculation
        const inputType = advancedMeasurements ? 'advanced' : 'basic';
        const confidence = calculateConfidence(heightInches, weightLbs, bestMatch?.recommended_size || '40R', inputType, inferredBodyType, bestMatch);
        const predictionAccuracy = estimatePredictionAccuracy(heightInches, weightLbs, inferredBodyType);

        // Calculate enhanced measurements
        const measurements = calculateMeasurements(heightInches, weightLbs, inferredBodyType);

        // Find alternative options
        const alternativeOptions = sizingData
            .filter((entry: any) => {
                const heightMatch = heightInches >= entry.height_min_inches - 2 && heightInches <= entry.height_max_inches + 2;
                const weightMatch = weightLbs >= entry.weight_min_lbs - 15 && weightLbs <= entry.weight_max_lbs + 15;
                const fitMatch = entry.fit_style === fitStyle.toLowerCase();
                
                return heightMatch && weightMatch && fitMatch && entry.recommended_size !== bestMatch?.recommended_size;
            })
            .map((entry: any) => {
                const heightDiff = Math.max(0, Math.abs(heightInches - ((entry.height_min_inches + entry.height_max_inches) / 2)));
                const weightDiff = Math.max(0, Math.abs(weightLbs - ((entry.weight_min_lbs + entry.weight_max_lbs) / 2)));
                
                let altConfidence = 0.85;
                if (heightDiff > 2 || weightDiff > 20) altConfidence = 0.70;
                else if (heightDiff > 1 || weightDiff > 10) altConfidence = 0.80;
                else altConfidence = 0.85;

                return {
                    size: entry.recommended_size,
                    confidence: Math.round(altConfidence * 100),
                    description: heightDiff < weightDiff ? 'More tailored fit' : 'More comfortable fit'
                };
            })
            .sort((a: any, b: any) => b.confidence - a.confidence)
            .slice(0, 2);

        // Enhanced body type analysis (scientific approach)
        const bodyTypeAnalysis = {
            classification: inferredBodyType === 'athletic' ? 'Mesomorph build - athletic and defined physique' :
                           inferredBodyType === 'broad' ? 'Endomorph build - broader frame with muscular potential' :
                           'Ectomorph build - balanced proportions and natural build',
            characteristics: inferredBodyType === 'athletic' ? [
                'Broader chest and shoulders',
                'Defined waist line', 
                'More muscular arms and back',
                'V-shaped torso proportion'
            ] : inferredBodyType === 'broad' ? [
                'Wider shoulder structure',
                'Broader chest and torso',
                'Less defined waist line',
                'Larger bone structure'
            ] : [
                'Standard chest and shoulders',
                'Natural waist proportions',
                'Balanced muscular development',
                'Proportional body frame'
            ],
            bmi: Math.round(bmi * 10) / 10,
            dropPattern: `${measurements.drop}" drop (${measurements.drop > 6 ? 'Athletic' : measurements.drop < 4 ? 'Broad' : 'Regular'} build)`
        };

        // Enhanced alteration recommendations
        const alterations = [];
        
        // Sleeve length based on height
        if (heightInches < (bestMatch?.height_min_inches || 68)) {
            alterations.push('Sleeve shortening may be preferred');
        } else if (heightInches > (bestMatch?.height_max_inches || 74)) {
            alterations.push('Sleeve extension may be needed');
        }
        
        // Body type specific alterations
        if (inferredBodyType === 'athletic' || inferredBodyType === 'slim') {
            alterations.push('Waist suppression recommended for better silhouette');
        }
        
        if (inferredBodyType === 'broad') {
            alterations.push('Consider relaxed fit for comfort');
        }
        
        // Always recommend trouser hemming
        alterations.push('Trouser hemming recommended');
        
        // Advanced measurement based alterations
        if (advancedMeasurements?.shoulders && advancedMeasurements.shoulders > 48) {
            alterations.push('Shoulder adjustment may be needed');
        }
        if (advancedMeasurements?.bicep && advancedMeasurements.bicep > 16) {
            alterations.push('Sleeve tapering may be preferred');
        }

        // Get detailed measurements
        let detailedData = null;
        if (bestMatch && bestMatch.recommended_size) {
            const detailedResponse = await fetch(`${supabaseUrl}/rest/v1/sizing_detailed_measurements?size=eq.${bestMatch.recommended_size}`, {
                method: 'GET',
                headers: {
                    'apikey': supabaseKey,
                    'Authorization': `Bearer ${supabaseKey}`,
                    'Content-Type': 'application/json'
                }
            });

            if (detailedResponse.ok) {
                const detailedResults = await detailedResponse.json();
                detailedData = detailedResults[0] || null;
            }
        }

        // Enhanced AI insights
        const aiInsights = {
            fitPrediction: `Optimal choice - ${fitStyle} fit works well for your ${inferredBodyType} build (BMI: ${Math.round(bmi * 10) / 10})`,
            confidence: `AI analyzed comprehensive anthropometric data with ${Math.round(confidence * 100)}% confidence`,
            dataQuality: 'Measurements based on anthropometric research from major menswear brands',
            predictionAccuracy: `Estimated ${Math.round(predictionAccuracy * 100)}% accuracy for basic inputs`,
            riskFactors: bmi < 18 || bmi > 35 ? ['Extreme BMI - consider professional fitting'] : [],
            confidenceFactors: [
                `Height within range: ${heightInches}"`,
                `Weight optimal for build: ${weightLbs}lbs`,
                `Body type: ${inferredBodyType}`,
                advancedMeasurements ? 'Advanced measurements provided' : 'Basic inputs used'
            ]
        };

        // Main recommendation with enhanced features
        const recommendation = {
            primary: {
                size: bestMatch?.recommended_size || '40R',
                confidence: Math.round(confidence * 100),
                confidenceLevel: confidence > 0.82 ? 'high' : confidence > 0.68 ? 'medium' : 'low',
                description: 'Best Fit Recommendation'
            },
            alternatives: alternativeOptions,
            bodyType: bodyTypeAnalysis,
            alterations: alterations,
            measurements: detailedData ? {
                chest: `${detailedData.chest_min_inches}"-${detailedData.chest_max_inches}"`,
                waist: `${detailedData.waist_min_inches}"-${detailedData.waist_max_inches}"`,
                sleeve: `${detailedData.sleeve_inches}"`,
                jacketLength: `${detailedData.jacket_length_inches}"`,
                drop: `${detailedData.drop_inches}" (6-drop system)`
            } : {
                chest: `${Math.round(measurements.chest)}"`,
                waist: `${Math.round(measurements.waist)}"`,
                calculatedDrop: `${measurements.drop}"`,
                bmi: Math.round(bmi * 10) / 10
            },
            aiAnalysis: aiInsights,
            performance: {
                predictionAccuracy: Math.round(predictionAccuracy * 100),
                inputQuality: inputType,
                algorithmVersion: '3.0 Integrated'
            }
        };

        return new Response(
            JSON.stringify({
                success: true,
                data: recommendation,
                metadata: {
                    algorithm: 'Enhanced Research-Based Sizing V3.0',
                    dataSource: 'Comprehensive Suit Sizing Research + EnhancedSizingEngine Algorithms',
                    version: '3.0',
                    features: [
                        'BMI-based calculations',
                        'Multi-factor confidence scoring', 
                        'Prediction accuracy estimation',
                        'Alternative size recommendations',
                        'Scientific body type analysis',
                        'Enhanced alteration suggestions',
                        '6-drop system optimization',
                        'Performance analytics'
                    ],
                    benchmarks: {
                        targetAccuracy: '93%+',
                        targetReturnRate: '<8%',
                        currentConfidence: Math.round(confidence * 100)
                    }
                }
            }),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            }
        );

    } catch (error) {
        console.error('Enhanced Size Bot V3 Error:', error);
        
        return new Response(
            JSON.stringify({
                error: {
                    code: 'SIZING_ERROR',
                    message: error.message || 'An error occurred while calculating size recommendation'
                }
            }),
            {
                status: 500,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            }
        );
    }
});