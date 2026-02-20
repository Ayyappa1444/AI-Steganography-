# Fix graphs to be bigger and more visible

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find and replace the graph label setFixedHeight to make them bigger
content = content.replace(
    'self.graph1_label.setFixedHeight(140)',
    'self.graph1_label.setFixedHeight(200)'
)
content = content.replace(
    'self.graph2_label.setFixedHeight(140)',
    'self.graph2_label.setFixedHeight(200)'
)
content = content.replace(
    'self.graph3_label.setFixedHeight(140)',
    'self.graph3_label.setFixedHeight(200)'
)

# Now update the generate_analysis_graphs function to create bigger graphs
old_scaling = '''            # Scale to fit the label areas
            conf_scaled = conf_pix.scaled(450, 130, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            dist_scaled = dist_pix.scaled(450, 130, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            stats_scaled = stats_pix.scaled(450, 130, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)'''

new_scaling = '''            # Scale to fit the label areas - BIGGER SIZE
            conf_scaled = conf_pix.scaled(700, 190, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            dist_scaled = dist_pix.scaled(700, 190, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            stats_scaled = stats_pix.scaled(700, 190, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)'''

content = content.replace(old_scaling, new_scaling)

# Also update the matplotlib figure sizes for bigger graphs
content = content.replace(
    "fig1, ax1 = plt.subplots(figsize=(5, 1.5))",
    "fig1, ax1 = plt.subplots(figsize=(8, 3))"
)
content = content.replace(
    "fig2, ax2 = plt.subplots(figsize=(5, 1.5))",
    "fig2, ax2 = plt.subplots(figsize=(8, 3))"
)
content = content.replace(
    "fig3, ax3 = plt.subplots(figsize=(5, 1.5))",
    "fig3, ax3 = plt.subplots(figsize=(8, 3))"
)

# Also increase DPI for clearer graphs
content = content.replace(
    "fig1.savefig('graph_confidence.png', dpi=100, bbox_inches='tight', facecolor='#1e293b')",
    "fig1.savefig('graph_confidence.png', dpi=150, bbox_inches='tight', facecolor='#1e293b')"
)
content = content.replace(
    "fig2.savefig('graph_distribution.png', dpi=100, bbox_inches='tight', facecolor='#1e293b')",
    "fig2.savefig('graph_distribution.png', dpi=150, bbox_inches='tight', facecolor='#1e293b')"
)
content = content.replace(
    "fig3.savefig('graph_stats.png', dpi=100, bbox_inches='tight', facecolor='#1e293b')",
    "fig3.savefig('graph_stats.png', dpi=150, bbox_inches='tight', facecolor='#1e293b')"
)

# Also increase font sizes for better readability
content = content.replace(
    "ax1.set_title(f'Confidence Score: {confidence:.1f}%', fontsize=12, color='white', fontweight='bold')",
    "ax1.set_title(f'Confidence Score: {confidence:.1f}%', fontsize=16, color='white', fontweight='bold')"
)
content = content.replace(
    "ax2.set_title('Pixel Value Distribution', fontsize=12, color='white', fontweight='bold')",
    "ax2.set_title('Pixel Value Distribution (Histogram)', fontsize=16, color='white', fontweight='bold')"
)
content = content.replace(
    "ax3.set_title('Image Statistics', fontsize=12, color='white', fontweight='bold')",
    "ax3.set_title('Image Statistics (Mean, Std, Min, Max)', fontsize=16, color='white', fontweight='bold')"
)

# Increase axis label sizes
content = content.replace(
    "ax1.set_xlabel('Percentage', fontsize=10, color='white')",
    "ax1.set_xlabel('Percentage', fontsize=14, color='white')"
)
content = content.replace(
    "ax2.set_xlabel('Pixel Value (0-255)', fontsize=10, color='white')",
    "ax2.set_xlabel('Pixel Value (0-255)', fontsize=14, color='white')"
)
content = content.replace(
    "ax2.set_ylabel('Frequency', fontsize=10, color='white')",
    "ax2.set_ylabel('Frequency (Count)', fontsize=14, color='white')"
)
content = content.replace(
    "ax3.set_ylabel('Value (% of 255)', fontsize=10, color='white')",
    "ax3.set_ylabel('Value (Normalized to %)', fontsize=14, color='white')"
)

# Increase tick sizes
content = content.replace(
    "ax1.tick_params(colors='white', labelsize=9)",
    "ax1.tick_params(colors='white', labelsize=12)"
)
content = content.replace(
    "ax2.tick_params(colors='white', labelsize=9)",
    "ax2.tick_params(colors='white', labelsize=12)"
)
content = content.replace(
    "ax3.tick_params(colors='white', labelsize=9)",
    "ax3.tick_params(colors='white', labelsize=12)"
)

# Increase value text sizes
content = content.replace(
    "ax1.text(confidence/2, 0, f'{confidence:.1f}%', ha='center', va='center', color='white', fontsize=10, fontweight='bold')",
    "ax1.text(confidence/2, 0, f'{confidence:.1f}%', ha='center', va='center', color='white', fontsize=14, fontweight='bold')"
)
content = content.replace(
    "ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, \n                        f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=9, fontweight='bold')",
    "ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, \n                        f'{val:.1f}', ha='center', va='bottom', color='white', fontsize=12, fontweight='bold')"
)

# Set proper y-limits
content = content.replace(
    "ax3.set_ylim(0, max(stat_percentages) * 1.2)",
    "ax3.set_ylim(0, max(stat_percentages) * 1.4)"
)

with open('C:/Users/K.swathi/Desktop/project/app/ui_main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Graphs made bigger and more visible!")
print("- Increased label heights from 140 to 200")
print("- Increased figure sizes from 5x1.5 to 8x3")
print("- Increased DPI from 100 to 150")
print("- Increased font sizes for titles, labels, and values")
print("- Larger scaling for display (700x190)")
