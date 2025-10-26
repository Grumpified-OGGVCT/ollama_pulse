#!/usr/bin/env python3
"""
Comprehensive Monitoring and Debugging System for Ollama Pulse

Tracks all workflow operations (successes and failures) for surgical fixes
and future dashboard integration with Ollama Proxy.
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict, field
from typing import List, Dict, Optional
from enum import Enum

class OperationStatus(Enum):
    SUCCESS = "success"
    FAILURE = "failure"
    WARNING = "warning"
    SKIPPED = "skipped"

class ErrorCategory(Enum):
    API_FAILURE = "api_failure"
    PARSING_ERROR = "parsing_error"
    NETWORK_ERROR = "network_error"
    VALIDATION_ERROR = "validation_error"
    TIMEOUT = "timeout"
    UNKNOWN = "unknown"

@dataclass
class IngestionMetrics:
    source: str
    timestamp: str
    duration_seconds: float
    entries_collected: int
    entries_high_quality: int
    success: bool
    method: str = "unknown"  # PRIMARY or FALLBACK
    error_message: Optional[str] = None
    error_category: Optional[str] = None

    @property
    def quality_ratio(self):
        return self.entries_high_quality / self.entries_collected if self.entries_collected > 0 else 0.0

@dataclass
class WorkflowOperation:
    """Tracks individual workflow operations"""
    operation_type: str  # e.g., "ingestion", "aggregation", "mining", "report_generation"
    source: str  # e.g., "official", "community", "tools"
    status: str  # SUCCESS, FAILURE, WARNING, SKIPPED
    timestamp: str
    duration_seconds: float
    details: Dict = field(default_factory=dict)
    error_message: Optional[str] = None
    error_category: Optional[str] = None

@dataclass
class WorkflowSummary:
    """Summary of a complete workflow run"""
    workflow_type: str  # "hourly_ingestion" or "daily_report"
    start_time: str
    end_time: str
    total_duration_seconds: float
    operations: List[WorkflowOperation]
    overall_status: str
    total_operations: int
    successful_operations: int
    failed_operations: int
    warnings: int

    @property
    def success_rate(self):
        return (self.successful_operations / self.total_operations * 100) if self.total_operations > 0 else 0.0

class MetricsCollector:
    """Enhanced metrics collector with comprehensive tracking"""

    def __init__(self, metrics_dir="data/metrics"):
        self.metrics_dir = Path(metrics_dir)
        self.metrics_dir.mkdir(parents=True, exist_ok=True)
        self.current_workflow_operations = []
        self.workflow_start_time = None

    def start_workflow(self, workflow_type: str):
        """Start tracking a new workflow"""
        self.workflow_start_time = datetime.now()
        self.current_workflow_operations = []
        print(f"📊 Started tracking workflow: {workflow_type}")

    def record_operation(self, operation: WorkflowOperation):
        """Record a single operation"""
        self.current_workflow_operations.append(operation)

        # Log to console with appropriate emoji
        status_emoji = {
            "success": "✅",
            "failure": "❌",
            "warning": "⚠️",
            "skipped": "⏭️"
        }
        emoji = status_emoji.get(operation.status.lower(), "ℹ️")

        print(f"{emoji} {operation.operation_type} - {operation.source}: {operation.status}")
        if operation.error_message:
            print(f"   Error: {operation.error_message}")

    def end_workflow(self, workflow_type: str, overall_status: str = "success"):
        """End workflow tracking and save summary"""
        if not self.workflow_start_time:
            print("⚠️  No workflow started")
            return

        end_time = datetime.now()
        duration = (end_time - self.workflow_start_time).total_seconds()

        # Calculate statistics
        successful = sum(1 for op in self.current_workflow_operations if op.status == "success")
        failed = sum(1 for op in self.current_workflow_operations if op.status == "failure")
        warnings = sum(1 for op in self.current_workflow_operations if op.status == "warning")

        summary = WorkflowSummary(
            workflow_type=workflow_type,
            start_time=self.workflow_start_time.isoformat(),
            end_time=end_time.isoformat(),
            total_duration_seconds=duration,
            operations=self.current_workflow_operations,
            overall_status=overall_status,
            total_operations=len(self.current_workflow_operations),
            successful_operations=successful,
            failed_operations=failed,
            warnings=warnings
        )

        # Save to file
        today = datetime.now().strftime("%Y-%m-%d")
        summary_file = self.metrics_dir / f"workflow_{workflow_type}_{today}.jsonl"

        with open(summary_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(summary)) + '\n')

        # Print summary
        print(f"\n📊 Workflow Summary: {workflow_type}")
        print(f"   Duration: {duration:.2f}s")
        print(f"   Success Rate: {summary.success_rate:.1f}%")
        print(f"   Operations: {successful} ✅ | {failed} ❌ | {warnings} ⚠️")
        print(f"   Saved to: {summary_file}\n")

        # Reset
        self.current_workflow_operations = []
        self.workflow_start_time = None

    def record_ingestion(self, metrics: IngestionMetrics):
        """Record ingestion metrics (backward compatibility)"""
        today = datetime.now().strftime("%Y-%m-%d")
        with open(self.metrics_dir / f"ingestion_{today}.jsonl", 'a', encoding='utf-8') as f:
            f.write(json.dumps(asdict(metrics)) + '\n')

    def check_auto_tune_trigger(self):
        """Check if quality is below threshold"""
        # TODO: Implement auto-tune logic
        return False

if __name__ == "__main__":
    print("✅ Comprehensive Monitoring System Ready")
    print("   - Workflow tracking")
    print("   - Operation logging")
    print("   - Error categorization")
    print("   - Dashboard-ready metrics")
