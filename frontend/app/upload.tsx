import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  SafeAreaView,
  Alert,
  StatusBar,
  KeyboardAvoidingView,
  Platform,
  Image,
  ActivityIndicator,
  ScrollView,
} from 'react-native';
import { router } from 'expo-router';
import * as ImagePicker from 'expo-image-picker';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Ionicons } from '@expo/vector-icons';

export default function UploadScreen() {
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState<boolean>(false);
  const [experienceLevel, setExperienceLevel] = useState<string>('beginner');

  useEffect(() => {
    loadUserPreferences();
    requestPermissions();
  }, []);

  const loadUserPreferences = async () => {
    try {
      const level = await AsyncStorage.getItem('user_experience_level');
      if (level) {
        setExperienceLevel(level);
      } else {
        // Redirect to onboarding if no preferences found
        router.replace('/');
      }
    } catch (error) {
      console.error('Error loading user preferences:', error);
    }
  };

  const requestPermissions = async () => {
    // Request camera permissions
    const { status } = await ImagePicker.requestCameraPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission Required', 'Camera permission is required to take photos.');
    }

    // Request media library permissions
    const mediaStatus = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (mediaStatus.status !== 'granted') {
      Alert.alert('Permission Required', 'Gallery access is required to select photos.');
    }
  };

  // Removed showImagePicker function - now using direct button actions

  const takePhoto = async () => {
    try {
      const result = await ImagePicker.launchCameraAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
        base64: true,
      });

      if (!result.canceled && result.assets[0]) {
        const asset = result.assets[0];
        if (asset.base64) {
          setSelectedImage(asset.base64);
        } else {
          Alert.alert('Error', 'Failed to process the image. Please try again.');
        }
      }
    } catch (error) {
      console.error('Error taking photo:', error);
      Alert.alert('Error', 'Failed to take photo. Please try again.');
    }
  };

  const pickImage = async () => {
    try {
      const result = await ImagePicker.launchImageLibraryAsync({
        mediaTypes: ImagePicker.MediaTypeOptions.Images,
        allowsEditing: true,
        aspect: [4, 3],
        quality: 0.8,
        base64: true,
      });

      if (!result.canceled && result.assets[0]) {
        const asset = result.assets[0];
        if (asset.base64) {
          setSelectedImage(asset.base64);
        } else {
          Alert.alert('Error', 'Failed to process the image. Please try again.');
        }
      }
    } catch (error) {
      console.error('Error picking image:', error);
      Alert.alert('Error', 'Failed to pick image. Please try again.');
    }
  };

  const analyzeChart = async () => {
    if (!selectedImage) {
      Alert.alert('No Image', 'Please select a chart image first.');
      return;
    }

    setIsAnalyzing(true);

    try {
      const backendUrl = process.env.EXPO_PUBLIC_BACKEND_URL;
      const response = await fetch(`${backendUrl}/api/analyze-chart`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          image_base64: selectedImage,
          experience_level: experienceLevel,
        }),
      });

      if (!response.ok) {
        throw new Error(`Analysis failed: ${response.status}`);
      }

      const analysisResult = await response.json();

      // Store the result and navigate to results screen
      await AsyncStorage.setItem('latest_analysis', JSON.stringify(analysisResult));
      router.push('/results');

    } catch (error) {
      console.error('Error analyzing chart:', error);
      Alert.alert(
        'Analysis Failed', 
        'Failed to analyze the chart. Please check your internet connection and try again.'
      );
    } finally {
      setIsAnalyzing(false);
    }
  };

  const clearImage = () => {
    setSelectedImage(null);
  };

  const navigateToSettings = () => {
    router.push('/settings');
  };

  return (
    <SafeAreaView style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor="#1a1a2e" />
      <KeyboardAvoidingView 
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardContainer}
      >
        <ScrollView contentContainerStyle={styles.scrollContainer}>
          {/* Header */}
          <View style={styles.header}>
            <View style={styles.headerLeft}>
              <Ionicons name="trending-up" size={28} color="#00d4aa" />
              <Text style={styles.headerTitle}>ChartAI</Text>
            </View>
            <TouchableOpacity 
              style={styles.settingsButton}
              onPress={navigateToSettings}
            >
              <Ionicons name="settings-outline" size={24} color="#8892b0" />
            </TouchableOpacity>
          </View>

          {/* Experience Level Badge */}
          <View style={styles.experienceBadge}>
            <Ionicons 
              name={experienceLevel === 'beginner' ? 'school' : 
                   experienceLevel === 'intermediate' ? 'bar-chart' : 'analytics'} 
              size={16} 
              color="#00d4aa" 
            />
            <Text style={styles.experienceText}>
              {experienceLevel.charAt(0).toUpperCase() + experienceLevel.slice(1)} Mode
            </Text>
          </View>

          {/* Upload Area */}
          <View style={styles.uploadContainer}>
            {selectedImage ? (
              <View style={styles.imageContainer}>
                <Image
                  source={{ uri: `data:image/jpeg;base64,${selectedImage}` }}
                  style={styles.selectedImage}
                  resizeMode="contain"
                />
                <TouchableOpacity 
                  style={styles.clearImageButton}
                  onPress={clearImage}
                >
                  <Ionicons name="close-circle" size={24} color="#ff6b6b" />
                </TouchableOpacity>
              </View>
            ) : (
              <TouchableOpacity 
                style={styles.uploadButton}
                onPress={showImagePicker}
              >
                <Ionicons name="cloud-upload-outline" size={48} color="#00d4aa" />
                <Text style={styles.uploadText}>Upload Chart</Text>
                <Text style={styles.uploadSubtext}>
                  Take a photo or choose from gallery
                </Text>
              </TouchableOpacity>
            )}
          </View>

          {/* Instructions */}
          <View style={styles.instructionsContainer}>
            <Text style={styles.instructionsTitle}>How to get the best analysis:</Text>
            <View style={styles.instructionItem}>
              <Ionicons name="checkmark-circle" size={16} color="#00d4aa" />
              <Text style={styles.instructionText}>
                Ensure the chart is clear and well-lit
              </Text>
            </View>
            <View style={styles.instructionItem}>
              <Ionicons name="checkmark-circle" size={16} color="#00d4aa" />
              <Text style={styles.instructionText}>
                Include price axis and time axis if visible
              </Text>
            </View>
            <View style={styles.instructionItem}>
              <Ionicons name="checkmark-circle" size={16} color="#00d4aa" />
              <Text style={styles.instructionText}>
                Avoid reflections or obstructions
              </Text>
            </View>
          </View>

          {/* Analyze Button */}
          <TouchableOpacity
            style={[
              styles.analyzeButton,
              (!selectedImage || isAnalyzing) && styles.disabledButton,
            ]}
            onPress={analyzeChart}
            disabled={!selectedImage || isAnalyzing}
          >
            {isAnalyzing ? (
              <View style={styles.loadingContainer}>
                <ActivityIndicator size="small" color="#ffffff" />
                <Text style={styles.analyzeButtonText}>Analyzing...</Text>
              </View>
            ) : (
              <Text style={[
                styles.analyzeButtonText,
                (!selectedImage) && styles.disabledButtonText,
              ]}>
                Analyze Chart
              </Text>
            )}
          </TouchableOpacity>

          {/* Footer Disclaimer */}
          <View style={styles.footer}>
            <Text style={styles.disclaimerText}>
              ⚠️ This analysis is for educational purposes only and is not financial advice.
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
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingTop: 20,
    paddingBottom: 20,
  },
  headerLeft: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    color: '#ffffff',
    marginLeft: 8,
  },
  settingsButton: {
    padding: 8,
  },
  experienceBadge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#16213e',
    borderRadius: 20,
    paddingHorizontal: 12,
    paddingVertical: 6,
    alignSelf: 'flex-start',
    marginBottom: 24,
  },
  experienceText: {
    color: '#00d4aa',
    fontSize: 14,
    fontWeight: '500',
    marginLeft: 6,
  },
  uploadContainer: {
    flex: 1,
    minHeight: 250,
    marginBottom: 24,
  },
  uploadButton: {
    backgroundColor: '#16213e',
    borderRadius: 16,
    borderWidth: 2,
    borderColor: '#00d4aa',
    borderStyle: 'dashed',
    paddingVertical: 60,
    alignItems: 'center',
    justifyContent: 'center',
  },
  uploadText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: '600',
    marginTop: 12,
  },
  uploadSubtext: {
    color: '#8892b0',
    fontSize: 14,
    marginTop: 4,
  },
  imageContainer: {
    position: 'relative',
    backgroundColor: '#16213e',
    borderRadius: 16,
    overflow: 'hidden',
  },
  selectedImage: {
    width: '100%',
    height: 250,
  },
  clearImageButton: {
    position: 'absolute',
    top: 10,
    right: 10,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    borderRadius: 12,
    padding: 4,
  },
  instructionsContainer: {
    backgroundColor: '#16213e',
    borderRadius: 12,
    padding: 16,
    marginBottom: 24,
  },
  instructionsTitle: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 12,
  },
  instructionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 8,
  },
  instructionText: {
    color: '#8892b0',
    fontSize: 14,
    marginLeft: 8,
    flex: 1,
  },
  analyzeButton: {
    backgroundColor: '#00d4aa',
    borderRadius: 12,
    paddingVertical: 16,
    alignItems: 'center',
    marginBottom: 20,
  },
  disabledButton: {
    backgroundColor: '#2a2a4e',
  },
  loadingContainer: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  analyzeButtonText: {
    color: '#ffffff',
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 8,
  },
  disabledButtonText: {
    color: '#8892b0',
  },
  footer: {
    paddingBottom: 20,
  },
  disclaimerText: {
    fontSize: 12,
    color: '#8892b0',
    textAlign: 'center',
    lineHeight: 16,
  },
});