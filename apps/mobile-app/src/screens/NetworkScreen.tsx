import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  RefreshControl,
  ActivityIndicator,
} from 'react-native';
import { useLUCAConnection } from '../hooks/useLUCAConnection';

export default function NetworkScreen() {
  const { status, isConnected, isLoading, refresh } = useLUCAConnection();
  const [refreshing, setRefreshing] = React.useState(false);

  const onRefresh = React.useCallback(async () => {
    setRefreshing(true);
    await refresh();
    setRefreshing(false);
  }, [refresh]);

  if (isLoading) {
    return (
      <View style={styles.centerContainer}>
        <ActivityIndicator size="large" color="#9333EA" />
        <Text style={styles.loadingText}>Connecting to LUCA...</Text>
      </View>
    );
  }

  const healthPercentage = status ? (status.health * 100).toFixed(1) : '0';
  const healthyNodes = status
    ? status.nodes.filter((n) => n.health > 0.7).length
    : 0;

  return (
    <ScrollView
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Connection Status */}
      <View style={styles.statusBanner}>
        <View
          style={[
            styles.statusDot,
            { backgroundColor: isConnected ? '#10B981' : '#EF4444' },
          ]}
        />
        <Text style={styles.statusText}>
          {isConnected ? 'Connected to LUCA Backend' : 'Disconnected'}
        </Text>
      </View>

      {/* Network Health */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Network Health</Text>
        <View style={styles.progressBarContainer}>
          <View
            style={[
              styles.progressBar,
              { width: `${healthPercentage}%`, backgroundColor: '#10B981' },
            ]}
          />
        </View>
        <Text style={styles.percentageText}>{healthPercentage}%</Text>
      </View>

      {/* Quick Stats */}
      <View style={styles.statsGrid}>
        <View style={[styles.statCard, { backgroundColor: '#F3E8FF' }]}>
          <Text style={styles.statLabel}>Active Nodes</Text>
          <Text style={[styles.statValue, { color: '#9333EA' }]}>
            {status?.node_count || 0}
          </Text>
        </View>

        <View style={[styles.statCard, { backgroundColor: '#DBEAFE' }]}>
          <Text style={styles.statLabel}>Healthy Nodes</Text>
          <Text style={[styles.statValue, { color: '#3B82F6' }]}>
            {healthyNodes}
          </Text>
        </View>
      </View>

      {/* Node List */}
      <View style={styles.card}>
        <Text style={styles.cardTitle}>Connected Nodes</Text>
        {status?.nodes.map((node) => (
          <View key={node.id} style={styles.nodeItem}>
            <View style={styles.nodeInfo}>
              <View
                style={[
                  styles.nodeDot,
                  {
                    backgroundColor:
                      node.health > 0.8
                        ? '#10B981'
                        : node.health > 0.5
                        ? '#EAB308'
                        : '#EF4444',
                  },
                ]}
              />
              <Text style={styles.nodeId}>{node.id}</Text>
            </View>
            <Text style={styles.nodeHealth}>
              {(node.health * 100).toFixed(0)}%
            </Text>
          </View>
        ))}
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Text style={styles.footerText}>
          © 2025 LUCA Network
        </Text>
        <Text style={styles.copyrightText}>
          Copyright © Lennart Wuchold (geboren am 28.02.2000 in 01744 Dippoldiswalde)
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F9FAFB',
  },
  centerContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#F9FAFB',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: '#6B7280',
  },
  statusBanner: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#FFF',
    padding: 16,
    marginBottom: 16,
  },
  statusDot: {
    width: 12,
    height: 12,
    borderRadius: 6,
    marginRight: 8,
  },
  statusText: {
    fontSize: 14,
    color: '#374151',
  },
  card: {
    backgroundColor: '#FFF',
    borderRadius: 12,
    padding: 20,
    marginHorizontal: 16,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#111827',
    marginBottom: 12,
  },
  progressBarContainer: {
    height: 16,
    backgroundColor: '#E5E7EB',
    borderRadius: 8,
    overflow: 'hidden',
    marginBottom: 8,
  },
  progressBar: {
    height: '100%',
    borderRadius: 8,
  },
  percentageText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#6B7280',
    textAlign: 'right',
  },
  statsGrid: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    marginBottom: 16,
    gap: 16,
  },
  statCard: {
    flex: 1,
    borderRadius: 12,
    padding: 16,
  },
  statLabel: {
    fontSize: 12,
    color: '#6B7280',
    marginBottom: 4,
  },
  statValue: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  nodeItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: '#F3F4F6',
  },
  nodeInfo: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  nodeDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 12,
  },
  nodeId: {
    fontSize: 14,
    fontFamily: 'monospace',
    color: '#374151',
  },
  nodeHealth: {
    fontSize: 14,
    color: '#6B7280',
  },
  footer: {
    padding: 24,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#9CA3AF',
    marginBottom: 4,
  },
  copyrightText: {
    fontSize: 10,
    color: '#D1D5DB',
    textAlign: 'center',
  },
});
