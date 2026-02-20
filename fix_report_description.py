# Fix the report tab to include detailed descriptions

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the analyze_image_action to include better report generation
old_analyze = '''        # Update all result displays
        self.result_label.setText(result_text)
        self.result_label.setStyleSheet(f"QLabel {{ font-size: 11px; font-weight: bold; padding: 8px; border-radius: 8px; background: {color}; color: white; }}")
        
        self.tab_result.setText(result_text)
        self.tab_result.setStyleSheet(f"QLabel {{ font-size: 14px; font-weight: bold; padding: 20px; border-radius: 10px; background: #0f172a; color: white; line-height: 1.6; }}")
        
        self.tab_report.setText(details)'''

new_analyze = '''        # Generate detailed description based on analysis
        description = self.generate_result_description(self.ai_path, confidence, selected_task)
        
        # Update all result displays
        self.result_label.setText(result_text)
        self.result_label.setStyleSheet(f"QLabel {{ font-size: 11px; font-weight: bold; padding: 8px; border-radius: 8px; background: {color}; color: white; }}")
        
        self.tab_result.setText(result_text + "\\n\\n" + description)
        self.tab_result.setStyleSheet(f"QLabel {{ font-size: 14px; font-weight: bold; padding: 20px; border-radius: 10px; background: #0f172a; color: white; line-height: 1.6; }}")
        
        # Combine details with description
        full_report = f"{description}<br><br>{details}"
        self.tab_report.setText(full_report)'''

content = content.replace(old_analyze, new_analyze)

# Add the generate_result_description method before analyze_image_action
# Find a good place to insert it
insert_marker = '''    def analyze_image_action(self):'''
new_method = '''    def generate_result_description(self, image_path, confidence, task_type):
        """Generate detailed description for analysis results"""
        try:
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            h, w = img.shape
            lsb = img & 1
            zero_pct = np.mean(lsb == 0) * 100
            one_pct = np.mean(lsb == 1) * 100
            mean_val = np.mean(img)
            std_val = np.std(img)
            
            # Determine result status
            if confidence > 70:
                status = "🔴 HIGH PROBABILITY OF STEGANOGRAPHY"
                interpretation = "This image shows strong indicators of hidden data. The LSB distribution deviates significantly from the expected 50/50 balance found in clean images."
                recommendation = "Recommendation: Further investigation recommended. The detected anomalies could indicate steganographic content or natural image variations."
            elif confidence > 40:
                status = "🟡 UNCERTAIN - FURTHER ANALYSIS NEEDED"
                interpretation = "The analysis shows moderate deviations in pixel statistics. This could indicate partial embedding or natural image characteristics."
                recommendation = "Recommendation: Try analyzing with different methods (LSB Analysis, Statistical Analysis) for more definitive results."
            else:
                status = "🟢 LIKELY CLEAN IMAGE"
                interpretation = "The image shows balanced LSB distribution consistent with natural图像. No significant statistical anomalies detected."
                recommendation = "Recommendation: This image appears to be clean, but note that some steganography methods may not be detectable by statistical analysis alone."
            
            description = f"""
<b>═══════════════════════════════════════════════════</b><br>
<b>📊 ANALYSIS RESULT DESCRIPTION</b><br>
<b>═══════════════════════════════════════════════════</b><br><br>

<b>🔍 Task Selected:</b> {task_type}<br>
<b>📐 Image Size:</b> {w} x {h} pixels<br><br>

<b>═══════════════════════════════════════════════════</b><br>
<b>🎯 DETECTION RESULT</b><br>
<b>═══════════════════════════════════════════════════</b><br>
<b>Status:</b> {status}<br>
<b>Confidence Score:</b> {confidence:.1f}%<br><br>

<b>═══════════════════════════════════════════════════</b><br>
<b>📈 STATISTICAL FINDINGS</b><br>
<b>═══════════════════════════════════════════════════</b><br>
<b>• LSB Distribution:</b> 0: {zero_pct:.1f}% | 1: {one_pct:.1f}%<br>
<b>• Deviation from 50/50:</b> {abs(zero_pct - 50):.2f}%<br>
<b>• Mean Pixel Value:</b> {mean_val:.2f}<br>
<b>• Standard Deviation:</b> {std_val:.2f}<br><br>

<b>═══════════════════════════════════════════════════</b><br>
<b>💡 INTERPRETATION</b><br>
<b>═══════════════════════════════════════════════════</b><br>
{interpretation}<br><br>

<b>═══════════════════════════════════════════════════</b><br>
<b>✅ RECOMMENDATION</b><br>
<b>═══════════════════════════════════════════════════</b><br>
{recommendation}
"""
            return description
        except Exception as e:
            return f"<b>Error generating description:</b> {str(e)}"

'''

content = content.replace(insert_marker, new_method + insert_marker)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Report description added!")
print("- Now shows detailed interpretation of results")
print("- Includes statistical findings with actual values")
print("- Provides interpretation and recommendations")
print("- Shows detection status with confidence score")
