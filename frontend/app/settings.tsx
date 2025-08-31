import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  StatusBar,
  Alert,
} from 'react-native';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';

export default function SettingsScreen() {
  const [currentLevel, setCurrentLevel] = useState<string>('beginner');

  useEffect(() => {
    loadCurrentLevel();
  }, []);

  const loadCurrentLevel = async () => {
    try {
      const level = await AsyncStorage.getItem('user_experience_level');
      if (level) {
        setCurrentLevel(level);
      }
    } catch (error) {
      console.error('Error loading current level:', error);
    }
  };

  const updateExperienceLevel = async (newLevel: string) => {
    try {
      await AsyncStorage.setItem('user_experience_level', newLevel);
      
      // Also update backend
      const backendUrl = process.env.EXPO_PUBLIC_BACKEND_URL;
      await fetch(`${backendUrl}/api/user-preferences`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          experience_level: newLevel,
        }),
      });

      setCurrentLevel(newLevel);
      Alert.alert('Updated', `Experience level changed to ${newLevel}`);
    } catch (error) {
      console.error('Error updating experience level:', error);
      Alert.alert('Error', 'Failed to update experience level. Please try again.');
    }
  };

  const showAnalysisHistory = () => {
    // TODO: Implement analysis history
    Alert.alert('Coming Soon', 'Analysis history will be available in a future update.');
  };

  const resetOnboarding = () => {
    Alert.alert(
      'Reset Onboarding',
      'This will clear your preferences and show the onboarding screen again. Continue?',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Reset',
          onPress: async () => {
            try {
              await AsyncStorage.removeItem('user_experience_level');
              router.replace('/');
            } catch (error) {
              console.error('Error resetting onboarding:', error);
            }
          },
        },
      ]
    );
  };

  const showAbout = () => {
    Alert.alert(
      'About ChartAI',
      'ChartAI is a smart trading assistant that uses AI to analyze financial charts and provide educational insights.\n\nVersion: 1.0.0\n\nThis app is for educational purposes only and does not provide financial advice.',
      [{ text: 'OK' }]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1a1a2e" />
      
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity 
          style={styles.backButton}
          onPress={() => router.back()}
        >
          <Ionicons name="arrow-back" size={24} color="#ffffff" />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Settings</Text>
        <View style={styles.placeholder} />
      </View>

      <ScrollView style={styles.scrollContainer} showsVerticalScrollIndicator={false}>
        {/* Experience Level Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Experience Level</Text>
          <Text style={styles.sectionDescription}>
            Change how detailed the analysis explanations should be
          </Text>
          
          <View style={styles.optionsContainer}>
            <TouchableOpacity
              style={[
                styles.optionItem,
                currentLevel === 'beginner' && styles.selectedOption,
              ]}
              onPress={() => updateExperienceLevel('beginner')}
            >
              <View style={styles.optionContent}>
                <Ionicons 
                  name="school" 
                  size={20} 
                  color={currentLevel === 'beginner' ? '#00d4aa' : '#8892b0'} 
                />
                <View style={styles.optionText}>
                  <Text style={[
                    styles.optionTitle,
                    currentLevel === 'beginner' && styles.selectedOptionText,
                  ]}>
                    Beginner
                  </Text>
                  <Text style={styles.optionSubtitle}>
                    Simple explanations and basic patterns
                  </Text>
                </View>
              </View>
              {currentLevel === 'beginner' && (
                <Ionicons name="checkmark" size={20} color="#00d4aa" />
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.optionItem,
                currentLevel === 'intermediate' && styles.selectedOption,
              ]}
              onPress={() => updateExperienceLevel('intermediate')}
            >
              <View style={styles.optionContent}>
                <Ionicons 
                  name="bar-chart" 
                  size={20} 
                  color={currentLevel === 'intermediate' ? '#00d4aa' : '#8892b0'} 
                />
                <View style={styles.optionText}>
                  <Text style={[
                    styles.optionTitle,
                    currentLevel === 'intermediate' && styles.selectedOptionText,
                  ]}>
                    Intermediate
                  </Text>
                  <Text style={styles.optionSubtitle}>
                    Detailed analysis with moderate complexity
                  </Text>
                </View>
              </View>
              {currentLevel === 'intermediate' && (
                <Ionicons name="checkmark" size={20} color="#00d4aa" />
              )}
            </TouchableOpacity>

            <TouchableOpacity
              style={[
                styles.optionItem,
                currentLevel === 'advanced' && styles.selectedOption,
              ]}
              onPress={() => updateExperienceLevel('advanced')}
            >
              <View style={styles.optionContent}>
                <Ionicons 
                  name="analytics" 
                  size={20} 
                  color={currentLevel === 'advanced' ? '#00d4aa' : '#8892b0'} 
                />
                <View style={styles.optionText}>
                  <Text style={[
                    styles.optionTitle,
                    currentLevel === 'advanced' && styles.selectedOptionText,
                  ]}>
                    Advanced
                  </Text>
                  <Text style={styles.optionSubtitle}>
                    Comprehensive analysis with advanced concepts
                  </Text>
                </View>
              </View>
              {currentLevel === 'advanced' && (
                <Ionicons name="checkmark" size={20} color="#00d4aa" />
              )}
            </TouchableOpacity>
          </View>
        </View>

        {/* App Features Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>App Features</Text>
          
          <TouchableOpacity style={styles.menuItem} onPress={showAnalysisHistory}>
            <Ionicons name="time-outline" size={20} color="#8892b0" />
            <Text style={styles.menuItemText}>Analysis History</Text>
            <Ionicons name="chevron-forward" size={16} color="#8892b0" />
          </TouchableOpacity>
        </View>

        {/* App Settings Section */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>App Settings</Text>
          
          <TouchableOpacity style={styles.menuItem} onPress={resetOnboarding}>
            <Ionicons name="refresh-outline" size={20} color="#8892b0" />
            <Text style={styles.menuItemText}>Reset Onboarding</Text>
            <Ionicons name="chevron-forward" size={16} color="#8892b0" />
          </TouchableOpacity>

          <TouchableOpacity style={styles.menuItem} onPress={showAbout}>
            <Ionicons name="information-circle-outline" size={20} color="#8892b0" />
            <Text style={styles.menuItemText}>About ChartAI</Text>
            <Ionicons name="chevron-forward" size={16} color="#8892b0" />
          </TouchableOpacity>
        </View>

        {/* Disclaimer */}
        <View style={styles.disclaimerContainer}>
          <Text style={styles.disclaimerText}>
            ChartAI provides educational analysis only. All trading decisions should be made 
            with careful consideration and proper risk management. This is not financial advice.
          </Text>
        </View>

        <View style={styles.bottomSpacer} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 24,
    paddingTop: 20,
    paddingBottom: 20,
  },
  backButton: {
    padding: 8,
  },
  headerTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#ffffff',
  },
  placeholder: {
    width: 40,
  },
  scrollContainer: {
    flex: 1,
    paddingHorizontal: 24,
  },
  section: {
    marginBottom: 32,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#ffffff',
    marginBottom: 8,
  },
  sectionDescription: {
    fontSize: 14,
    color: '#8892b0',
    marginBottom: 16,
    lineHeight: 20,
  },
  optionsContainer: {
    gap: 12,
  },
  optionItem: {
    backgroundColor: '#16213e',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderWidth: 1,
    borderColor: '#16213e',
  },
  selectedOption: {
    borderColor: '#00d4aa',
    backgroundColor: '#0f1419',
  },
  optionContent: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  optionText: {
    marginLeft: 12,
    flex: 1,
  },
  optionTitle: {
    fontSize: 16,
    fontWeight: '500',
    color: '#ffffff',
    marginBottom: 2,
  },
  selectedOptionText: {
    color: '#00d4aa',
  },
  optionSubtitle: {
    fontSize: 12,
    color: '#8892b0',
  },
  menuItem: {
    backgroundColor: '#16213e',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  menuItemText: {
    fontSize: 16,
    color: '#ffffff',
    flex: 1,
    marginLeft: 12,
  },
  disclaimerContainer: {
    backgroundColor: '#16213e',
    borderRadius: 12,
    padding: 16,
    marginBottom: 20,
  },
  disclaimerText: {
    fontSize: 12,
    color: '#8892b0',
    lineHeight: 16,
    textAlign: 'center',
  },
  bottomSpacer: {
    height: 40,
  },
});