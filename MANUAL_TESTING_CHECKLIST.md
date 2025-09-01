# ChartAI Manual Testing Checklist

## 📱 Frontend Testing

### Onboarding Flow
- [ ] App loads successfully on iOS and Android
- [ ] Welcome screen displays with proper branding
- [ ] Experience level selection works correctly
- [ ] All three levels (Beginner, Intermediate, Advanced) are selectable
- [ ] Selected level is highlighted properly
- [ ] "Continue" button works and saves preferences
- [ ] Navigation to upload screen works

### Upload Screen
- [ ] Header displays correctly with ChartAI branding
- [ ] Experience level badge shows correct level
- [ ] Instructions card displays helpful tips
- [ ] Camera permission request works
- [ ] "Take Photo" button opens camera successfully
- [ ] "Choose from Gallery" button opens photo library
- [ ] Selected image displays properly
- [ ] Clear image button works
- [ ] Analyze button is disabled when no image selected
- [ ] Analyze button becomes enabled after image selection
- [ ] Loading state shows during analysis
- [ ] Error handling works for network failures

### Results Screen
- [ ] Analysis results display properly
- [ ] Trading plan shows all fields (Entry, Exit, Stop Loss, Risk/Reward)
- [ ] Chart visualizations render correctly
- [ ] Risk/Reward pie chart displays when data available
- [ ] Price levels bar chart shows support/resistance counts
- [ ] Pattern detection list displays found patterns
- [ ] Support and resistance levels show with proper colors
- [ ] Trend analysis displays comprehensively
- [ ] Detailed explanation is readable and appropriate for user level
- [ ] Financial disclaimer is prominently displayed
- [ ] "Analyze Another" button works
- [ ] Back navigation works properly

### Settings Screen
- [ ] Settings screen loads correctly
- [ ] Experience level can be changed
- [ ] Changes are saved properly
- [ ] App info displays correctly
- [ ] Version number shows
- [ ] Disclaimer text is present

## 🧠 AI Analysis Testing

### Experience Level Differentiation
- [ ] **Beginner**: Simple explanations, basic terminology
- [ ] **Intermediate**: Moderate complexity, technical analysis terms
- [ ] **Advanced**: Comprehensive analysis, professional terminology
- [ ] Same chart produces different explanations for different levels
- [ ] Explanations are appropriate for target audience

### Chart Analysis Quality
- [ ] **Pattern Detection**: Identifies common patterns (triangles, head & shoulders, etc.)
- [ ] **Support Levels**: Identifies key price support areas
- [ ] **Resistance Levels**: Identifies key price resistance areas  
- [ ] **Trend Analysis**: Correctly identifies bullish/bearish/sideways trends
- [ ] **Trading Plan**: Provides realistic entry/exit/stop-loss levels
- [ ] **Risk/Reward**: Calculates reasonable risk-reward ratios

### Chart Types
Test with different chart types:
- [ ] Stock charts (daily, hourly timeframes)
- [ ] Cryptocurrency charts
- [ ] Forex charts
- [ ] Futures charts
- [ ] Charts with clear patterns
- [ ] Charts with support/resistance lines drawn
- [ ] Charts with volume indicators
- [ ] Blurry or poor quality images (should handle gracefully)

### Disclaimer Compliance
- [ ] Every analysis includes "not financial advice" disclaimer
- [ ] "Educational purposes only" is clearly stated
- [ ] Disclaimers are prominently displayed
- [ ] Legal compliance messaging is appropriate

## 🔧 Technical Testing

### Performance
- [ ] App launches quickly (< 3 seconds)
- [ ] Image upload is responsive
- [ ] AI analysis completes in reasonable time (< 30 seconds)
- [ ] Smooth scrolling in results
- [ ] No memory leaks during extended use
- [ ] Charts render smoothly

### Error Handling
- [ ] Network connection failures handled gracefully
- [ ] Invalid image formats rejected properly
- [ ] Server errors display user-friendly messages
- [ ] Retry mechanisms work
- [ ] App doesn't crash on errors

### Data Persistence
- [ ] User preferences persist between app sessions
- [ ] Latest analysis is saved and accessible
- [ ] App state is maintained during background/foreground transitions

### Cross-Platform Compatibility
- [ ] **iOS**: All features work on iPhone and iPad
- [ ] **Android**: All features work on various Android devices
- [ ] UI scales properly on different screen sizes
- [ ] Touch interactions work correctly
- [ ] Platform-specific UI guidelines followed

## 📊 Backend Testing

### API Endpoints
- [ ] `/api/health` - Health check works
- [ ] `/api/user-preferences` - User preferences CRUD operations
- [ ] `/api/analyze-chart` - Chart analysis endpoint
- [ ] Proper HTTP status codes returned
- [ ] Error responses include helpful messages
- [ ] API rate limiting (if implemented) works correctly

### Data Validation
- [ ] Image base64 validation works
- [ ] Experience level validation works
- [ ] Required fields are enforced
- [ ] Invalid requests return appropriate errors

### AI Integration
- [ ] AI service connectivity works
- [ ] Responses are properly formatted
- [ ] JSON parsing handles edge cases
- [ ] Fallback mechanisms work when AI service fails

## 🎯 User Experience Testing

### Usability
- [ ] App is intuitive for first-time users
- [ ] Navigation is logical and consistent
- [ ] Visual hierarchy guides user attention
- [ ] Loading states keep users informed
- [ ] Error messages are helpful, not technical
- [ ] Overall flow feels natural

### Accessibility
- [ ] Text is readable (contrast, size)
- [ ] Touch targets are appropriately sized
- [ ] App works with screen readers (if applicable)
- [ ] Color coding has text alternatives

### Content Quality
- [ ] All text is professional and error-free
- [ ] Technical explanations are accurate
- [ ] Disclaimers are legally appropriate
- [ ] Educational content is valuable

## 🔍 Edge Cases

### Image Quality
- [ ] Very large images (>5MB)
- [ ] Very small images (<100KB)
- [ ] Screenshots with UI elements
- [ ] Charts with poor lighting
- [ ] Charts with watermarks
- [ ] Multiple charts in one image
- [ ] Non-chart images (should be handled gracefully)

### Network Conditions
- [ ] Slow internet connection
- [ ] Intermittent connectivity
- [ ] Complete network failure
- [ ] Server maintenance/downtime

### Device Scenarios
- [ ] Low battery mode
- [ ] Low storage space
- [ ] Background app refresh disabled
- [ ] Airplane mode scenarios
- [ ] Device rotation (portrait/landscape)

## 📝 Test Results Documentation

For each test item:
- [ ] Mark as ✅ Pass, ❌ Fail, or ⚠️ Issue
- [ ] Note device/OS version tested
- [ ] Document any issues found
- [ ] Include screenshots for visual issues
- [ ] Rate severity: Critical/High/Medium/Low

## 🚀 Pre-Release Checklist

Before releasing to app stores:
- [ ] All critical tests pass
- [ ] No high-severity issues remain
- [ ] Performance meets standards
- [ ] Legal disclaimers reviewed
- [ ] App store metadata prepared
- [ ] Privacy policy updated
- [ ] Terms of service reviewed
- [ ] Beta testing completed with real users