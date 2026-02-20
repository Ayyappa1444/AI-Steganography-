# Fix and enhance the UI with all new features

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add imports for new modules
old_imports = '''# Import stego modules
from stego.image_stego import hide_message as hide_image_msg, extract_message as extract_image_msg
from stego.video_stego import hide_message_in_video, extract_message_from_video'''

new_imports = '''# Import stego modules
from stego.image_stego import hide_message as hide_image_msg, extract_message as extract_image_msg
from stego.video_stego import hide_message_in_video, extract_message_from_video

# Import enhanced AI modules
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from ai.steganalysis_models import EnhancedSteganalysis, DCTSteganography, PerformanceMetrics
    from ai.cnn_steganalysis import SteganalysisCNN, EnsembleDetector
    ENHANCED_AI_AVAILABLE = True
except ImportError:
    ENHANCED_AI_AVAILABLE = False
    print("Enhanced AI modules not available")'''

content = content.replace(old_imports, new_imports)

# 2. Update the task dropdown to include new methods
old_dropdown = '''        self.task_combo.addItems([
            "🔍 Steganalysis Detection",
            "📊 LSB Heatmap Analysis", 
            "📈 Statistical Analysis",
            "🎯 Confidence Evaluation",
            "🖼️ Full Analysis Report"
        ])'''

new_dropdown = '''        self.task_combo.addItems([
            "🔍 Steganalysis Detection",
            "📊 LSB Heatmap Analysis", 
            "📈 Statistical Analysis",
            "🎯 Confidence Evaluation",
            "🖼️ Full Analysis Report",
            "📐 Chi-Square Analysis",
            "📊 RS Analysis",
            "🔢 SPAM Features",
            "📉 PVD Analysis",
            "📊 Histogram Analysis",
            "🧠 CNN Detection",
            "🎯 Ensemble Detection"
        ])'''

content = content.replace(old_dropdown, new_dropdown)

# 3. Update the analyze_image_action to handle new methods
old_analyze = '''        # Analyze based on selected task
        if "Steganalysis" in selected_task:
            result_text, color, confidence, details = self.analyze_cnn_with_details_extended(self.ai_path)
        elif "LSB Heatmap" in selected_task:
            result_text, color, confidence, details = self.analyze_lsb_extended(self.ai_path)
        elif "Statistical" in selected_task:
            result_text, color, confidence, details = self.analyze_statistical_extended(self.ai_path)
        elif "Confidence" in selected_task:
            result_text, color, confidence, details = self.analyze_confidence_extended(self.ai_path)
        else:  # Full Analysis
            result_text, color, confidence, details = self.analyze_full_extended(self.ai_path)'''

new_analyze = '''        # Analyze based on selected task
        if "Chi-Square" in selected_task:
            result_text, color, confidence, details = self.analyze_chi_square(self.ai_path)
        elif "RS Analysis" in selected_task:
            result_text, color, confidence, details = self.analyze_rs(self.ai_path)
        elif "SPAM" in selected_task:
            result_text, color, confidence, details = self.analyze_spam(self.ai_path)
        elif "PVD" in selected_task:
            result_text, color, confidence, details = self.analyze_pvd(self.ai_path)
        elif "Histogram" in selected_task:
            result_text, color, confidence, details = self.analyze_histogram(self.ai_path)
        elif "CNN" in selected_task:
            result_text, color, confidence, details = self.analyze_cnn_method(self.ai_path)
        elif "Ensemble" in selected_task:
            result_text, color, confidence, details = self.analyze_ensemble(self.ai_path)
        elif "Steganalysis" in selected_task:
            result_text, color, confidence, details = self.analyze_cnn_with_details_extended(self.ai_path)
        elif "LSB Heatmap" in selected_task:
            result_text, color, confidence, details = self.analyze_lsb_extended(self.ai_path)
        elif "Statistical" in selected_task:
            result_text, color, confidence, details = self.analyze_statistical_extended(self.ai_path)
        elif "Confidence" in selected_task:
            result_text, color, confidence, details = self.analyze_confidence_extended(self.ai_path)
        else:  # Full Analysis
            result_text, color, confidence, details = self.analyze_full_extended(self.ai_path)'''

content = content.replace(old_analyze, new_analyze)

# 4. Add new analysis methods before analyze_image_action
insert_marker = '''    def analyze_image_action(self):'''

new_methods = '''    def analyze_chi_square(self, image_path):
        """Chi-Square Analysis"""
        try:
            if not ENHANCED_AI_AVAILABLE:
                return "❌ Enhanced modules not available", "#dc2626", 0, "Error"
            
            analyzer = EnhancedSteganalysis()
            result = analyzer.chi_square_analysis(image_path)
            
            prob = result.get('probability', 0)
            if prob > 50:
                status = "🔴 STEGO DETECTED"
                color = "#dc2626"
            else:
                status = "🟢 LIKELY CLEAN"
                color = "#16a34a"
            
            result_text = f"{status}\\n\\nChi-Square: {result.get('chi_square', 0):.2f}\\nProbability: {prob:.1f}%"
            details = f"""<b>📐 Chi-Square Analysis Report</b><br><br>
            <b>Chi-Square Value:</b> {result.get('chi_square', 0):.4f}<br>
            <b>Detection Probability:</b> {prob:.2f}%<br>
            <b>Even Pairs:</b> {result.get('even_pairs', 0)}<br>
            <b>Odd Pairs:</b> {result.get('odd_pairs', 0)}<br>
            <b>Interpretation:</b> {result.get('interpretation', 'N/A')}"""
            
            return result_text, color, prob, details
        except Exception as e:
            return f"❌ Error: {str(e)}", "#dc2626", 0, str(e)
    
    def analyze_rs(self, image_path):
        """RS Analysis"""
        try:
            if not ENHANCED_AI_AVAILABLE:
                return "❌ Enhanced modules not available", "#dc2626", 0, "Error"
            
            analyzer = EnhancedSteganalysis()
            result = analyzer.rs_analysis(image_path)
            
            prob = result.get('probability', 0)
            if prob > 50:
                status = "🔴 STEGO DETECTED"
                color = "#dc2626"
            else:
                status = "🟢 LIKELY CLEAN"
                color = "#16a34a"
            
            result_text = f"{status}\\n\\nRS Score: {result.get('rs_score', 0):.2f}\\nProbability: {prob:.1f}%"
            details = f"""<b>📊 RS Analysis Report</b><br><br>
            <b>RS Score:</b> {result.get('rs_score', 0):.4f}<br>
            <b>R Value:</b> {result.get('R', 0):.4f}<br>
            <b>S Value:</b> {result.get('S', 0):.4f}<br>
            <b>Detection Probability:</b> {prob:.2f}%<br>
            <b>Interpretation:</b> {result.get('interpretation', 'N/A')}"""
            
            return result_text, color, prob, details
        except Exception as e:
            return f"❌ Error: {str(e)}", "#dc2626", 0, str(e)
    
    def analyze_spam(self, image_path):
        """SPAM Features Analysis"""
        try:
            if not ENHANCED_AI_AVAILABLE:
                return "❌ Enhanced modules not available", "#dc2626", 0, "Error"
            
            analyzer = EnhancedSteganalysis()
            result = analyzer.spam_features(image_path)
            
            prob = result.get('probability', 0)
            if prob > 50:
                status = "🔴 STEGO DETECTED"
                color = "#dc2626"
            else:
                status = "🟢 LIKELY CLEAN"
                color = "#16a34a"
            
            result_text = f"{status}\\n\\nSPAM Score: {result.get('spam_score', 0):.2f}\\nProbability: {prob:.1f}%"
            details = f"""<b>🔢 SPAM Features Report</b><br><br>
            <b>SPAM Score:</b> {result.get('spam_score', 0):.4f}<br>
            <b>Mean (H):</b> {result.get('mean_horizontal', 0):.4f}<br>
            <b>Mean (V):</b> {result.get('mean_vertical', 0):.4f}<br>
            <b>Std (H):</b> {result.get('std_horizontal', 0):.4f}<br>
            <b>Std (V):</b> {result.get('std_vertical', 0):.4f}<br>
            <b>Detection Probability:</b> {prob:.2f}%<br>
            <b>Interpretation:</b> {result.get('interpretation', 'N/A')}"""
            
            return result_text, color, prob, details
        except Exception as e:
            return f"❌ Error: {str(e)}", "#dc2626", 0, str(e)
    
    def analyze_pvd(self, image_path):
        """PVD Analysis"""
        try:
            if not ENHANCED_AI_AVAILABLE:
                return "❌ Enhanced modules not available", "#dc2626", 0, "Error"
            
            analyzer = EnhancedSteganalysis()
            result = analyzer.pixel_value_difference(image_path)
            
            prob = result.get('probability', 0)
            if prob > 50:
                status = "🔴 STEGO DETECTED"
                color = "#dc2626"
            else:
                status = "🟢 LIKELY CLEAN"
                color = "#16a34a"
            
            result_text = f"{status}\\n\\nPVD Score: {result.get('pvd_score', 0):.2f}\\nProbability: {prob:.1f}%"
            details = f"""<b>📉 PVD Analysis Report</b><br><br>
            <b>PVD Score:</b> {result.get('pvd_score', 0):.4f}<br>
            <b>Mean Difference:</b> {result.get('mean_difference', 0):.4f}<br>
            <b>Std Difference:</b> {result.get('std_difference', 0):.4f}<br>
            <b>Entropy:</b> {result.get('entropy', 0):.4f}<br>
            <b>Detection Probability:</b> {prob:.2f}%<br>
            <b>Interpretation:</b> {result.get('interpretation', 'N/A')}"""
            
            return result_text, color, prob, details
        except Exception as e:
            return f"❌ Error: {str(e)}", "#dc2626", 0, str(e)
    
    def analyze_histogram(self, image_path):
        """Histogram Analysis"""
        try:
            if not ENHANCED_AI_AVAILABLE:
                return "❌ Enhanced modules not available", "#dc2626", 0, "Error"
            
            analyzer = EnhancedSteganalysis()
            result = analyzer.histogram_analysis(image_path)
            
            prob = result.get('probability', 0)
            if prob > 50:
                status = "🔴 STEGO DETECTED"
                color = "#dc2626"
            else:
                status = "🟢 LIKELY CLEAN"
                color = "#16a34a"
            
            result_text = f"{status}\\n\\nHistogram Score: {result.get('histogram_score', 0):.2f}\\nProbability: {prob:.1f}%"
            details = f"""<b>📊 Histogram Analysis Report</b><br><br>
            <b>Histogram Score:</b> {result.get('histogram_score', 0):.4f}<br>
            <b>Mean:</b> {result.get('mean', 0):.2f}<br>
            <b>Std Dev:</b> {result.get('std', 0):.2f}<br>
            <b>Smoothness:</b> {result.get('smoothness', 0):.4f}<br>
            <b>Entropy:</b> {result.get('entropy', 0):.4f}<br>
            <b>Chi-Square:</b> {result.get('chi_square', 0):.2f}<br>
            <b>Detection Probability:</b> {prob:.2f}%<br>
            <b>Interpretation:</b> {result.get('interpretation', 'N/A')}"""
            
            return result_text, color, prob, details
        except Exception as e:
            return f"❌ Error: {str(e)}", "#dc2626", 0, str(e)
    
    def analyze_cnn_method(self, image_path):
        """CNN-based Detection"""
        try:
            if not ENHANCED_AI_AVAILABLE:
                return "❌ Enhanced modules not available", "#dc2626", 0, "Error"
            
            cnn = SteganalysisCNN()
            result = cnn.predict(image_path)
            
            prob = result.get('probability', 0)
            if prob > 50:
                status = "🔴 STEGO DETECTED"
                color = "#dc2626"
            else:
                status = "🟢 LIKELY CLEAN"
                color = "#16a34a"
            
            result_text = f"{status}\\n\\nCNN Prediction: {prob:.1f}%\\nMethod: {result.get('method', 'N/A')}"
            details = f"""<b>🧠 CNN Steganalysis Report</b><br><br>
            <b>Detection Method:</b> {result.get('method', 'N/A')}<br>
            <b>Prediction Probability:</b> {prob:.2f}%<br>
            <b>Prediction:</b> {result.get('prediction', 'N/A')}<br>
            <b>Confidence:</b> {result.get('confidence', 0):.2f}%<br>
            <b>Note:</b> CNN-based detection uses deep learning for higher accuracy"""
            
            return result_text, color, prob, details
        except Exception as e:
            return f"❌ Error: {str(e)}", "#dc2626", 0, str(e)
    
    def analyze_ensemble(self, image_path):
        """Ensemble Detection - combines all methods"""
        try:
            if not ENHANCED_AI_AVAILABLE:
                return "❌ Enhanced modules not available", "#dc2626", 0, "Error"
            
            detector = EnsembleDetector()
            result = detector.detect(image_path)
            
            prob = result.get('ensemble_probability', 0)
            if prob > 50:
                status = "🔴 STEGO DETECTED"
                color = "#dc2626"
            else:
                status = "🟢 LIKELY CLEAN"
                color = "#16a34a"
            
            result_text = f"{status}\\n\\nEnsemble Probability: {prob:.1f}%\\nMethods Used: {result.get('methods_used', 0)}"
            details = f"""<b>🎯 Ensemble Detection Report</b><br><br>
            <b>Ensemble Probability:</b> {prob:.2f}%<br>
            <b>Prediction:</b> {result.get('prediction', 'N/A')}<br>
            <b>Confidence:</b> {result.get('confidence', 0):.2f}%<br>
            <b>Detection Methods Combined:</b> {result.get('methods_used', 0)}<br>
            <b><br>Note:</b> Ensemble combines CNN + Statistical methods for best accuracy"""
            
            return result_text, color, prob, details
        except Exception as e:
            return f"❌ Error: {str(e)}", "#dc2626", 0, str(e)

'''

content = content.replace(insert_marker, new_methods + insert_marker)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Enhanced UI created!")
print("- Added Chi-Square Analysis")
print("- Added RS Analysis")
print("- Added SPAM Features Analysis")
print("- Added PVD Analysis")
print("- Added Histogram Analysis")
print("- Added CNN Detection")
print("- Added Ensemble Detection")
print("- Updated dropdown with all new methods")
