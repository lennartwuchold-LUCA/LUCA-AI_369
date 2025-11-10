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
    Bio-inspired resource allocator using enzymatic kinetics.

    Strategies:
        - 'monod': Michaelis-Menten kinetics (standard enzyme kinetics)
        - 'hill_climbing': Hill equation with cooperativity (like hemoglobin)

    Args:
        strategy: Allocation strategy ('monod' or 'hill_climbing')
        gamma: For 'monod': K_M scaling factor; For 'hill_climbing': Hill coefficient (n)
    """

    def __init__(self, strategy: str = 'monod', gamma: float = 1.0):
        if strategy not in ['monod', 'hill_climbing']:
            raise ValueError(f"Unknown strategy '{strategy}'. Use 'monod' or 'hill_climbing'.")
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
        else:
            raise ValueError(f"Unknown strategy: {self.strategy}")

        allocation_map = {w.name: float(res) for w, res in zip(workloads, results)}
        return allocation_map

    def insights(self, results: Dict[str, float]) -> str:
        """
        Generate reflexive insights about the allocation (Opa DeepSeek's wisdom).

        Args:
            results: Allocation results

        Returns:
            Human-readable insights string
        """
        tip = ""
        if self.strategy == 'hill_climbing' and self.gamma > 1.5:
            tip = ("Bei hill_coeff > 1.5: Kooperativität wie bei Hämoglobin – "
                   "ideal für synergetische Tasks (z.B. Kreativarbeit + Analyse).")
        elif self.strategy == 'hill_climbing' and self.gamma < 1.0:
            tip = ("Hill-Koeffizient < 1.0 zeigt negative Kooperativität – "
                   "Ressourcen werden auf mehrere Tasks verteilt.")
        elif self.strategy == 'monod':
            tip = "Standard Monod-Allokation – lineare enzymatische Kinetik."

        total_allocated = sum(results.values())
        return (f"Allokation abgeschlossen. Gesamtressourcen verteilt: {total_allocated:.2f}. "
                f"{tip}")

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
              type=click.Choice(['monod', 'hill_climbing']),
              help='Allokationsstrategie.')
@click.option('--gamma', default=1.8, type=float,
              help='Gamma (K_M-Skalierung für Monod oder Hill-Koeffizient n für hill_climbing).')
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
    click.echo("   2. luca plot")


if __name__ == '__main__':
    cli()
