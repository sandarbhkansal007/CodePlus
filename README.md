# CodePulse - Universal Code Quality & Analytics Platform

**Analyze any codebase, in any language, anywhere.**

CodePulse is a comprehensive code analysis platform that supports **12+ programming languages** and provides health scoring, anomaly detection, and automated documentation generation.

## 🌐 Multi-Language Support

CodePulse works with projects in **any of these languages**:

**Python** • **JavaScript** • **TypeScript** • **Java** • **C/C++** • **C#** • **Go** • **Ruby** • **PHP** • **Swift** • **Kotlin** • **Rust**

## ✨ Key Features

### For All Languages:
- 📊 **Health Score (0-100)** - Universal code quality assessment
- 📈 **File Structure Analysis** - Detailed project organization metrics
- 🎨 **Language Distribution** - Visual breakdown of multi-language codebases
- 📁 **Line Counting** - Code, comments, and blank lines for all languages
- 🔄 **Git Activity Tracking** - Commit history and contributor analysis
- 📄 **Documentation Generation** - Auto-generated README with architecture diagrams

### Python-Specific Deep Analysis:
- 🧬 **Code Personality** - 7 personality types (Academic Researcher, Startup Hustle, etc.)
- 🔍 **Complexity Analysis** - McCabe cyclomatic complexity calculation
- 🎨 **Style Detection** - PEP 8 compliance and naming conventions
- 🚨 **Anomaly Detection** - 6 advanced algorithms for security and performance issues
  - SQL Injection detection
  - Hardcoded secrets detection
  - N+1 query problems
  - Memory leak detection
  - Concurrency issues
  - Missing error handling

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/codepulse.git
cd codepulse

# Install dependencies for dashboard
pip install -r requirements_dashboard.txt
```

### Run Web Dashboard

```bash
cd codepulse
streamlit run streamlit_app.py
```

Then open http://localhost:8501 and analyze any project!

### CLI Analysis

```bash
cd codepulse
python backend/codepulse_analyzer.py /path/to/any/project
```

Works with Python, JavaScript, Java, C++, Go, Rust, and more!

## 📊 Example Use Cases

### Analyze a Python Project
```bash
python backend/codepulse_analyzer.py ~/my-django-app
```
**Result:** Full analysis with health score, personality, complexity, and anomaly detection

### Analyze a JavaScript/React Project
```bash
python backend/codepulse_analyzer.py ~/my-react-app
```
**Result:** Health score, file metrics, language distribution, git activity

### Analyze a Multi-Language Project
```bash
python backend/codepulse_analyzer.py ~/fullstack-app
```
**Result:** Complete breakdown of all languages, file distribution, unified health score

### Analyze a Java/Spring Project
```bash
python backend/codepulse_analyzer.py ~/spring-boot-app
```
**Result:** Project structure, file metrics, health assessment

## 🎯 Perfect For

- **Any Programming Language** - Python, JavaScript, Java, C++, Go, Rust, and more
- **Any Project Size** - From small scripts to enterprise applications
- **Mixed Language Projects** - Frontend + Backend in different languages
- **Open Source Projects** - Analyze GitHub repositories
- **Code Reviews** - Quick health check before merging
- **Technical Debt Assessment** - Identify problem areas
- **Learning Projects** - Understand code quality metrics

## 📁 Project Structure

```
codepulse/
├── backend/
│   ├── analyzer/              # Multi-language code analysis
│   │   ├── file_reader.py     # Scans files in 12+ languages
│   │   ├── complexity.py      # Complexity analysis (Python)
│   │   ├── style_detector.py  # Style detection (Python)
│   │   ├── anomaly_detector.py # Security & performance checks
│   │   └── git_analyzer.py    # Git history (all languages)
│   ├── scorer/                # Health scoring
│   │   ├── health_calculator.py
│   │   ├── personality.py
│   │   └── comparator.py
│   └── generator/
│       └── readme_generator.py # Auto-documentation
├── streamlit_app.py           # Web dashboard
├── sample_project/            # Demo project
└── docs/                      # Documentation
```

## 🎓 How It Works

1. **Universal File Scanner** - Detects and analyzes files in 12+ languages
2. **Language Detection** - Automatically identifies programming languages
3. **Metric Collection** - Counts lines, files, and calculates basic metrics
4. **Deep Analysis** - Advanced features for Python (AST parsing, complexity)
5. **Health Scoring** - Unified score across all languages
6. **Visualization** - Beautiful charts and graphs in web dashboard

## 📚 Documentation

- [Quick Start Guide](codepulse/QUICKSTART.md)
- [How to Run](codepulse/HOW_TO_RUN.md)
- [Examples](codepulse/EXAMPLES.md)
- [Anomaly Detection Algorithms](codepulse/ANOMALY_DETECTION_ALGORITHMS.md)
- [Implementation Summary](codepulse/IMPLEMENTATION_SUMMARY.md)

## 🌟 Why CodePulse?

- ✅ **Language Agnostic** - Analyze any codebase
- ✅ **No Configuration** - Works out of the box
- ✅ **Beautiful Dashboard** - Streamlit-based web interface
- ✅ **Actionable Insights** - Get specific recommendations
- ✅ **Export Reports** - JSON and Markdown export
- ✅ **Free & Open Source** - Use it anywhere

## 🔧 Requirements

- Python 3.8 or higher
- Git (optional, for activity tracking)
- Streamlit (for web dashboard)

## 📝 License

This project is licensed under the Apache License - see the [LICENSE](LICENSE) file for details.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add support for more languages
- Improve analysis algorithms
- Enhance visualizations
- Fix bugs and issues

---

**Made with ❤️ for developers working in any language**
