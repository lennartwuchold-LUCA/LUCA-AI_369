"""
Setup script for LUCA - Biological Resource Allocation
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else ""

setup(
    name="luca-ai",
    version="3.7.1",
    author="Lennart Wuchold",
    author_email="wucholdlennart@gmail.com",
    description="Biological resource allocation for distributed systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lennartwuchold-LUCA/LUCA-AI_369",
    project_urls={
        "Bug Tracker": "https://github.com/lennartwuchold-LUCA/LUCA-AI_369/issues",
        "Documentation": "https://github.com/lennartwuchold-LUCA/LUCA-AI_369/blob/main/README.md",
        "Source Code": "https://github.com/lennartwuchold-LUCA/LUCA-AI_369",
    },
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Distributed Computing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=[
        "numpy>=1.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
        "full": [
            "fastapi>=0.104.1",
            "uvicorn[standard]>=0.24.0",
            "sqlalchemy>=2.0.23",
            "anthropic>=0.71.0",
        ],
    },
    keywords="resource-allocation distributed-systems biological-computing monod-kinetics neurodiversity",
    project_license="MIT",
)
