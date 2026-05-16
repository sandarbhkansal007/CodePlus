# 🚀 START HERE - CodePulse Quick Start

## ✅ Step 1: You're Already Set Up!

The dependencies are installed. You're ready to go!

## 🌟 Step 2: Launch the Dashboard

Open your terminal and run:

```bash
cd /Users/sandarbhkansal/repo-tree/codepulse
python3 -m streamlit run streamlit_app.py
```

**OR** use the shortcut:

```bash
cd /Users/sandarbhkansal/repo-tree/codepulse
./run_dashboard.sh
```

## 🎉 Step 3: Open Your Browser

The dashboard will automatically open at:
```
http://localhost:8501
```

If it doesn't open automatically, just copy that URL into Chrome/Safari/Firefox!

## 📊 Step 4: Analyze Your Code

1. In the sidebar, enter project path (or use `.` for current directory)
2. Click **"🔍 Analyze Project"**
3. Wait 5-10 seconds
4. **BOOM! 💥** You'll see:
   - Health Score (0-100)
   - Code Personality
   - Beautiful charts and graphs
   - Detailed insights

## 🎓 For Your Demo

**Quick Demo (2 minutes):**
```bash
# Terminal 1: Launch dashboard
cd /Users/sandarbhkansal/repo-tree/codepulse
python3 -m streamlit run streamlit_app.py

# In the browser:
# 1. Enter "." as project path
# 2. Click "Analyze Project"
# 3. Show the beautiful visualizations!
```

## 📝 What You'll See

### Main Dashboard Features:
✅ **Health Score Gauge** - Beautiful circular meter
✅ **Component Breakdown** - 5 health factors visualized
✅ **Code Personality** - Fun classification (Python Purist, etc.)
✅ **Language Distribution** - Pie chart
✅ **Complexity Analysis** - Most complex files
✅ **Git Activity** - Commit history and contributors
✅ **Export to JSON** - Download reports

## 💻 Alternative: Command Line

Don't want the dashboard? Use CLI:

```bash
python3 backend/codepulse_analyzer.py .
```

This gives you a text-based report in the terminal!

## 🆘 Need Help?

**Dashboard won't start?**
```bash
# Try this:
python3 -m pip install streamlit plotly
python3 -m streamlit run streamlit_app.py
```

**Can't find the file?**
```bash
# Make sure you're in the right directory:
cd /Users/sandarbhkansal/repo-tree/codepulse
ls -la streamlit_app.py  # Should show the file
```

**Browser doesn't open?**
- Manually go to: http://localhost:8501
- Or try: http://127.0.0.1:8501

## 🎯 Quick Tips

1. **Analyze from project root** - Best results when you analyze the whole project
2. **Git repos get more data** - Activity score needs git history
3. **Python projects work best** - Full AST analysis for Python
4. **Takes 5-30 seconds** - Depends on project size

## 📚 More Info

- **Full Guide**: Read `HOW_TO_RUN.md`
- **Examples**: Check `EXAMPLES.md`
- **Technical Details**: See `IMPLEMENTATION_SUMMARY.md`

## 🎉 You're Ready!

Just run this and enjoy:
```bash
cd /Users/sandarbhkansal/repo-tree/codepulse
python3 -m streamlit run streamlit_app.py
```

**Have fun analyzing your code! 🚀**
