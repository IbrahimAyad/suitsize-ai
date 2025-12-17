/**
 * Enhanced Size Bot Edge Function
 * Uses comprehensive research data for competitive sizing recommendations
 * Implements 4-field minimal approach with 6-drop system
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
        // Parse request body
        const requestData = await req.json();
        const { height, weight, fitStyle, bodyType, unit = 'imperial' } = requestData;

        // Validate required fields
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

        // Convert to inches if metric
        const heightInches = unit === 'metric' ? Math.round(height / 2.54) : height;
        const weightLbs = unit === 'metric' ? Math.round(weight * 2.20462) : weight;

        // Get Supabase client
        const supabaseUrl = Deno.env.get('SUPABASE_URL')!;
        const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!;

        // Query simple sizing lookup table
        const lookupResponse = await fetch(`${supabaseUrl}/rest/v1/sizing_lookup_simple`, {
            method: 'GET',
            headers: {
                'apikey': supabaseKey,
                'Authorization': `Bearer ${supabaseKey}`,
                'Content-Type': 'application/json'
            }
        });

        if (!lookupResponse.ok) {
            throw new Error(`Database query failed: ${lookupResponse.statusText}`);
        }

        const sizingData = await lookupResponse.json();

        // Find matching size based on 4-field approach
        const match = sizingData.find((entry: any) => {
            const heightMatch = heightInches >= entry.height_min_inches && heightInches <= entry.height_max_inches;
            const weightMatch = weightLbs >= entry.weight_min_lbs && weightLbs <= entry.weight_max_lbs;
            const fitMatch = entry.fit_style === fitStyle.toLowerCase();
            const bodyTypeMatch = entry.body_type === bodyType.toLowerCase();

            return heightMatch && weightMatch && fitMatch && bodyTypeMatch;
        });

        // If no exact match, find closest match with relaxed body type
        let finalMatch = match;
        if (!finalMatch) {
            finalMatch = sizingData.find((entry: any) => {
                const heightMatch = heightInches >= entry.height_min_inches && heightInches <= entry.height_max_inches;
                const weightMatch = weightLbs >= entry.weight_min_lbs && weightLbs <= entry.weight_max_lbs;
                const fitMatch = entry.fit_style === fitStyle.toLowerCase();
                
                return heightMatch && weightMatch && fitMatch;
            });
        }

        // If still no match, use general closest match
        if (!finalMatch) {
            finalMatch = sizingData.find((entry: any) => {
                const heightMatch = heightInches >= entry.height_min_inches && heightInches <= entry.height_max_inches;
                const weightMatch = weightLbs >= entry.weight_min_lbs && weightLbs <= entry.weight_max_lbs;
                
                return heightMatch && weightMatch;
            }) || sizingData[0]; // fallback to first entry
        }

        // Get detailed measurements if available
        const detailedResponse = await fetch(`${supabaseUrl}/rest/v1/sizing_detailed_measurements?size=eq.${finalMatch.recommended_size}`, {
            method: 'GET',
            headers: {
                'apikey': supabaseKey,
                'Authorization': `Bearer ${supabaseKey}`,
                'Content-Type': 'application/json'
            }
        });

        let detailedData = null;
        if (detailedResponse.ok) {
            const detailedResults = await detailedResponse.json();
            detailedData = detailedResults[0] || null;
        }

        // Calculate confidence score
        let confidence = finalMatch.confidence_score || 0.95;
        
        // Adjust confidence based on match quality
        if (!match && finalMatch) {
            confidence = 0.85; // Lower confidence for approximate match
        }

        // Apply body type adjustments if detailed data available
        let adjustments = [];
        if (detailedData && detailedData.body_type_adjustments) {
            const bodyTypeAdjustments = detailedData.body_type_adjustments;
            const requestedBodyType = bodyType.toLowerCase();
            
            if (bodyTypeAdjustments[requestedBodyType]) {
                const adjustment = bodyTypeAdjustments[requestedBodyType];
                if (adjustment.chest) {
                    adjustments.push(`Chest adjustment: ${adjustment.chest > 0 ? '+' : ''}${adjustment.chest}" for ${requestedBodyType} body type`);
                }
            }
        }

        // Generate recommendation
        const recommendation = {
            size: finalMatch.recommended_size,
            confidence: confidence,
            confidenceLevel: confidence >= 0.9 ? 'High' : confidence >= 0.8 ? 'Medium' : 'Low',
            bodyType: bodyType || 'regular',
            rationale: `Size ${finalMatch.recommended_size} recommended based on ${heightInches}" height, ${weightLbs} lbs weight, ${fitStyle} fit, and ${bodyType || 'regular'} body type.`,
            alterations: adjustments,
            measurements: detailedData ? {
                chest: `${detailedData.chest_min_inches}"-${detailedData.chest_max_inches}"`,
                waist: `${detailedData.waist_min_inches}"-${detailedData.waist_max_inches}"`,
                sleeve: `${detailedData.sleeve_inches}"`,
                jacketLength: `${detailedData.jacket_length_inches}"`,
                drop: `${detailedData.drop_inches}" (6-drop system)`
            } : null
        };

        // Return success response
        return new Response(
            JSON.stringify({
                success: true,
                data: recommendation,
                metadata: {
                    algorithm: 'Enhanced Research-Based Sizing',
                    dataSource: 'Comprehensive Suit Sizing Research',
                    version: '2.0',
                    features: ['6-drop system', 'Body type adjustments', 'Confidence scoring']
                }
            }),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            }
        );

    } catch (error) {
        console.error('Enhanced Size Bot Error:', error);
        
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
