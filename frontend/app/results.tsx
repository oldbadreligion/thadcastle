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

interface TradingPlan {
  entry_price?: string;
  exit_price?: string;
  stop_loss?: string;
  risk_reward_ratio?: string;
}

interface AnalysisResult {
  id: string;
  patterns_detected: string[];
  support_levels: string[];
  resistance_levels: string[];
  trend_analysis: string;
  trading_plan: TradingPlan;
  explanation: string;
  experience_level: string;
  created_at: string;
}

export default function ResultsScreen() {
  const [analysisResult, setAnalysisResult] = useState<AnalysisResult | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadAnalysisResult();
  }, []);

  const loadAnalysisResult = async () => {
    try {
      const resultJson = await AsyncStorage.getItem('latest_analysis');
      if (resultJson) {
        const result = JSON.parse(resultJson);
        setAnalysisResult(result);
      } else {
        Alert.alert('No Results', 'No analysis results found.', [
          { text: 'OK', onPress: () => router.replace('/upload') }
        ]);
      }
    } catch (error) {
      console.error('Error loading analysis result:', error);
      Alert.alert('Error', 'Failed to load analysis results.', [
        { text: 'OK', onPress: () => router.replace('/upload') }
      ]);
    } finally {
      setLoading(false);
    }
  };

  const analyzeAnother = () => {
    router.replace('/upload');
  };

  const shareResults = () => {
    // TODO: Implement sharing functionality
    Alert.alert('Share', 'Sharing functionality will be available in a future update.');
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>Loading results...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!analysisResult) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.loadingText}>No results found</Text>
        </View>
      </SafeAreaView>
    );
  }

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
        <Text style={styles.headerTitle}>Analysis Results</Text>
        <TouchableOpacity 
          style={styles.shareButton}
          onPress={shareResults}
        >
          <Ionicons name="share-outline" size={24} color="#8892b0" />
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.scrollContainer} showsVerticalScrollIndicator={false}>
        {/* Trading Plan Card - Enhanced */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <Ionicons name="trending-up" size={20} color="#00d4aa" />
            <Text style={styles.cardTitle}>Trading Plan</Text>
          </View>
          <View style={styles.tradingPlanContainer}>
            <View style={styles.tradingPlanItem}>
              <Text style={styles.tradingPlanLabel}>📊 Entry Price</Text>
              <Text style={styles.tradingPlanValue}>
                {analysisResult.trading_plan.entry_price || 'Analysis needed'}
              </Text>
            </View>
            <View style={styles.tradingPlanItem}>
              <Text style={styles.tradingPlanLabel}>🎯 Exit Price</Text>
              <Text style={styles.tradingPlanValue}>
                {analysisResult.trading_plan.exit_price || 'Analysis needed'}
              </Text>
            </View>
            <View style={styles.tradingPlanItem}>
              <Text style={styles.tradingPlanLabel}>🛡️ Stop Loss</Text>
              <Text style={styles.tradingPlanValue}>
                {analysisResult.trading_plan.stop_loss || 'Analysis needed'}
              </Text>
            </View>
            <View style={styles.tradingPlanItem}>
              <Text style={styles.tradingPlanLabel}>⚖️ Risk/Reward</Text>
              <Text style={styles.tradingPlanValue}>
                {analysisResult.trading_plan.risk_reward_ratio || 'Analysis needed'}
              </Text>
            </View>
          </View>
        </View>

        {/* Patterns Detected */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <Ionicons name="analytics" size={20} color="#00d4aa" />
            <Text style={styles.cardTitle}>Patterns Detected</Text>
          </View>
          <View style={styles.listContainer}>
            {analysisResult.patterns_detected.length > 0 ? (
              analysisResult.patterns_detected.map((pattern, index) => (
                <View key={index} style={styles.listItem}>
                  <Ionicons name="checkmark-circle" size={16} color="#00d4aa" />
                  <Text style={styles.listText}>{pattern}</Text>
                </View>
              ))
            ) : (
              <Text style={styles.noDataText}>No specific patterns detected</Text>
            )}
          </View>
        </View>

        {/* Support & Resistance */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <Ionicons name="bar-chart" size={20} color="#00d4aa" />
            <Text style={styles.cardTitle}>Support & Resistance</Text>
          </View>
          <View style={styles.levelsContainer}>
            <View style={styles.levelSection}>
              <Text style={styles.levelSectionTitle}>Support Levels</Text>
              {analysisResult.support_levels.length > 0 ? (
                analysisResult.support_levels.map((level, index) => (
                  <View key={index} style={styles.levelItem}>
                    <View style={[styles.levelIndicator, { backgroundColor: '#00d4aa' }]} />
                    <Text style={styles.levelText}>{level}</Text>
                  </View>
                ))
              ) : (
                <Text style={styles.noDataText}>No support levels identified</Text>
              )}
            </View>
            <View style={styles.levelSection}>
              <Text style={styles.levelSectionTitle}>Resistance Levels</Text>
              {analysisResult.resistance_levels.length > 0 ? (
                analysisResult.resistance_levels.map((level, index) => (
                  <View key={index} style={styles.levelItem}>
                    <View style={[styles.levelIndicator, { backgroundColor: '#ff6b6b' }]} />
                    <Text style={styles.levelText}>{level}</Text>
                  </View>
                ))
              ) : (
                <Text style={styles.noDataText}>No resistance levels identified</Text>
              )}
            </View>
          </View>
        </View>

        {/* Trend Analysis */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <Ionicons name="trending-up" size={20} color="#00d4aa" />
            <Text style={styles.cardTitle}>Trend Analysis</Text>
          </View>
          <Text style={styles.trendText}>
            {analysisResult.trend_analysis || 'No trend analysis available'}
          </Text>
        </View>

        {/* Detailed Explanation */}
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <Ionicons name="information-circle" size={20} color="#00d4aa" />
            <Text style={styles.cardTitle}>Detailed Explanation</Text>
          </View>
          <Text style={styles.explanationText}>
            {analysisResult.explanation}
          </Text>
        </View>

        {/* Disclaimer */}
        <View style={styles.disclaimerCard}>
          <Ionicons name="warning" size={20} color="#ff9800" />
          <Text style={styles.disclaimerText}>
            This analysis is for educational purposes only and is not financial advice. 
            Always do your own research and consider consulting with a financial advisor.
          </Text>
        </View>

        {/* Action Buttons */}
        <View style={styles.actionButtons}>
          <TouchableOpacity style={styles.analyzeAnotherButton} onPress={analyzeAnother}>
            <Ionicons name="camera" size={20} color="#ffffff" />
            <Text style={styles.analyzeAnotherText}>Analyze Another Chart</Text>
          </TouchableOpacity>
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    color: '#ffffff',
    fontSize: 18,
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
  shareButton: {
    padding: 8,
  },
  scrollContainer: {
    flex: 1,
    paddingHorizontal: 24,
  },
  card: {
    backgroundColor: '#16213e',
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  cardTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: '#ffffff',
    marginLeft: 8,
  },
  tradingPlanContainer: {
    gap: 12,
  },
  tradingPlanGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    justifyContent: 'space-between',
  },
  tradingPlanItem: {
    width: '48%',
    backgroundColor: '#1a1a2e',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
  },
  tradingPlanLabel: {
    fontSize: 12,
    color: '#8892b0',
    marginBottom: 4,
  },
  tradingPlanValue: {
    fontSize: 16,
    fontWeight: '600',
    color: '#ffffff',
  },
  listContainer: {
    gap: 12,
  },
  listItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  listText: {
    fontSize: 14,
    color: '#ffffff',
    marginLeft: 8,
    flex: 1,
  },
  noDataText: {
    fontSize: 14,
    color: '#8892b0',
    fontStyle: 'italic',
  },
  levelsContainer: {
    gap: 16,
  },
  levelSection: {
    gap: 8,
  },
  levelSectionTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: '#ffffff',
    marginBottom: 4,
  },
  levelItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  levelIndicator: {
    width: 8,
    height: 8,
    borderRadius: 4,
    marginRight: 12,
  },
  levelText: {
    fontSize: 14,
    color: '#ffffff',
  },
  trendText: {
    fontSize: 14,
    color: '#ffffff',
    lineHeight: 20,
  },
  explanationText: {
    fontSize: 14,
    color: '#ffffff',
    lineHeight: 22,
  },
  disclaimerCard: {
    backgroundColor: '#2a1f1a',
    borderRadius: 12,
    padding: 16,
    flexDirection: 'row',
    marginBottom: 24,
    borderLeftWidth: 4,
    borderLeftColor: '#ff9800',
  },
  disclaimerText: {
    fontSize: 12,
    color: '#ff9800',
    marginLeft: 12,
    flex: 1,
    lineHeight: 16,
  },
  actionButtons: {
    gap: 12,
  },
  analyzeAnotherButton: {
    backgroundColor: '#00d4aa',
    borderRadius: 12,
    paddingVertical: 16,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
  },
  analyzeAnotherText: {
    color: '#ffffff',
    fontSize: 16,
    fontWeight: '600',
    marginLeft: 8,
  },
  bottomSpacer: {
    height: 40,
  },
});