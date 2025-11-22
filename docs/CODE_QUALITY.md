# Code-Qualitäts-Richtlinien für L.U.C.A 369

Dieses Dokument beschreibt die Code-Qualitätsstandards und -werkzeuge, die im L.U.C.A 369 Projekt verwendet werden, um Stabilität, Lesbarkeit und Wartbarkeit sicherzustellen.

## 📋 Übersicht

L.U.C.A 369 folgt dem **369/370 Qualitätsstandard** (≈ 0.997297 = 99.7% Qualität). Dies spiegelt sich nicht nur in der Architektur, sondern auch in der Code-Qualität wider.

### Die 5 Säulen der Code-Qualität

1. **Stabilität und Qualitätssicherung** (Tests & CI/CD)
2. **Code-Lesbarkeit und Stil** (Formatierung & Linting)
3. **Dokumentation im Code** (Docstrings & Typisierung)
4. **Abhängigkeitsmanagement** (Poetry)
5. **Architektur** (12-Layer-Modularität)

## 🔧 Werkzeuge und Konfiguration

### 1. Formatierung

#### Black
- **Zweck**: Automatische Code-Formatierung nach PEP 8
- **Konfiguration**: `.flake8` und `pyproject.toml`
- **Line Length**: 88 Zeichen (Black-Standard)

```bash
# Code formatieren
poetry run black luca/ tests/ backend/

# Nur prüfen (ohne Änderungen)
poetry run black --check luca/
```

#### isort
- **Zweck**: Automatische Import-Sortierung
- **Konfiguration**: Kompatibel mit Black (`profile = "black"`)

```bash
# Imports sortieren
poetry run isort luca/ tests/ backend/

# Nur prüfen
poetry run isort --check-only luca/
```

### 2. Linting

#### Flake8
- **Zweck**: Stilprüfung, Bug-Erkennung, Code-Komplexität
- **Konfiguration**: `.flake8`
- **Plugins**:
  - `flake8-docstrings`: Prüft Docstring-Qualität
  - `flake8-bugbear`: Erkennt häufige Fehler

```bash
# Linting durchführen
poetry run flake8 luca/ backend/

# Mit detaillierten Statistiken
poetry run flake8 luca/ --count --show-source --statistics
```

**Wichtige Konfigurationen**:
- `max-line-length = 88` (Black-kompatibel)
- `max-complexity = 10` (McCabe-Komplexität)
- Ignoriert: E203, E266, E501, W503 (Black-Konflikte)

### 3. Type Checking

#### MyPy
- **Zweck**: Statische Typ-Prüfung
- **Konfiguration**: `pyproject.toml`
- **Python Version**: 3.11+

```bash
# Type checking durchführen
poetry run mypy luca/

# Mit detailliertem Output
poetry run mypy luca/ --show-error-codes
```

**Best Practices**:
- Verwenden Sie Type Hints für alle Funktionsparameter und Rückgabewerte
- Nutzen Sie `from typing import ...` für komplexe Typen
- Beispiel:
  ```python
  def process_data(input_data: List[Dict[str, Any]]) -> Optional[str]:
      """Process input data and return result."""
      ...
  ```

### 4. Testing

#### Pytest
- **Zweck**: Unit- und Integrationstests
- **Konfiguration**: `pyproject.toml` (`[tool.pytest.ini_options]`)
- **Testabdeckung**: Ziel ist > 80%

```bash
# Alle Tests ausführen
poetry run pytest

# Mit Verbose-Output
poetry run pytest -v

# Nur Unit-Tests
poetry run pytest -m unit

# Nur Integrationstests
poetry run pytest -m integration

# Parallel ausführen (schneller)
poetry run pytest -n auto
```

**Test-Organisation**:
- Unit-Tests: Testen einzelne Funktionen/Klassen
- Integrationstests: Testen Zusammenspiel mehrerer Module
- Marker: `@pytest.mark.unit`, `@pytest.mark.integration`, `@pytest.mark.slow`

## 🚀 Pre-commit Hooks

Pre-commit Hooks stellen sicher, dass Code-Qualität automatisch vor jedem Commit geprüft wird.

### Installation

```bash
# Pre-commit hooks installieren
poetry install
poetry run pre-commit install
```

### Verwendung

```bash
# Manuell auf alle Dateien ausführen
poetry run pre-commit run --all-files

# Nur auf geänderte Dateien (automatisch bei git commit)
git commit -m "Deine Nachricht"
```

### Konfigurierte Hooks

Die `.pre-commit-config.yaml` enthält:

1. **Black**: Code-Formatierung
2. **isort**: Import-Sortierung
3. **Flake8**: Linting
4. **MyPy**: Type Checking (optional, nicht blockierend)
5. **Standard-Hooks**:
   - Trailing Whitespace entfernen
   - End-of-file fixer
   - YAML/JSON/TOML Validierung
   - Große Dateien blockieren (> 1MB)
   - Private Keys erkennen

## 🏗️ CI/CD Pipeline

GitHub Actions führt automatisch Qualitätsprüfungen bei jedem Push/PR aus:

### Workflow: `luca_ci.yml`

1. **Test Job** (Python 3.11, 3.12):
   - Dependencies installieren
   - Tests ausführen (`pytest`)
   - Code-Stil prüfen (`black`, `isort`)
   - Linting (`flake8`)

2. **Lint Job**:
   - Type Checking (`mypy`)

3. **Build Job**:
   - Package bauen (`poetry build`)

### Lokale Simulation

```bash
# Simuliere CI lokal
poetry run black --check luca/ tests/ backend/
poetry run isort --check-only luca/ tests/ backend/
poetry run flake8 luca/ backend/
poetry run mypy luca/
poetry run pytest
```

## 📐 Architektur: 12-Layer-System

### Abstrakte Basisklasse

Alle 12 Consciousness Layers implementieren die abstrakte Basisklasse:

```python
from luca.core.base_layer import AbstractLayer, LayerID, LayerMetrics

class MyLayer(AbstractLayer[InputType, OutputType]):
    def __init__(self):
        super().__init__(
            layer_id=LayerID.LAYER_3,
            layer_name="My Custom Layer"
        )

    def process(self, input_data: InputType) -> OutputType:
        """Implementiere Layer-spezifische Verarbeitung."""
        ...

    def validate_input(self, input_data: InputType) -> bool:
        """Validiere Eingabedaten."""
        return isinstance(input_data, InputType)
```

### Layer-Orchestrierung

```python
from luca.core.base_layer import LayerOrchestrator

orchestrator = LayerOrchestrator()
orchestrator.add_layer(layer_3)
orchestrator.add_layer(layer_6)
orchestrator.add_layer(layer_9)

result = orchestrator.process_through_layers(input_data)
```

### Vorteile

- **Konsistente Schnittstelle**: Alle Layers haben die gleiche API
- **Testbarkeit**: Jeder Layer kann isoliert getestet werden
- **Modularität**: Layers können einfach ausgetauscht werden
- **Metriken**: Jeder Layer liefert standardisierte Metriken

## 📦 Abhängigkeitsmanagement mit Poetry

### Warum Poetry?

- **Deterministische Builds**: `poetry.lock` garantiert identische Abhängigkeiten
- **Moderne Verwaltung**: Einfachere Syntax als `requirements.txt`
- **Isolation**: Automatisches Virtual Environment Management
- **Extras**: Optionale Dependency-Gruppen (`[backend]`, `[universal]`)

### Installation von Dependencies

```bash
# Alle Dependencies installieren
poetry install

# Mit Backend-Dependencies
poetry install --extras backend

# Mit Universal Root Kernel
poetry install --extras universal

# Alle optionalen Dependencies
poetry install --extras all

# Development Dependencies
poetry install --with dev
```

### requirements.txt Export

Für Deployment-Systeme, die `requirements.txt` benötigen:

```bash
# Minimale Dependencies
poetry export -f requirements.txt --output requirements.txt --without-hashes

# Mit Backend
poetry export -f requirements.txt --output requirements.txt --without-hashes --extras backend

# Alle Dependencies
poetry export -f requirements.txt --output requirements.txt --without-hashes --extras all
```

**⚠️ Wichtig**: Bearbeiten Sie `requirements.txt` NICHT manuell. Ändern Sie stattdessen `pyproject.toml` und exportieren Sie neu.

## 📝 Docstrings und Dokumentation

### Docstring-Stil: Google Format

```python
def calculate_resonance(
    blocks: List[InfoBlock],
    quality_threshold: float = 0.997
) -> Dict[str, float]:
    """
    Calculate resonance quality of information blocks.

    This function analyzes a sequence of InfoBlocks and calculates
    their collective resonance based on the 369/370 quality standard.

    Args:
        blocks: List of InfoBlock objects to analyze
        quality_threshold: Minimum quality score (default: 369/370)

    Returns:
        Dictionary containing:
            - 'resonance': Overall resonance score (0.0-1.0)
            - 'quality': Quality relative to threshold
            - 'coherence': How consistent the blocks are

    Raises:
        ValueError: If blocks list is empty

    Example:
        >>> blocks = [InfoBlock(...), InfoBlock(...)]
        >>> result = calculate_resonance(blocks)
        >>> print(result['resonance'])
        0.998
    """
    if not blocks:
        raise ValueError("Blocks list cannot be empty")

    # Implementation...
    return {"resonance": 0.998, "quality": 1.0, "coherence": 0.995}
```

### Modul-Docstrings

Jede Datei sollte mit einem Modul-Docstring beginnen:

```python
"""
LUCA Layer 6: Growth Kinetics

This module implements bio-inspired growth models for resource allocation.

Author: Lennart Wuchold
Date: 2025-11-22
Standard: 369/370
"""
```

## 🎯 Qualitätsstandards

### Code-Qualität Checkliste

Vor jedem Commit:

- [ ] Code ist mit Black formatiert
- [ ] Imports sind mit isort sortiert
- [ ] Flake8 zeigt keine Fehler
- [ ] Type Hints sind vorhanden (wo sinnvoll)
- [ ] Docstrings sind vorhanden (alle öffentlichen Funktionen/Klassen)
- [ ] Tests sind geschrieben (für neue Funktionalität)
- [ ] Tests laufen erfolgreich durch
- [ ] MyPy zeigt keine kritischen Fehler

### Pull Request Anforderungen

- Alle CI/CD Checks müssen grün sein
- Code Coverage sollte nicht sinken
- Neue Features benötigen Tests
- Breaking Changes müssen dokumentiert sein

## 🔍 Troubleshooting

### Flake8 Fehler ignorieren

Nur in Ausnahmefällen:

```python
# noqa: E501 - Zeile zu lang
very_long_line = "..." # noqa: E501

# noqa: F401 - Ungenutzer Import (oft in __init__.py)
from module import something  # noqa: F401
```

### MyPy Type Ignore

```python
result = external_function()  # type: ignore[no-untyped-call]
```

### Pre-commit Hooks temporär überspringen

```bash
git commit --no-verify -m "Emergency fix"
```

**⚠️ Nur in Notfällen verwenden!**

## 📚 Weitere Ressourcen

- **Black**: https://black.readthedocs.io/
- **isort**: https://pycqa.github.io/isort/
- **Flake8**: https://flake8.pycqa.org/
- **MyPy**: https://mypy.readthedocs.io/
- **Pytest**: https://docs.pytest.org/
- **Pre-commit**: https://pre-commit.com/
- **Poetry**: https://python-poetry.org/docs/

## 🌟 Beitragen

Wenn Sie zu L.U.C.A 369 beitragen möchten:

1. Fork das Repository
2. Installieren Sie pre-commit hooks: `poetry run pre-commit install`
3. Erstellen Sie einen Feature-Branch
4. Schreiben Sie Tests für neue Features
5. Stellen Sie sicher, dass alle Qualitätsprüfungen bestehen
6. Erstellen Sie einen Pull Request

**Der 369/370 Standard gilt auch für Code-Qualität! 🚀**
