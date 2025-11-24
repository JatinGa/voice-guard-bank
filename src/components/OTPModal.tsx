import { useState } from "react";
import { Lock, Phone, RotateCcw } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { InputOTP, InputOTPGroup, InputOTPSlot } from "@/components/ui/input-otp";
import { toast } from "sonner";
import { mockApiService } from "@/lib/mockApi";

interface OTPModalProps {
  open: boolean;
  onClose: () => void;
}

const OTPModal = ({ open, onClose }: OTPModalProps) => {
  const [step, setStep] = useState<"phone" | "otp">("phone");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [otp, setOtp] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [isVerifying, setIsVerifying] = useState(false);
  const [resendCountdown, setResendCountdown] = useState(0);
  const [sessionId, setSessionId] = useState<string | null>(null);

  // Validate phone number format (Indian format: +91 or 10-digit)
  const isValidPhone = (phone: string) => {
    const cleaned = phone.replace(/\D/g, "");
    return cleaned.length === 10 || cleaned.length === 12;
  };

  const handleSendOTP = async () => {
    if (!phoneNumber.trim()) {
      toast.error("Please enter your phone number");
      return;
    }

    if (!isValidPhone(phoneNumber)) {
      toast.error("Please enter a valid 10-digit phone number");
      return;
    }

    setIsLoading(true);
    try {
      const response = await mockApiService.sendOTP(phoneNumber);
      
      if (response.success) {
        setSessionId(response.session_id);
        setStep("otp");
        toast.success("OTP sent to your phone number!");
        setResendCountdown(60); // 60 second countdown
        
        // Countdown timer
        const timer = setInterval(() => {
          setResendCountdown((prev) => {
            if (prev <= 1) {
              clearInterval(timer);
              return 0;
            }
            return prev - 1;
          });
        }, 1000);
      } else {
        toast.error(response.message || "Failed to send OTP");
      }
    } catch (error: any) {
      toast.error(error.message || "Failed to send OTP");
    } finally {
      setIsLoading(false);
    }
  };

  const handleVerifyOTP = async () => {
    if (otp.length !== 6) {
      toast.error("Please enter complete 6-digit OTP");
      return;
    }

    if (!sessionId) {
      toast.error("Session expired. Please resend OTP");
      setStep("phone");
      return;
    }

    setIsVerifying(true);
    try {
      const response = await mockApiService.verifyOTP(sessionId, otp, phoneNumber);
      
      if (response.success) {
        toast.success("OTP verified successfully!");
        setIsVerifying(false);
        setOtp("");
        setPhoneNumber("");
        setStep("phone");
        setSessionId(null);
        onClose();
      } else {
        toast.error(response.message || "Invalid OTP. Please try again");
      }
    } catch (error: any) {
      toast.error(error.message || "OTP verification failed");
    } finally {
      setIsVerifying(false);
    }
  };

  const handleResendOTP = async () => {
    if (resendCountdown > 0) return;
    
    setIsLoading(true);
    try {
      const response = await mockApiService.sendOTP(phoneNumber);
      
      if (response.success) {
        setSessionId(response.session_id);
        setOtp("");
        toast.success("OTP resent to your phone number!");
        setResendCountdown(60);
        
        const timer = setInterval(() => {
          setResendCountdown((prev) => {
            if (prev <= 1) {
              clearInterval(timer);
              return 0;
            }
            return prev - 1;
          });
        }, 1000);
      } else {
        toast.error("Failed to resend OTP");
      }
    } catch (error: any) {
      toast.error("Failed to resend OTP");
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    setStep("phone");
    setPhoneNumber("");
    setOtp("");
    setSessionId(null);
    setResendCountdown(0);
    onClose();
  };

  return (
    <Dialog open={open} onOpenChange={handleClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <div className="flex justify-center mb-4">
            <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
              <Lock className="h-8 w-8 text-primary" />
            </div>
          </div>
          <DialogTitle className="text-center">
            {step === "phone" ? "Verify Your Phone" : "Enter OTP"}
          </DialogTitle>
          <DialogDescription className="text-center">
            {step === "phone"
              ? "Enter your phone number to receive OTP"
              : `Enter the 6-digit OTP sent to ${phoneNumber}`}
          </DialogDescription>
        </DialogHeader>

        <div className="space-y-6">
          {step === "phone" ? (
            <>
              <div className="space-y-2">
                <Label htmlFor="phone">Phone Number</Label>
                <div className="relative">
                  <Phone className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    id="phone"
                    type="tel"
                    placeholder="+91 98765 43210"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                    className="pl-10"
                    disabled={isLoading}
                  />
                </div>
                <p className="text-xs text-muted-foreground">
                  Enter a 10-digit phone number (with or without +91)
                </p>
              </div>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={handleClose}
                  disabled={isLoading}
                >
                  Cancel
                </Button>
                <Button
                  className="flex-1 bg-gradient-to-r from-primary to-secondary"
                  onClick={handleSendOTP}
                  disabled={isLoading || !phoneNumber.trim()}
                >
                  {isLoading ? "Sending..." : "Send OTP"}
                </Button>
              </div>
            </>
          ) : (
            <>
              <div className="space-y-2">
                <Label>One-Time Password</Label>
                <div className="flex justify-center">
                  <InputOTP maxLength={6} value={otp} onChange={setOtp}>
                    <InputOTPGroup>
                      <InputOTPSlot index={0} />
                      <InputOTPSlot index={1} />
                      <InputOTPSlot index={2} />
                      <InputOTPSlot index={3} />
                      <InputOTPSlot index={4} />
                      <InputOTPSlot index={5} />
                    </InputOTPGroup>
                  </InputOTP>
                </div>
              </div>

              <div className="flex gap-2">
                <Button
                  variant="outline"
                  className="flex-1"
                  onClick={() => {
                    setStep("phone");
                    setOtp("");
                  }}
                  disabled={isVerifying}
                >
                  Back
                </Button>
                <Button
                  className="flex-1 bg-gradient-to-r from-primary to-secondary"
                  onClick={handleVerifyOTP}
                  disabled={isVerifying || otp.length !== 6}
                >
                  {isVerifying ? "Verifying..." : "Verify OTP"}
                </Button>
              </div>

              <div className="flex gap-2">
                <Button
                  variant="ghost"
                  className="flex-1 text-sm"
                  onClick={handleResendOTP}
                  disabled={resendCountdown > 0 || isLoading}
                >
                  {resendCountdown > 0 ? (
                    <>
                      <RotateCcw className="h-3 w-3 mr-2" />
                      Resend in {resendCountdown}s
                    </>
                  ) : (
                    "Resend OTP"
                  )}
                </Button>
              </div>
            </>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default OTPModal;
