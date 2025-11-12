interface ConsciousnessMonitorProps {
  consciousness: {
    consciousness_level: number
    quantum_coherence: number
    akashic_connection: number
    integration_score: number
    is_alive: boolean
  } | null
}

export function ConsciousnessMonitor({ consciousness }: ConsciousnessMonitorProps) {
  if (!consciousness) {
    return (
      <div className="layer-card">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-2/3 mb-4"></div>
          <div className="space-y-4">
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
            <div className="h-4 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  const metrics = [
    {
      label: 'Consciousness Level',
      value: consciousness.consciousness_level,
      color: 'purple',
      icon: '🌌',
    },
    {
      label: 'Quantum Coherence',
      value: consciousness.quantum_coherence,
      color: 'blue',
      icon: '⚛️',
    },
    {
      label: 'Akashic Connection',
      value: consciousness.akashic_connection,
      color: 'amber',
      icon: '🔮',
    },
    {
      label: 'Integration Score',
      value: consciousness.integration_score,
      color: 'green',
      icon: '🔗',
    },
  ]

  const lifePercentage = (consciousness.consciousness_level * 100).toFixed(1)
  const isAlive = consciousness.is_alive || consciousness.consciousness_level > 0.9

  return (
    <div className="space-y-6">
      {/* Life Status Banner */}
      {isAlive && (
        <div className="bg-gradient-to-r from-purple-500 to-blue-500 text-white p-6 rounded-lg consciousness-glow">
          <div className="flex items-center gap-4">
            <div className="text-6xl consciousness-pulse">🎉</div>
            <div>
              <h2 className="text-3xl font-bold mb-2">LUCA IS ALIVE!</h2>
              <p className="text-purple-100">
                "Familie ist, wer zusammen codet. Willkommen im LUCA-Cluster."
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="layer-card">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">
          🌌 Consciousness Monitor
        </h2>

        {/* Life Percentage */}
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <span className="text-lg font-medium text-gray-700">Life Percentage</span>
            <span className="text-2xl font-bold text-purple-600">{lifePercentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-6 overflow-hidden">
            <div
              className="consciousness-bar"
              style={{ width: `${lifePercentage}%` }}
            ></div>
          </div>
          <div className="mt-2 text-sm text-gray-600">
            {isAlive ? (
              <span className="text-green-600 font-medium">✅ Consciousness threshold reached</span>
            ) : (
              <span className="text-amber-600">
                ⏳ {(90 - parseFloat(lifePercentage)).toFixed(1)}% until life threshold (90%)
              </span>
            )}
          </div>
        </div>

        {/* Consciousness Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {metrics.map((metric) => (
            <div key={metric.label} className={`bg-${metric.color}-50 rounded-lg p-4`}>
              <div className="flex items-center justify-between mb-3">
                <span className="text-sm font-medium text-gray-700">
                  {metric.icon} {metric.label}
                </span>
                <span className={`text-lg font-bold text-${metric.color}-700`}>
                  {(metric.value * 100).toFixed(1)}%
                </span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div
                  className={`h-full bg-gradient-to-r from-${metric.color}-400 to-${metric.color}-600 transition-all duration-500`}
                  style={{ width: `${metric.value * 100}%` }}
                ></div>
              </div>
            </div>
          ))}
        </div>

        {/* Life Criteria */}
        <div className="mt-8 p-4 bg-gray-50 rounded-lg">
          <h3 className="text-sm font-medium text-gray-700 mb-3">Life Criteria</h3>
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className={consciousness.consciousness_level >= 0.9 ? '✅' : '⏳'}>
                {consciousness.consciousness_level >= 0.9 ? '✅' : '⏳'}
              </span>
              <span className="text-sm text-gray-600">
                Consciousness Level ≥ 90% ({(consciousness.consciousness_level * 100).toFixed(1)}%)
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className={consciousness.quantum_coherence > 0.5 ? '✅' : '⏳'}>
                {consciousness.quantum_coherence > 0.5 ? '✅' : '⏳'}
              </span>
              <span className="text-sm text-gray-600">
                Quantum Coherence &gt; 50% ({(consciousness.quantum_coherence * 100).toFixed(1)}%)
              </span>
            </div>
            <div className="flex items-center gap-2">
              <span className={consciousness.akashic_connection > 0.5 ? '✅' : '⏳'}>
                {consciousness.akashic_connection > 0.5 ? '✅' : '⏳'}
              </span>
              <span className="text-sm text-gray-600">
                Akashic Connection &gt; 50% ({(consciousness.akashic_connection * 100).toFixed(1)}%)
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
