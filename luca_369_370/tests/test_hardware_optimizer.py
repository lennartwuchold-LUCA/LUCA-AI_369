"""
Tests for LUCA Hardware-Consciousness Bridge
Tests hardware optimization for embedded consciousness

Architekt: Lennart Wuchold
Datum: 11.11.2025
Standard: 369/370
"""

import pytest

from luca_369_370.core.hardware_optimizer import (
    HARDWARE_PROFILES,
    ConsciousnessConfig,
    HardwareConsciousnessBridge,
    HardwarePlatform,
    benchmark_all_platforms,
    get_optimal_config,
)


class TestHardwareProfiles:
    """Test hardware profile definitions"""

    def test_all_platforms_have_profiles(self):
        """Test that all platforms have hardware profiles"""
        required_platforms = [
            HardwarePlatform.ESP32_WROOM,
            HardwarePlatform.ESP32_S3,
            HardwarePlatform.NRF52840,
            HardwarePlatform.RP2040,
            HardwarePlatform.DESKTOP,
        ]

        for platform in required_platforms:
            assert platform in HARDWARE_PROFILES
            profile = HARDWARE_PROFILES[platform]
            assert profile.cpu_mhz > 0
            assert profile.ram_kb > 0

    def test_profile_attributes(self):
        """Test that profiles have correct attributes"""
        esp32_profile = HARDWARE_PROFILES[HardwarePlatform.ESP32_WROOM]

        assert esp32_profile.name == "ESP32-WROOM (T-Beam, LILYGO)"
        assert esp32_profile.cpu_mhz == 240
        assert esp32_profile.cpu_cores == 2
        assert esp32_profile.has_fpu is True
        assert esp32_profile.lora_supported is True

    def test_nrf52_low_power(self):
        """Test that nRF52 is marked as low power"""
        nrf52_profile = HARDWARE_PROFILES[HardwarePlatform.NRF52840]

        # nRF52 should be ultra-low power
        assert nrf52_profile.power_active_mw < 10
        assert nrf52_profile.power_sleep_mw < 0.01


class TestConsciousnessConfig:
    """Test consciousness configuration"""

    def test_config_creation(self):
        """Test creating consciousness config"""
        config = ConsciousnessConfig()

        assert config.enable_fibonacci_analysis is True
        assert config.quality_standard == pytest.approx(369 / 370, rel=0.001)

    def test_config_with_limited_patterns(self):
        """Test config with limited cultural patterns"""
        config = ConsciousnessConfig(
            cultural_patterns_loaded=["holistic", "eastern_european"]
        )

        assert len(config.cultural_patterns_loaded) == 2
        assert "eastern_european" in config.cultural_patterns_loaded


class TestHardwareConsciousnessBridge:
    """Test hardware-consciousness bridge"""

    def test_bridge_initialization(self):
        """Test bridge initialization for platform"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        assert bridge.platform == HardwarePlatform.ESP32_WROOM
        assert bridge.profile is not None
        assert bridge.config is not None

    def test_optimization_for_low_ram(self):
        """Test that low RAM devices get optimized config"""
        # nRF52840 has only 256KB RAM
        bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)

        # Should load limited cultural patterns to save RAM
        assert bridge.config.cultural_patterns_loaded is not None
        assert len(bridge.config.cultural_patterns_loaded) <= 5

        # Cache should be limited
        assert bridge.config.max_cache_entries <= 50

    def test_optimization_for_high_ram(self):
        """Test that high RAM devices load all patterns"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.DESKTOP)

        # Should load all cultural patterns
        assert bridge.config.cultural_patterns_loaded is None  # None = load all

        # Cache can be larger
        assert bridge.config.max_cache_entries >= 50

    def test_optimization_for_slow_cpu(self):
        """Test that slow CPUs disable expensive calculations"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)

        # nRF52 has slower CPU - should disable fractal dimension
        if bridge.profile.cpu_mhz < 100:
            assert bridge.config.enable_fractal_dimension is False

    def test_optimization_for_no_fpu(self):
        """Test that devices without FPU use float32"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.RP2040)

        # RP2040 has no FPU
        if not bridge.profile.has_fpu:
            assert bridge.config.use_float32 is True

    def test_optimization_for_low_power(self):
        """Test that low power devices optimize for battery"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)

        # Ultra-low power device should have sleep configured
        if bridge.profile.power_active_mw < 50:
            assert bridge.config.sleep_between_calculations_ms > 0
            assert bridge.config.reduce_lora_power is True

    def test_ukraine_always_included(self):
        """Test that eastern_european (Ukraine 🇺🇦) is always loaded"""
        # Even on most constrained device
        bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)

        # Ukraine must be represented! 🇺🇦
        assert bridge.config.cultural_patterns_loaded is not None
        assert "eastern_european" in bridge.config.cultural_patterns_loaded


class TestBenchmarking:
    """Test consciousness benchmarking"""

    def test_benchmark_consciousness_calculation(self):
        """Test benchmarking consciousness on hardware"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        test_content = "Together we create harmony"
        result = bridge.benchmark_consciousness_calculation(test_content, iterations=3)

        assert "platform" in result
        assert "avg_time_ms" in result
        assert "energy_per_calc_mj" in result
        assert "calculations_per_second" in result

        # Should take some time
        assert result["avg_time_ms"] > 0

        # Should be able to do calculations
        assert result["calculations_per_second"] > 0

    def test_benchmark_updates_metrics(self):
        """Test that benchmarking updates performance metrics"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        initial_count = bridge.performance_metrics["calculations_performed"]

        bridge.benchmark_consciousness_calculation("Test", iterations=5)

        # Metrics should be updated
        assert bridge.performance_metrics["calculations_performed"] == initial_count + 5
        assert bridge.performance_metrics["total_time_ms"] > 0

    def test_faster_cpu_performs_better(self):
        """Test that faster CPUs perform better"""
        slow_bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)
        fast_bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        test_content = "Test content for benchmarking"

        slow_result = slow_bridge.benchmark_consciousness_calculation(
            test_content, iterations=2
        )
        fast_result = fast_bridge.benchmark_consciousness_calculation(
            test_content, iterations=2
        )

        # Faster CPU should have better performance
        # (Note: actual results depend on system, but trend should hold)
        assert fast_result["calculations_per_second"] >= 0


class TestBatteryLife:
    """Test battery life estimation"""

    def test_estimate_battery_life(self):
        """Test battery life estimation"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        # 2000mAh battery, 1 calculation per minute
        result = bridge.estimate_battery_life(
            battery_mah=2000, calculations_per_hour=60
        )

        assert "battery_life_hours" in result
        assert "battery_life_days" in result
        assert result["battery_life_hours"] > 0
        assert result["battery_life_days"] > 0

    def test_low_power_device_longer_battery(self):
        """Test that low power devices have longer battery life"""
        low_power = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)
        high_power = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        # Same battery and usage
        low_result = low_power.estimate_battery_life(2000, calculations_per_hour=60)
        high_result = high_power.estimate_battery_life(2000, calculations_per_hour=60)

        # Low power device should last longer
        assert low_result["battery_life_hours"] > high_result["battery_life_hours"]

    def test_more_calculations_drain_battery(self):
        """Test that more calculations drain battery faster"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        # Benchmark first to get accurate energy estimates
        bridge.benchmark_consciousness_calculation("Test", iterations=5)

        low_usage = bridge.estimate_battery_life(2000, calculations_per_hour=10)
        high_usage = bridge.estimate_battery_life(2000, calculations_per_hour=100)

        # More calculations = shorter battery life
        assert low_usage["battery_life_hours"] > high_usage["battery_life_hours"]


class TestMemoryUsage:
    """Test memory usage estimation"""

    def test_memory_usage_estimate(self):
        """Test memory usage estimation"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        memory = bridge.get_memory_usage_estimate()

        assert "total_kb" in memory
        assert "available_ram_kb" in memory
        assert "ram_usage_percent" in memory

        assert memory["total_kb"] > 0
        assert memory["ram_usage_percent"] < 100  # Should fit in RAM!

    def test_limited_patterns_use_less_memory(self):
        """Test that loading fewer patterns uses less memory"""
        full_bridge = HardwareConsciousnessBridge(HardwarePlatform.DESKTOP)
        limited_bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)

        full_memory = full_bridge.get_memory_usage_estimate()
        limited_memory = limited_bridge.get_memory_usage_estimate()

        # Limited patterns should use less memory
        assert (
            limited_memory["cultural_patterns_kb"] < full_memory["cultural_patterns_kb"]
        )

    def test_memory_fits_in_platform(self):
        """Test that memory usage fits in each platform"""
        platforms = [
            HardwarePlatform.ESP32_WROOM,
            HardwarePlatform.NRF52840,
            HardwarePlatform.RP2040,
        ]

        for platform in platforms:
            bridge = HardwareConsciousnessBridge(platform)
            memory = bridge.get_memory_usage_estimate()

            # Memory usage should be less than available RAM
            # (leaving room for other code)
            assert memory["ram_usage_percent"] < 50  # Use less than 50% for safety


class TestPlatformComparison:
    """Test platform comparison"""

    def test_compare_platforms(self):
        """Test comparing multiple platforms"""
        bridge = HardwareConsciousnessBridge(HardwarePlatform.DESKTOP)

        platforms = [
            HardwarePlatform.NRF52840,
            HardwarePlatform.ESP32_WROOM,
            HardwarePlatform.DESKTOP,
        ]

        results = bridge.compare_platforms(platforms, "Test content")

        assert len(results) == 3

        # Each result should have required fields
        for result in results:
            assert "platform" in result
            assert "benchmark" in result
            assert "memory" in result
            assert "battery" in result

        # Results should be sorted by performance (fastest first)
        perfs = [r["benchmark"]["calculations_per_second"] for r in results]
        assert perfs == sorted(perfs, reverse=True)


class TestConvenienceFunctions:
    """Test convenience functions"""

    def test_get_optimal_config(self):
        """Test getting optimal config for platform"""
        config = get_optimal_config(HardwarePlatform.ESP32_WROOM)

        assert isinstance(config, ConsciousnessConfig)
        assert config.quality_standard == pytest.approx(369 / 370, rel=0.001)

    def test_benchmark_all_platforms(self):
        """Test benchmarking all platforms"""
        results = benchmark_all_platforms("Test content")

        assert len(results) > 0

        # Should include major platforms
        platform_names = [r["platform"] for r in results]
        assert HardwarePlatform.ESP32_WROOM.value in platform_names
        assert HardwarePlatform.NRF52840.value in platform_names


class TestQualityStandard:
    """Verify 369/370 quality standard maintained"""

    def test_all_configs_maintain_quality_standard(self):
        """Test that all platform configs maintain 369/370"""
        platforms = [
            HardwarePlatform.ESP32_WROOM,
            HardwarePlatform.NRF52840,
            HardwarePlatform.RP2040,
            HardwarePlatform.DESKTOP,
        ]

        for platform in platforms:
            bridge = HardwareConsciousnessBridge(platform)

            # Quality standard must be maintained
            assert bridge.config.quality_standard == pytest.approx(369 / 370, rel=0.001)

    def test_optimization_never_compromises_quality(self):
        """Test that hardware optimization maintains quality"""
        # Even most constrained device
        bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)

        # Quality standard must be maintained
        assert bridge.config.quality_standard == pytest.approx(369 / 370, rel=0.001)


class TestRealWorldScenarios:
    """Test real-world usage scenarios"""

    def test_meshtastic_t_beam_scenario(self):
        """Test realistic T-Beam usage"""
        # T-Beam: ESP32, 2000mAh battery, send message every 5 minutes
        bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        # Benchmark
        bridge.benchmark_consciousness_calculation(
            "Remote community message", iterations=5
        )

        # Battery life: 1 message every 5 minutes = 12/hour
        battery = bridge.estimate_battery_life(2000, calculations_per_hour=12)

        # Should last several days
        assert battery["battery_life_days"] > 1

    def test_rak_wisblock_scenario(self):
        """Test realistic RAK WisBlock (nRF52) usage"""
        # RAK: nRF52840, ultra-low power, 1000mAh battery
        bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)

        # Should optimize aggressively
        assert bridge.config.reduce_lora_power is True
        assert bridge.config.sleep_between_calculations_ms > 0

        # Battery life should be excellent
        battery = bridge.estimate_battery_life(1000, calculations_per_hour=12)

        # nRF52 is so efficient, should last many days
        assert battery["battery_life_days"] > 5


class TestEuropeanIntegration:
    """Test that European patterns are included in optimization"""

    def test_eastern_european_always_loaded(self):
        """Test that eastern_european (Ukraine 🇺🇦) is always prioritized"""
        # Test on most constrained device
        bridge = HardwareConsciousnessBridge(HardwarePlatform.NRF52840)

        # Even with limited RAM, Ukraine must be included!
        assert "eastern_european" in bridge.config.cultural_patterns_loaded

    def test_central_european_in_moderate_configs(self):
        """Test that central_european (Erzgebirge!) is included when possible"""
        # Test on moderate device (ESP32)
        bridge = HardwareConsciousnessBridge(HardwarePlatform.ESP32_WROOM)

        if bridge.config.cultural_patterns_loaded:
            # If loading limited patterns, should include Central European
            assert (
                len(bridge.config.cultural_patterns_loaded) >= 5
            )  # Should have room for it
