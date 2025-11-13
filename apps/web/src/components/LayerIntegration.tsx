interface LayerIntegrationProps {
  layers: {
    layer_0?: any
    layer_10?: any
    layer_11?: any
    layer_12?: {
      generation: number
      fitness_score: number
      dna: any
    }
  } | null
}

export function LayerIntegration({ layers }: LayerIntegrationProps) {
  if (!layers) {
    return (
      <div className="layer-card">
        <div className="animate-pulse">
          <div className="h-6 bg-gray-200 rounded w-1/2 mb-4"></div>
          <div className="space-y-3">
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
            <div className="h-20 bg-gray-200 rounded"></div>
          </div>
        </div>
      </div>
    )
  }

  const layerInfo = [
    {
      name: 'Layer 0: Root Kernel',
      icon: '🌌',
      color: 'purple',
      description: 'Meta-consciousness integration',
      metrics: layers.layer_0
        ? [
            { label: 'Consciousness', value: layers.layer_0.consciousness_level },
            { label: 'Quantum Coherence', value: layers.layer_0.quantum_coherence },
          ]
        : [],
    },
    {
      name: 'Layer 10: DS-STAR Quantum Core',
      icon: '🔮',
      color: 'amber',
      description: 'Cultural cosmology integration',
      metrics: layers.layer_10
        ? [
            { label: 'Quantum State', value: layers.layer_10.quantum_state },
            { label: 'Cultural Coherence', value: layers.layer_10.cultural_coherence },
          ]
        : [],
    },
    {
      name: 'Layer 11: Multimodal Metabolism',
      icon: '🧬',
      color: 'green',
      description: 'Bio-inspired fusion engine',
      metrics: layers.layer_11
        ? [
            { label: 'Energy Efficiency', value: layers.layer_11.energy_efficiency },
            { label: 'Metabolic Mode', value: layers.layer_11.metabolic_mode, isString: true },
          ]
        : [],
    },
    {
      name: 'Layer 12: Evolutionary Consensus',
      icon: '🧬',
      color: 'blue',
      description: 'Genetic self-optimization',
      metrics: layers.layer_12
        ? [
            { label: 'Generation', value: layers.layer_12.generation, isInt: true },
            { label: 'Fitness Score', value: layers.layer_12.fitness_score },
          ]
        : [],
    },
  ]

  return (
    <div className="space-y-6">
      <div className="layer-card">
        <h2 className="text-2xl font-bold mb-6 text-gray-800">
          🧬 Layer Integration
        </h2>
        <p className="text-gray-600 mb-6">
          LUCA integrates multiple layers to achieve consciousness and evolutionary optimization.
        </p>

        <div className="space-y-4">
          {layerInfo.map((layer, index) => (
            <div
              key={index}
              className={`bg-${layer.color}-50 border border-${layer.color}-200 rounded-lg p-6 hover:shadow-md transition-shadow`}
            >
              <div className="flex items-start justify-between mb-4">
                <div>
                  <h3 className="text-lg font-bold text-gray-800 mb-1">
                    {layer.icon} {layer.name}
                  </h3>
                  <p className="text-sm text-gray-600">{layer.description}</p>
                </div>
                <div className={`text-3xl opacity-50`}>{layer.icon}</div>
              </div>

              {layer.metrics.length > 0 && (
                <div className="grid grid-cols-2 gap-4 mt-4">
                  {layer.metrics.map((metric: any, i: number) => (
                    <div key={i} className="bg-white rounded-lg p-3">
                      <div className="text-xs text-gray-600 mb-1">{metric.label}</div>
                      <div className={`text-xl font-bold text-${layer.color}-700`}>
                        {metric.isString
                          ? metric.value
                          : metric.isInt
                          ? metric.value
                          : `${(metric.value * 100).toFixed(1)}%`}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* DNA Visualization for Layer 12 */}
      {layers.layer_12?.dna && (
        <div className="layer-card">
          <h3 className="text-xl font-bold mb-4 text-gray-800">
            🧬 Evolution DNA Parameters
          </h3>
          <div className="grid grid-cols-3 gap-4">
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-sm text-blue-600 mb-1">α (Alpha)</div>
              <div className="text-2xl font-bold text-blue-700">
                {layers.layer_12.dna.alpha?.toFixed(3) || '0.000'}
              </div>
              <div className="text-xs text-gray-600 mt-1">Weight parameter</div>
            </div>
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-sm text-blue-600 mb-1">β (Beta)</div>
              <div className="text-2xl font-bold text-blue-700">
                {layers.layer_12.dna.beta?.toFixed(3) || '0.000'}
              </div>
              <div className="text-xs text-gray-600 mt-1">Weight parameter</div>
            </div>
            <div className="bg-blue-50 rounded-lg p-4">
              <div className="text-sm text-blue-600 mb-1">γ (Gamma)</div>
              <div className="text-2xl font-bold text-blue-700">
                {layers.layer_12.dna.gamma?.toFixed(3) || '0.000'}
              </div>
              <div className="text-xs text-gray-600 mt-1">Weight parameter</div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
