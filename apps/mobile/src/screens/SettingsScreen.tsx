import React from 'react';
import { View, Text, StyleSheet, ScrollView, Linking } from 'react-native';

export default function SettingsScreen() {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.card}>
        <Text style={styles.cardTitle}>About LUCA Network</Text>
        <Text style={styles.infoText}>
          Living Universal Cognition Array - A self-evolving mesh network with
          consciousness integration.
        </Text>
        <Text style={styles.version}>Version 1.0.0</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Layers</Text>
        <Text style={styles.layerText}>🌌 Layer 0: Root Kernel</Text>
        <Text style={styles.layerText}>🔮 Layer 10: DS-STAR Quantum</Text>
        <Text style={styles.layerText}>🧬 Layer 11: Multimodal Metabolism</Text>
        <Text style={styles.layerText}>🧬 Layer 12: Evolutionary Consensus</Text>
      </View>

      <View style={styles.card}>
        <Text style={styles.cardTitle}>Copyright</Text>
        <Text style={styles.copyrightText}>
          © 2025 LUCA Network{'\n'}
          Open Source. Built with 💜 by the LUCA Community.{'\n\n'}
          Copyright © Lennart Wuchold{'\n'}
          (geboren am 28.02.2000 in 01744 Dippoldiswalde)
        </Text>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#F9FAFB' },
  card: {
    backgroundColor: '#FFF',
    borderRadius: 12,
    padding: 20,
    marginHorizontal: 16,
    marginTop: 16,
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
  infoText: { fontSize: 14, color: '#6B7280', lineHeight: 20, marginBottom: 12 },
  version: { fontSize: 12, color: '#9CA3AF', marginTop: 8 },
  layerText: { fontSize: 14, color: '#374151', marginBottom: 8 },
  copyrightText: { fontSize: 12, color: '#6B7280', lineHeight: 18 },
});
