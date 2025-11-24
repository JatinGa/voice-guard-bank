"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum


class StressLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskLevel(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


# Request schemas
class VoiceTranscribeRequest(BaseModel):
    audio_file_path: str = Field(..., description="Path to audio file")
    user_id: Optional[str] = Field(default="user_123")


class VoiceLivenessRequest(BaseModel):
    transcript: str = Field(..., description="User's spoken response")
    challenge_phrase: str = Field(..., description="Challenge phrase given to user")


class TransactionRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Transfer amount")
    recipient_account: str = Field(..., description="Recipient account number")
    recipient_name: str = Field(..., description="Recipient name")
    user_id: Optional[str] = Field(default="user_123")


class RiskEvaluationRequest(BaseModel):
    transcript: str = Field(..., description="Voice transcription")
    amount: Optional[float] = Field(default=0)
    is_liveness_passed: bool = Field(default=False)
    stress_level: Optional[StressLevel] = Field(default="low")


# Response schemas
class TranscriptionResponse(BaseModel):
    text: str
    language: str = "en"
    duration: float = 0
    confidence: float = 0.5
    error: Optional[str] = None


class LivenessResponse(BaseModel):
    passed: bool
    score: int = Field(..., ge=0, le=100)
    confidence: float = Field(..., ge=0, le=1)
    reasons: List[str]
    transcript: str


class BalanceResponse(BaseModel):
    account_number: str
    balance: float
    currency: str
    timestamp: str


class TransactionResponse(BaseModel):
    success: bool
    transaction_id: Optional[str] = None
    amount: Optional[float] = None
    recipient: Optional[str] = None
    new_balance: Optional[float] = None
    message: str
    timestamp: str
    error: Optional[str] = None


class RiskEvaluationResponse(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: RiskLevel
    factors: List[str]
    requires_additional_verification: bool
    recommendations: Optional[List[str]] = None


class HealthResponse(BaseModel):
    status: str = "healthy"
    message: str
    timestamp: str
