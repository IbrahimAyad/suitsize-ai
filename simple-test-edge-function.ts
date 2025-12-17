/**
 * Simple test edge function to verify database access
 */

Deno.serve(async (req) => {
    const corsHeaders = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type',
        'Access-Control-Allow-Methods': 'POST, GET, OPTIONS, PUT, DELETE, PATCH',
    };

    if (req.method === 'OPTIONS') {
        return new Response(null, { status: 200, headers: corsHeaders });
    }

    try {
        const supabaseUrl = Deno.env.get('SUPABASE_URL');
        const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');

        if (!supabaseUrl || !supabaseKey) {
            throw new Error('Missing Supabase configuration');
        }

        // Test direct database access with simple query
        const testResponse = await fetch(`${supabaseUrl}/rest/v1/sizing_lookup_simple?select=*&limit=3`, {
            method: 'GET',
            headers: {
                'apikey': supabaseKey,
                'Authorization': `Bearer ${supabaseKey}`,
                'Content-Type': 'application/json',
                'Prefer': 'return=representation'
            }
        });

        if (!testResponse.ok) {
            const errorText = await testResponse.text();
            throw new Error(`Database query failed: ${testResponse.status} - ${errorText}`);
        }

        const data = await testResponse.json();

        return new Response(
            JSON.stringify({
                success: true,
                message: 'Database connection successful',
                data: data,
                count: data.length
            }),
            {
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            }
        );

    } catch (error) {
        console.error('Test Error:', error);
        
        return new Response(
            JSON.stringify({
                error: {
                    code: 'TEST_ERROR',
                    message: error.message
                }
            }),
            {
                status: 500,
                headers: { ...corsHeaders, 'Content-Type': 'application/json' }
            }
        );
    }
});
