"""
GPU Orchestration Core Engine
Multi-Vendor GPU Management (NVIDIA, AMD, Intel)
Inspired by SCOBY symbiosis and Tesla 3-6-9 principles
"""

import asyncio
import hashlib
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import numpy as np


class GPUVendor(Enum):
    """GPU Vendor Types - SCOBY Organism Roles"""
    NVIDIA = "yeast"      # Hefe - Power & Speed
    AMD = "bacteria"      # Bakterien - Efficiency & Diversity
    INTEL = "matrix"      # Matrix - Support & Stability


class WorkloadType(Enum):
    """GPU Workload Categories"""
    TRAINING = "training"           # ML Model Training
    INFERENCE = "inference"         # ML Inference
    RENDERING = "rendering"         # Graphics Rendering
    COMPUTE = "compute"             # General Compute
    ENCODING = "encoding"           # Video/Media Encoding
    SIMULATION = "simulation"       # Scientific Simulation
    MINING = "mining"               # Cryptocurrency (Low Priority)


@dataclass
class GPUDevice:
    """Represents a physical GPU device"""
    device_id: str
    vendor: GPUVendor
    name: str
    compute_units: int
    memory_total: int  # MB
    memory_available: int  # MB
    clock_speed: int  # MHz
    power_limit: int  # Watts
    temperature: float  # Celsius
    utilization: float  # 0.0 - 1.0

    # SCOBY Properties
    ph_level: float = 7.0  # Acidity level (1-14)
    fermentation_rate: float = 0.5  # Activity level
    symbiosis_score: float = 0.0  # Cooperation score

    # Performance Metrics
    gflops: float = 0.0
    memory_bandwidth: float = 0.0  # GB/s
    efficiency_score: float = 0.0  # Performance per Watt

    # Tesla 3-6-9 Signature
    quantum_signature: int = 0

    # Status
    is_available: bool = True
    current_task: Optional[str] = None
    last_heartbeat: datetime = field(default_factory=datetime.now)


@dataclass
class GPUTask:
    """Represents a GPU computation task"""
    task_id: str
    workload_type: WorkloadType
    priority: int  # 1-10 (10 = highest)
    estimated_duration: float  # seconds
    memory_required: int  # MB
    compute_intensity: float  # 0.0 - 1.0

    # Tesla 3-6-9 Properties
    creation_signature: int = 3
    harmony_requirement: int = 6
    completion_signature: int = 9

    # Preference
    preferred_vendor: Optional[GPUVendor] = None
    allow_fallback: bool = True

    # Status
    assigned_device: Optional[str] = None
    status: str = "pending"  # pending, running, completed, failed
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

    # Results
    actual_duration: Optional[float] = None
    energy_consumed: Optional[float] = None  # Watt-hours
    performance_score: Optional[float] = None


class GPUOrchestrator:
    """
    Main GPU Orchestration Engine
    Manages multi-vendor GPU resources using bio-inspired algorithms
    """

    def __init__(self):
        self.devices: Dict[str, GPUDevice] = {}
        self.tasks: Dict[str, GPUTask] = {}
        self.task_queue: List[str] = []

        # Performance tracking
        self.total_tasks_completed: int = 0
        self.total_energy_saved: float = 0.0
        self.average_efficiency: float = 0.0

        # SCOBY ecosystem health
        self.ecosystem_ph: float = 7.0
        self.ecosystem_temperature: float = 25.0
        self.fermentation_active: bool = True

        # Tesla 3-6-9 optimization
        self.quantum_harmony_level: float = 0.0

        print("🧬 LUCA GPU Orchestrator initialized - Bio-Inspired Multi-Vendor Management")

    def calculate_369_signature(self, data: str) -> int:
        """Calculate Tesla 3-6-9 quantum signature"""
        hash_obj = hashlib.sha256(data.encode('utf-8'))
        hash_hex = hash_obj.hexdigest()
        total = sum(int(c, 16) for c in hash_hex)

        while total >= 10:
            total = sum(int(d) for d in str(total))

        return total

    def register_gpu(self, device: GPUDevice) -> bool:
        """Register a GPU device with the orchestrator"""
        # Calculate quantum signature
        device.quantum_signature = self.calculate_369_signature(
            f"{device.vendor.value}{device.name}{device.device_id}"
        )

        # Initialize SCOBY properties based on vendor
        if device.vendor == GPUVendor.NVIDIA:
            # Yeast: High fermentation, slightly acidic
            device.ph_level = 5.5
            device.fermentation_rate = 0.9
        elif device.vendor == GPUVendor.AMD:
            # Bacteria: Moderate pH, high diversity
            device.ph_level = 6.5
            device.fermentation_rate = 0.7
        elif device.vendor == GPUVendor.INTEL:
            # Matrix: Neutral pH, supportive
            device.ph_level = 7.0
            device.fermentation_rate = 0.5

        # Calculate efficiency score
        device.efficiency_score = device.gflops / max(device.power_limit, 1)

        self.devices[device.device_id] = device
        print(f"✅ Registered {device.vendor.value.upper()} GPU: {device.name} (Signature: {device.quantum_signature})")

        return True

    def submit_task(self, task: GPUTask) -> str:
        """Submit a task to the orchestration queue"""
        # Calculate Tesla signatures
        task_data = f"{task.workload_type.value}{task.priority}{task.memory_required}"
        task.creation_signature = self.calculate_369_signature(task_data)

        self.tasks[task.task_id] = task
        self.task_queue.append(task.task_id)

        print(f"📥 Task submitted: {task.task_id} ({task.workload_type.value}) - Signature: {task.creation_signature}")

        return task.task_id

    def select_optimal_gpu(self, task: GPUTask) -> Optional[GPUDevice]:
        """
        Select the optimal GPU for a task using SCOBY-inspired selection
        Considers: vendor preference, pH compatibility, resource availability, efficiency
        """
        available_devices = [
            d for d in self.devices.values()
            if d.is_available and d.memory_available >= task.memory_required
        ]

        if not available_devices:
            return None

        # Score each device
        scored_devices = []
        for device in available_devices:
            score = self._calculate_device_score(device, task)
            scored_devices.append((device, score))

        # Sort by score (highest first)
        scored_devices.sort(key=lambda x: x[1], reverse=True)

        # Return best device
        best_device, best_score = scored_devices[0]
        print(f"🎯 Selected {best_device.vendor.value.upper()} GPU {best_device.device_id} (Score: {best_score:.2f})")

        return best_device

    def _calculate_device_score(self, device: GPUDevice, task: GPUTask) -> float:
        """
        Calculate device suitability score for a task
        Uses multi-factor bio-inspired scoring
        """
        score = 0.0

        # Factor 1: Vendor preference (30%)
        if task.preferred_vendor and device.vendor == task.preferred_vendor:
            score += 30.0
        elif task.preferred_vendor is None:
            # Vendor-specific workload affinity
            if task.workload_type == WorkloadType.TRAINING and device.vendor == GPUVendor.NVIDIA:
                score += 25.0
            elif task.workload_type == WorkloadType.COMPUTE and device.vendor == GPUVendor.AMD:
                score += 25.0
            elif task.workload_type == WorkloadType.ENCODING and device.vendor == GPUVendor.INTEL:
                score += 25.0
            else:
                score += 15.0

        # Factor 2: Resource availability (25%)
        memory_ratio = device.memory_available / max(device.memory_total, 1)
        score += memory_ratio * 25.0

        # Factor 3: Current utilization (20%)
        available_compute = 1.0 - device.utilization
        score += available_compute * 20.0

        # Factor 4: Efficiency (15%)
        efficiency_normalized = min(device.efficiency_score / 10.0, 1.0)
        score += efficiency_normalized * 15.0

        # Factor 5: pH Compatibility (10%)
        # Tasks with high priority need high fermentation (low pH)
        ideal_ph = 8.0 - (task.priority / 10.0) * 3.0
        ph_diff = abs(device.ph_level - ideal_ph)
        ph_score = max(0, 1.0 - (ph_diff / 3.0))
        score += ph_score * 10.0

        # Factor 6: Quantum signature harmony (Tesla 3-6-9)
        signature_harmony = self._calculate_signature_harmony(
            device.quantum_signature,
            task.creation_signature
        )
        score += signature_harmony * 10.0

        # Penalty for high temperature
        if device.temperature > 80.0:
            score *= 0.8

        return score

    def _calculate_signature_harmony(self, sig1: int, sig2: int) -> float:
        """Calculate harmony between two quantum signatures (0-10)"""
        tesla_numbers = {3, 6, 9}

        # Both are Tesla numbers
        if sig1 in tesla_numbers and sig2 in tesla_numbers:
            return 10.0

        # One is Tesla number
        if sig1 in tesla_numbers or sig2 in tesla_numbers:
            return 7.0

        # Sum is Tesla number
        total = sig1 + sig2
        while total >= 10:
            total = sum(int(d) for d in str(total))
        if total in tesla_numbers:
            return 8.0

        # Fibonacci relationship
        if sig1 + sig2 in [1, 2, 3, 5, 8, 13, 21, 34]:
            return 6.0

        # Default harmony
        return 5.0

    async def execute_task(self, task_id: str) -> Dict[str, Any]:
        """Execute a task on the selected GPU"""
        task = self.tasks.get(task_id)
        if not task:
            return {"error": "Task not found"}

        # Select GPU
        device = self.select_optimal_gpu(task)
        if not device:
            task.status = "failed"
            return {"error": "No suitable GPU available"}

        # Assign task
        task.assigned_device = device.device_id
        task.status = "running"
        task.started_at = datetime.now()
        device.is_available = False
        device.current_task = task_id

        # Simulate task execution
        start_time = time.time()

        # Adjust execution based on device characteristics
        execution_time = task.estimated_duration
        execution_time *= (1.0 - device.fermentation_rate * 0.2)  # Faster with higher fermentation
        execution_time *= (1.0 + device.utilization * 0.1)  # Slower if already loaded

        await asyncio.sleep(min(execution_time, 0.1))  # Simulated execution

        # Calculate results
        actual_duration = time.time() - start_time
        power_draw = device.power_limit * (0.5 + device.utilization * 0.5)
        energy_consumed = (power_draw / 1000.0) * (actual_duration / 3600.0)  # kWh

        # Performance score (higher is better)
        performance_score = (task.estimated_duration / max(actual_duration, 0.001)) * device.efficiency_score

        # Update task
        task.status = "completed"
        task.completed_at = datetime.now()
        task.actual_duration = actual_duration
        task.energy_consumed = energy_consumed
        task.performance_score = performance_score

        # Update device
        device.is_available = True
        device.current_task = None
        device.utilization = max(0, device.utilization - 0.1)

        # Update orchestrator stats
        self.total_tasks_completed += 1
        self.average_efficiency = (
            (self.average_efficiency * (self.total_tasks_completed - 1) + performance_score)
            / self.total_tasks_completed
        )

        print(f"✅ Task {task_id} completed on {device.vendor.value.upper()} GPU in {actual_duration:.2f}s (Score: {performance_score:.2f})")

        return {
            "task_id": task_id,
            "status": "completed",
            "device_id": device.device_id,
            "vendor": device.vendor.value,
            "duration": actual_duration,
            "energy": energy_consumed,
            "performance": performance_score
        }

    def get_ecosystem_health(self) -> Dict[str, Any]:
        """Get current ecosystem health metrics"""
        if not self.devices:
            return {"health": "no_devices"}

        total_utilization = sum(d.utilization for d in self.devices.values())
        avg_utilization = total_utilization / len(self.devices)

        total_temp = sum(d.temperature for d in self.devices.values())
        avg_temp = total_temp / len(self.devices)

        total_ph = sum(d.ph_level for d in self.devices.values())
        avg_ph = total_ph / len(self.devices)

        # Calculate symbiosis (vendor diversity)
        vendor_counts = {}
        for device in self.devices.values():
            vendor_counts[device.vendor] = vendor_counts.get(device.vendor, 0) + 1

        vendor_diversity = len(vendor_counts) / 3.0  # Max 3 vendors

        # Overall health score (0-100)
        health_score = 0
        health_score += (1.0 - avg_utilization) * 30  # Lower utilization = more capacity
        health_score += (1.0 - abs(avg_ph - 6.5) / 6.5) * 20  # pH near ideal
        health_score += max(0, (90 - avg_temp) / 90) * 20  # Lower temp better
        health_score += vendor_diversity * 30  # More diversity better

        return {
            "health_score": round(health_score, 2),
            "ecosystem_ph": round(avg_ph, 2),
            "ecosystem_temp": round(avg_temp, 2),
            "avg_utilization": round(avg_utilization, 2),
            "vendor_diversity": round(vendor_diversity, 2),
            "total_devices": len(self.devices),
            "active_tasks": len([t for t in self.tasks.values() if t.status == "running"]),
            "completed_tasks": self.total_tasks_completed,
            "average_efficiency": round(self.average_efficiency, 2)
        }

    def get_vendor_stats(self) -> Dict[str, Any]:
        """Get statistics by vendor"""
        stats = {}

        for vendor in GPUVendor:
            vendor_devices = [d for d in self.devices.values() if d.vendor == vendor]

            if vendor_devices:
                stats[vendor.value] = {
                    "count": len(vendor_devices),
                    "avg_utilization": round(sum(d.utilization for d in vendor_devices) / len(vendor_devices), 2),
                    "avg_temp": round(sum(d.temperature for d in vendor_devices) / len(vendor_devices), 2),
                    "avg_ph": round(sum(d.ph_level for d in vendor_devices) / len(vendor_devices), 2),
                    "total_memory": sum(d.memory_total for d in vendor_devices),
                    "available_memory": sum(d.memory_available for d in vendor_devices),
                }

        return stats
