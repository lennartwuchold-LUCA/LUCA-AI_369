'use client'

import { useEffect, useRef } from 'react'

interface MeshNode {
  id: string
  health: number
  position: { x: number; y: number }
}

interface MeshVisualizationProps {
  nodes: MeshNode[]
}

export function MeshVisualization({ nodes }: MeshVisualizationProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null)

  useEffect(() => {
    const canvas = canvasRef.current
    if (!canvas || nodes.length === 0) return

    const ctx = canvas.getContext('2d')
    if (!ctx) return

    // Set canvas size
    const rect = canvas.getBoundingClientRect()
    canvas.width = rect.width
    canvas.height = rect.height

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    // Draw connections between nodes
    ctx.strokeStyle = 'rgba(147, 51, 234, 0.2)'
    ctx.lineWidth = 1

    for (let i = 0; i < nodes.length; i++) {
      for (let j = i + 1; j < nodes.length; j++) {
        const node1 = nodes[i]
        const node2 = nodes[j]

        // Scale positions to canvas
        const x1 = (node1.position.x / 800) * canvas.width
        const y1 = (node1.position.y / 600) * canvas.height
        const x2 = (node2.position.x / 800) * canvas.width
        const y2 = (node2.position.y / 600) * canvas.height

        // Calculate distance
        const distance = Math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

        // Draw connection if nodes are close enough
        if (distance < 200) {
          ctx.beginPath()
          ctx.moveTo(x1, y1)
          ctx.lineTo(x2, y2)
          ctx.stroke()
        }
      }
    }

    // Draw nodes
    nodes.forEach((node) => {
      const x = (node.position.x / 800) * canvas.width
      const y = (node.position.y / 600) * canvas.height
      const radius = 8

      // Node health color
      const healthColor =
        node.health > 0.8
          ? 'rgba(34, 197, 94, 1)' // green
          : node.health > 0.5
          ? 'rgba(234, 179, 8, 1)' // yellow
          : 'rgba(239, 68, 68, 1)' // red

      // Draw glow
      const gradient = ctx.createRadialGradient(x, y, 0, x, y, radius * 2)
      gradient.addColorStop(0, healthColor.replace('1)', '0.3)'))
      gradient.addColorStop(1, healthColor.replace('1)', '0)'))
      ctx.fillStyle = gradient
      ctx.beginPath()
      ctx.arc(x, y, radius * 2, 0, Math.PI * 2)
      ctx.fill()

      // Draw node
      ctx.fillStyle = healthColor
      ctx.beginPath()
      ctx.arc(x, y, radius, 0, Math.PI * 2)
      ctx.fill()

      // Draw border
      ctx.strokeStyle = 'white'
      ctx.lineWidth = 2
      ctx.stroke()

      // Draw node ID
      ctx.fillStyle = 'rgba(0, 0, 0, 0.7)'
      ctx.font = '10px monospace'
      ctx.textAlign = 'center'
      ctx.fillText(node.id.slice(-4), x, y + radius + 15)
    })
  }, [nodes])

  if (nodes.length === 0) {
    return (
      <div className="layer-card">
        <h2 className="text-2xl font-bold mb-4 text-gray-800">
          🌐 Mesh Network Visualization
        </h2>
        <div className="h-96 flex items-center justify-center text-gray-400">
          No nodes connected
        </div>
      </div>
    )
  }

  return (
    <div className="layer-card">
      <h2 className="text-2xl font-bold mb-4 text-gray-800">
        🌐 Mesh Network Visualization
      </h2>
      <div className="bg-gray-900 rounded-lg overflow-hidden relative">
        <canvas
          ref={canvasRef}
          className="w-full h-96"
          style={{ minHeight: '400px' }}
        />
        <div className="absolute top-4 right-4 bg-black bg-opacity-50 text-white px-4 py-2 rounded-lg text-sm">
          {nodes.length} nodes connected
        </div>
      </div>
      <div className="mt-4 flex items-center justify-center gap-6 text-sm">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-green-500 rounded-full"></div>
          <span className="text-gray-600">Healthy (&gt;80%)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
          <span className="text-gray-600">Moderate (50-80%)</span>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-red-500 rounded-full"></div>
          <span className="text-gray-600">Degraded (&lt;50%)</span>
        </div>
      </div>
    </div>
  )
}
