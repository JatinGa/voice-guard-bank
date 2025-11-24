import { Mic, MicOff, Loader } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { useRef, useState } from "react";
import { mockApiService } from "@/lib/mockApi";

interface VoiceButtonProps {
  isRecording: boolean;
  onRecord: (recording: boolean) => void;
  challengePhrase?: string | null;
  onResult?: (result: { transcript?: string; liveness?: number; details?: any }) => void;
}

const VoiceButton = ({ isRecording, onRecord, challengePhrase, onResult }: VoiceButtonProps) => {
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const recognitionRef = useRef<any>(null);
  const [isProcessing, setIsProcessing] = useState(false);

  const startRecording = async () => {
    try {
      setIsProcessing(true);
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognitionRef.current = recognition;
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = "en-IN";

        let finalTranscript = "";

        recognition.onresult = (event: any) => {
          for (let i = event.resultIndex; i < event.results.length; ++i) {
            if (event.results[i].isFinal) {
              finalTranscript += event.results[i][0].transcript;
            }
          }
        };

        recognition.onend = async () => {
          onRecord(false);
          if (finalTranscript) {
            try {
              // Use local mock API service
              const livenessResp = await mockApiService.voiceLiveness(finalTranscript, challengePhrase);

              onResult?.({
                transcript: finalTranscript,
                liveness: livenessResp.score,
                details: { livenessResp },
              });
            } catch (err) {
              console.error("Liveness check failed", err);
              onResult?.({ transcript: finalTranscript, liveness: 75 });
            }
          }
          setIsProcessing(false);
        };

        recognition.onerror = (event: any) => {
          console.error("Speech recognition error", event.error);
          onRecord(false);
          setIsProcessing(false);
          onResult?.({ details: { error: `Speech: ${event.error}` } });
        };

        recognition.start();
        onRecord(true);
        return;
      }

      // Fallback: audio recording
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => chunksRef.current.push(e.data);
      mediaRecorder.onstop = async () => {
        onRecord(false);
        const mockTranscript = "check my balance";
        try {
          // Use local mock API service
          const livenessResp = await mockApiService.voiceLiveness(mockTranscript, challengePhrase);

          onResult?.({
            transcript: mockTranscript,
            liveness: livenessResp.score,
          });
        } catch (err) {
          console.error("Recording failed", err);
          onResult?.({ details: { error: String(err) } });
        }
        setIsProcessing(false);
      };

      mediaRecorder.start();
      onRecord(true);
    } catch (err) {
      console.error("Could not start recording:", err);
      onRecord(false);
      setIsProcessing(false);
      onResult?.({ details: { error: String(err) } });
    }
  };

  const stopRecording = () => {
    try {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      } else if (mediaRecorderRef.current && mediaRecorderRef.current.state !== "inactive") {
        mediaRecorderRef.current.stop();
      }
    } catch (err) {
      console.warn("stopRecording error", err);
    }
  };

  return (
    <Button
      onClick={() => (isRecording ? stopRecording() : startRecording())}
      variant={isRecording ? "destructive" : "default"}
      size="icon"
      className={cn(
        "rounded-full transition-all",
        (isRecording || isProcessing) && "animate-pulse shadow-lg scale-110"
      )}
      disabled={isProcessing}
    >
      {isProcessing ? (
        <Loader className="h-5 w-5 animate-spin" />
      ) : isRecording ? (
        <MicOff className="h-5 w-5" />
      ) : (
        <Mic className="h-5 w-5" />
      )}
    </Button>
  );
};

export default VoiceButton;
