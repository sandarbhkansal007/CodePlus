# CodePulse - Quick Start Guide

## 🚀 Get Started in 2 Minutes

### Step 1: No Installation Needed!
CodePulse uses only Python standard library. Just make sure you have Python 3.8+:

```bash
python3 --version
```

### Step 2: Run the Analyzer

#### Analyze Current Directory
```bash
python3 codepulse/backend/codepulse_analyzer.py .
```

#### Analyze Any Project
```bash
python3 codepulse/backend/codepulse_analyzer.py /path/to/your/project
```

#### Save Results to JSON
```bash
python3 codepulse/backend/codepulse_analyzer.py /path/to/project --json results.json
```

### Step 3: See the Demo
```bash
python3 codepulse/demo.py
```

## 📊 What You'll See

```
📊 CODEPULSE ANALYSIS REPORT

📈 Summary:
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
   Personality: Python Purist
   Pythonic code, follows PEP 8, snake_case naming
```

## 🎯 Individual Components

### File Reader
```bash
python3 -c "
from codepulse.backend.analyzer.file_reader import FileReader
reader = FileReader('.')
summary = reader.get_project_summary()
print(f'Files: {summary[\"total_files\"]}')
print(f'Lines: {summary[\"code_lines\"]:,}')
"
```

### Complexity Calculator
```bash
python3 codepulse/backend/analyzer/complexity.py yourfile.py
```

### Style Detector
```bash
python3 codepulse/backend/analyzer/style_detector.py yourfile.py
```

### Git Analyzer
```bash
python3 codepulse/backend/analyzer/git_analyzer.py .
```

## 💡 Tips

1. **Best Results**: Analyze Python projects (full AST support)
2. **Git Required**: For activity score, project must be a git repository
3. **Large Projects**: May take 10-30 seconds for 100+ files
4. **JSON Output**: Use `--json` to save results for later analysis

## 🎓 For Your College Project

### Week 1 Demo
```bash
# Show basic file analysis
python3 codepulse/backend/analyzer/file_reader.py .

# Show complexity analysis
python3 codepulse/backend/analyzer/complexity.py setup.py
```

### Week 2 Demo
```bash
# Show style detection
python3 codepulse/backend/analyzer/style_detector.py setup.py

# Show git analysis
python3 codepulse/backend/analyzer/git_analyzer.py .
```

### Week 3+ Demo
```bash
# Show complete analysis
python3 codepulse/backend/codepulse_analyzer.py . --json results.json

# Show demo of all features
python3 codepulse/demo.py
```

## 🔧 Test Individual Modules

All modules can run standalone:

```bash
# Test file reader
cd codepulse/backend
python3 -m analyzer.file_reader /path/to/project

# Test AST parser
python3 -m analyzer.ast_parser yourfile.py

# Test complexity
python3 -m analyzer.complexity yourfile.py

# Test style
python3 -m analyzer.style_detector yourfile.py

# Test git
python3 -m analyzer.git_analyzer /path/to/repo

# Test health calculator
python3 -m scorer.health_calculator

# Test personality classifier
python3 -m scorer.personality
```

## 📈 Understanding Scores

### Health Score (0-100)
- **90-100**: Excellent - Professional quality
- **80-89**: Good - Minor improvements needed
- **70-79**: Fair - Some attention needed
- **60-69**: Needs Improvement - Address issues
- **0-59**: Poor - Significant refactoring needed

### Activity Score
Based on git commits in last 7 days:
- 7+ commits = 100/100
- 3-6 commits = 43-86/100
- 1-2 commits = 14-29/100
- 0 commits = 0/100

### Quality Score
Based on code complexity:
- Avg complexity 1-5 = 100/100
- Avg complexity 5-10 = 80-100/100
- Avg complexity 10-15 = 50-80/100
- Avg complexity 15-20 = 20-50/100
- Avg complexity 20+ = 0-20/100

### Safety Score
Based on code smells:
- 0 issues = 100/100
- Each high severity issue = -10 points
- Each medium severity issue = -5 points
- Each low severity issue = -2 points

### Documentation Score
Based on comment ratio:
- 20%+ comments = 100/100
- 15-20% = 85-100/100
- 10-15% = 70-85/100
- 5-10% = 50-70/100
- 0-5% = 0-50/100

### Organization Score
Based on code consistency:
- Directly maps consistency % to score

## 🧬 Personality Types

1. **Academic Researcher**: Well-documented, thoughtful
2. **Enterprise Corporate**: Highly structured, formal
3. **Startup Hustle**: Fast-moving, pragmatic
4. **Clean Coder**: Simple, maintainable
5. **Weekend Hacker**: Experimental, mixed styles
6. **Python Purist**: Pythonic, PEP 8 compliant
7. **Pragmatic Developer**: Balanced approach

## 🆘 Troubleshooting

### "Not a git repository"
- Activity score will be 50/100 (neutral)
- Other scores work fine without git

### "No Python files found"
- Analyzer works best with Python projects
- File reader works with all languages
- AST parsing only works for Python

### "Syntax error in file"
- File will be skipped
- Other files will be analyzed normally

### Slow analysis
- Large projects take time
- Be patient for 100+ files
- Consider analyzing a subdirectory

## 📚 Next Steps

1. Read full README.md for details
2. Check out the implementation in backend/
3. Try analyzing different projects
4. Compare your project with others
5. Track improvements over time

---

**Questions?** Open an issue on GitHub!
