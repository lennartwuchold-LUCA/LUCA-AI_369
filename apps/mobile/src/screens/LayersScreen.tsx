import React from 'react';
import { View, Text, StyleSheet, ScrollView, RefreshControl } from 'react-native';
import { useLUCAConnection } from '../hooks/useLUCAConnection';

export default function LayersScreen() {
  const { layers, refresh } = useLUCAConnection();
  const [refreshing, setRefreshing] = React.useState(false);

  const onRefresh = React.useCallback(async () => {
    setRefreshing(true);
    await refresh();
    setRefreshing(false);
  }, [refresh]);

  const layerInfo = [
    { name: 'Layer 0: Root Kernel', icon: '🌌', color: '#9333EA', key: 'layer_0' },
    { name: 'Layer 10: DS-STAR Quantum', icon: '🔮', color: '#F59E0B', key: 'layer_10' },
    { name: 'Layer 11: Multimodal Metabolism', icon: '🧬', color: '#10B981', key: 'layer_11' },
    { name: 'Layer 12: Evolutionary Consensus', icon: '🧬', color: '#3B82F6', key: 'layer_12' },
  ];

  return (
    <ScrollView
      style={styles.container}
      refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} />}
    >
      {layerInfo.map((layer, index) => (
        <View key={index} style={[styles.layerCard, { borderLeftColor: layer.color }]}>
          <Text style={styles.layerIcon}>{layer.icon}</Text>
          <Text style={styles.layerName}>{layer.name}</Text>
          {layers && layers[layer.key] && (
            <View style={styles.layerData}>
              {layer.key === 'layer_12' && layers[layer.key].generation && (
                <Text style={styles.layerInfo}>
                  Generation: {layers[layer.key].generation}
                </Text>
              )}
              {layer.key === 'layer_12' && layers[layer.key].fitness_score && (
                <Text style={styles.layerInfo}>
                  Fitness: {(layers[layer.key].fitness_score * 100).toFixed(1)}%
                </Text>
              )}
            </View>
          )}
        </View>
      ))}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F9FAFB' },
  layerCard: {
    backgroundColor: '#FFF',
    padding: 20,
    margin: 16,
    borderRadius: 12,
    borderLeftWidth: 4,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  layerIcon: { fontSize: 32, marginBottom: 8 },
  layerName: { fontSize: 18, fontWeight: 'bold', color: '#111827', marginBottom: 8 },
  layerData: { marginTop: 8 },
  layerInfo: { fontSize: 14, color: '#6B7280', marginTop: 4 },
});
