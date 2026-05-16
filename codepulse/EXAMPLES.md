# CodePulse - Usage Examples

## 🎯 Basic Examples

### Example 1: Analyze Current Project
```bash
python3 codepulse/backend/codepulse_analyzer.py .
```

**Output:**
```
🔍 Analyzing project: /Users/you/project
📁 Scanning files...
   Found 25 files
   Total lines: 3,456
🐍 Analyzing Python files...
   Analyzed 25 Python files
💊 Calculating health score...
   Overall health: 78.5/100
🧬 Code DNA: Python Purist
✅ Analysis complete in 0.5 seconds
```

### Example 2: Save Results to JSON
```bash
python3 codepulse/backend/codepulse_analyzer.py . --json my_analysis.json
```

**my_analysis.json:**
```json
{
  "project_path": "/Users/you/project",
  "analysis_timestamp": "2026-05-16T19:31:19",
  "health": {
    "overall_score": 78.5,
    "rating": "good",
    "components": {
      "activity": {"score": 85.0},
      "quality": {"score": 72.0},
      ...
    }
  },
  "personality": {
    "personality": "Python Purist",
    "confidence": 87.5
  }
}
```

### Example 3: Analyze Different Project
```bash
python3 codepulse/backend/codepulse_analyzer.py ~/projects/my-app
```

## 🔧 Module Examples

### File Reader Example
```python
from codepulse.backend.analyzer.file_reader import FileReader

# Scan project
reader = FileReader('/path/to/project')
summary = reader.get_project_summary()

print(f"Total files: {summary['total_files']}")
print(f"Code lines: {summary['code_lines']:,}")
print(f"Languages: {list(summary['language_stats'].keys())}")

# Get details for each file
for file_info in summary['files']:
    print(f"{file_info['path']}: {file_info['lines']['code']} lines")
```

**Output:**
```
Total files: 25
Code lines: 3,456
Languages: ['Python', 'JavaScript']
src/main.py: 150 lines
src/utils.py: 89 lines
...
```

### Complexity Calculator Example
```python
from codepulse.backend.analyzer.complexity import ComplexityCalculator

# Analyze a file
calc = ComplexityCalculator('myfile.py')
metrics = calc.get_metrics()

print(f"File complexity: {metrics['file_complexity']}")
print(f"Average complexity: {metrics['average_complexity']}")

# Function-level details
for func in metrics['function_complexities']:
    print(f"{func['name']}: {func['complexity']} ({func['rating']})")

# Code smells
for smell in metrics['code_smells']:
    print(f"[{smell['severity']}] {smell['message']}")
```

**Output:**
```
File complexity: 48
Average complexity: 6.4
login: 8 (moderate)
validate_token: 12 (complex)
[HIGH] Function 'process_data' has complexity 15 (>10)
```

### Style Detector Example
```python
from codepulse.backend.analyzer.style_detector import StyleDetector

detector = StyleDetector('myfile.py')
fingerprint = detector.get_fingerprint()

print(f"Indentation: {fingerprint['indentation']['style']}")
print(f"Naming: {fingerprint['naming']['dominant_style']}")
print(f"Comments: {fingerprint['comments']['comment_ratio']}%")
print(f"Consistency: {fingerprint['overall_consistency']}%")

personality = detector.classify_personality(fingerprint)
print(f"Personality: {personality}")
```

**Output:**
```
Indentation: spaces_4
Naming: snake_case
Comments: 12.5%
Consistency: 87.3%
Personality: Python Purist
```

### Git Analyzer Example
```python
from codepulse.backend.analyzer.git_analyzer import GitAnalyzer

git = GitAnalyzer('/path/to/repo')
analysis = git.get_analysis()

print(f"Total commits: {analysis['total_commits']:,}")
print(f"Recent activity: {analysis['commits_last_7_days']} commits")
print(f"Contributors: {analysis['contributor_count']}")
print(f"Activity score: {analysis['activity_score']}/100")

# Hot files
for hot in analysis['hot_files'][:5]:
    print(f"{hot['file']}: {hot['changes']} changes")
```

**Output:**
```
Total commits: 523
Recent activity: 12 commits
Contributors: 5
Activity score: 85.7/100
src/main.py: 89 changes
src/utils.py: 67 changes
```

### Health Calculator Example
```python
from codepulse.backend.scorer.health_calculator import HealthCalculator

calculator = HealthCalculator()

health = calculator.calculate_health_score(
    file_metrics,      # From FileReader
    complexity_metrics, # From ComplexityCalculator
    style_metrics,     # From StyleDetector
    git_metrics        # From GitAnalyzer
)

print(f"Health: {health['overall_score']}/100")
print(f"Rating: {health['rating']}")

for component, data in health['components'].items():
    print(f"{component}: {data['score']}/100")

# Get insights
insights = calculator.get_health_insights(health)
for insight in insights:
    print(insight)
```

**Output:**
```
Health: 78.5/100
Rating: good
activity: 85.0/100
quality: 72.0/100
safety: 65.0/100
👍 Your code is healthy overall, with room for minor improvements.
⚠️ Safety is low (65/100). Consider improving...
```

### Personality Classifier Example
```python
from codepulse.backend.scorer.personality import PersonalityClassifier

classifier = PersonalityClassifier()

result = classifier.classify(
    file_metrics,
    style_metrics,
    complexity_metrics
)

print(f"Personality: {result['personality']}")
print(f"Confidence: {result['confidence']}%")
print(f"Description: {result['description']}")

# Get traits
traits = classifier.get_personality_traits(result['personality'])
for trait in traits:
    print(f"  • {trait}")
```

**Output:**
```
Personality: Python Purist
Confidence: 87.5%
Description: Pythonic code, follows PEP 8, snake_case naming
  • Pythonic code
  • PEP 8 compliant
  • Snake case naming
```

## 🎓 College Project Examples

### Demo 1: Basic File Analysis
```python
#!/usr/bin/env python3
"""Demo for Week 1-2"""
from codepulse.backend.analyzer.file_reader import FileReader

print("📁 File Analysis Demo\n")

reader = FileReader('.')
summary = reader.get_project_summary()

print(f"Project: {summary['project_path']}")
print(f"Files: {summary['total_files']}")
print(f"Lines: {summary['code_lines']:,}")

for lang, stats in summary['language_stats'].items():
    percent = (stats['code'] / summary['code_lines'] * 100)
    print(f"{lang}: {percent:.1f}%")
```

### Demo 2: Code Quality Analysis
```python
#!/usr/bin/env python3
"""Demo for Week 3-4"""
from codepulse.backend.analyzer.complexity import ComplexityCalculator
from pathlib import Path

print("📊 Code Quality Demo\n")

# Analyze all Python files
for py_file in Path('.').rglob('*.py'):
    calc = ComplexityCalculator(str(py_file))
    metrics = calc.get_metrics()
    
    print(f"{py_file.name}:")
    print(f"  Complexity: {metrics['average_complexity']:.1f}")
    print(f"  Quality: {metrics['quality_rating']}")
    print()
```

### Demo 3: Style Analysis
```python
#!/usr/bin/env python3
"""Demo for Week 5-6"""
from codepulse.backend.analyzer.style_detector import StyleDetector
from pathlib import Path

print("🎨 Style Analysis Demo\n")

files = list(Path('.').rglob('*.py'))[:5]

for py_file in files:
    detector = StyleDetector(str(py_file))
    fp = detector.get_fingerprint()
    
    print(f"{py_file.name}:")
    print(f"  Indentation: {fp['indentation']['style']}")
    print(f"  Naming: {fp['naming']['dominant_style']}")
    print(f"  Consistency: {fp['overall_consistency']}%")
    print()
```

### Demo 4: Complete Analysis
```python
#!/usr/bin/env python3
"""Demo for Final Presentation"""
from codepulse.backend.codepulse_analyzer import CodePulseAnalyzer

print("🚀 Complete Analysis Demo\n")

analyzer = CodePulseAnalyzer('.')
results = analyzer.analyze()

# Print report
analyzer.print_report(results)

# Save results
analyzer.save_results(results, 'demo_results.json')
```

## 📊 Comparison Examples

### Compare Two Projects
```python
from codepulse.backend.codepulse_analyzer import CodePulseAnalyzer
from codepulse.backend.scorer.comparator import ProjectComparator

# Analyze two projects
analyzer1 = CodePulseAnalyzer('project1')
results1 = analyzer1.analyze()

analyzer2 = CodePulseAnalyzer('project2')
results2 = analyzer2.analyze()

# Compare health
comparator = ProjectComparator()
comparison = comparator.compare_health(
    results1['health'],
    results2['health']
)

print(f"Project 1: {comparison['project1_score']}/100")
print(f"Project 2: {comparison['project2_score']}/100")
print(f"Difference: {comparison['difference']} points")
print(f"Winner: {comparison['winner']}")
```

### Track Progress Over Time
```python
import json
from datetime import datetime

# Save analysis with timestamp
analyzer = CodePulseAnalyzer('.')
results = analyzer.analyze()

# Add to history file
history = []
try:
    with open('health_history.json', 'r') as f:
        history = json.load(f)
except FileNotFoundError:
    pass

history.append({
    'date': datetime.now().isoformat(),
    'health_score': results['health']['overall_score'],
    'personality': results['personality']['personality']
})

with open('health_history.json', 'w') as f:
    json.dump(history, f, indent=2)

# Show progress
print("Health History:")
for entry in history[-5:]:
    print(f"{entry['date'][:10]}: {entry['health_score']}/100")
```

## 🎯 Real-World Use Cases

### Use Case 1: Code Review Helper
```bash
# Before code review
python3 codepulse/backend/codepulse_analyzer.py . --json before.json

# After changes
python3 codepulse/backend/codepulse_analyzer.py . --json after.json

# Compare
python3 -c "
import json
before = json.load(open('before.json'))
after = json.load(open('after.json'))
print(f'Health change: {before['health']['overall_score']:.1f} -> {after['health']['overall_score']:.1f}')
print(f'Quality: {before['health']['components']['quality']['score']:.1f} -> {after['health']['components']['quality']['score']:.1f}')
"
```

### Use Case 2: Onboarding Tool
```python
# New developer analyzing codebase
from codepulse.backend.codepulse_analyzer import CodePulseAnalyzer

analyzer = CodePulseAnalyzer('/path/to/new/project')
results = analyzer.analyze()

print("\n🎯 Onboarding Summary:")
print(f"Project size: {results['summary']['total_lines']:,} lines")
print(f"Complexity: {results['summary']['health_score']}/100")
print(f"Style: {results['personality']['personality']}")
print(f"\n💡 What you need to know:")
for insight in results['insights'][:3]:
    print(f"  {insight}")
```

### Use Case 3: Team Standards Checker
```python
# Check if project meets team standards
analyzer = CodePulseAnalyzer('.')
results = analyzer.analyze()

standards = {
    'min_health': 80,
    'min_documentation': 70,
    'max_complexity': 10
}

health = results['health']
passed = []
failed = []

if health['overall_score'] >= standards['min_health']:
    passed.append("Overall health")
else:
    failed.append(f"Health: {health['overall_score']:.1f} < {standards['min_health']}")

if health['components']['documentation']['score'] >= standards['min_documentation']:
    passed.append("Documentation")
else:
    failed.append(f"Documentation: {health['components']['documentation']['score']:.1f} < {standards['min_documentation']}")

print("\n✅ Passed:", ", ".join(passed))
if failed:
    print("❌ Failed:", ", ".join(failed))
```

## 🔄 Automation Examples

### Daily Health Check
```bash
#!/bin/bash
# daily_check.sh

echo "Running daily health check..."
python3 codepulse/backend/codepulse_analyzer.py . --json daily_$(date +%Y%m%d).json

# Extract score
score=$(python3 -c "import json; print(json.load(open('daily_$(date +%Y%m%d).json'))['health']['overall_score'])")

echo "Today's health: $score/100"

if (( $(echo "$score < 70" | bc -l) )); then
    echo "⚠️ Health dropped below 70!"
    # Send notification
fi
```

### Git Hook Integration
```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Checking code health before commit..."
python3 codepulse/backend/codepulse_analyzer.py . --json temp_analysis.json

score=$(python3 -c "import json; print(json.load(open('temp_analysis.json'))['health']['overall_score'])")

if (( $(echo "$score < 60" | bc -l) )); then
    echo "❌ Code health too low ($score/100). Please improve before committing."
    rm temp_analysis.json
    exit 1
fi

echo "✅ Code health OK ($score/100)"
rm temp_analysis.json
```

## 📈 Reporting Examples

### Generate Report
```python
from codepulse.backend.codepulse_analyzer import CodePulseAnalyzer

analyzer = CodePulseAnalyzer('.')
results = analyzer.analyze()

# Custom report
print(f"""
PROJECT HEALTH REPORT
=====================
Date: {results['analysis_timestamp'][:10]}

Overall Health: {results['health']['overall_score']}/100
Rating: {results['health']['rating'].upper()}

Strengths:
""")

# Show top 3 components
components = sorted(
    results['health']['components'].items(),
    key=lambda x: x[1]['score'],
    reverse=True
)

for name, data in components[:3]:
    print(f"  ✅ {name.title()}: {data['score']:.1f}/100")

print("\nAreas for Improvement:")
for name, data in components[-2:]:
    print(f"  ⚠️ {name.title()}: {data['score']:.1f}/100")
```

---

## 💡 Tips

1. **Run regularly**: Track progress over time
2. **Before commits**: Check health before pushing
3. **After refactoring**: Verify improvements
4. **New projects**: Understand codebase quickly
5. **Team standards**: Enforce code quality

## 🎓 For Students

These examples are perfect for:
- Project demonstrations
- Progress tracking
- Learning about code quality
- Portfolio projects

Start with simple examples and build up to complete analysis!
