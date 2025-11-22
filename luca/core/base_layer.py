"""
Abstract Base Layer for LUCA's 12-Layer Consciousness Architecture

This module provides the abstract base class that all 12 consciousness layers
must implement, ensuring a consistent interface and promoting modularity.

Author: Lennart Wuchold
Date: 2025-11-22
Standard: 369/370
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import IntEnum
from typing import Any, Dict, Generic, Optional, TypeVar

# Type variable for layer input/output
InputType = TypeVar("InputType")
OutputType = TypeVar("OutputType")


class LayerID(IntEnum):
    """Enumeration of the 12 consciousness layers + root kernel (Layer 0)"""

    ROOT_KERNEL = 0  # Meta-layer that integrates all others
    LAYER_1 = 1  # Foundation layer
    LAYER_2 = 2  # Building layer
    LAYER_3 = 3  # Fibonacci optimization
    LAYER_4 = 4  # Pattern recognition
    LAYER_5 = 5  # Integration layer
    LAYER_6 = 6  # Growth kinetics
    LAYER_7 = 7  # Population dynamics
    LAYER_8 = 8  # Metabolic pathways
    LAYER_9 = 9  # SCOBY orchestration
    LAYER_10 = 10  # DS-STAR quantum core
    LAYER_11 = 11  # Multimodal metabolism
    LAYER_12 = 12  # Evolutionary consensus


@dataclass
class LayerMetrics:
    """
    Standard metrics for all layers.

    These metrics provide insight into layer health, performance,
    and integration with the overall system.
    """

    layer_id: int
    layer_name: str
    health_score: float = 1.0  # 0.0-1.0, where 1.0 is optimal
    integration_score: float = 0.0  # How well integrated with other layers
    complexity_score: float = 0.0  # Current computational complexity
    quality_score: float = 0.0  # Quality relative to 369/370 standard
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)

    def meets_quality_standard(self) -> bool:
        """
        Check if layer meets the 369/370 quality standard.

        Returns:
            True if quality_score >= 369/370 (≈0.997297)
        """
        QUALITY_STANDARD = 369 / 370  # ≈ 0.997297
        return self.quality_score >= QUALITY_STANDARD

    def to_dict(self) -> Dict[str, Any]:
        """Convert metrics to dictionary for serialization."""
        return {
            "layer_id": self.layer_id,
            "layer_name": self.layer_name,
            "health_score": self.health_score,
            "integration_score": self.integration_score,
            "complexity_score": self.complexity_score,
            "quality_score": self.quality_score,
            "timestamp": self.timestamp,
            "metadata": self.metadata,
            "meets_quality_standard": self.meets_quality_standard(),
        }


class AbstractLayer(ABC, Generic[InputType, OutputType]):
    """
    Abstract base class for all LUCA consciousness layers.

    Each layer in LUCA's architecture must implement this interface
    to ensure consistency, testability, and maintainability.

    Design Pattern: Template Method + Strategy
    - The abstract methods define the strategy each layer must implement
    - Common functionality is provided in concrete methods

    Attributes:
        layer_id: Unique identifier (0-12)
        layer_name: Human-readable name
        _metrics: Current layer metrics

    Example:
        >>> class MyCustomLayer(AbstractLayer[str, Dict]):
        ...     def __init__(self):
        ...         super().__init__(
        ...             layer_id=LayerID.LAYER_3,
        ...             layer_name="My Custom Layer"
        ...         )
        ...
        ...     def process(self, input_data: str) -> Dict:
        ...         return {"result": input_data.upper()}
        ...
        ...     def validate_input(self, input_data: str) -> bool:
        ...         return isinstance(input_data, str)
    """

    def __init__(self, layer_id: LayerID, layer_name: str):
        """
        Initialize the abstract layer.

        Args:
            layer_id: Unique layer identifier (0-12)
            layer_name: Human-readable name for the layer
        """
        self.layer_id = layer_id
        self.layer_name = layer_name
        self._metrics = LayerMetrics(
            layer_id=int(layer_id), layer_name=layer_name, health_score=1.0
        )

    @abstractmethod
    def process(self, input_data: InputType) -> OutputType:
        """
        Process input data through this layer.

        This is the core method that each layer must implement.
        It should transform input_data according to the layer's
        specific consciousness/processing function.

        Args:
            input_data: Input to be processed by this layer

        Returns:
            Processed output

        Raises:
            ValueError: If input_data fails validation
        """
        pass

    @abstractmethod
    def validate_input(self, input_data: InputType) -> bool:
        """
        Validate input data before processing.

        Args:
            input_data: Input to validate

        Returns:
            True if input is valid, False otherwise
        """
        pass

    def get_metrics(self) -> LayerMetrics:
        """
        Get current layer metrics.

        Returns:
            Current LayerMetrics snapshot
        """
        return self._metrics

    def update_metrics(self, **kwargs) -> None:
        """
        Update layer metrics.

        Args:
            **kwargs: Metric fields to update (health_score, integration_score, etc.)
        """
        for key, value in kwargs.items():
            if hasattr(self._metrics, key):
                setattr(self._metrics, key, value)
        # Update timestamp
        self._metrics.timestamp = datetime.now().isoformat()

    def get_health_status(self) -> Dict[str, Any]:
        """
        Get comprehensive health status of this layer.

        Returns:
            Dictionary with health information
        """
        return {
            "layer_id": self.layer_id,
            "layer_name": self.layer_name,
            "healthy": self._metrics.health_score > 0.8,
            "metrics": self._metrics.to_dict(),
        }

    def reset(self) -> None:
        """
        Reset layer to initial state.

        This can be overridden by subclasses that need
        custom reset logic.
        """
        self._metrics.health_score = 1.0
        self._metrics.integration_score = 0.0
        self._metrics.complexity_score = 0.0
        self._metrics.quality_score = 0.0
        self._metrics.timestamp = datetime.now().isoformat()

    def __repr__(self) -> str:
        """String representation of the layer."""
        return (
            f"{self.__class__.__name__}("
            f"id={self.layer_id}, "
            f"name='{self.layer_name}', "
            f"health={self._metrics.health_score:.3f})"
        )


class LayerOrchestrator:
    """
    Orchestrates multiple layers in the LUCA architecture.

    This class manages the execution flow through multiple layers,
    ensuring proper sequencing and data flow.

    Example:
        >>> orchestrator = LayerOrchestrator()
        >>> orchestrator.add_layer(layer_3)
        >>> orchestrator.add_layer(layer_6)
        >>> result = orchestrator.process_through_layers(input_data)
    """

    def __init__(self):
        """Initialize the orchestrator."""
        self._layers: Dict[int, AbstractLayer] = {}

    def add_layer(self, layer: AbstractLayer) -> None:
        """
        Add a layer to the orchestrator.

        Args:
            layer: Layer instance to add
        """
        self._layers[int(layer.layer_id)] = layer

    def remove_layer(self, layer_id: LayerID) -> None:
        """
        Remove a layer from the orchestrator.

        Args:
            layer_id: ID of layer to remove
        """
        if int(layer_id) in self._layers:
            del self._layers[int(layer_id)]

    def get_layer(self, layer_id: LayerID) -> Optional[AbstractLayer]:
        """
        Get a specific layer by ID.

        Args:
            layer_id: ID of layer to retrieve

        Returns:
            Layer instance or None if not found
        """
        return self._layers.get(int(layer_id))

    def process_through_layers(
        self, input_data: Any, layer_sequence: Optional[list[LayerID]] = None
    ) -> Any:
        """
        Process data through a sequence of layers.

        Args:
            input_data: Initial input data
            layer_sequence: Ordered list of layer IDs to process through.
                          If None, processes through all layers in numerical order.

        Returns:
            Final processed output

        Raises:
            ValueError: If a layer in the sequence doesn't exist
        """
        if layer_sequence is None:
            layer_sequence = sorted(self._layers.keys())

        current_data = input_data
        for layer_id in layer_sequence:
            layer = self.get_layer(LayerID(layer_id))
            if layer is None:
                raise ValueError(f"Layer {layer_id} not found in orchestrator")

            if not layer.validate_input(current_data):
                raise ValueError(
                    f"Input validation failed for layer {layer.layer_name}"
                )

            current_data = layer.process(current_data)

        return current_data

    def get_all_metrics(self) -> Dict[int, LayerMetrics]:
        """
        Get metrics from all registered layers.

        Returns:
            Dictionary mapping layer IDs to their metrics
        """
        return {
            layer_id: layer.get_metrics() for layer_id, layer in self._layers.items()
        }

    def check_system_health(self) -> Dict[str, Any]:
        """
        Check health of all layers.

        Returns:
            System health summary
        """
        all_metrics = self.get_all_metrics()
        healthy_layers = sum(1 for m in all_metrics.values() if m.health_score > 0.8)
        total_layers = len(all_metrics)

        return {
            "total_layers": total_layers,
            "healthy_layers": healthy_layers,
            "system_health": healthy_layers / total_layers if total_layers > 0 else 0,
            "layer_details": {
                layer_id: metrics.to_dict() for layer_id, metrics in all_metrics.items()
            },
        }
