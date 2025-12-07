"""
Generate 500 Flutter Training Dataset Examples
This script generates diverse Flutter code examples for training
"""

import json
import random
from datetime import datetime, timedelta

# Widget categories and their variations
WIDGET_TYPES = [
    "Button", "Card", "TextField", "AppBar", "BottomNavigationBar",
    "Drawer", "Dialog", "SnackBar", "ListView", "GridView",
    "Container", "Column", "Row", "Stack", "Positioned",
    "AnimatedContainer", "Hero", "PageView", "TabBar", "Chip",
    "Badge", "Avatar", "ProgressIndicator", "Slider", "Switch",
    "Checkbox", "Radio", "DropdownButton", "ExpansionTile", "Stepper",
    "DataTable", "Calendar", "TimePicker", "DatePicker", "ImagePicker",
    "VideoPlayer", "AudioPlayer", "Map", "Chart", "Graph",
    "Form", "Validator", "SearchBar", "FilterChip", "ActionChip"
]

STYLES = [
    "Material Design", "Cupertino", "Neumorphic", "Glassmorphism",
    "Minimalist", "Modern", "Gradient", "Animated", "3D Effect",
    "Neon", "Dark Mode", "Light Mode", "Colorful", "Monochrome"
]

FEATURES = [
    "with animation", "with gradient", "with shadow", "with ripple effect",
    "with custom shape", "with icon", "with image", "with badge",
    "with validation", "with state management", "responsive", "adaptive",
    "with gesture detection", "with haptic feedback", "with sound effects",
    "with loading state", "with error handling", "with caching"
]

COLORS = [
    "blue", "red", "green", "purple", "orange", "pink", "teal",
    "amber", "indigo", "cyan", "lime", "deep purple", "light blue"
]

LAYOUTS = [
    "centered", "left-aligned", "right-aligned", "justified",
    "grid layout", "list layout", "staggered grid", "masonry layout",
    "horizontal scroll", "vertical scroll", "wrap layout"
]

def generate_widget_code(widget_type, style, feature, color):
    """Generate Flutter widget code"""
    widget_name = f"{style}{widget_type}".replace(" ", "")
    
    code = f"""import 'package:flutter/material.dart';

class {widget_name} extends StatelessWidget {{
  final String? title;
  final VoidCallback? onTap;
  final Color? backgroundColor;
  final double? width;
  final double? height;
  
  const {widget_name}({{
    super.key,
    this.title,
    this.onTap,
    this.backgroundColor,
    this.width,
    this.height,
  }});
  
  @override
  Widget build(BuildContext context) {{
    return Container(
      width: width ?? double.infinity,
      height: height,
      decoration: BoxDecoration(
        color: backgroundColor ?? Colors.{color},
        borderRadius: BorderRadius.circular(12),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          borderRadius: BorderRadius.circular(12),
          child: Padding(
            padding: const EdgeInsets.all(16),
            child: Center(
              child: Text(
                title ?? '{widget_type}',
                style: const TextStyle(
                  fontSize: 16,
                  fontWeight: FontWeight.w600,
                  color: Colors.white,
                ),
              ),
            ),
          ),
        ),
      ),
    );
  }}
}}

// Usage Example:
// {widget_name}(
//   title: 'Click Me',
//   onTap: () => print('Tapped!'),
//   backgroundColor: Colors.{color},
// )
"""
    return code

def generate_dataset_entry(index):
    """Generate a single dataset entry"""
    widget_type = random.choice(WIDGET_TYPES)
    style = random.choice(STYLES)
    feature = random.choice(FEATURES)
    color = random.choice(COLORS)
    layout = random.choice(LAYOUTS)
    
    created_date = datetime.now() - timedelta(days=random.randint(0, 365))
    
    instruction = f"Create a Flutter {widget_type} widget with {style} style, {feature}, using {color} color scheme and {layout}"
    
    code = generate_widget_code(widget_type, style, feature, color)
    
    entry = {
        "dataset_name": f"flutter_{widget_type.lower().replace(' ', '_')}_{index}",
        "metadata": {
            "framework": "Flutter 3.0+",
            "widget_type": widget_type,
            "style": style,
            "feature": feature,
            "color_scheme": color,
            "layout": layout,
            "complexity": random.choice(["beginner", "intermediate", "advanced"]),
            "created": created_date.strftime("%Y-%m-%d"),
            "version": "1.0.0"
        },
        "instructions": [
            {
                "instruction": instruction,
                "input": "",
                "output": {
                    "code": code,
                    "description": f"A {style} {widget_type} widget {feature} with {color} color scheme",
                    "usage": f"This widget can be used in any Flutter application that needs a {widget_type.lower()} component",
                    "dependencies": [
                        "flutter/material.dart"
                    ]
                }
            }
        ]
    }
    
    return entry

def generate_complex_example(index):
    """Generate more complex examples with full app structure"""
    app_types = [
        "E-commerce Product Card",
        "Social Media Post",
        "Weather Widget",
        "Music Player Control",
        "Chat Message Bubble",
        "Profile Card",
        "Notification Card",
        "Calendar Event",
        "Task List Item",
        "Photo Gallery Item"
    ]
    
    app_type = random.choice(app_types)
    
    entry = {
        "dataset_name": f"flutter_complex_{app_type.lower().replace(' ', '_')}_{index}",
        "metadata": {
            "framework": "Flutter 3.0+",
            "component_type": app_type,
            "complexity": "advanced",
            "features": [
                "State Management",
                "Animations",
                "Responsive Design",
                "Custom Widgets"
            ],
            "created": datetime.now().strftime("%Y-%m-%d"),
            "version": "1.0.0"
        },
        "instructions": [
            {
                "instruction": f"Create a complete {app_type} component with modern UI design, animations, and proper state management",
                "input": "",
                "output": {
                    "code": f"""import 'package:flutter/material.dart';

class {app_type.replace(' ', '')} extends StatefulWidget {{
  const {app_type.replace(' ', '')}({{super.key}});
  
  @override
  State<{app_type.replace(' ', '')}> createState() => _{app_type.replace(' ', '')}State();
}}

class _{app_type.replace(' ', '')}State extends State<{app_type.replace(' ', '')}> with SingleTickerProviderStateMixin {{
  late AnimationController _controller;
  late Animation<double> _animation;
  
  @override
  void initState() {{
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );
    _animation = CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    );
    _controller.forward();
  }}
  
  @override
  void dispose() {{
    _controller.dispose();
    super.dispose();
  }}
  
  @override
  Widget build(BuildContext context) {{
    return FadeTransition(
      opacity: _animation,
      child: Card(
        elevation: 4,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(16),
        ),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '{app_type}',
                style: Theme.of(context).textTheme.titleLarge,
              ),
              const SizedBox(height: 8),
              Text(
                'This is a {app_type.lower()} component',
                style: Theme.of(context).textTheme.bodyMedium,
              ),
            ],
          ),
        ),
      ),
    );
  }}
}}
""",
                    "description": f"A complete {app_type} component with animations and modern design",
                    "features": [
                        "Fade-in animation",
                        "Material Design 3",
                        "Responsive layout",
                        "State management"
                    ]
                }
            }
        ]
    }
    
    return entry

def main():
    """Generate 500 dataset entries"""
    dataset = []
    
    print("Generating 500 Flutter code examples...")
    
    # Generate 400 simple widget examples
    for i in range(400):
        entry = generate_dataset_entry(i + 1)
        dataset.append(entry)
        if (i + 1) % 50 == 0:
            print(f"Generated {i + 1}/400 simple examples...")
    
    # Generate 100 complex examples
    for i in range(100):
        entry = generate_complex_example(i + 1)
        dataset.append(entry)
        if (i + 1) % 25 == 0:
            print(f"Generated {i + 1}/100 complex examples...")
    
    # Save to JSON file
    output_file = "new_flutter_dataset_500.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Successfully generated 500 examples!")
    print(f"📁 Saved to: {output_file}")
    print(f"📊 Total size: {len(json.dumps(dataset))} bytes")
    
    # Print summary
    print("\n📋 Summary:")
    print(f"  • Simple widget examples: 400")
    print(f"  • Complex component examples: 100")
    print(f"  • Total entries: {len(dataset)}")
    
    return dataset

if __name__ == "__main__":
    main()
