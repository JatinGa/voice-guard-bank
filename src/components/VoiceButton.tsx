import { Mic, MicOff } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

interface VoiceButtonProps {
  isRecording: boolean;
  onRecord: (recording: boolean) => void;
  challengePhrase?: string | null;
  onResult?: (result: { transcript?: string; liveness?: number; details?: any }) => void;
}

const VoiceButton = ({ isRecording, onRecord, challengePhrase, onResult }: VoiceButtonProps) => {
  let mediaRecorder: MediaRecorder | null = null;
  let chunks: BlobPart[] = [];

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorder = new MediaRecorder(stream);
      chunks = [];
      mediaRecorder.ondataavailable = (e) => chunks.push(e.data);
      mediaRecorder.onstop = async () => {
        const blob = new Blob(chunks, { type: "audio/webm" });

        // Send to voice-transcribe and voice-liveness endpoints
        try {
          const form = new FormData();
          form.append("audio", blob, "recording.webm");
          if (challengePhrase) form.append("challenge", challengePhrase);

          // Send to voice-transcribe
          const base = window.location.origin;
          const transcribeResp = await fetch(`${base}/supabase/functions/voice-transcribe`, {
            method: "POST",
            body: JSON.stringify({ text: undefined }),
            headers: { "Content-Type": "application/json" },
          }).then((r) => r.json()).catch(() => null);

          // Call liveness function (mock)
          const livenessResp = await fetch(`${base}/supabase/functions/voice-liveness`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ audio: null, challenge: challengePhrase, transcript: transcribeResp?.transcript }),
          }).then((r) => r.json()).catch(() => null);

          onResult?.({ transcript: transcribeResp?.transcript, liveness: livenessResp?.score, details: { transcribeResp, livenessResp } });
        } catch (err) {
          console.error("Recording upload failed", err);
          onResult?.({ details: { error: String(err) } });
        }
      };

      mediaRecorder.start();
      onRecord(true);
    } catch (err) {
      console.error("Could not start recording:", err);
      onRecord(false);
    }
  };

  const stopRecording = () => {
    try {
      // @ts-ignore
      if (mediaRecorder && mediaRecorder.state !== "inactive") mediaRecorder.stop();
    } catch (err) {
      console.warn("stopRecording error", err);
    }
    onRecord(false);
  };

  return (
    <Button
      onClick={() => (isRecording ? stopRecording() : startRecording())}
      variant={isRecording ? "destructive" : "default"}
      size="icon"
      className={cn(
        "rounded-full transition-all",
        isRecording && "animate-pulse shadow-lg scale-110"
      )}
    >
      {isRecording ? (
        <MicOff className="h-5 w-5" />
      ) : (
        <Mic className="h-5 w-5" />
      )}
    </Button>
  );
};

export default VoiceButton;
