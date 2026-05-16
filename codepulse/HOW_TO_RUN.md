# 🚀 How to Run CodePulse

## Method 1: Web Dashboard (Recommended!) 🌟

### Step 1: Install Dependencies

```bash
# Install Streamlit and Plotly (only needed for dashboard)
pip3 install streamlit plotly
```

Or install from requirements file:
```bash
pip3 install -r codepulse/requirements_dashboard.txt
```

### Step 2: Run the Dashboard

**Option A: Using the run script (easiest)**
```bash
cd codepulse
./run_dashboard.sh
```

**Option B: Direct command**
```bash
cd codepulse
streamlit run streamlit_app.py
```

### Step 3: Open in Browser

The dashboard will automatically open in your browser at:
```
http://localhost:8501
```

If it doesn't open automatically, just copy that URL into your browser!

### Step 4: Analyze Your Code

1. In the sidebar, enter your project path (or use `.` for current directory)
2. Click **"🔍 Analyze Project"**
3. Wait a few seconds while it analyzes
4. Explore the beautiful dashboard! 🎉

---

## Method 2: Command Line Interface (CLI)

### No Installation Required!

The CLI uses only Python standard library - zero dependencies!

### Basic Usage

```bash
# Analyze current directory
python3 codepulse/backend/codepulse_analyzer.py .

# Analyze specific project
python3 codepulse/backend/codepulse_analyzer.py /path/to/project

# Save results to JSON
python3 codepulse/backend/codepulse_analyzer.py . --json results.json
```

### Example Output

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

✅ Analysis complete!

======================================================================
📊 CODEPULSE ANALYSIS REPORT
======================================================================

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
```

---

## Method 3: Interactive Demo

### Run the Demo Script

```bash
python3 codepulse/demo.py
```

This shows you all the features in action!

---

## Method 4: Python API

### Use in Your Own Scripts

```python
from codepulse.backend.codepulse_analyzer import CodePulseAnalyzer

# Analyze a project
analyzer = CodePulseAnalyzer('/path/to/project')
results = analyzer.analyze()

# Access results
print(f"Health Score: {results['health']['overall_score']}/100")
print(f"Personality: {results['personality']['personality']}")

# Save to JSON
analyzer.save_results(results, 'my_analysis.json')
```

---

## 🎯 What You'll See in the Dashboard

### 1. Overview Section
- **Health Score**: Big number (0-100) showing overall code health
- **Files Count**: Total files analyzed
- **Lines of Code**: Total code lines
- **Rating**: Excellent / Good / Fair / Poor

### 2. Gauge Charts
- Beautiful circular gauge showing your health score
- Color-coded: Green (good), Yellow (fair), Red (poor)

### 3. Component Breakdown Bar Chart
Shows 5 health components:
- 🏃 **Activity**: Recent git commits
- 💪 **Quality**: Code complexity
- 🛡️ **Safety**: Code smells
- 📚 **Documentation**: Comment coverage
- 📁 **Organization**: Code consistency

### 4. Code DNA / Personality
- Your code's personality type (e.g., "Python Purist")
- Confidence percentage
- Personality traits (bullet points)
- Style fingerprint (metrics)

### 5. Insights & Recommendations
- ✅ What's going well
- ⚠️ What needs attention
- 💡 Actionable suggestions

### 6. Detailed Tabs

#### 📁 Files Tab
- Language distribution pie chart
- File statistics
- List of all files with line counts

#### 📊 Complexity Tab
- Average complexity score
- Total code smells
- Most complex files (expandable)
- Function-level complexity

#### 🎨 Style Tab
- Indentation style distribution
- Naming convention breakdown
- Consistency scores
- Distribution histogram

#### 🔄 Git Activity Tab
- Total commits
- Recent activity (last 7 days)
- Top contributors with progress bars
- Hot files (most changed)

#### 💾 Export Tab
- Download JSON report
- Preview JSON data

---

## 📸 Dashboard Features

### Interactive Elements
- ✅ Real-time progress bars during analysis
- ✅ Expandable sections for detailed info
- ✅ Beautiful gradient cards
- ✅ Interactive Plotly charts (hover for details)
- ✅ Download reports as JSON

### Beautiful Visuals
- 🎨 Gradient color schemes
- 📊 Gauge charts
- 📈 Bar charts
- 🥧 Pie charts
- 📉 Histograms
- 🌈 Color-coded metrics

---

## 🎓 For Your College Project Demo

### Step-by-Step Demo Flow

**1. Introduction (1 minute)**
```bash
# Show the simple CLI first
python3 codepulse/backend/codepulse_analyzer.py .
```
Explain: "This is the command-line version. Now let me show you the dashboard..."

**2. Launch Dashboard (30 seconds)**
```bash
cd codepulse
streamlit run streamlit_app.py
```
Wait for browser to open...

**3. Demonstrate Features (3-4 minutes)**

- **Point 1**: "Here's the overall health score - 78.5 out of 100"
- **Point 2**: "This gauge shows it visually"
- **Point 3**: "These bars break down the 5 health components"
- **Point 4**: "Our tool also identifies code personality - Python Purist!"
- **Point 5**: "It gives actionable insights"
- **Point 6**: "Click through tabs to see detailed analysis"
- **Point 7**: "You can export reports as JSON"

**4. Analyze Different Project (1 minute)**
- Enter different path in sidebar
- Click analyze
- Show how it works on any project

**5. Conclusion (30 seconds)**
"As you can see, CodePulse provides comprehensive code analysis with a beautiful, easy-to-use interface!"

---

## ⚡ Quick Troubleshooting

### Dashboard won't start?

```bash
# Install dependencies
pip3 install streamlit plotly

# Try again
cd codepulse
streamlit run streamlit_app.py
```

### Port 8501 already in use?

```bash
# Use different port
streamlit run streamlit_app.py --server.port 8502
```

### Can't analyze project?

Make sure:
- ✅ Path exists and is correct
- ✅ You have read permissions
- ✅ It's a valid project directory

### No Python files found?

- The analyzer works best with Python projects
- File reader works with all languages
- But complexity/style analysis needs Python files

---

## 📊 Understanding the Results

### Health Score Ranges
- **90-100**: Excellent - Professional quality code
- **80-89**: Good - Minor improvements needed
- **70-79**: Fair - Some attention required
- **60-69**: Needs Improvement - Address issues
- **0-59**: Poor - Significant refactoring needed

### Personality Types

1. **Academic Researcher** - Well-documented, thoughtful
2. **Enterprise Corporate** - Highly structured, formal
3. **Startup Hustle** - Fast-moving, pragmatic
4. **Clean Coder** - Simple, maintainable
5. **Weekend Hacker** - Experimental, mixed styles
6. **Python Purist** - Pythonic, PEP 8 compliant
7. **Pragmatic Developer** - Balanced approach

### Component Scores

Each component is scored 0-100:
- **High (80+)**: Doing great! ✅
- **Medium (60-79)**: Room for improvement ⚡
- **Low (<60)**: Needs attention ⚠️

---

## 🎯 Best Practices

### For Best Results

1. **Analyze from project root** - Use `.` when in project directory
2. **Commit your code** - Git history improves activity score
3. **Add comments** - Improves documentation score
4. **Keep functions simple** - Reduces complexity
5. **Be consistent** - Improves organization score

### Regular Analysis

```bash
# Daily health check
python3 codepulse/backend/codepulse_analyzer.py . --json daily.json

# Compare over time
python3 codepulse/backend/codepulse_analyzer.py . --json $(date +%Y%m%d).json
```

---

## 🔥 Advanced Usage

### Analyze Multiple Projects

```python
projects = ['project1', 'project2', 'project3']

for project in projects:
    analyzer = CodePulseAnalyzer(project)
    results = analyzer.analyze()
    print(f"{project}: {results['health']['overall_score']:.1f}/100")
```

### Compare Projects

```python
from codepulse.backend.scorer.comparator import ProjectComparator

# Analyze two projects
results1 = CodePulseAnalyzer('project1').analyze()
results2 = CodePulseAnalyzer('project2').analyze()

# Compare
comparator = ProjectComparator()
comparison = comparator.compare_health(
    results1['health'],
    results2['health']
)

print(f"Winner: {comparison['winner']}")
```

---

## 💡 Tips for Impressive Demo

1. **Prepare two projects**: One with good health, one with poor health
2. **Show comparison**: Demonstrate how scores differ
3. **Explain metrics**: Walk through each component
4. **Highlight personality**: It's unique and memorable
5. **Show JSON export**: Proves it can integrate with other tools
6. **Mention zero dependencies**: CLI works anywhere!

---

## 🎉 Summary

**Three Ways to Run:**
1. 🌟 **Dashboard** (Best for demos): `streamlit run streamlit_app.py`
2. 💻 **CLI** (Best for automation): `python3 codepulse_analyzer.py .`
3. 🐍 **Python API** (Best for integration): Import and use in your code

**Choose based on your need:**
- **Presentation/Demo**: Use Dashboard
- **Quick Check**: Use CLI
- **Automation**: Use Python API
- **Learning**: Try all three!

---

**Now go run it and see your code's health! 🚀**
