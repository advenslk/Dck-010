from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional


@dataclass(frozen=True)
class SecurityPolicy:
    min_account_age_days: int = 30
    min_member_age_days: int = 7
    max_risk_score: int = 49
    max_recent_attempts: int = 3


def _days_since(timestamp: Optional[datetime], now: datetime) -> Optional[float]:
    if timestamp is None:
        return None
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)
    return max(0.0, (now - timestamp).total_seconds() / 86400)


def evaluate_vps_request(
    *,
    account_created_at: Optional[datetime],
    member_joined_at: Optional[datetime],
    trust_score: int = 100,
    restricted: bool = False,
    recent_attempts: int = 0,
    policy: SecurityPolicy = SecurityPolicy(),
    now: Optional[datetime] = None,
):
    """Return (allowed, risk_score, reasons) for a VPS deployment request."""
    now = now or datetime.now(timezone.utc)
    reasons = []
    score = 0

    account_age = _days_since(account_created_at, now)
    member_age = _days_since(member_joined_at, now)

    if restricted:
        reasons.append("account is restricted")
        score += 100

    if account_age is None:
        reasons.append("account age could not be verified")
        score += 20
    elif account_age < policy.min_account_age_days:
        reasons.append(f"Discord account must be at least {policy.min_account_age_days} days old")
        score += 40

    if member_age is None:
        reasons.append("server membership age could not be verified")
        score += 10
    elif member_age < policy.min_member_age_days:
        reasons.append(f"server membership must be at least {policy.min_member_age_days} days old")
        score += 25

    if trust_score < 80:
        score += min(30, (80 - max(0, trust_score)) // 2)
    if trust_score < 50:
        reasons.append("trust score is below the VPS safety threshold")
        score += 30

    if recent_attempts >= policy.max_recent_attempts:
        reasons.append("too many recent VPS deployment attempts")
        score += min(30, recent_attempts * 5)

    return score <= policy.max_risk_score and not restricted and not reasons, score, reasons
