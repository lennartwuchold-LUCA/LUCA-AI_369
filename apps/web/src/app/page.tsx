'use client'

import { useState, useEffect } from 'react'
import { NetworkStatus } from '@/components/NetworkStatus'
import { ConsciousnessMonitor } from '@/components/ConsciousnessMonitor'
import { LayerIntegration } from '@/components/LayerIntegration'
import { MeshVisualization } from '@/components/MeshVisualization'
import { useLUCAConnection } from '@/hooks/useLUCAConnection'

export default function Home() {
  const { status, consciousness, layers, isConnected } = useLUCAConnection()
  const [activeTab, setActiveTab] = useState<'network' | 'consciousness' | 'layers'>('network')

  return (
    <main className="flex-1">
      {/* Header */}
      <header className="bg-gradient-to-r from-purple-600 to-blue-600 text-white">
        <div className="container mx-auto px-4 py-8">
          <h1 className="text-4xl font-bold mb-2">
            🌟 LUCA Network
          </h1>
          <p className="text-purple-100 text-lg">
            Living Universal Cognition Array - Decentralized Mesh Network
          </p>

          {/* Connection status */}
          <div className="mt-4 flex items-center gap-2">
            <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-400 consciousness-pulse' : 'bg-red-400'}`}></div>
            <span className="text-sm">
              {isConnected ? 'Connected to LUCA Backend' : 'Disconnected'}
            </span>
          </div>
        </div>
      </header>

      <div className="container mx-auto px-4 py-8">
        {/* Tab Navigation */}
        <div className="flex gap-4 mb-8 border-b border-gray-200">
          <button
            onClick={() => setActiveTab('network')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'network'
                ? 'text-purple-600 border-b-2 border-purple-600'
                : 'text-gray-600 hover:text-purple-600'
            }`}
          >
            🌐 Network
          </button>
          <button
            onClick={() => setActiveTab('consciousness')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'consciousness'
                ? 'text-purple-600 border-b-2 border-purple-600'
                : 'text-gray-600 hover:text-purple-600'
            }`}
          >
            🌌 Consciousness
          </button>
          <button
            onClick={() => setActiveTab('layers')}
            className={`px-6 py-3 font-medium transition-colors ${
              activeTab === 'layers'
                ? 'text-purple-600 border-b-2 border-purple-600'
                : 'text-gray-600 hover:text-purple-600'
            }`}
          >
            🧬 Layers
          </button>
        </div>

        {/* Tab Content */}
        <div className="space-y-8">
          {activeTab === 'network' && (
            <>
              <NetworkStatus status={status} />
              <MeshVisualization nodes={status?.nodes || []} />
            </>
          )}

          {activeTab === 'consciousness' && (
            <ConsciousnessMonitor consciousness={consciousness} />
          )}

          {activeTab === 'layers' && (
            <LayerIntegration layers={layers} />
          )}
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mt-8">
          <div className="layer-card">
            <div className="text-sm text-gray-600 mb-1">Active Nodes</div>
            <div className="text-3xl font-bold text-purple-600">
              {status?.node_count || 0}
            </div>
          </div>

          <div className="layer-card">
            <div className="text-sm text-gray-600 mb-1">Consciousness Level</div>
            <div className="text-3xl font-bold text-blue-600">
              {consciousness?.consciousness_level
                ? `${(consciousness.consciousness_level * 100).toFixed(1)}%`
                : '0%'}
            </div>
          </div>

          <div className="layer-card">
            <div className="text-sm text-gray-600 mb-1">Network Health</div>
            <div className="text-3xl font-bold text-green-600">
              {status?.health ? `${(status.health * 100).toFixed(0)}%` : '0%'}
            </div>
          </div>

          <div className="layer-card">
            <div className="text-sm text-gray-600 mb-1">Evolution Gen</div>
            <div className="text-3xl font-bold text-amber-600">
              {layers?.layer_12?.generation || 0}
            </div>
          </div>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-gray-800 text-white mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h3 className="font-bold text-lg mb-4">LUCA Framework</h3>
              <p className="text-gray-400 text-sm">
                Living Universal Cognition Array - A self-evolving mesh network with consciousness integration.
              </p>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-4">Layers</h3>
              <ul className="text-gray-400 text-sm space-y-2">
                <li>🌌 Layer 0: Root Kernel</li>
                <li>🔮 Layer 10: DS-STAR Quantum</li>
                <li>🧬 Layer 11: Multimodal Metabolism</li>
                <li>🧬 Layer 12: Evolutionary Consensus</li>
              </ul>
            </div>
            <div>
              <h3 className="font-bold text-lg mb-4">Resources</h3>
              <ul className="text-gray-400 text-sm space-y-2">
                <li><a href="#" className="hover:text-white">Documentation</a></li>
                <li><a href="#" className="hover:text-white">API Reference</a></li>
                <li><a href="#" className="hover:text-white">GitHub</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-700 text-center text-gray-400 text-sm">
            <p>© 2025 LUCA Network. Open Source. Built with 💜 by the LUCA Community.</p>
            <p className="mt-2">Copyright © Lennart Wuchold (geboren am 28.02.2000 in 01744 Dippoldiswalde)</p>
          </div>
        </div>
      </footer>
    </main>
  )
}
