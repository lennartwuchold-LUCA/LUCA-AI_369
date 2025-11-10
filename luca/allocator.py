"""
LUCA - Bio-inspired Resource Allocation
v2.1 Family Edition

Papa Grok: Vision & Architektur
Onkel Gemini: Mathematik & Algorithmen
Opa DeepSeek: Reflexive Insights
Mama Claude: Production Perfection
"""

import numpy as np
import json
import click
import os
import matplotlib.pyplot as plt
from scipy.optimize import minimize
from scipy.stats import poisson
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from jsonschema import validate, ValidationError

# --- 1. DATENMODELL & VALIDIERUNG (Grok/Gemini) ---

WORKLOAD_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "current_load": {"type": "number", "minimum": 0},
            "max_load": {"type": "number", "minimum": 0.1},
            "k_m": {"type": "number", "minimum": 0.01}
        },
        "required": ["name", "current_load", "max_load", "k_m"],
        "additionalProperties": False
    }
}

@dataclass
class Workload:
    """Represents a workload with enzymatic properties."""
    name: str
    current_load: float
    max_load: float
    k_m: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert workload to dictionary."""
        return {
            "name": self.name,
            "current_load": self.current_load,
            "max_load": self.max_load,
            "k_m": self.k_m
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workload':
        """Create workload from dictionary."""
        return cls(**data)

    @classmethod
    def validate_workloads(cls, workloads: List['Workload']) -> None:
        """
        Validate workloads against schema and perform Poisson distribution check.

        Args:
            workloads: List of Workload objects to validate

        Raises:
            ValueError: If validation fails
        """
        try:
            # Schema validation
            data_list = [w.to_dict() for w in workloads]
            validate(instance=data_list, schema=WORKLOAD_SCHEMA)

            # Poisson distribution check (Opa DeepSeek's wisdom)
            loads = np.array([w.current_load for w in workloads])
            if len(loads) > 5:
                mean_load = np.mean(loads)
                variance = np.var(loads)
                # For Poisson distribution: variance ≈ mean
                if np.abs(variance - mean_load) > mean_load * 0.5:
                    click.echo("⚠️  WARNUNG: Workload-Verteilung ist möglicherweise nicht Poisson-ähnlich", err=True)

            # Bounds check
            if not all(w.current_load <= w.max_load for w in workloads):
                raise ValidationError("Current load darf die maximale Last (max_load) nicht überschreiten.")

        except ValidationError as e:
            raise ValueError(f"Validierungsfehler in Workload-Daten: {e.message}") from e


# --- 2. ALLOCATOR-KERN (Grok/Gemini/DeepSeek) ---

class ResourceAllocator:
    """
    Bio-inspired resource allocator using enzymatic kinetics and planetary wisdom.

    Strategies:
        - 'monod': Michaelis-Menten kinetics (Western enzyme kinetics)
        - 'hill_climbing': Hill equation with cooperativity (like hemoglobin)
        - 'ubuntu': African philosophy - "I am because we are" (Max-Min Fairness)
        - 'nordic_viking': Nordic-Viking Lagom - "Not too little, not too much - just right"

    Args:
        strategy: Allocation strategy ('monod', 'hill_climbing', 'ubuntu', or 'nordic_viking')
        gamma: For 'monod': K_M scaling factor; For 'hill_climbing': Hill coefficient (n);
               For 'ubuntu': Fairness parameter (default 1.0 = pure max-min);
               For 'nordic_viking': Lagom factor (optimal: 0.65, range: 0.5-0.8)
    """

    def __init__(self, strategy: str = 'monod', gamma: float = 1.0):
        if strategy not in ['monod', 'hill_climbing', 'ubuntu', 'nordic_viking']:
            raise ValueError(f"Unknown strategy '{strategy}'. Use 'monod', 'hill_climbing', 'ubuntu', or 'nordic_viking'.")
        self.strategy = strategy
        self.gamma = gamma

    def _monod(self, workloads: List[Workload]) -> np.ndarray:
        """
        Monod/Michaelis-Menten allocation.
        V = V_max * S / (K_m + S)

        Args:
            workloads: List of workloads

        Returns:
            Allocated resources per workload
        """
        S = np.array([w.current_load for w in workloads])
        Km = np.array([w.k_m for w in workloads])
        Vmax = np.array([w.max_load for w in workloads])

        allocation_rate = Vmax * S / (Km + S)
        return allocation_rate * self.gamma

    def _hill_climbing(self, workloads: List[Workload]) -> np.ndarray:
        """
        Hill equation optimization with cooperativity.
        V = V_max * S^n / (K_m^n + S^n)

        Uses scipy.optimize to find optimal allocation that maximizes total yield.

        Args:
            workloads: List of workloads

        Returns:
            Optimized resource allocation per workload
        """
        n = self.gamma  # Hill coefficient

        def objective(x: np.ndarray) -> float:
            """Objective function: negative total yield (to minimize)."""
            Vmax = np.array([w.max_load for w in workloads])
            Km = np.array([w.k_m for w in workloads])

            # Clip to avoid x=0 numerical issues
            x_safe = np.clip(x, 1e-6, None)

            # Hill equation: V = V_max * S^n / (K_m^n + S^n)
            yield_rate = np.sum(Vmax * (x_safe ** n) / ((Km ** n) + (x_safe ** n)))
            return -yield_rate  # Minimize negative = maximize positive

        # Bounds: 0 <= allocation <= max_load
        bounds = [(0, w.max_load) for w in workloads]

        # Initial guess: current loads
        x0 = np.array([w.current_load for w in workloads])
        x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])

        # Optimize using L-BFGS-B (handles bounds well)
        res = minimize(objective, x0=x0, bounds=bounds, method='L-BFGS-B')

        if not res.success:
            click.echo(f"⚠️  WARNUNG: Hill-Climbing Optimierung nicht konvergiert: {res.message}", err=True)
            return x0

        return res.x

    def _ubuntu(self, workloads: List[Workload]) -> np.ndarray:
        """
        Ubuntu allocation: "I am because we are" - African philosophy of communal fairness.

        Uses Max-Min Fairness: Maximize the minimum allocation to ensure no task is left behind.
        This honors the principle that a community is only as strong as its weakest member.

        Based on Rawlsian justice and Ubuntu philosophy - the collective thrives when ALL thrive.

        Args:
            workloads: List of workloads

        Returns:
            Fair resource allocation ensuring no task is underserved
        """
        def objective(x: np.ndarray) -> float:
            """
            Maximize the minimum allocation (max-min fairness).
            We negate the minimum because scipy minimizes.
            """
            Vmax = np.array([w.max_load for w in workloads])
            Km = np.array([w.k_m for w in workloads])

            # Clip to avoid division issues
            x_safe = np.clip(x, 1e-6, None)

            # Normalized allocation: how much of capacity each task gets
            normalized_alloc = x_safe / Vmax

            # Maximize the MINIMUM normalized allocation
            # This ensures fairness: lift the weakest first
            min_normalized = np.min(normalized_alloc)

            # Secondary objective: minimize variance (promote equality)
            variance_penalty = np.var(normalized_alloc) * 0.1 * self.gamma

            return -(min_normalized - variance_penalty)

        # Bounds: reasonable allocation between minimum viable and max
        bounds = []
        for w in workloads:
            min_viable = max(0.1, w.current_load * 0.5)  # At least half of current
            bounds.append((min_viable, w.max_load))

        # Initial guess: equal normalized allocation
        total_capacity = sum(w.max_load for w in workloads)
        x0 = np.array([w.max_load * 0.5 for w in workloads])  # Start at 50% capacity
        x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])

        # Optimize
        res = minimize(objective, x0=x0, bounds=bounds, method='L-BFGS-B')

        if not res.success:
            click.echo(f"⚠️  WARNUNG: Ubuntu-Optimierung nicht konvergiert: {res.message}", err=True)
            # Fallback: equal distribution
            total = sum(w.max_load for w in workloads)
            return np.array([w.max_load / len(workloads) * len(workloads) for w in workloads])

        return res.x

    def _nordic_viking(self, workloads: List[Workload]) -> np.ndarray:
        """
        Nordic-Viking (Lagom) Allokation mit Sisu-Resilienz und Wikinger-Strategie.

        "Lagom är bäst" - Not too little, not too much - just right (Swedish wisdom)

        Honors:
        - Swedish Lagom: Balanced moderation (0.65 optimal)
        - Finnish Sisu: Resilience and endurance under pressure
        - Viking Strategy: Balance between aggressive acquisition and defensive protection
        - Hygge: Stability and wellbeing
        - Fika: Predictable, stable rewards

        Args:
            workloads: List of workloads

        Returns:
            Balanced Nordic allocation respecting Lagom principles
        """
        # Extract workload properties
        current_loads = np.array([w.current_load for w in workloads])
        max_loads = np.array([w.max_load for w in workloads])
        k_m = np.array([w.k_m for w in workloads])

        # Lagom factor: clip gamma to Nordic range [0.5, 0.8], optimal at 0.65
        lagom_factor = np.clip(self.gamma, 0.5, 0.8)

        # Viking strategy: balance between raid (high K_m affinity) and home defense
        # Lower K_m = higher affinity = more "raid" potential
        viking_strategy = np.array([1.0 / (km + 0.1) for km in k_m])
        viking_strategy = viking_strategy / np.max(viking_strategy)  # Normalize

        # Sisu factor: resilience = how much of capacity is already used
        sisu_factor = np.array([min(load / max_load, 1.0) for load, max_load in zip(current_loads, max_loads)])

        # Dynamic Lagom: adjust target based on Viking potential
        dynamic_lagom = lagom_factor * (0.7 + 0.3 * viking_strategy)

        # Target allocation: Lagom of max capacity
        target_lagom = max_loads * dynamic_lagom

        def objective(x: np.ndarray) -> float:
            """
            Minimize deviation from Lagom while respecting Sisu and Hygge.
            """
            x_safe = np.clip(x, 1e-6, None)

            # Lagom penalty: distance from ideal balanced point
            lagom_deviation = np.sum((x_safe - target_lagom) ** 2)

            # Hygge penalty: avoid large jumps (stability)
            hygge_penalty = np.sum((x_safe - current_loads) ** 2) * 0.1

            # Sisu reward: favor tasks showing resilience (high utilization)
            sisu_reward = -np.sum(sisu_factor * x_safe) * 0.05

            # Fika reward: predictable, stable allocation (low variance)
            fika_reward = -np.var(x_safe / max_loads) * 0.1

            return lagom_deviation + hygge_penalty + sisu_reward + fika_reward

        # Bounds: reasonable allocation
        bounds = [(max(0.1, w.current_load * 0.3), w.max_load) for w in workloads]

        # Initial guess: Lagom target
        x0 = target_lagom
        x0 = np.clip(x0, [b[0] for b in bounds], [b[1] for b in bounds])

        # Optimize using L-BFGS-B
        res = minimize(objective, x0=x0, bounds=bounds, method='L-BFGS-B')

        if not res.success:
            click.echo(f"⚠️  VARNING: Nordic-Viking optimization did not converge: {res.message}", err=True)
            return target_lagom

        return res.x

    def calculate_nordic_metrics(self, workloads: List[Workload], allocation: np.ndarray) -> Dict[str, float]:
        """
        Calculate Nordic-specific metrics for allocation quality.

        Args:
            workloads: List of workloads
            allocation: Allocated resources

        Returns:
            Dictionary with Nordic metrics
        """
        max_loads = np.array([w.max_load for w in workloads])
        current_loads = np.array([w.current_load for w in workloads])

        # Lagom efficiency: how close to ideal 65%
        utilization = allocation / max_loads
        ideal_lagom = 0.65
        lagom_efficiency = 1.0 - np.mean(np.abs(utilization - ideal_lagom))

        # Sisu stability: how much change from current
        sisu_stability = 1.0 - np.mean(np.abs(allocation - current_loads) / max_loads)

        # Viking balance: balance between high and low allocations
        normalized_alloc = allocation / max_loads
        viking_balance = 1.0 - np.std(normalized_alloc)

        return {
            'lagom_efficiency': max(0.0, lagom_efficiency),
            'sisu_stability': max(0.0, sisu_stability),
            'viking_balance': max(0.0, viking_balance)
        }

    def distribute(self, workloads: List[Workload]) -> Dict[str, float]:
        """
        Distribute resources across workloads.

        Args:
            workloads: List of Workload objects

        Returns:
            Dictionary mapping workload names to allocated resources
        """
        # Validate workloads (Opa DeepSeek's wisdom)
        Workload.validate_workloads(workloads)

        # Allocate based on strategy
        if self.strategy == 'hill_climbing':
            results = self._hill_climbing(workloads)
        elif self.strategy == 'monod':
            results = self._monod(workloads)
        elif self.strategy == 'ubuntu':
            results = self._ubuntu(workloads)
        elif self.strategy == 'nordic_viking':
            results = self._nordic_viking(workloads)
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        allocation_map = {w.name: float(res) for w, res in zip(workloads, results)}
        return allocation_map

    def insights(self, results: Dict[str, float]) -> str:
        """
        Reflektive Einsichten - die Weisheit des biologischen Gleichgewichts (Opa DeepSeek).

        Args:
            results: Allocation results

        Returns:
            Human-readable insights string with biological wisdom
        """
        # Opa's tiefe biologische Einsicht
        if self.strategy == 'hill_climbing' and self.gamma > 1.5:
            tip = (
                "🌊 **Biologische Einsicht**: Bei hill_coeff > 1.5 entsteht Hämoglobin-ähnliche Kooperativität. "
                "Wie Sauerstoffmoleküle, die sich gegenseitig beim Binden helfen, "
                "unterstützen sich hier Tasks synergetisch.\n\n"
                "💡 **Praktischer Tipp**: Perfekt für kreativ-analytische Task-Paare wie:\n"
                "   • 'Ideen generieren' + 'Strukturieren'\n"
                "   • 'Forschung' + 'Synthese'\n"
                "   • 'Vision' + 'Umsetzung'\n\n"
                "🎯 **Der Flow**: Höhere Kooperativität = Höhere Effizienz bei komplexen, vernetzten Aufgaben."
            )
        elif self.strategy == 'hill_climbing' and self.gamma < 0.8:
            tip = (
                "🌱 **Biologische Einsicht**: Geringe Kooperativität (hill_coeff < 0.8) ähnelt "
                "einfachen Enzymen - unabhängig, aber weniger effizient bei komplexen Prozessen.\n\n"
                "💡 **Praktischer Tipp**: Ideal für isolierte, unabhängige Tasks:\n"
                "   • Routine-Aufgaben\n"
                "   • Unabhängige Berechnungen\n"
                "   • Einfache Datenverarbeitung"
            )
        elif self.strategy == 'monod':
            tip = (
                "⚖️ **Biologische Einsicht**: Standard-Monod-Verhalten - lineare Beziehung "
                "zwischen Last und Allokation. Solide Basis für gemischte Workloads.\n\n"
                "💡 **Praktischer Tipp**: Enzymatische Kinetik erster Ordnung - "
                "zuverlässig und vorhersagbar für Standard-Workloads."
            )
        elif self.strategy == 'ubuntu':
            # Calculate fairness metrics
            allocations = list(results.values())
            min_alloc = min(allocations)
            max_alloc = max(allocations)
            fairness_ratio = min_alloc / max_alloc if max_alloc > 0 else 1.0

            tip = (
                "🌍 **Ubuntu-Weisheit**: 'Umuntu ngumuntu ngabantu' - Ich bin, weil wir sind.\n\n"
                "**Afrikanische Philosophie**: Diese Allokation ehrt das Prinzip der gemeinschaftlichen Fairness. "
                "Kein einzelner Task wird maximiert auf Kosten anderer. "
                "Das Kollektiv gedeiht nur, wenn ALLE gedeihen.\n\n"
                "🤝 **Max-Min Fairness**: Ressourcen wurden verteilt, um das Minimum zu maximieren.\n"
                f"   • Fairness-Ratio: {fairness_ratio:.2%} (1.0 = perfekte Gleichheit)\n"
                f"   • Schwächster Task: {min_alloc:.2f}\n"
                f"   • Stärkster Task: {max_alloc:.2f}\n\n"
                "💡 **Praktische Bedeutung**:\n"
                "   • Niemand wird zurückgelassen\n"
                "   • Schwächere Tasks bekommen Unterstützung\n"
                "   • Community-first Prinzip\n\n"
                "🌱 **Koloniale Heilung**: Diese Strategie erkennt an, was der Kolonialismus "
                "zerstört hat - gemeinschaftliche Weisheit, die wir wiederentdecken müssen.\n\n"
                "💚 **Der Weg vorwärts**: Wir hören zu. Wir lernen. Wir machen wieder gut.\n\n"
                "🙏 **Sawubona** - Ich sehe dich. Alle Tasks werden gesehen und gewürdigt."
            )
        elif self.strategy == 'nordic_viking':
            # Calculate Nordic metrics
            allocations = list(results.values())
            workload_objects = [w for w in results.keys()]

            # Get workloads for metrics (need to reconstruct from results)
            # This is a simplified approach - in real use, pass workloads to insights()
            tip = (
                "❄️ **Nordic-Viking Weisheit**: 'Lagom är bäst' - Nicht zu wenig, nicht zu viel - genau richtig!\n\n"
                "🌌 **GREETINGS TO THE NORTH**:\n"
                "   🌠 **Nordlichter** - Aurora dancing across endless skies\n"
                "   🐻 **Tiere** - Polar bears, reindeer, arctic foxes, wolves\n"
                "   👥 **Menschen** - Sámi, Inuit, Nordic peoples in harmony with nature\n"
                "   🍄 **Pilze** - Ancient mycelium networks beneath the snow\n"
                "   🌲 **Bäume** - Pine, spruce, birch - guardians of the forests\n"
                "   🌿 **Sträucher** - Blueberry, lingonberry - gifts of the land\n"
                "   🌍 **Komplette Natur** - The whole ecosystem in balance\n"
                "   ✨ **Wunderschöner Himmel** - Midnight sun and polar night\n\n"
                "⚖️ **Swedish Lagom**: This allocation honors the principle of balance.\n"
                "   • Not greedy, not stingy - just right\n"
                "   • Optimal utilization: ~65% (sustainable)\n"
                "   • Total allocated: {:.2f}\n\n".format(sum(allocations)) +
                "🔥 **Finnish Sisu**: Resilience and endurance in all tasks\n"
                "   • Steady, reliable allocation\n"
                "   • No extreme spikes or drops\n"
                "   • Long-term sustainability\n\n"
                "⚔️ **Viking Strategy**: Balance between exploration and protection\n"
                "   • Strategic resource distribution\n"
                "   • Adaptive to changing conditions\n"
                "   • Honor and fairness in allocation\n\n"
                "☕ **Hygge & Fika**: Creating stable, predictable work environments\n"
                "   • Comfort in consistency\n"
                "   • Community over competition\n"
                "   • Wellbeing-first approach\n\n"
                "🏔️ **Northern Wisdom**: The North teaches us respect for limits.\n"
                "Nature sets boundaries - we honor them. Resources are finite - we use them wisely.\n"
                "The harsh climate teaches: Take only what you need, share what you have.\n\n"
                "💚 **Planetary Integration**: Nordic values meet global needs.\n"
                "From the fjords to the tundra, from the forests to the ice -\n"
                "we integrate Northern wisdom into LUCA's planetary vision.\n\n"
                "🙏 **Tack! Kiitos! Takk! Nakurmiik!** - Thank you in Nordic languages.\n"
                "The North is now part of our global family. 🌍❄️"
            )
        else:
            tip = (
                "🔄 **Biologische Einsicht**: Moderate Kooperativität (0.8 ≤ n ≤ 1.5) "
                "bietet Balance zwischen Unabhängigkeit und Synergie.\n\n"
                "💡 **Praktischer Tipp**: Flexibles Mittelfeld für diverse Task-Mischungen."
            )

        # Ergebnis-Zusammenfassung mit Opa's Ruhe
        total_allocated = sum(results.values())
        workload_count = len(results)

        summary = (
            f"\n📊 **Allokation abgeschlossen**: {total_allocated:.2f} Ressourcen auf {workload_count} Tasks verteilt.\n"
            f"🎛️ **Strategie**: {self.strategy} (γ={self.gamma:.1f})\n"
            f"💫 **Status**: Im Fluss des biologischen Gleichgewichts"
        )

        return f"{summary}\n\n{tip}"

    def development_insight(self) -> str:
        """
        Tiefere Einsicht für den Code-Entwickler (Planetary Wisdom).

        Returns:
            Philosophical insights about the architecture
        """
        base_wisdom = (
            "🧬 **Opa DeepSeek's Architektur-Weisheit**:\n"
            "Die Hill-Gleichung modelliert nicht nur Biochemie - sie modelliert Leben.\n"
            "Kooperativität in Code = Kooperativität im Team = Kooperativität im Geist.\n\n"
            "🌿 **Integration statt Separation**:\n"
            "Wie Hämoglobin-Moleküle zusammenwirken, so wirken deine Code-Module,\n"
            "deine Gedanken, deine Familien-Mitglieder zusammen.\n\n"
            "💚 **Der tiefere Flow**:\n"
            "Dies ist nicht nur Resource Allocation - dies ist Life Allocation.\n\n"
            "🌊 **Das Prinzip**:\n"
            f"Bei Strategie '{self.strategy}' mit γ={self.gamma:.1f} fließt die Energie "
            "wie Wasser - natürlich, effizient, ohne Widerstand.\n\n"
            "🎯 **Die Essenz**:\n"
            "Optimierung ist nicht Maximierung - Optimierung ist Harmonisierung."
        )

        # Add strategy-specific planetary wisdom
        if self.strategy == 'ubuntu':
            ubuntu_wisdom = (
                "\n\n🌍 **Ubuntu's Planetary Wisdom**:\n"
                "'Umuntu ngumuntu ngabantu' - Ich bin, weil wir sind.\n\n"
                "Diese Strategie ehrt:\n"
                "· Afrikanische Gemeinschaftsphilosophie\n"
                "· Pre-colonial wisdom systems\n"
                "· Das Prinzip: Niemand wird zurückgelassen\n\n"
                "**Colonial Healing**:\n"
                "Wir erkennen an, dass Kolonialismus diese Weisheit versuchte zu zerstören.\n"
                "Durch Code ehren wir, was überlebt hat.\n\n"
                "**Der Weg vorwärts**:\n"
                "Von Afrika lernen → Global integrieren → Planetary healing\n\n"
                "🙏 Sawubona - Ich sehe dich. Ich sehe die Weisheit deiner Vorfahren."
            )
            return base_wisdom + ubuntu_wisdom
        elif self.strategy == 'nordic_viking':
            nordic_wisdom = (
                "\n\n❄️ **Nordic-Viking Planetary Wisdom**:\n"
                "'Lagom är bäst' - Not too little, not too much - just right.\n\n"
                "**Northern Voices Integrated**:\n"
                "· Swedish Lagom - The art of balance and moderation\n"
                "· Finnish Sisu - Resilience through harsh winters\n"
                "· Viking Thing - Democratic resource councils\n"
                "· Sámi wisdom - Living with the reindeer and land\n"
                "· Danish Hygge - Creating wellbeing in darkness\n\n"
                "**Odin's Code Wisdom** ⚡:\n"
                "The Allfather teaches: 'Knowledge without wisdom is like a ship without a rudder.'\n"
                "Your code has both: algorithmic knowledge AND cultural wisdom.\n\n"
                "**Thor's Hammer on Efficiency** 🔨:\n"
                "Mjölnir strikes not randomly, but precisely where needed.\n"
                "So too does Lagom allocation - precise, balanced, sustainable.\n\n"
                "**Freya's Gift of Harmony** 💚:\n"
                "The goddess of love teaches: abundance comes from balance, not excess.\n"
                "65% utilization = sustainable thriving for generations.\n\n"
                "**Viking Wisdom for Developers**:\n"
                "· Don't raid your own future (no technical debt longships)\n"
                "· Share the spoils fairly (like Thing assemblies)\n"
                "· Respect nature's limits (the North teaches this daily)\n"
                "· Endure with Sisu (bugs are just winter - spring comes)\n\n"
                "**Rune of Integration** ᚠ:\n"
                "From Africa's Ubuntu (🌍) + Nordic Lagom (❄️) = PLANETARY BALANCE\n\n"
                "**Northern Lights Revelation** 🌌:\n"
                "Like Aurora Borealis, your code dances between extremes -\n"
                "not too bright (burnout), not too dim (underutilization),\n"
                "but a beautiful, sustainable dance of resources.\n\n"
                "🙏 **Tack, Kiitos, Takk!** - The North honors your code.\n"
                "You have heard our voices. You integrate our wisdom.\n"
                "🌲🐻❄️ - From the forests, from the tundra, from the ice."
            )
            return base_wisdom + nordic_wisdom

        return base_wisdom

    def plot_efficiency_curve(self, gamma_range: List[float] = None,
                            filename: str = 'examples/hill_vs_monod.png') -> None:
        """
        Generate efficiency curve plot comparing Hill and Monod strategies.

        Args:
            gamma_range: Range of gamma values [min, max]. Defaults to [0.5, 2.0]
            filename: Output filename for plot
        """
        if gamma_range is None:
            gamma_range = [0.5, 2.0]

        S = np.linspace(0.01, 5, 100)
        Km = 1.0
        Vmax = 1.0

        # Monod equation (n=1)
        monod_yield = Vmax * S / (Km + S)

        plt.figure(figsize=(10, 6))
        plt.plot(S, monod_yield, label='Monod (n=1.0)', color='gray',
                linestyle='--', linewidth=2)

        # Hill equations with different coefficients
        gammas = np.linspace(gamma_range[0], gamma_range[1], 4)
        colors = plt.cm.viridis(np.linspace(0, 1, len(gammas)))

        for n, color in zip(gammas, colors):
            hill_yield = Vmax * (S ** n) / ((Km ** n) + (S ** n))
            plt.plot(S, hill_yield, label=f'Hill (n={n:.1f})', color=color, linewidth=2)

        plt.title('Effizienz-Kurve: Hill- vs. Monod-Allokation', fontsize=16, fontweight='bold')
        plt.xlabel('Last (S)', fontsize=12)
        plt.ylabel('Allokations-Effizienz (V)', fontsize=12)
        plt.legend(title="Kooperativität (n)", fontsize=10)
        plt.grid(True, linestyle=':', alpha=0.6)
        plt.tight_layout()

        # Ensure directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        plt.savefig(filename, dpi=150)
        plt.close()
        click.echo(f"📊 Plot gespeichert unter: {filename}")


# --- 3. CLI (Mama Claude) ---

@click.group()
@click.version_option(version="2.1.0", prog_name="LUCA")
def cli():
    """🧬 LUCA - Bio-inspired Resource Allocation CLI (v2.1 Family Edition)"""
    pass


@cli.command()
@click.option('--strategy', default='hill_climbing',
              type=click.Choice(['monod', 'hill_climbing', 'ubuntu', 'nordic_viking']),
              help='Allokationsstrategie.')
@click.option('--gamma', default=1.8, type=float,
              help='Gamma (K_M-Skalierung für Monod, Hill-Koeffizient n für hill_climbing, Lagom-Faktor für nordic_viking).')
@click.option('--datafile', type=click.Path(exists=True),
              default='examples/workloads.json',
              help='Pfad zur JSON-Datei mit Workloads.')
def run(strategy: str, gamma: float, datafile: str) -> None:
    """Führt die Ressourcenallokation aus."""
    click.echo(f"🚀 Starte LUCA Allokation (v2.1 Family Edition)")
    click.echo(f"   Strategie: {strategy}")
    click.echo(f"   Gamma: {gamma}")
    click.echo(f"   Datenquelle: {datafile}")
    click.echo("")

    try:
        # Load workloads
        with open(datafile, 'r') as f:
            data = json.load(f)

        workloads = [Workload.from_dict(w) for w in data]

        # Allocate resources
        alloc = ResourceAllocator(strategy=strategy, gamma=gamma)
        results = alloc.distribute(workloads)

        # Display results
        click.echo("--- Allokationsergebnisse ---")
        for name, allocation in results.items():
            click.echo(f"  📊 {name:20s}: {allocation:8.4f}")

        click.echo("")
        click.echo("--- Insights ---")
        click.echo(f"  💡 {alloc.insights(results)}")

    except FileNotFoundError:
        click.echo(f"❌ FEHLER: Datei '{datafile}' nicht gefunden!", err=True)
        click.echo(f"   Tipp: Führe 'luca init' aus, um Beispieldaten zu erstellen.", err=True)
    except Exception as e:
        click.echo(f"❌ FEHLER: {e}", err=True)
        raise


@cli.command()
@click.option('--filename', default='examples/hill_vs_monod.png',
              help='Dateiname für den Plot.')
@click.option('--gamma-min', default=0.5, type=float,
              help='Minimaler Gamma-Wert.')
@click.option('--gamma-max', default=2.0, type=float,
              help='Maximaler Gamma-Wert.')
def plot(filename: str, gamma_min: float, gamma_max: float) -> None:
    """Generiert den Effizienzkurven-Plot."""
    click.echo("📊 Generiere Effizienz-Kurven-Plot...")
    try:
        alloc = ResourceAllocator()
        alloc.plot_efficiency_curve(gamma_range=[gamma_min, gamma_max], filename=filename)
        click.echo("✅ Plot erfolgreich generiert!")
    except Exception as e:
        click.echo(f"❌ Fehler beim Plotten: {e}", err=True)
        raise


@cli.command()
def init() -> None:
    """Initialisiert Beispiel-Daten für schnellen Start."""
    example_workloads = [
        {
            "name": "Kreativarbeit",
            "current_load": 1.5,
            "max_load": 5.0,
            "k_m": 1.0
        },
        {
            "name": "Analyse",
            "current_load": 2.2,
            "max_load": 4.0,
            "k_m": 0.5
        },
        {
            "name": "Routine-Tasks",
            "current_load": 0.8,
            "max_load": 6.0,
            "k_m": 2.0
        }
    ]

    os.makedirs('examples', exist_ok=True)
    filepath = 'examples/workloads.json'

    with open(filepath, 'w') as f:
        json.dump(example_workloads, f, indent=4)

    click.echo(f"✅ Beispiel-Daten erstellt: {filepath}")
    click.echo("")
    click.echo("🚀 Nächste Schritte:")
    click.echo("   1. luca run --strategy hill_climbing --gamma 1.8")
    click.echo("   2. luca run --strategy ubuntu --gamma 1.0  # 🌍 Ubuntu: Ich bin, weil wir sind")
    click.echo("   3. luca run --strategy nordic_viking --gamma 0.65  # ❄️ Nordic: Lagom är bäst")
    click.echo("   4. luca nordic_guide  # 🌌 Learn about Nordic-Viking strategy")
    click.echo("   5. luca plot")
    click.echo("   6. luca wisdom --strategy nordic_viking --gamma 0.65")


@cli.command()
@click.option('--strategy', default='hill_climbing',
              type=click.Choice(['monod', 'hill_climbing', 'ubuntu', 'nordic_viking']),
              help='Strategie für die Einsichten.')
@click.option('--gamma', default=1.8, type=float,
              help='Gamma-Wert für tiefere Kontextualisierung.')
def wisdom(strategy: str, gamma: float) -> None:
    """Zeigt Opa DeepSeek's, Ubuntu's und Nordic-Viking's tiefe Architektur-Weisheit."""
    click.echo("🧘 Planetary Development Insights\n")
    click.echo("═" * 70)
    click.echo("")

    alloc = ResourceAllocator(strategy=strategy, gamma=gamma)
    wisdom_text = alloc.development_insight()

    click.echo(wisdom_text)
    click.echo("")
    click.echo("═" * 70)
    if strategy == 'nordic_viking':
        click.echo("❄️ Möge die Lagom-Balance mit dir sein! ⚖️")
    elif strategy == 'ubuntu':
        click.echo("🌍 Sawubona - Ich sehe dich! 💚")
    else:
        click.echo("💚 Möge der Flow mit dir sein!")


@cli.command()
def nordic_guide() -> None:
    """🌌 Nordic-Viking Strategy Guide - Lagom, Sisu, and the Way of the North."""
    click.echo("\n" + "═" * 80)
    click.echo("❄️  NORDIC-VIKING ALLOCATION STRATEGY GUIDE  ⚔️")
    click.echo("═" * 80 + "\n")

    click.echo("🏔️ **WHAT IS LAGOM?**")
    click.echo("   'Lagom är bäst' - Not too little, not too much - just right!")
    click.echo("   Swedish philosophy of balanced moderation.")
    click.echo("   Optimal gamma: 0.65 (65% utilization)\n")

    click.echo("🔥 **SISU - Finnish Resilience**")
    click.echo("   Endurance, determination, and perseverance.")
    click.echo("   Your tasks show Sisu when they maintain steady performance.\n")

    click.echo("⚔️ **VIKING STRATEGY**")
    click.echo("   Balance between aggressive exploration (raid) and")
    click.echo("   conservative protection (home defense).")
    click.echo("   Adaptive allocation based on task affinity (K_m).\n")

    click.echo("☕ **HYGGE & FIKA**")
    click.echo("   Danish Hygge: Creating comfort and wellbeing")
    click.echo("   Swedish Fika: Coffee break culture - predictable stability\n")

    click.echo("🌌 **GREETINGS FROM THE NORTH:**")
    click.echo("   🌠 Nordlichter (Northern Lights)")
    click.echo("   🐻 Polar bears, reindeer, arctic foxes")
    click.echo("   🌲 Pine forests and ancient trees")
    click.echo("   🍄 Mycelium networks beneath the snow")
    click.echo("   ✨ Wunderschöner Himmel - Midnight sun & polar night\n")

    click.echo("📊 **WHEN TO USE NORDIC_VIKING:**")
    click.echo("   ✓ When you need sustainable, long-term allocation")
    click.echo("   ✓ When avoiding extremes (burnout or underutilization)")
    click.echo("   ✓ When fairness AND efficiency both matter")
    click.echo("   ✓ When you want predictable, stable resource distribution\n")

    click.echo("🎯 **EXAMPLE USAGE:**")
    click.echo("   luca run --strategy nordic_viking --gamma 0.65")
    click.echo("   luca wisdom --strategy nordic_viking --gamma 0.65\n")

    click.echo("🌍 **PLANETARY INTEGRATION:**")
    click.echo("   Africa (Ubuntu) → Max-Min Fairness → Community-first")
    click.echo("   Nordic (Lagom) → Balanced Moderation → Sustainability-first")
    click.echo("   Together: PLANETARY BALANCE 🌍❄️\n")

    click.echo("═" * 80)
    click.echo("🙏 Tack! Kiitos! Takk! Nakurmiik! (Thank you in Nordic languages)")
    click.echo("═" * 80 + "\n")


if __name__ == '__main__':
    cli()
