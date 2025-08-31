import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  ScrollView,
  Alert,
  StatusBar,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';
import { router } from 'expo-router';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';

export default function OnboardingScreen() {
  const [selectedLevel, setSelectedLevel] = useState<string>('');
  const [hasOnboarded, setHasOnboarded] = useState<boolean>(false);

  useEffect(() => {
    checkOnboardingStatus();
  }, []);

  const checkOnboardingStatus = async () => {
    try {
      const level = await AsyncStorage.getItem('user_experience_level');
      if (level) {
        setHasOnboarded(true);
        // Navigate to main app
        router.replace('/upload');
      }
    } catch (error) {
      console.error('Error checking onboarding status:', error);
    }
  };

  const saveExperienceLevel = async () => {
    if (!selectedLevel) {
      Alert.alert('Selection Required', 'Please select your trading experience level.');
      return;
    }

    try {
      await AsyncStorage.setItem('user_experience_level', selectedLevel);
      
      // Also save to backend
      const backendUrl = process.env.EXPO_PUBLIC_BACKEND_URL;
      await fetch(`${backendUrl}/api/user-preferences`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          experience_level: selectedLevel,
        }),
      });

      // Navigate to main app
      router.replace('/upload');
    } catch (error) {
      console.error('Error saving experience level:', error);
      Alert.alert('Error', 'Failed to save your preferences. Please try again.');
    }
  };

  if (hasOnboarded) {
    return (
      <View style={styles.loadingContainer}>
        <Text style={styles.loadingText}>Loading...</Text>
      </View>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1a1a2e" />
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardContainer}
      >
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          <View style={styles.header}>
            <View style={styles.logoContainer}>
              <Ionicons name="trending-up" size={50} color="#00d4aa" />
            </View>
            <Text style={styles.title}>Welcome to ChartAI</Text>
            <Text style={styles.subtitle}>Smart Trading Assistant</Text>
          </View>

          <View style={styles.contentContainer}>
            <Text style={styles.questionText}>
              What's your trading experience level?
            </Text>
            <Text style={styles.descriptionText}>
              This helps us provide explanations tailored to your knowledge level.
            </Text>

            <View style={styles.optionsContainer}>
              <TouchableOpacity
                style={[
                  styles.optionCard,
                  selectedLevel === 'beginner' && styles.selectedOption,
                ]}
                onPress={() => setSelectedLevel('beginner')}
              >
                <View style={styles.optionHeader}>
                  <Ionicons 
                    name="school" 
                    size={24} 
                    color={selectedLevel === 'beginner' ? '#00d4aa' : '#8892b0'} 
                  />
                  <Text style={[
                    styles.optionTitle,
                    selectedLevel === 'beginner' && styles.selectedOptionText,
                  ]}>
                    Beginner
                  </Text>
                </View>
                <Text style={[
                  styles.optionDescription,
                  selectedLevel === 'beginner' && styles.selectedOptionDescription,
                ]}>
                  New to trading or technical analysis. Simple explanations and basic patterns.
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[
                  styles.optionCard,
                  selectedLevel === 'intermediate' && styles.selectedOption,
                ]}
                onPress={() => setSelectedLevel('intermediate')}
              >
                <View style={styles.optionHeader}>
                  <Ionicons 
                    name="bar-chart" 
                    size={24} 
                    color={selectedLevel === 'intermediate' ? '#00d4aa' : '#8892b0'} 
                  />
                  <Text style={[
                    styles.optionTitle,
                    selectedLevel === 'intermediate' && styles.selectedOptionText,
                  ]}>
                    Intermediate
                  </Text>
                </View>
                <Text style={[
                  styles.optionDescription,
                  selectedLevel === 'intermediate' && styles.selectedOptionDescription,
                ]}>
                  Some trading experience. Detailed analysis with moderate complexity.
                </Text>
              </TouchableOpacity>

              <TouchableOpacity
                style={[
                  styles.optionCard,
                  selectedLevel === 'advanced' && styles.selectedOption,
                ]}
                onPress={() => setSelectedLevel('advanced')}
              >
                <View style={styles.optionHeader}>
                  <Ionicons 
                    name="analytics" 
                    size={24} 
                    color={selectedLevel === 'advanced' ? '#00d4aa' : '#8892b0'} 
                  />
                  <Text style={[
                    styles.optionTitle,
                    selectedLevel === 'advanced' && styles.selectedOptionText,
                  ]}>
                    Advanced
                  </Text>
                </View>
                <Text style={[
                  styles.optionDescription,
                  selectedLevel === 'advanced' && styles.selectedOptionDescription,
                ]}>
                  Experienced trader. Comprehensive analysis with advanced concepts.
                </Text>
              </TouchableOpacity>
            </View>
          </View>

          <View style={styles.footer}>
            <TouchableOpacity
              style={[
                styles.continueButton,
                !selectedLevel && styles.disabledButton,
              ]}
              onPress={saveExperienceLevel}
              disabled={!selectedLevel}
            >
              <Text style={[
                styles.continueButtonText,
                !selectedLevel && styles.disabledButtonText,
              ]}>
                Continue
              </Text>
            </TouchableOpacity>

            <Text style={styles.disclaimerText}>
              All analysis provided is for educational purposes only and is not financial advice.
            </Text>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1a1a2e',
  },
  keyboardContainer: {
    flex: 1,
  },
  scrollContainer: {
    flexGrow: 1,
    paddingHorizontal: 24,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    backgroundColor: '#1a1a2e',
  },
  loadingText: {
    color: '#ffffff',
    fontSize: 18,
  },
  header: {
    alignItems: 'center',
    paddingTop: 40,
    paddingBottom: 20,
  },
  logoContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    backgroundColor: '#16213e',
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 20,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 8,
  },
  subtitle: {
    fontSize: 18,
    color: '#8892b0',
    textAlign: 'center',
  },
  contentContainer: {
    flex: 1,
    paddingVertical: 20,
  },
  questionText: {
    fontSize: 24,
    fontWeight: '600',
    color: '#ffffff',
    textAlign: 'center',
    marginBottom: 8,
  },
  descriptionText: {
    fontSize: 16,
    color: '#8892b0',
    textAlign: 'center',
    marginBottom: 32,
    lineHeight: 22,
  },
  optionsContainer: {
    gap: 16,
  },
  optionCard: {
    backgroundColor: '#16213e',
    borderRadius: 16,
    padding: 20,
    borderWidth: 2,
    borderColor: '#16213e',
  },
  selectedOption: {
    borderColor: '#00d4aa',
    backgroundColor: '#0f1419',
  },
  optionHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  optionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#ffffff',
    marginLeft: 12,
  },
  selectedOptionText: {
    color: '#00d4aa',
  },
  optionDescription: {
    fontSize: 14,
    color: '#8892b0',
    lineHeight: 20,
    marginLeft: 36,
  },
  selectedOptionDescription: {
    color: '#a8b2d1',
  },
  footer: {
    paddingBottom: 20,
  },
  continueButton: {
    backgroundColor: '#00d4aa',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginBottom: 20,
  },
  disabledButton: {
    backgroundColor: '#2a2a4e',
  },
  continueButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: '600',
  },
  disabledButtonText: {
    color: '#8892b0',
  },
  disclaimerText: {
    fontSize: 12,
    color: '#8892b0',
    textAlign: 'center',
    lineHeight: 16,
  },
});