#!/bin/bash
# Simple script to run CodePulse Dashboard

echo "🚀 Starting CodePulse Dashboard..."
echo ""
echo "📍 Location: $(pwd)"
echo ""

# Check Python version
python3 --version

# Check if streamlit is installed
echo ""
echo "Checking Streamlit..."
python3 -c "import streamlit; print(f'✅ Streamlit version: {streamlit.__version__}')" 2>/dev/null || {
    echo "❌ Streamlit not found. Installing..."
    pip3 install streamlit plotly
}

echo ""
echo "🌐 Starting dashboard..."
echo "📱 Dashboard will open at: http://localhost:8501"
echo ""
echo "💡 To analyze the sample project:"
echo "   1. In the sidebar, enter: ../sample_project"
echo "   2. Click 'Analyze Project'"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Run streamlit
cd "$(dirname "$0")"
python3 -m streamlit run streamlit_app.py --server.headless=true
