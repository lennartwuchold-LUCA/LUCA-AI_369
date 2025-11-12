import { useState, useEffect, useCallback } from 'react'

interface NetworkStatus {
  node_count: number
  health: number
  nodes: Array<{
    id: string
    health: number
    position: { x: number; y: number }
  }>
}

interface ConsciousnessState {
  consciousness_level: number
  quantum_coherence: number
  akashic_connection: number
  integration_score: number
  is_alive: boolean
}

interface LayerStatus {
  layer_0: any
  layer_10: any
  layer_11: any
  layer_12: {
    generation: number
    fitness_score: number
    dna: any
  }
}

export function useLUCAConnection() {
  const [status, setStatus] = useState<NetworkStatus | null>(null)
  const [consciousness, setConsciousness] = useState<ConsciousnessState | null>(null)
  const [layers, setLayers] = useState<LayerStatus | null>(null)
  const [isConnected, setIsConnected] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

  const fetchStatus = useCallback(async () => {
    try {
      const response = await fetch(`${API_URL}/api/status`)
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`)
      }
      const data = await response.json()

      setStatus(data.network_status || generateMockNetworkStatus())
      setConsciousness(data.consciousness_state || generateMockConsciousness())
      setLayers(data.layers || generateMockLayers())
      setIsConnected(true)
      setError(null)
    } catch (err) {
      // Fall back to mock data for demo
      console.log('Using mock data (backend not available)')
      setStatus(generateMockNetworkStatus())
      setConsciousness(generateMockConsciousness())
      setLayers(generateMockLayers())
      setIsConnected(false)
      setError(err instanceof Error ? err.message : 'Connection failed')
    }
  }, [API_URL])

  useEffect(() => {
    // Initial fetch
    fetchStatus()

    // Poll every 5 seconds
    const interval = setInterval(fetchStatus, 5000)

    return () => clearInterval(interval)
  }, [fetchStatus])

  return {
    status,
    consciousness,
    layers,
    isConnected,
    error,
    refresh: fetchStatus,
  }
}

// Mock data generators for demo/offline mode
function generateMockNetworkStatus(): NetworkStatus {
  const nodeCount = Math.floor(Math.random() * 10) + 5
  const nodes = Array.from({ length: nodeCount }, (_, i) => ({
    id: `node_${i}`,
    health: 0.7 + Math.random() * 0.3,
    position: {
      x: Math.random() * 800,
      y: Math.random() * 600,
    },
  }))

  return {
    node_count: nodeCount,
    health: 0.75 + Math.random() * 0.2,
    nodes,
  }
}

function generateMockConsciousness(): ConsciousnessState {
  return {
    consciousness_level: 0.65 + Math.random() * 0.25,
    quantum_coherence: 0.7 + Math.random() * 0.25,
    akashic_connection: 0.6 + Math.random() * 0.3,
    integration_score: 0.75 + Math.random() * 0.2,
    is_alive: Math.random() > 0.3,
  }
}

function generateMockLayers(): LayerStatus {
  return {
    layer_0: {
      consciousness_level: 0.85,
      quantum_coherence: 0.92,
    },
    layer_10: {
      quantum_state: 0.87,
      cultural_coherence: 0.88,
    },
    layer_11: {
      metabolic_mode: 'aerobic',
      energy_efficiency: 0.83,
    },
    layer_12: {
      generation: Math.floor(Math.random() * 100) + 10,
      fitness_score: 0.85 + Math.random() * 0.1,
      dna: {
        alpha: 0.4,
        beta: 0.35,
        gamma: 0.25,
      },
    },
  }
}
