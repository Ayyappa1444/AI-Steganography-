# Fix graphs to display actual data

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the generate_analysis_graphs function to be more robust and display actual data
old_graph_func = '''    def generate_analysis_graphs(self, image_path, confidence):
        """Generate analysis graphs"""
        try:
            # Get stored analysis data
            data = getattr(self, 'last_analysis', None)
            if not data:
                return
            
            # Graph 1 - Confidence Gauge (bar chart)
            fig1, ax1 = plt.subplots(figsize=(3, 1.8))
            ax1.barh(['Confidence'], [confidence], color='#8b5cf6', height=0.4)
            ax1.barh(['Confidence'], [100-confidence], left=confidence, color='#374151', height=0.4)
            ax1.set_xlim(0, 100)
            ax1.set_title(f'Confidence: {confidence:.1f}%', fontsize=10, color='white')
            ax1.tick_params(colors='white', labelsize=8)
            ax1.spines['top'].set_visible(False)
            ax1.spines['right'].set_visible(False)
            ax1.spines['bottom'].set_color('white')
            ax1.spines['left'].set_visible(False)
            fig1.patch.set_facecolor('#1e293b')
            ax1.set_facecolor('#1e293b')
            ax1.tick_params(colors='white')
            plt.tight_layout()
            fig1.savefig('graph_confidence.png', dpi=80, bbox_inches='tight')
            plt.close(fig1)
            
            # Graph 2 - Pixel Distribution (histogram)
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            fig2, ax2 = plt.subplots(figsize=(3, 1.8))
            ax2.hist(img.flatten(), bins=50, color='#ef4444', alpha=0.7)
            ax2.set_title('Pixel Distribution', fontsize=10, color='white')
            ax2.tick_params(colors='white', labelsize=8)
            ax2.spines['top'].set_visible(False)
            ax2.spines['right'].set_visible(False)
            ax2.spines['bottom'].set_color('white')
            ax2.spines['left'].set_color('white')
            fig2.patch.set_facecolor('#1e293b')
            ax2.set_facecolor('#1e293b')
            ax2.tick_params(colors='white')
            plt.tight_layout()
            fig2.savefig('graph_distribution.png', dpi=80, bbox_inches='tight')
            plt.close(fig2)
            
            # Graph 3 - Model Statistics
            fig3, ax3 = plt.subplots(figsize=(3, 1.8))
            stats = ['Mean', 'Std', 'Min', 'Max']
            values = [data['mean']/255*100, data['std']/255*100, data['min']/255*100, data['max']/255*100]
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
            ax3.bar(stats, values, color=colors, width=0.6)
            ax3.set_title('Image Statistics (%)', fontsize=10, color='white')
            ax3.tick_params(colors='white', labelsize=8)
            ax3.spines['top'].set_visible(False)
            ax3.spines['right'].set_visible(False)
            ax3.spines['bottom'].set_color('white')
            ax3.spines['left'].set_color('white')
            fig3.patch.set_facecolor('#1e293b')
            ax3.set_facecolor('#1e293b')
            ax3.tick_params(colors='white')
            plt.tight_layout()
            fig3.savefig('graph_stats.png', dpi=80, bbox_inches='tight')
            plt.close(fig3)
            
            # Load and display graphs (BIG size for column layout)
            # Also update the text to show actual data values
            conf_pix = QPixmap('graph_confidence.png').scaled(480, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            dist_pix = QPixmap('graph_distribution.png').scaled(480, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            stats_pix = QPixmap('graph_stats.png').scaled(480, 120, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            # Update labels with images
            self.graph1_label.setPixmap(conf_pix)
            self.graph2_label.setPixmap(dist_pix)
            self.graph3_label.setPixmap(stats_pix)
            
        except Exception as e:
            print(f"Graph generation error: {e}")'''

new_graph_func = '''    def generate_analysis_graphs(self, image_path, confidence):
        """Generate analysis graphs - with actual data display"""
        try:
            # Get stored analysis data
            data = getattr(self, 'last_analysis', None)
            if not data:
                # If no stored data, analyze the image now
                img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    return
                h, w = img.shape
                lsb = img & 1
                zero_pct = np.mean(lsb == 0) * 100
                one_pct = np.mean(lsb == 1) * 100
                mean_val = np.mean(img)
                std_val = np.std(img)
                min_val = np.min(img)
                max_val = np.max(img)
                data = {
                    'confidence': confidence,
                    'zero_pct': zero_pct,
                    'one_pct': one_pct,
                    'mean': mean_val,
                    'std': std_val,
                    'min': min_val,
                    'max': max_val,
                    'width': w,
                    'height': h
                }
            
            # Read the image for pixel distribution
            img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            
            # Graph 1 - Confidence Gauge (horizontal bar chart)
            fig1, ax1 = plt.subplots(figsize=(5, 1.5))
            bars1 = ax1.barh(['Detection'], [confidence], color='#8b5cf6', height=0.5)
            ax1.barh(['Detection'], [100-confidence], left=confidence, color='#374151', height=0.5)
            ax1.set_xlim(0, 100)
            ax1.set_title(f'Confidence Score: {confidence:.1f}%', fontsize=12, color='white', fontweight='bold')
            ax1.set_xlabel('Percentage', fontsize=10, color='white')
            ax1.tick_params(colors='white', labelsize=9)
            for spine in ax1.spines.values():
                spine.set_color('white')
            fig1.patch.set_facecolor('#1e293b')
            ax1.set_facecolor('#1e293b')
            # Add value text
            ax1.text(confidence/2, 0, f'{confidence:.1f}%', ha='center', va='center', color='white', fontsize=10, fontweight='bold')
            plt.tight_layout()
            fig1.savefig('graph_confidence.png', dpi=100, bbox_inches='tight', facecolor='#1e293b')
            plt.close(fig1)
            
            # Graph 2 - Pixel Distribution (histogram)
            fig2, ax2 = plt.subplots(figsize=(5, 1.5))
            n, bins, patches = ax2.hist(img.flatten(), bins=50, color='#ef4444', alpha=0.8, edgecolor='white')
            ax2.set_title('Pixel Value Distribution', fontsize=12, color='white', fontweight='bold')
            ax2.set_xlabel('Pixel Value (0-255)', fontsize=10, color='white')
            ax2.set_ylabel('Frequency', fontsize=10, color='white')
            ax2.tick_params(colors='white', labelsize=9)
            for spine in ax2.spines.values():
                spine.set_color('white')
            fig2.patch.set_facecolor('#1e293b')
            ax2.set_facecolor('#1e293b')
            plt.tight_layout()
            fig2.savefig('graph_distribution.png', dpi=100, bbox_inches='tight', facecolor='#1e293b')
            plt.close(fig2)
            
            # Graph 3 - Model Statistics (vertical bar chart with values)
            fig3, ax3 = plt.subplots(figsize=(5, 1.5))
            stats_labels = ['Mean', 'Std Dev', 'Min', 'Max']
            stat_values = [data['mean'], data['std'], data['min'], data['max']]
            # Normalize to percentage for visualization
            stat_percentages = [v/255*100 for v in stat_values]
            colors = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444']
            bars = ax3.bar(stats_labels, stat_percentages, color=colors, width=0.6, edgecolor='white')
            ax3.set_title('Image Statistics', fontsize=12, color='white', fontweight='bold')
            ax3.set_ylabel('Value (% of 255)', fontsize=10, color='white')
            ax3.tick_params(colors='white', labelsize=9)
            for spine in ax3.spines.values():
                spine.set_color('white')
            # Add value labels on bars
            for bar, val, pct in zip(bars, stat_values, stat_percentages):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                        f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=9, fontweight='bold')
            fig3.patch.set_facecolor('#1e293b')
            ax3.set_facecolor('#1e293b')
            ax3.set_ylim(0, max(stat_percentages) * 1.2)
            plt.tight_layout()
            fig3.savefig('graph_stats.png', dpi=100, bbox_inches='tight', facecolor='#1e293b')
            plt.close(fig3)
            
            # Load and display graphs - LARGE size
            conf_pix = QPixmap('graph_confidence.png')
            dist_pix = QPixmap('graph_distribution.png')
            stats_pix = QPixmap('graph_stats.png')
            
            # Scale to fit the label areas
            conf_scaled = conf_pix.scaled(450, 130, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            dist_scaled = dist_pix.scaled(450, 130, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            stats_scaled = stats_pix.scaled(450, 130, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            
            # Update labels with graphs
            self.graph1_label.setPixmap(conf_scaled)
            self.graph2_label.setPixmap(dist_scaled)
            self.graph3_label.setPixmap(stats_scaled)
            
            print(f"Graphs generated successfully! Confidence: {confidence:.1f}%")
            
        except Exception as e:
            print(f"Graph generation error: {e}")
            import traceback
            traceback.print_exc()'''

content = content.replace(old_graph_func, new_graph_func)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Graphs display fixed!")
print("- Now generates actual data visualizations")
print("- Larger, more detailed graphs")
print("- Includes actual values in the charts")
