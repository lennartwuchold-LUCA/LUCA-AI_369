/**
 * LUCA Mobile App
 * Copyright © 2025 Lennart Wuchold (geboren am 28.02.2000 in 01744 Dippoldiswalde)
 *
 * Living Universal Cognition Array - Mobile Application
 */

import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';

// Screens
import NetworkScreen from './src/screens/NetworkScreen';
import ConsciousnessScreen from './src/screens/ConsciousnessScreen';
import LayersScreen from './src/screens/LayersScreen';
import SettingsScreen from './src/screens/SettingsScreen';

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <StatusBar style="light" />
        <Tab.Navigator
          screenOptions={{
            headerStyle: {
              backgroundColor: '#9333EA',
            },
            headerTintColor: '#fff',
            headerTitleStyle: {
              fontWeight: 'bold',
            },
            tabBarActiveTintColor: '#9333EA',
            tabBarInactiveTintColor: 'gray',
          }}
        >
          <Tab.Screen
            name="Network"
            component={NetworkScreen}
            options={{
              tabBarLabel: 'Network',
              headerTitle: '🌐 LUCA Network',
            }}
          />
          <Tab.Screen
            name="Consciousness"
            component={ConsciousnessScreen}
            options={{
              tabBarLabel: 'Consciousness',
              headerTitle: '🌌 Consciousness',
            }}
          />
          <Tab.Screen
            name="Layers"
            component={LayersScreen}
            options={{
              tabBarLabel: 'Layers',
              headerTitle: '🧬 Layers',
            }}
          />
          <Tab.Screen
            name="Settings"
            component={SettingsScreen}
            options={{
              tabBarLabel: 'Settings',
              headerTitle: '⚙️ Settings',
            }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
