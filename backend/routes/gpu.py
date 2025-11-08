"""
GPU Orchestration API Routes
FastAPI endpoints for LUCA GPU orchestration system
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from backend.gpu_orchestration.core import (
    GPUOrchestrator, GPUDevice, GPUTask, GPUVendor, WorkloadType
)
from backend.gpu_orchestration.scoby_balancer import SCOBYLoadBalancer, OrganismRole
from backend.gpu_orchestration.ph_allocator import pHResourceAllocator, AllocationRequest
from backend.gpu_orchestration.tesla_optimizer import Tesla369Optimizer
from backend.gpu_orchestration.performance_monitor import PerformanceMonitor
from backend.benchmarks.benchmark_runner import BenchmarkRunner


router = APIRouter(prefix="/api/gpu", tags=["GPU Orchestration"])

# Global instances
orchestrator = GPUOrchestrator()
scoby_balancer = SCOBYLoadBalancer()
ph_allocator = pHResourceAllocator(total_capacity=100.0)
tesla_optimizer = Tesla369Optimizer()
performance_monitor = PerformanceMonitor()
benchmark_runner = BenchmarkRunner(orchestrator)


# === Pydantic Models ===

class GPUDeviceCreate(BaseModel):
    device_id: str
    vendor: str  # "nvidia", "amd", "intel"
    name: str
    compute_units: int
    memory_total: int
    clock_speed: int
    power_limit: int


class GPUTaskCreate(BaseModel):
    task_id: str
    workload_type: str
    priority: int
    estimated_duration: float
    memory_required: int
    compute_intensity: float
    preferred_vendor: Optional[str] = None


class OptimizationRequest(BaseModel):
    value: float
    target_signature: Optional[int] = None
    constraint_min: Optional[float] = None
    constraint_max: Optional[float] = None


# === GPU Orchestration Endpoints ===

@router.post("/devices/register")
async def register_gpu_device(device: GPUDeviceCreate):
    """Register a new GPU device with the orchestrator"""
    try:
        # Map vendor string to enum
        vendor_map = {
            "nvidia": GPUVendor.NVIDIA,
            "amd": GPUVendor.AMD,
            "intel": GPUVendor.INTEL
        }

        vendor = vendor_map.get(device.vendor.lower())
        if not vendor:
            raise HTTPException(400, f"Invalid vendor: {device.vendor}")

        # Create GPU device
        gpu_device = GPUDevice(
            device_id=device.device_id,
            vendor=vendor,
            name=device.name,
            compute_units=device.compute_units,
            memory_total=device.memory_total,
            memory_available=device.memory_total,
            clock_speed=device.clock_speed,
            power_limit=device.power_limit,
            temperature=25.0,
            utilization=0.0,
            gflops=device.compute_units * device.clock_speed / 1000.0,
            memory_bandwidth=device.memory_total / 1000.0
        )

        # Register with orchestrator
        orchestrator.register_gpu(gpu_device)

        # Register with SCOBY balancer
        role_map = {
            GPUVendor.NVIDIA: OrganismRole.YEAST,
            GPUVendor.AMD: OrganismRole.BACTERIA,
            GPUVendor.INTEL: OrganismRole.MATRIX
        }
        scoby_balancer.register_organism(device.device_id, role_map[vendor])

        # Register with pH allocator
        ph_allocator.register_resource(device.device_id, float(device.memory_total))

        return {
            "success": True,
            "device_id": device.device_id,
            "vendor": device.vendor,
            "quantum_signature": gpu_device.quantum_signature
        }

    except Exception as e:
        raise HTTPException(500, str(e))


@router.post("/tasks/submit")
async def submit_task(task: GPUTaskCreate, background_tasks: BackgroundTasks):
    """Submit a GPU task for execution"""
    try:
        # Map workload type
        workload_map = {
            "training": WorkloadType.TRAINING,
            "inference": WorkloadType.INFERENCE,
            "rendering": WorkloadType.RENDERING,
            "compute": WorkloadType.COMPUTE,
            "encoding": WorkloadType.ENCODING,
            "simulation": WorkloadType.SIMULATION
        }

        workload = workload_map.get(task.workload_type.lower())
        if not workload:
            raise HTTPException(400, f"Invalid workload type: {task.workload_type}")

        # Map vendor preference
        vendor = None
        if task.preferred_vendor:
            vendor_map = {
                "nvidia": GPUVendor.NVIDIA,
                "amd": GPUVendor.AMD,
                "intel": GPUVendor.INTEL
            }
            vendor = vendor_map.get(task.preferred_vendor.lower())

        # Create GPU task
        gpu_task = GPUTask(
            task_id=task.task_id,
            workload_type=workload,
            priority=task.priority,
            estimated_duration=task.estimated_duration,
            memory_required=task.memory_required,
            compute_intensity=task.compute_intensity,
            preferred_vendor=vendor
        )

        # Submit task
        task_id = orchestrator.submit_task(gpu_task)

        # Execute in background
        background_tasks.add_task(execute_task_async, task_id)

        return {
            "success": True,
            "task_id": task_id,
            "creation_signature": gpu_task.creation_signature,
            "status": "submitted"
        }

    except Exception as e:
        raise HTTPException(500, str(e))


async def execute_task_async(task_id: str):
    """Execute task asynchronously"""
    result = await orchestrator.execute_task(task_id)

    # Record performance metrics
    if result.get("status") == "completed":
        performance_monitor.record_task_completion(
            duration=result.get("duration", 0),
            energy=result.get("energy", 0),
            success=True
        )


@router.get("/tasks/{task_id}")
async def get_task_status(task_id: str):
    """Get task status"""
    task = orchestrator.tasks.get(task_id)

    if not task:
        raise HTTPException(404, "Task not found")

    return {
        "task_id": task.task_id,
        "workload_type": task.workload_type.value,
        "status": task.status,
        "assigned_device": task.assigned_device,
        "creation_signature": task.creation_signature,
        "created_at": task.created_at.isoformat(),
        "started_at": task.started_at.isoformat() if task.started_at else None,
        "completed_at": task.completed_at.isoformat() if task.completed_at else None,
        "performance_score": task.performance_score
    }


@router.get("/ecosystem/health")
async def get_ecosystem_health():
    """Get ecosystem health metrics"""
    health = orchestrator.get_ecosystem_health()
    scoby_status = scoby_balancer.get_ecosystem_status()
    ph_stats = ph_allocator.get_allocation_stats()

    return {
        "orchestrator": health,
        "scoby": scoby_status,
        "ph_allocation": ph_stats,
        "performance": performance_monitor.get_current_stats()
    }


@router.get("/devices")
async def list_devices():
    """List all registered GPU devices"""
    devices = []

    for device_id, device in orchestrator.devices.items():
        devices.append({
            "device_id": device_id,
            "vendor": device.vendor.value,
            "name": device.name,
            "memory_total": device.memory_total,
            "memory_available": device.memory_available,
            "utilization": device.utilization,
            "temperature": device.temperature,
            "ph_level": device.ph_level,
            "fermentation_rate": device.fermentation_rate,
            "quantum_signature": device.quantum_signature,
            "is_available": device.is_available
        })

    return {"devices": devices, "total": len(devices)}


@router.get("/stats/vendor")
async def get_vendor_stats():
    """Get statistics by GPU vendor"""
    return orchestrator.get_vendor_stats()


# === SCOBY Load Balancing Endpoints ===

@router.post("/scoby/distribute")
async def scoby_distribute_load(
    total_workload: float = 1.0,
    workload_type: str = "balanced"
):
    """Distribute workload using SCOBY balancing"""
    distribution = scoby_balancer.calculate_load_distribution(
        total_workload, workload_type
    )

    return {
        "distribution": distribution,
        "fermentation_rate": scoby_balancer.calculate_fermentation_rate(),
        "ecosystem": scoby_balancer.get_ecosystem_status()
    }


@router.post("/scoby/optimize/throughput")
async def optimize_scoby_throughput():
    """Optimize SCOBY ecosystem for throughput"""
    result = scoby_balancer.optimize_for_throughput()

    return {
        "optimization": "throughput",
        "result": result,
        "new_state": scoby_balancer.get_ecosystem_status()
    }


@router.post("/scoby/optimize/efficiency")
async def optimize_scoby_efficiency():
    """Optimize SCOBY ecosystem for efficiency"""
    result = scoby_balancer.optimize_for_efficiency()

    return {
        "optimization": "efficiency",
        "result": result,
        "new_state": scoby_balancer.get_ecosystem_status()
    }


# === pH Allocation Endpoints ===

@router.post("/ph/allocate")
async def allocate_resources(
    request_id: str,
    amount: float,
    priority: int = 5,
    duration: float = 60.0
):
    """Allocate resources using pH-based allocation"""
    allocation_request = AllocationRequest(
        request_id=request_id,
        amount=amount,
        priority=priority,
        duration=duration
    )

    success, resource_id, allocated = ph_allocator.allocate(allocation_request)

    return {
        "success": success,
        "resource_id": resource_id,
        "allocated": allocated,
        "ph_stats": ph_allocator.get_allocation_stats()
    }


@router.post("/ph/deallocate/{request_id}")
async def deallocate_resources(request_id: str):
    """Deallocate resources"""
    success = ph_allocator.deallocate(request_id)

    return {
        "success": success,
        "ph_stats": ph_allocator.get_allocation_stats()
    }


@router.post("/ph/rebalance")
async def rebalance_resources():
    """Rebalance pH-based resource allocation"""
    actions = ph_allocator.rebalance()

    return {
        "actions": actions,
        "ph_stats": ph_allocator.get_allocation_stats()
    }


@router.post("/ph/update")
async def update_ph(new_ph: float, resource_id: Optional[str] = None):
    """Update pH level"""
    ph_allocator.update_ph(new_ph, resource_id)

    return {
        "updated": True,
        "ph_stats": ph_allocator.get_allocation_stats()
    }


# === Tesla 3-6-9 Optimization Endpoints ===

@router.post("/tesla/optimize")
async def tesla_optimize_value(req: OptimizationRequest):
    """Optimize a value using Tesla 3-6-9 principle"""
    result = tesla_optimizer.optimize_value(
        req.value,
        req.target_signature,
        req.constraint_min,
        req.constraint_max
    )

    return {
        "original": result.original_value,
        "optimized": result.optimized_value,
        "improvement": result.improvement,
        "signature": result.signature,
        "harmony": result.harmony_level,
        "path": result.optimization_path
    }


@router.post("/tesla/optimize/throughput")
async def tesla_optimize_throughput(
    current_throughput: float,
    target_improvement: float = 0.1
):
    """Optimize throughput using Tesla principle"""
    result = tesla_optimizer.optimize_throughput(
        current_throughput, target_improvement
    )

    return {
        "metric": "throughput",
        "original": result.original_value,
        "optimized": result.optimized_value,
        "improvement": result.improvement,
        "signature": result.signature
    }


@router.post("/tesla/optimize/latency")
async def tesla_optimize_latency(
    current_latency: float,
    target_improvement: float = 0.2
):
    """Optimize latency using Tesla principle"""
    result = tesla_optimizer.optimize_latency(
        current_latency, target_improvement
    )

    return {
        "metric": "latency",
        "original": result.original_value,
        "optimized": result.optimized_value,
        "improvement": result.improvement,
        "signature": result.signature
    }


@router.get("/tesla/stats")
async def get_tesla_stats():
    """Get Tesla optimization statistics"""
    return tesla_optimizer.get_optimization_stats()


# === Performance Monitoring Endpoints ===

@router.get("/performance/stats")
async def get_performance_stats():
    """Get current performance statistics"""
    return performance_monitor.get_current_stats()


@router.get("/performance/report")
async def get_performance_report():
    """Get comprehensive performance report"""
    return performance_monitor.get_performance_report()


@router.get("/performance/timeseries/{metric_name}")
async def get_metric_timeseries(
    metric_name: str,
    duration: Optional[int] = None
):
    """Get time series data for a metric"""
    return {
        "metric": metric_name,
        "data": performance_monitor.get_time_series(metric_name, duration)
    }


# === Benchmark Endpoints ===

@router.post("/benchmarks/run")
async def run_benchmarks(background_tasks: BackgroundTasks):
    """Run comprehensive benchmark suite"""
    background_tasks.add_task(run_benchmarks_async)

    return {
        "status": "started",
        "message": "Benchmark suite is running in background"
    }


async def run_benchmarks_async():
    """Run benchmarks asynchronously"""
    results = await benchmark_runner.run_all_benchmarks()
    benchmark_runner.export_results("/home/user/LUCA-AI_369/benchmark_results.json")


@router.get("/benchmarks/results")
async def get_benchmark_results():
    """Get latest benchmark results"""
    if not benchmark_runner.results:
        raise HTTPException(404, "No benchmark results available")

    return {
        "total_benchmarks": len(benchmark_runner.results),
        "results": [r.to_dict() for r in benchmark_runner.results[-10:]]
    }


# === Health Check ===

@router.get("/health")
async def gpu_health_check():
    """GPU orchestration system health check"""
    return {
        "status": "healthy",
        "components": {
            "orchestrator": len(orchestrator.devices) > 0,
            "scoby_balancer": len(scoby_balancer.organisms) > 0,
            "ph_allocator": len(ph_allocator.resources) > 0,
            "tesla_optimizer": tesla_optimizer.total_optimizations >= 0,
            "performance_monitor": True
        },
        "devices": len(orchestrator.devices),
        "active_tasks": len([t for t in orchestrator.tasks.values() if t.status == "running"]),
        "completed_tasks": orchestrator.total_tasks_completed
    }
