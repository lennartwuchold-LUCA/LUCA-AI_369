"""
Performance Monitoring and Metrics System
Real-time monitoring of GPU orchestration performance
"""

import time
import statistics
from typing import Dict, List, Optional, Deque
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque, defaultdict
import json


@dataclass
class PerformanceMetric:
    """Single performance metric measurement"""
    timestamp: datetime
    metric_name: str
    value: float
    unit: str
    tags: Dict[str, str] = field(default_factory=dict)


@dataclass
class PerformanceSnapshot:
    """Snapshot of system performance"""
    timestamp: datetime
    throughput: float  # tasks/sec
    latency_p50: float  # ms
    latency_p99: float  # ms
    cpu_utilization: float  # %
    gpu_utilization: float  # %
    memory_utilization: float  # %
    energy_efficiency: float  # tasks/watt
    active_tasks: int
    queued_tasks: int


class PerformanceMonitor:
    """
    Real-time performance monitoring system

    Tracks:
    - Throughput metrics
    - Latency distributions
    - Resource utilization
    - Energy efficiency
    - Bio-inspired metrics (pH, fermentation rate, etc.)
    """

    def __init__(self, window_size: int = 1000):
        self.window_size = window_size

        # Metric storage (circular buffers)
        self.metrics: Dict[str, Deque[PerformanceMetric]] = defaultdict(
            lambda: deque(maxlen=window_size)
        )

        # Snapshots
        self.snapshots: Deque[PerformanceSnapshot] = deque(maxlen=window_size)

        # Counters
        self.total_tasks_completed: int = 0
        self.total_tasks_failed: int = 0
        self.total_energy_consumed: float = 0.0

        # Timing
        self.start_time: datetime = datetime.now()
        self.last_snapshot_time: datetime = datetime.now()

        print("📊 Performance Monitor initialized - Real-time metrics tracking")

    def record_metric(
        self,
        metric_name: str,
        value: float,
        unit: str = "",
        tags: Optional[Dict[str, str]] = None
    ):
        """Record a single metric"""
        metric = PerformanceMetric(
            timestamp=datetime.now(),
            metric_name=metric_name,
            value=value,
            unit=unit,
            tags=tags or {}
        )

        self.metrics[metric_name].append(metric)

    def record_task_completion(
        self,
        duration: float,
        energy: float,
        success: bool = True
    ):
        """Record task completion"""
        if success:
            self.total_tasks_completed += 1
        else:
            self.total_tasks_failed += 1

        self.total_energy_consumed += energy

        # Record metrics
        self.record_metric("task_duration", duration, "seconds")
        self.record_metric("task_energy", energy, "wh")

    def take_snapshot(
        self,
        active_tasks: int = 0,
        queued_tasks: int = 0,
        gpu_util: float = 0.0
    ) -> PerformanceSnapshot:
        """Take a performance snapshot"""
        now = datetime.now()

        # Calculate throughput (tasks/sec since last snapshot)
        time_delta = (now - self.last_snapshot_time).total_seconds()
        if time_delta > 0:
            throughput = self.total_tasks_completed / time_delta
        else:
            throughput = 0.0

        # Calculate latencies
        durations = [m.value * 1000 for m in self.metrics["task_duration"]]  # Convert to ms
        if durations:
            durations_sorted = sorted(durations)
            p50_idx = len(durations_sorted) // 2
            p99_idx = int(len(durations_sorted) * 0.99)

            latency_p50 = durations_sorted[p50_idx] if durations_sorted else 0.0
            latency_p99 = durations_sorted[p99_idx] if durations_sorted else 0.0
        else:
            latency_p50 = 0.0
            latency_p99 = 0.0

        # Calculate energy efficiency
        if self.total_energy_consumed > 0:
            energy_efficiency = self.total_tasks_completed / self.total_energy_consumed
        else:
            energy_efficiency = 0.0

        snapshot = PerformanceSnapshot(
            timestamp=now,
            throughput=throughput,
            latency_p50=latency_p50,
            latency_p99=latency_p99,
            cpu_utilization=0.0,  # Would be measured from system
            gpu_utilization=gpu_util,
            memory_utilization=0.0,  # Would be measured from system
            energy_efficiency=energy_efficiency,
            active_tasks=active_tasks,
            queued_tasks=queued_tasks
        )

        self.snapshots.append(snapshot)
        self.last_snapshot_time = now

        return snapshot

    def get_current_stats(self) -> Dict[str, any]:
        """Get current performance statistics"""
        uptime = (datetime.now() - self.start_time).total_seconds()

        # Latest snapshot
        latest_snapshot = self.snapshots[-1] if self.snapshots else None

        # Success rate
        total_tasks = self.total_tasks_completed + self.total_tasks_failed
        success_rate = (
            self.total_tasks_completed / total_tasks
            if total_tasks > 0 else 1.0
        )

        # Average metrics
        avg_throughput = 0.0
        avg_latency = 0.0

        if self.snapshots:
            avg_throughput = statistics.mean(s.throughput for s in self.snapshots)

        durations = [m.value for m in self.metrics["task_duration"]]
        if durations:
            avg_latency = statistics.mean(durations) * 1000  # ms

        return {
            "uptime": round(uptime, 2),
            "total_tasks_completed": self.total_tasks_completed,
            "total_tasks_failed": self.total_tasks_failed,
            "success_rate": round(success_rate, 4),
            "throughput": {
                "current": round(latest_snapshot.throughput, 2) if latest_snapshot else 0.0,
                "average": round(avg_throughput, 2)
            },
            "latency": {
                "p50": round(latest_snapshot.latency_p50, 2) if latest_snapshot else 0.0,
                "p99": round(latest_snapshot.latency_p99, 2) if latest_snapshot else 0.0,
                "average": round(avg_latency, 2)
            },
            "energy": {
                "total_consumed": round(self.total_energy_consumed, 4),
                "efficiency": round(latest_snapshot.energy_efficiency, 2) if latest_snapshot else 0.0
            },
            "tasks": {
                "active": latest_snapshot.active_tasks if latest_snapshot else 0,
                "queued": latest_snapshot.queued_tasks if latest_snapshot else 0
            }
        }

    def get_time_series(
        self,
        metric_name: str,
        duration: Optional[int] = None
    ) -> List[Dict[str, any]]:
        """Get time series data for a metric"""
        if metric_name not in self.metrics:
            return []

        metrics = list(self.metrics[metric_name])

        if duration:
            # Filter by duration (seconds)
            cutoff = datetime.now().timestamp() - duration
            metrics = [
                m for m in metrics
                if m.timestamp.timestamp() >= cutoff
            ]

        return [
            {
                "timestamp": m.timestamp.isoformat(),
                "value": m.value,
                "unit": m.unit,
                "tags": m.tags
            }
            for m in metrics
        ]

    def get_performance_report(self) -> Dict[str, any]:
        """Generate comprehensive performance report"""
        stats = self.get_current_stats()

        # Calculate trends
        throughput_trend = "stable"
        latency_trend = "stable"

        if len(self.snapshots) >= 10:
            recent_throughput = [s.throughput for s in list(self.snapshots)[-10:]]
            recent_latency = [s.latency_p50 for s in list(self.snapshots)[-10:]]

            # Simple trend detection
            if recent_throughput[-1] > recent_throughput[0] * 1.1:
                throughput_trend = "increasing"
            elif recent_throughput[-1] < recent_throughput[0] * 0.9:
                throughput_trend = "decreasing"

            if recent_latency[-1] > recent_latency[0] * 1.1:
                latency_trend = "increasing"
            elif recent_latency[-1] < recent_latency[0] * 0.9:
                latency_trend = "decreasing"

        return {
            "timestamp": datetime.now().isoformat(),
            "stats": stats,
            "trends": {
                "throughput": throughput_trend,
                "latency": latency_trend
            },
            "health_score": self._calculate_health_score(),
            "recommendations": self._generate_recommendations()
        }

    def _calculate_health_score(self) -> float:
        """Calculate overall system health score (0-100)"""
        score = 100.0

        # Factor 1: Success rate (40 points)
        total_tasks = self.total_tasks_completed + self.total_tasks_failed
        if total_tasks > 0:
            success_rate = self.total_tasks_completed / total_tasks
            score -= (1.0 - success_rate) * 40

        # Factor 2: Latency (30 points)
        if self.snapshots:
            latest = self.snapshots[-1]
            if latest.latency_p99 > 100:  # > 100ms is bad
                score -= min(30, (latest.latency_p99 - 100) / 10)

        # Factor 3: Queue depth (30 points)
        if self.snapshots:
            latest = self.snapshots[-1]
            if latest.queued_tasks > 100:
                score -= min(30, (latest.queued_tasks - 100) / 10)

        return max(0, min(100, score))

    def _generate_recommendations(self) -> List[str]:
        """Generate performance recommendations"""
        recommendations = []

        if not self.snapshots:
            return recommendations

        latest = self.snapshots[-1]

        # High latency
        if latest.latency_p99 > 100:
            recommendations.append(
                "High P99 latency detected. Consider scaling horizontally or "
                "adjusting pH levels for better fermentation."
            )

        # High queue depth
        if latest.queued_tasks > 50:
            recommendations.append(
                "Queue depth is high. Add more GPU resources or optimize "
                "task distribution with SCOBY balancing."
            )

        # Low throughput
        if latest.throughput < 100:
            recommendations.append(
                "Throughput is below optimal. Apply Tesla 3-6-9 optimization "
                "to boost performance."
            )

        # Low GPU utilization
        if latest.gpu_utilization < 0.5:
            recommendations.append(
                "GPU utilization is low. Increase workload or adjust pH "
                "to stimulate more activity."
            )

        if not recommendations:
            recommendations.append("System is performing optimally! 🚀")

        return recommendations

    def export_metrics(self, filename: str = "performance_metrics.json"):
        """Export all metrics to JSON file"""
        data = {
            "report": self.get_performance_report(),
            "snapshots": [
                {
                    "timestamp": s.timestamp.isoformat(),
                    "throughput": s.throughput,
                    "latency_p50": s.latency_p50,
                    "latency_p99": s.latency_p99,
                    "energy_efficiency": s.energy_efficiency,
                    "active_tasks": s.active_tasks,
                    "queued_tasks": s.queued_tasks
                }
                for s in self.snapshots
            ],
            "time_series": {
                name: self.get_time_series(name)
                for name in self.metrics.keys()
            }
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"📈 Metrics exported to {filename}")
