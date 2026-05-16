# CodePulse - Universal Code Quality & Analytics Platform

**A Fitbit for your code!** CodePulse analyzes codebases in **12+ programming languages** and provides health scores, personality profiles, and anomaly detection.

## 🌐 Multi-Language Support

CodePulse works with any project in any of these languages:

**Supported Languages:** Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Ruby, PHP, Swift, Kotlin, Rust

## 🎯 What Does It Do?

CodePulse provides comprehensive insights for **all types of projects**:

1. **Health Score (0-100)** - Overall code quality assessment for any language
2. **Language Distribution** - Visual breakdown of your multi-language codebase
3. **Code DNA** - Project personality profile (Python projects)
4. **Anomaly Detection** - Security and performance issue detection (Python projects)
5. **Documentation Generation** - Auto-generated README with architecture diagrams

## 🚀 Quick Start

### Requirements
- Python 3.8 or higher
- Git (optional, for activity tracking)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/codepulse.git
cd codepulse

# No dependencies needed! Uses Python standard library
```

### Run Analysis

```bash
# Analyze current directory
python backend/codepulse_analyzer.py .

# Analyze specific project
python backend/codepulse_analyzer.py /path/to/your/project

# Save results to JSON
python backend/codepulse_analyzer.py /path/to/project --json results.json
```

## 📊 Example Output

```
==================================================================
📊 CODEPULSE ANALYSIS REPORT
==================================================================

📁 Project: /Users/you/my-project
🕐 Analyzed: 2026-05-16T10:30:45

📈 Summary:
   Files: 25
   Lines of Code: 3,456
   Health Score: 78.5/100
   Rating: GOOD
   Personality: Python Purist

💊 Health Breakdown:
   activity       : [████████████████░░░░] 85.0/100
   quality        : [██████████████░░░░░░] 72.0/100
   safety         : [█████████████░░░░░░░] 65.0/100
   documentation  : [████████████████░░░░] 80.0/100
   organization   : [███████████████░░░░░] 75.0/100

🧬 Code DNA:
   Type: Python Purist
   Confidence: 87.5%
   Pythonic code, follows PEP 8, snake_case naming

   Traits:
      • Pythonic code
      • PEP 8 compliant
      • Snake case naming
      • List comprehensions
      • Standard library preferred

💡 Insights:
   👍 Your code is healthy overall, with room for minor improvements.
   ⚠️ Safety is low (65/100). Consider improving code smells and potential issues.
   ✅ Activity is excellent (85/100)!
```

## 🏗️ Project Structure

```
codepulse/
├── backend/
│   ├── analyzer/              # Code analysis modules
│   │   ├── file_reader.py     # Scans and reads files
│   │   ├── ast_parser.py      # Parses Python AST
│   │   ├── complexity.py      # Calculates complexity
│   │   ├── style_detector.py  # Detects coding style
│   │   └── git_analyzer.py    # Git history analysis
│   ├── scorer/                # Health scoring modules
│   │   ├── health_calculator.py   # Health score calculation
│   │   ├── personality.py         # Personality classification
│   │   └── comparator.py          # Project comparison
│   └── codepulse_analyzer.py  # Main analysis script
├── docs/                      # Documentation
└── README.md
```

## 🎓 How It Works

### 1. Universal File Analysis (All Languages)
- Scans code files in **12+ programming languages**
- Counts lines (total, code, comments, blank) for all languages
- Detects programming languages automatically
- Generates language distribution charts
- Calculates basic health metrics for any codebase
- Works with mixed-language projects (e.g., Python + JavaScript frontend/backend)

**Works with:** Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Ruby, PHP, Swift, Kotlin, Rust

### 2. Advanced Code Analysis (Python-Specific)
- Parses Abstract Syntax Trees (AST) for deep code understanding
- Extracts functions, classes, imports, and relationships
- Calculates cyclomatic complexity (McCabe complexity)
- Detects code smells (long functions, high complexity, nested loops)
- **Anomaly Detection**: Security vulnerabilities, performance issues, memory leaks

### 3. Style Analysis (Python-Focused)
- Detects indentation style (tabs vs spaces)
- Identifies naming conventions (snake_case, camelCase, PascalCase)
- Analyzes comment density and quality
- Measures code consistency across files
- PEP 8 compliance checking

### 4. Git Analysis (Language-Agnostic)
- Works with **any language** in git repositories
- Counts commits (total and recent activity)
- Identifies contributors and their impact
- Finds hot files (frequently changed)
- Calculates activity score for project health

### 5. Health Score Calculation (All Languages)
Universal weighted score based on:
- **Activity (20%)**: Recent git commits (any language)
- **Quality (25%)**: Code complexity (Python detailed, others basic)
- **Safety (25%)**: Code organization and potential issues
- **Documentation (15%)**: Comment coverage (all languages)
- **Organization (15%)**: File structure and consistency

### 6. Personality Classification (Python Projects)
Classifies code into 7 personality types:
- **Academic Researcher**: Well-documented, thoughtful
- **Enterprise Corporate**: Highly structured, formal
- **Startup Hustle**: Fast-moving, pragmatic
- **Clean Coder**: Simple, maintainable
- **Weekend Hacker**: Experimental, mixed styles
- **Python Purist**: Pythonic, PEP 8 compliant
- **Pragmatic Developer**: Balanced approach

### 7. Documentation Generation (All Languages)
- Auto-generates README.md with project structure
- Creates architecture diagrams using Mermaid
- Works with multi-language projects
- Includes language distribution visualizations

## 🔧 Individual Module Usage

### File Reader
```python
from analyzer.file_reader import FileReader

reader = FileReader('/path/to/project')
summary = reader.get_project_summary()
print(f"Total files: {summary['total_files']}")
print(f"Lines of code: {summary['code_lines']}")
```

### Complexity Calculator
```python
from analyzer.complexity import ComplexityCalculator

calc = ComplexityCalculator('myfile.py')
metrics = calc.get_metrics()
print(f"File complexity: {metrics['file_complexity']}")
print(f"Average complexity: {metrics['average_complexity']}")
```

### Style Detector
```python
from analyzer.style_detector import StyleDetector

detector = StyleDetector('myfile.py')
fingerprint = detector.get_fingerprint()
print(f"Indentation: {fingerprint['indentation']['style']}")
print(f"Naming: {fingerprint['naming']['dominant_style']}")
```

### Git Analyzer
```python
from analyzer.git_analyzer import GitAnalyzer

git = GitAnalyzer('/path/to/repo')
analysis = git.get_analysis()
print(f"Total commits: {analysis['total_commits']}")
print(f"Activity score: {analysis['activity_score']}")
```

### Health Calculator
```python
from scorer.health_calculator import HealthCalculator

calculator = HealthCalculator()
health = calculator.calculate_health_score(
    file_metrics,
    complexity_metrics,
    style_metrics,
    git_metrics
)
print(f"Health: {health['overall_score']}/100")
```

### Personality Classifier
```python
from scorer.personality import PersonalityClassifier

classifier = PersonalityClassifier()
personality = classifier.classify(
    file_metrics,
    style_metrics,
    complexity_metrics
)
print(f"Personality: {personality['personality']}")
```

## 📈 Health Score Guide

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | Excellent | Outstanding code quality |
| 80-89 | Good | Healthy code with minor improvements needed |
| 70-79 | Fair | Acceptable quality, some attention needed |
| 60-69 | Needs Improvement | Several issues to address |
| 0-59 | Poor | Significant refactoring recommended |

## 🧬 Personality Types

### Academic Researcher
- Well-documented code (15%+ comments)
- High consistency (80%+)
- Moderate complexity
- Formal naming conventions

### Enterprise Corporate
- Highly structured
- Strict coding standards
- Extensive documentation
- Design patterns

### Startup Hustle
- Fast-moving
- Low comment ratio
- Mixed consistency
- Results-focused

### Clean Coder
- Simple solutions
- Well-tested
- Highly consistent
- Low complexity

### Weekend Hacker
- Experimental
- Mixed styles
- Irregular patterns
- Learning focused

### Python Purist
- Pythonic code
- PEP 8 compliant
- Snake case naming
- Standard library preferred

### Pragmatic Developer
- Balanced approach
- Moderate everything
- Gets things done

## 🎯 Use Cases

### For Students
- Track code quality improvements over time
- Learn good coding practices
- Prepare projects for evaluation
- Compare with professional codebases

### For Developers
- Quick health check of new projects
- Onboarding to legacy code
- Code review assistance
- Technical debt assessment

### For Teams
- Consistent code quality standards
- Track project health trends
- Identify areas needing attention
- Compare team coding styles

## 🔮 Future Features

- [ ] Web dashboard with charts
- [ ] Trend tracking over time
- [ ] Team leaderboard
- [ ] Multi-project comparison
- [ ] GitHub integration
- [ ] Alerts for health drops
- [ ] Export reports to PDF
- [ ] Support for more languages
- [ ] CLI with more options
- [ ] VS Code extension

## 🤝 Contributing

This is a college project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - Feel free to use this project for learning!

## 👥 Team

- **Person 1**: Analyzer modules (file reading, AST parsing, complexity)
- **Person 2**: Scoring modules (health calculation, personality)
- **Person 3**: Web interface (coming soon!)

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ for B.Tech Final Year Project**
