import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AbusePolicy:
    cpu_warn_percent: float = 95.0
    memory_warn_percent: float = 95.0
    pids_warn_percent: float = 90.0
    hard_cpu_percent: float = 98.0
    hard_memory_percent: float = 98.0
    violation_samples: int = 5


@dataclass(frozen=True)
class ContainerUsage:
    cpu_percent: float
    memory_percent: float
    pids: int


@dataclass(frozen=True)
class AbuseDecision:
    violated: bool
    reason: str = ""


def parse_docker_stats(line: str) -> Optional[ContainerUsage]:
    """Parse: CPU %, memory %, PIDs from docker stats --format output."""
    parts = [p.strip() for p in line.split("|")]
    if len(parts) != 3:
        return None
    try:
        cpu = float(parts[0].rstrip("%"))
        memory = float(parts[1].rstrip("%"))
        pids = int(parts[2])
    except (TypeError, ValueError):
        return None
    return ContainerUsage(cpu, memory, pids)


def evaluate_usage(
    usage: ContainerUsage,
    *,
    pids_limit: int,
    consecutive_violations: int,
    policy: AbusePolicy = AbusePolicy(),
) -> AbuseDecision:
    if pids_limit <= 0:
        return AbuseDecision(False)

    pids_pct = (usage.pids / pids_limit) * 100.0

    if pids_pct >= policy.pids_warn_percent and consecutive_violations >= policy.violation_samples:
        return AbuseDecision(True, f"PID usage {usage.pids}/{pids_limit} ({pids_pct:.0f}%)")

    severe_resources = (
        usage.cpu_percent >= policy.hard_cpu_percent
        and usage.memory_percent >= policy.hard_memory_percent
    )
    sustained_resources = (
        usage.cpu_percent >= policy.cpu_warn_percent
        and usage.memory_percent >= policy.memory_warn_percent
        and consecutive_violations >= policy.violation_samples
    )

    if severe_resources and consecutive_violations >= policy.violation_samples:
        return AbuseDecision(
            True,
            f"CPU {usage.cpu_percent:.1f}% and memory {usage.memory_percent:.1f}% sustained",
        )

    if sustained_resources:
        return AbuseDecision(
            True,
            f"CPU {usage.cpu_percent:.1f}% and memory {usage.memory_percent:.1f}% sustained",
        )

    return AbuseDecision(False)


def warning_level(
    usage: ContainerUsage,
    *,
    pids_limit: int,
    policy: AbusePolicy = AbusePolicy(),
) -> str:
    pids_pct = (usage.pids / max(1, pids_limit)) * 100.0
    if pids_pct >= policy.pids_warn_percent:
        return "high"
    if usage.cpu_percent >= policy.cpu_warn_percent or usage.memory_percent >= policy.memory_warn_percent:
        return "elevated"
    return "normal"
