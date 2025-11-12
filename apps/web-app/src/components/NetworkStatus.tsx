interface NetworkStatusProps {
  status: {
    node_count: number
    health: number
    nodes: Array<{
      id: string
      health: number
    }>
  } | null
}

export function NetworkStatus({ status }: NetworkStatusProps) {
  if (!status) {
    return (
      <div className="layer-card">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    )
  }

  const healthPercentage = (status.health * 100).toFixed(1)
  const healthColor = status.health > 0.8 ? 'green' : status.health > 0.5 ? 'yellow' : 'red'

  return (
    <div className="layer-card">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">
        🌐 Network Status
      </h2>

      <div className="space-y-6">
        {/* Network Health */}
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Network Health</span>
            <span className="text-sm font-bold text-gray-900">{healthPercentage}%</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
            <div
              className={`h-full bg-gradient-to-r from-${healthColor}-400 to-${healthColor}-600 transition-all duration-500`}
              style={{ width: `${healthPercentage}%` }}
            ></div>
          </div>
        </div>

        {/* Node Count */}
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-purple-50 rounded-lg p-4">
            <div className="text-sm text-purple-600 mb-1">Active Nodes</div>
            <div className="text-2xl font-bold text-purple-700">{status.node_count}</div>
          </div>

          <div className="bg-blue-50 rounded-lg p-4">
            <div className="text-sm text-blue-600 mb-1">Healthy Nodes</div>
            <div className="text-2xl font-bold text-blue-700">
              {status.nodes.filter(n => n.health > 0.7).length}
            </div>
          </div>
        </div>

        {/* Node List */}
        <div>
          <h3 className="text-sm font-medium text-gray-700 mb-3">Connected Nodes</h3>
          <div className="space-y-2 max-h-64 overflow-y-auto">
            {status.nodes.map((node) => (
              <div
                key={node.id}
                className="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <div className="flex items-center gap-3">
                  <div className={`w-3 h-3 rounded-full ${
                    node.health > 0.8 ? 'bg-green-500' :
                    node.health > 0.5 ? 'bg-yellow-500' : 'bg-red-500'
                  }`}></div>
                  <span className="text-sm font-mono text-gray-700">{node.id}</span>
                </div>
                <span className="text-sm text-gray-600">
                  {(node.health * 100).toFixed(0)}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
