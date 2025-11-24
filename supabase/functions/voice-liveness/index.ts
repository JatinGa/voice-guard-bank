import { serve } from "https://deno.land/std@0.168.0/http/server.ts";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
};

serve(async (req) => {
  if (req.method === "OPTIONS") {
    return new Response(null, { headers: corsHeaders });
  }

  try {
    const { transcript, challenge } = await req.json();

    console.log("voice-liveness called", { transcript, challenge });

    // Very small mock of liveness scoring:
    // - If transcript includes the challenge phrase -> high score
    // - If transcript contains filler words or mismatch -> lower score
    const text = (transcript || "").toLowerCase();
    const challengeText = (challenge || "").toLowerCase();

    const fillerWords = ["umm", "uhh", "er", "ah", "hmm"];
    let fillerCount = 0;
    fillerWords.forEach((w) => { if (text.includes(w)) fillerCount++; });

    let score = 50;
    if (challengeText && text.includes(challengeText)) score += 40;
    else score -= 20;

    score -= fillerCount * 10;
    score = Math.max(0, Math.min(100, score));

    const response = {
      score,
      passed: score >= 60,
      reason: score >= 60 ? "challenge matched" : "challenge mismatch or filler detected",
      transcript: transcript || null,
    };

    return new Response(JSON.stringify(response), { headers: { ...corsHeaders, "Content-Type": "application/json" } });
  } catch (error) {
    console.error("Error in voice-liveness:", error);
    return new Response(JSON.stringify({ error: error instanceof Error ? error.message : "Unknown error" }), { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } });
  }
});
