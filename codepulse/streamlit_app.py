#!/usr/bin/env python3
"""
CodePulse Streamlit Dashboard
A beautiful web interface for code health analysis
"""

import streamlit as st
import sys
from pathlib import Path
import json
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from analyzer.file_reader import FileReader
from analyzer.complexity import ComplexityCalculator
from analyzer.style_detector import StyleDetector
from analyzer.git_analyzer import GitAnalyzer
from analyzer.anomaly_detector import AnomalyDetector
from analyzer.universal_analyzer import UniversalAnalyzer
from scorer.health_calculator import HealthCalculator
from scorer.personality import PersonalityClassifier
from generator.readme_generator import ReadmeGenerator

# Page config
st.set_page_config(
    page_title="CodePulse - Code Health Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .score-excellent { color: #28a745; }
    .score-good { color: #17a2b8; }
    .score-fair { color: #ffc107; }
    .score-poor { color: #dc3545; }
    .personality-badge {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
    }

    /* Fix dropdown positioning */
    [data-baseweb="popover"] {
        position: absolute !important;
    }

    /* Ensure dropdown appears below select box */
    [data-baseweb="select"] {
        position: relative !important;
    }

    /* Style the personality section better */
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }

    .stMetric label {
        font-size: 0.9rem !important;
        color: #aaa !important;
    }

    .stMetric [data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        font-weight: 600 !important;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data(ttl=300)
def analyze_project(project_path):
    """Analyze project and return results"""
    try:
        # File analysis
        reader = FileReader(project_path)
        file_metrics = reader.get_project_summary()

        # Analyze all code files
        complexity_results = []
        style_results = []

        python_files = [f for f in file_metrics['files'] if f['language'] == 'Python']
        non_python_files = [f for f in file_metrics['files'] if f['language'] != 'Python' and f['language'] != 'Unknown']
        all_code_files = python_files + non_python_files[:20]  # Limit non-Python to 20 files

        progress_bar = st.progress(0)
        status_text = st.empty()

        for i, file_info in enumerate(all_code_files):
            status_text.text(f"Processing: {file_info['name']} ({i+1}/{len(all_code_files)})")
            progress_bar.progress((i + 1) / len(all_code_files))

            try:
                if file_info['language'] == 'Python':
                    # Use Python-specific analyzers
                    complexity_calc = ComplexityCalculator(file_info['absolute_path'])
                    complexity_metrics = complexity_calc.get_metrics()
                    if complexity_metrics:
                        complexity_results.append(complexity_metrics)

                    style_detector = StyleDetector(file_info['absolute_path'])
                    style_fingerprint = style_detector.get_fingerprint()
                    if style_fingerprint:
                        style_results.append(style_fingerprint)
                else:
                    # Use universal analyzer for other languages
                    universal = UniversalAnalyzer(file_info['absolute_path'])

                    complexity_metrics = universal.analyze_complexity()
                    if complexity_metrics:
                        # Convert to format expected by dashboard
                        complexity_results.append({
                            'file': complexity_metrics['file'],
                            'language': complexity_metrics['language'],
                            'average_complexity': complexity_metrics['estimated_complexity'],
                            'file_complexity': complexity_metrics['estimated_complexity'],
                            'max_nesting_depth': complexity_metrics['max_nesting_depth'],
                            'quality_rating': complexity_metrics['quality_rating'],
                            'function_complexities': [
                                {
                                    'name': f"Function {j+1}",
                                    'complexity': complexity_metrics['estimated_complexity'] / max(complexity_metrics['function_count'], 1),
                                    'rating': complexity_metrics['quality_rating']
                                }
                                for j in range(min(complexity_metrics['function_count'], 5))
                            ],
                            'code_smells': []
                        })

                    style_metrics = universal.analyze_style()
                    if style_metrics:
                        # Convert to format expected by dashboard
                        style_results.append({
                            'file': style_metrics['file'],
                            'language': style_metrics['language'],
                            'indentation': style_metrics['indentation'],
                            'naming': {'dominant_style': style_metrics['naming_style']},
                            'overall_consistency': 75.0  # Default reasonable value
                        })
            except:
                continue

        progress_bar.empty()
        status_text.empty()

        # Git analysis
        try:
            git_analyzer = GitAnalyzer(project_path)
            git_metrics = git_analyzer.get_analysis()
        except:
            git_metrics = None

        # Calculate health
        calculator = HealthCalculator()
        if git_metrics is None:
            git_metrics = {'commits_last_7_days': 0, 'activity_score': 50.0}

        health_data = calculator.calculate_health_score(
            file_metrics['files'],
            complexity_results,
            style_results,
            git_metrics
        )

        # Classify personality
        classifier = PersonalityClassifier()
        personality_data = classifier.classify(
            file_metrics['files'],
            style_results,
            complexity_results
        )

        # Detect anomalies
        status_text.text("Detecting anomalies...")
        detector = AnomalyDetector(project_path)
        anomalies = detector.detect_all(file_metrics['files'])

        # Get insights
        insights = calculator.get_health_insights(health_data)

        # Get traits
        traits = classifier.get_personality_traits(personality_data['personality'])

        return {
            'file_metrics': file_metrics,
            'health': health_data,
            'personality': personality_data,
            'traits': traits,
            'insights': insights,
            'anomalies': anomalies,
            'git_metrics': git_metrics,
            'complexity_results': complexity_results,
            'style_results': style_results
        }

    except Exception as e:
        st.error(f"Error analyzing project: {e}")
        return None


def get_score_color(score):
    """Get color class based on score"""
    if score >= 90:
        return "score-excellent"
    elif score >= 80:
        return "score-good"
    elif score >= 70:
        return "score-fair"
    else:
        return "score-poor"


def create_gauge_chart(score, title):
    """Create a gauge chart for a score"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title, 'font': {'size': 20}},
        delta={'reference': 80},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1},
            'bar': {'color': "darkblue"},
            'bgcolor': "white",
            'borderwidth': 2,
            'bordercolor': "gray",
            'steps': [
                {'range': [0, 60], 'color': '#ffcccc'},
                {'range': [60, 80], 'color': '#ffffcc'},
                {'range': [80, 100], 'color': '#ccffcc'}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_component_bar_chart(health_data):
    """Create bar chart for health components"""
    components = health_data['components']

    names = [c.replace('_', ' ').title() for c in components.keys()]
    scores = [components[c]['score'] for c in components.keys()]

    colors = ['#28a745' if s >= 80 else '#ffc107' if s >= 60 else '#dc3545' for s in scores]

    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=scores,
            marker_color=colors,
            text=scores,
            texttemplate='%{text:.1f}',
            textposition='outside'
        )
    ])

    fig.update_layout(
        title="Health Components Breakdown",
        yaxis_title="Score",
        yaxis_range=[0, 110],
        height=400,
        showlegend=False
    )

    return fig


def create_language_pie_chart(file_metrics):
    """Create pie chart for language distribution"""
    lang_stats = file_metrics['language_stats']

    languages = list(lang_stats.keys())
    lines = [lang_stats[lang]['code'] for lang in languages]

    fig = px.pie(
        values=lines,
        names=languages,
        title="Language Distribution by Lines of Code"
    )

    fig.update_layout(height=400)
    return fig


def main():
    """Main Streamlit app"""

    # Header
    st.markdown('<div class="main-header">CodePulse</div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #888; margin-top: -1.5rem; margin-bottom: 2rem;">Universal Code Quality & Analytics Platform • All Languages Supported</p>', unsafe_allow_html=True)

    # Sidebar
    st.sidebar.title("⚙️ Configuration")

    # Project path input
    default_path = st.sidebar.text_input(
        "Project Path",
        value=".",
        help="Enter the path to your project directory"
    )

    analyze_button = st.sidebar.button("🔍 Analyze Project", type="primary", use_container_width=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.info("""
    **CodePulse** - Universal code analyzer supporting 12+ programming languages

    **Features:**
    - 📊 Health Score & Quality Metrics
    - 🧬 Code Personality Detection
    - 🚨 Anomaly Detection (Python)
    - 📈 Multi-Language Support
    - 📄 Documentation Generation

    **Supported Languages:**
    Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Ruby, PHP, Swift, Kotlin, Rust
    """)

    # Main content
    if analyze_button or 'results' in st.session_state:

        with st.spinner("🔍 Analyzing your code... This may take a few moments..."):
            results = analyze_project(default_path)

        if results:
            st.session_state['results'] = results
            display_dashboard(results)
    else:
        # Welcome screen
        st.markdown("""
        ## 👋 Welcome to CodePulse

        **Universal code analysis platform supporting 12+ programming languages**

        Analyze any project - Python, JavaScript, Java, C++, Go, Rust, and more!

        ### What You'll Get:
        - **📊 Health Score** - Overall code quality rating (0-100) for any language
        - **🧬 Code Personality** - Discover your development style (Python projects)
        - **📈 Detailed Metrics** - File structure, language distribution, and organization
        - **🚨 Anomaly Detection** - Security and performance issue detection (Python)
        - **📄 Documentation** - Auto-generated README with architecture diagrams

        ### Supported Languages:
        Python, JavaScript, TypeScript, Java, C/C++, C#, Go, Ruby, PHP, Swift, Kotlin, Rust

        ### How to Start:
        1. Enter your project path in the sidebar (or use `.` for current directory)
        2. Click **"Analyze Project"**
        3. Explore comprehensive analysis results across all your code

        **Note:** Advanced features like complexity analysis and anomaly detection currently support Python projects. Basic metrics and health scoring work for all languages.

        ---
        """)

        # Show example metrics
        st.markdown("### Sample Analysis Output")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Health Score", "85.3/100")
        with col2:
            st.metric("Total Files", "127")
        with col3:
            st.metric("Lines of Code", "15,420")
        with col4:
            st.metric("Issues Found", "3")


def display_dashboard(results):
    """Display the analysis dashboard"""

    health = results['health']
    personality = results['personality']
    file_metrics = results['file_metrics']

    # Top metrics row
    st.markdown("## 📊 Project Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        score = health['overall_score']
        color = get_score_color(score)
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 10px; color: white;'>
            <div style='font-size: 2.5rem; font-weight: bold;'>{score:.1f}</div>
            <div>Health Score</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); border-radius: 10px; color: white;'>
            <div style='font-size: 2.5rem; font-weight: bold;'>{file_metrics['total_files']}</div>
            <div>Files</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); border-radius: 10px; color: white;'>
            <div style='font-size: 2.5rem; font-weight: bold;'>{file_metrics['code_lines']:,}</div>
            <div>Lines of Code</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); border-radius: 10px; color: white;'>
            <div style='font-size: 2rem; font-weight: bold;'>{health['rating'].upper()}</div>
            <div>Rating</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Main charts row
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            create_gauge_chart(health['overall_score'], "Overall Health Score"),
            use_container_width=True
        )

    with col2:
        st.plotly_chart(
            create_component_bar_chart(health),
            use_container_width=True
        )

    # Personality section
    st.markdown("## 🧬 Code Personality Profile")

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown(f"""
        <div class='personality-badge'>
            {personality['personality']}
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        **Confidence:** {personality['confidence']:.1f}%

        **Description:**
        {personality['description']}
        """)

    with col2:
        st.markdown("### Key Traits")
        for trait in results['traits']:
            st.markdown(f"✨ {trait}")

    with col3:
        st.markdown("### Style Fingerprint")
        metrics = personality['metrics']

        st.metric("Comment Ratio", f"{metrics['comment_ratio']}%")
        st.metric("Consistency", f"{metrics['consistency']:.1f}%")
        st.metric("Avg Complexity", f"{metrics['complexity']:.1f}")
        st.metric("Naming Style", metrics['naming_style'])

    st.markdown("---")

    # Insights section
    st.markdown("## 💡 Insights & Recommendations")

    for insight in results['insights']:
        if '🚨' in insight or '⚠️' in insight:
            st.warning(insight)
        elif '✅' in insight or '🎉' in insight:
            st.success(insight)
        else:
            st.info(insight)

    st.markdown("---")

    # Detailed metrics tabs
    st.markdown("## 📈 Detailed Analysis")

    tabs = st.tabs([
        "📁 Project Files",
        "📊 Complexity Analysis",
        "🎨 Code Style",
        "🔄 Git Activity",
        "🚨 Anomaly Detection",
        "💾 Export & Reports"
    ])

    # Files tab
    with tabs[0]:
        st.markdown("### Project Structure Overview")

        # Language distribution
        col1, col2 = st.columns([1, 1])

        with col1:
            st.plotly_chart(
                create_language_pie_chart(file_metrics),
                use_container_width=True
            )

        with col2:
            st.markdown("### Language Statistics")
            for lang, stats in file_metrics['language_stats'].items():
                st.markdown(f"""
                **{lang}**
                - Files: {stats['files']}
                - Lines: {stats['code']:,}
                """)

        # File list
        st.markdown("### File List (Top 20)")
        file_data = []
        for file_info in file_metrics['files'][:20]:
            file_data.append({
                'File': file_info['path'],
                'Language': file_info['language'],
                'Lines': file_info['lines']['code'],
                'Size': f"{file_info['size']:,} bytes"
            })

        st.dataframe(file_data, use_container_width=True)

    # Complexity tab
    with tabs[1]:
        st.markdown("### Code Complexity Metrics")

        if results['complexity_results']:
            # Summary
            avg_complexity = sum(c['average_complexity'] for c in results['complexity_results']) / len(results['complexity_results'])
            total_smells = sum(len(c['code_smells']) for c in results['complexity_results'])

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Complexity", f"{avg_complexity:.1f}")
            with col2:
                st.metric("Total Code Smells", total_smells)
            with col3:
                st.metric("Files Analyzed", len(results['complexity_results']))

            # Most complex files
            st.markdown("### Most Complex Files")
            complex_files = sorted(
                results['complexity_results'],
                key=lambda x: x['average_complexity'],
                reverse=True
            )[:10]

            for file_complex in complex_files:
                with st.expander(f"📄 {Path(file_complex['file']).name} - Complexity: {file_complex['average_complexity']:.1f}"):
                    st.markdown(f"**Quality Rating:** {file_complex['quality_rating'].upper()}")
                    st.markdown(f"**File Complexity:** {file_complex['file_complexity']}")
                    st.markdown(f"**Max Nesting Depth:** {file_complex['max_nesting_depth']}")

                    if file_complex['function_complexities']:
                        st.markdown("**Functions:**")
                        for func in file_complex['function_complexities'][:5]:
                            st.text(f"  • {func['name']}: {func['complexity']} ({func['rating']})")

                    if file_complex['code_smells']:
                        st.markdown("**Code Smells:**")
                        for smell in file_complex['code_smells']:
                            st.text(f"  • [{smell['severity'].upper()}] {smell['message']}")
        else:
            st.info("No code files found to analyze.")

    # Style tab
    with tabs[2]:
        st.markdown("### Coding Style Analysis")

        if results['style_results']:
            # Aggregate style stats
            all_indents = [s['indentation']['style'] for s in results['style_results']]
            all_naming = [s['naming']['dominant_style'] for s in results['style_results']]

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### Indentation Style")
                from collections import Counter
                indent_counts = Counter(all_indents)
                for style, count in indent_counts.most_common():
                    percent = (count / len(all_indents) * 100)
                    st.progress(percent / 100, text=f"{style}: {count} files ({percent:.1f}%)")

            with col2:
                st.markdown("### Naming Convention")
                naming_counts = Counter(all_naming)
                for style, count in naming_counts.most_common():
                    percent = (count / len(all_naming) * 100)
                    st.progress(percent / 100, text=f"{style}: {count} files ({percent:.1f}%)")

            # Consistency scores
            st.markdown("### Consistency Scores")
            consistency_scores = [s['overall_consistency'] for s in results['style_results']]
            avg_consistency = sum(consistency_scores) / len(consistency_scores)

            st.metric("Average Consistency", f"{avg_consistency:.1f}%")

            # Distribution
            fig = go.Figure(data=[go.Histogram(x=consistency_scores, nbinsx=20)])
            fig.update_layout(
                title="Consistency Score Distribution",
                xaxis_title="Consistency %",
                yaxis_title="Number of Files",
                height=300
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No code files found for style analysis.")

    # Git tab
    with tabs[3]:
        st.markdown("### Git Activity Analysis")

        if results['git_metrics'] and results['git_metrics'].get('total_commits', 0) > 0:
            git = results['git_metrics']

            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Commits", f"{git['total_commits']:,}")
            with col2:
                st.metric("Recent Commits (7d)", git['commits_last_7_days'])
            with col3:
                st.metric("Contributors", git['contributor_count'])
            with col4:
                st.metric("Activity Score", f"{git['activity_score']:.1f}/100")

            # Contributors
            st.markdown("### Top Contributors")
            for contrib in git['contributors'][:10]:
                st.progress(
                    min(contrib['commits'] / git['total_commits'], 1.0),
                    text=f"{contrib['name']}: {contrib['commits']} commits"
                )

            # Hot files
            if git.get('hot_files'):
                st.markdown("### Hot Files (Most Changed)")
                for hot in git['hot_files'][:10]:
                    st.text(f"🔥 {hot['file']}: {hot['changes']} changes")
        else:
            st.info("Not a git repository or no git history available.")

    # Anomalies tab
    with tabs[4]:
        st.markdown("### 🚨 Production Issues & Anomalies")

        if 'anomalies' in results and results['anomalies']['total_count'] > 0:
            anomalies = results['anomalies']

            # Summary metrics
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Total Anomalies", anomalies['total_count'])
            with col2:
                critical = anomalies['severity_counts']['critical']
                st.metric("🔴 Critical", critical, delta=f"-{critical}" if critical > 0 else None)
            with col3:
                high = anomalies['severity_counts']['high']
                st.metric("🟠 High", high, delta=f"-{high}" if high > 0 else None)
            with col4:
                medium = anomalies['severity_counts']['medium']
                st.metric("🟡 Medium", medium)

            st.markdown("---")

            # Category tabs
            anomaly_tabs = st.tabs([
                "🔒 Security",
                "💾 Database",
                "🔄 Concurrency",
                "🔗 Dependencies",
                "💧 Memory",
                "⚠️ Error Handling"
            ])

            # Security Issues
            with anomaly_tabs[0]:
                security_issues = anomalies.get('security_issues', [])
                if security_issues:
                    st.markdown(f"### Found {len(security_issues)} Security Issues")

                    for issue in security_issues:
                        severity_color = {
                            'critical': '🔴',
                            'high': '🟠',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(issue['severity'], '⚪')

                        with st.expander(f"{severity_color} {issue['title']} - {issue['file']}"):
                            st.markdown(f"**Severity:** {issue['severity'].upper()}")
                            st.markdown(f"**Description:** {issue['description']}")
                            if 'line' in issue:
                                st.markdown(f"**Line:** {issue['line']}")
                            st.markdown(f"**Impact:** {issue['impact']}")
                            st.markdown(f"**Suggestion:** {issue['suggestion']}")
                else:
                    st.success("✅ No security issues found!")

            # Database Issues
            with anomaly_tabs[1]:
                db_issues = anomalies.get('database_issues', [])
                if db_issues:
                    st.markdown(f"### Found {len(db_issues)} Database Issues")

                    for issue in db_issues:
                        severity_color = {
                            'critical': '🔴',
                            'high': '🟠',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(issue['severity'], '⚪')

                        with st.expander(f"{severity_color} {issue['title']} - {issue['file']}"):
                            st.markdown(f"**Type:** {issue['type']}")
                            st.markdown(f"**Description:** {issue['description']}")
                            if 'line' in issue:
                                st.markdown(f"**Line:** {issue['line']}")
                            st.markdown(f"**Impact:** {issue['impact']}")
                            st.markdown(f"**Suggestion:** {issue['suggestion']}")
                else:
                    st.success("✅ No database issues found!")

            # Concurrency Issues
            with anomaly_tabs[2]:
                concurrency_issues = anomalies.get('concurrency_issues', [])
                if concurrency_issues:
                    st.markdown(f"### Found {len(concurrency_issues)} Concurrency Issues")

                    for issue in concurrency_issues:
                        severity_color = {
                            'critical': '🔴',
                            'high': '🟠',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(issue['severity'], '⚪')

                        with st.expander(f"{severity_color} {issue['title']} - {issue['file']}"):
                            st.markdown(f"**Type:** {issue['type']}")
                            st.markdown(f"**Description:** {issue['description']}")
                            if 'line' in issue:
                                st.markdown(f"**Line:** {issue['line']}")
                            st.markdown(f"**Impact:** {issue['impact']}")
                            st.markdown(f"**Suggestion:** {issue['suggestion']}")
                else:
                    st.success("✅ No concurrency issues found!")

            # Circular Dependencies
            with anomaly_tabs[3]:
                circular_deps = anomalies.get('circular_dependencies', [])
                if circular_deps:
                    st.markdown(f"### Found {len(circular_deps)} Circular Dependencies")

                    for issue in circular_deps:
                        with st.expander(f"🔴 {issue['title']}"):
                            st.markdown(f"**Chain:** {issue['description']}")
                            st.markdown(f"**Impact:** {issue['impact']}")
                            st.markdown(f"**Suggestion:** {issue['suggestion']}")
                            st.markdown(f"**Files Involved:**")
                            for file in issue['files']:
                                st.text(f"  • {file}")
                else:
                    st.success("✅ No circular dependencies found!")

            # Memory Leaks
            with anomaly_tabs[4]:
                memory_issues = anomalies.get('memory_leaks', [])
                if memory_issues:
                    st.markdown(f"### Found {len(memory_issues)} Potential Memory Leaks")

                    for issue in memory_issues:
                        severity_color = {
                            'critical': '🔴',
                            'high': '🟠',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(issue['severity'], '⚪')

                        with st.expander(f"{severity_color} {issue['title']} - {issue['file']}"):
                            st.markdown(f"**Type:** {issue['type']}")
                            st.markdown(f"**Description:** {issue['description']}")
                            if 'line' in issue:
                                st.markdown(f"**Line:** {issue['line']}")
                            st.markdown(f"**Impact:** {issue['impact']}")
                            st.markdown(f"**Suggestion:** {issue['suggestion']}")
                else:
                    st.success("✅ No memory leak issues found!")

            # Error Handling
            with anomaly_tabs[5]:
                error_issues = anomalies.get('error_handling', [])
                if error_issues:
                    st.markdown(f"### Found {len(error_issues)} Error Handling Issues")

                    for issue in error_issues:
                        severity_color = {
                            'critical': '🔴',
                            'high': '🟠',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(issue['severity'], '⚪')

                        with st.expander(f"{severity_color} {issue['title']} - {issue['file']}"):
                            st.markdown(f"**Type:** {issue['type']}")
                            st.markdown(f"**Description:** {issue['description']}")
                            if 'line' in issue:
                                st.markdown(f"**Line:** {issue['line']}")
                            st.markdown(f"**Impact:** {issue['impact']}")
                            st.markdown(f"**Suggestion:** {issue['suggestion']}")
                else:
                    st.success("✅ No error handling issues found!")

        else:
            st.info("No anomalies detected. Your code looks clean! ✨")

    # Export tab
    with tabs[5]:
        st.markdown("### Export Analysis Results")

        # JSON Export
        st.markdown("#### JSON Report")

        # Prepare JSON
        export_data = {
            'project_path': file_metrics['project_path'],
            'analysis_timestamp': datetime.now().isoformat(),
            'health': health,
            'personality': personality,
            'file_metrics': file_metrics,
            'insights': results['insights']
        }

        json_str = json.dumps(export_data, indent=2, default=str)

        st.download_button(
            label="📥 Download JSON Report",
            data=json_str,
            file_name=f"codepulse_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

        # Show JSON preview
        with st.expander("Preview JSON"):
            st.json(export_data)

        st.markdown("---")

        # README Export
        st.markdown("#### 📄 README Documentation Generator")
        st.markdown("Generate comprehensive documentation with code flow diagrams and architecture visualizations")

        # Initialize README generator
        readme_gen = ReadmeGenerator(
            project_path=file_metrics['project_path'],
            analysis_results=results
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Full Project README**")
            st.markdown("Complete documentation with:")
            st.markdown("- Project overview & health metrics")
            st.markdown("- Architecture diagrams")
            st.markdown("- Code flow visualizations")
            st.markdown("- Module documentation")
            st.markdown("- Getting started guide")

            # Generate button
            generate_full = st.button("🔄 Generate Full README", key="gen_full")

            # Handle generation
            if generate_full:
                with st.spinner("Generating README..."):
                    full_readme = readme_gen.generate_full_readme()
                    st.session_state['full_readme'] = full_readme
                st.success("✅ README generated!")
                st.rerun()

            # Show download and preview if README exists
            if 'full_readme' in st.session_state:
                col_a, col_b = st.columns([1, 1])
                with col_a:
                    st.download_button(
                        label="📥 Download",
                        data=st.session_state['full_readme'],
                        file_name=f"README_{datetime.now().strftime('%Y%m%d')}.md",
                        mime="text/markdown",
                        use_container_width=True
                    )
                with col_b:
                    # Use checkbox instead of button to avoid rerun
                    show_preview = st.checkbox("👁️ Preview", key="preview_full_check", value=st.session_state.get('show_full_preview', False))
                    st.session_state['show_full_preview'] = show_preview

                if st.session_state.get('show_full_preview', False):
                    with st.expander("README Preview", expanded=True):
                        st.markdown(st.session_state['full_readme'])

        with col2:
            st.markdown("**File-Specific README**")
            st.markdown("Documentation for individual file with:")
            st.markdown("- File metrics & analysis")
            st.markdown("- Code structure breakdown")
            st.markdown("- Function/class documentation")
            st.markdown("- Flow diagrams")

            # File selector - all code files
            all_files = [f['path'] for f in file_metrics.get('files', []) if f['language'] != 'Unknown']

            if all_files:
                selected_file = st.selectbox(
                    "Select a file",
                    all_files,
                    key="file_readme_selector"
                )

                st.markdown("")
                st.markdown("")
                st.markdown("")

                # Generate button
                generate_file = st.button("🔄 Generate File README", key="gen_file")

                # Handle generation
                if generate_file:
                    with st.spinner(f"Generating README for {selected_file}..."):
                        file_readme = readme_gen.generate_file_readme(selected_file)
                        st.session_state['file_readme'] = file_readme
                        st.session_state['file_readme_name'] = selected_file
                    st.success(f"✅ README generated!")
                    st.rerun()

                # Show download and preview if README exists
                if 'file_readme' in st.session_state:
                    col_a, col_b = st.columns([1, 1])
                    with col_a:
                        st.download_button(
                            label="📥 Download",
                            data=st.session_state['file_readme'],
                            file_name=f"{Path(st.session_state['file_readme_name']).stem}_README.md",
                            mime="text/markdown",
                            use_container_width=True
                        )
                    with col_b:
                        # Use checkbox instead of button to avoid rerun
                        show_file_preview = st.checkbox("👁️ Preview", key="preview_file_check", value=st.session_state.get('show_file_preview', False))
                        st.session_state['show_file_preview'] = show_file_preview

                    if st.session_state.get('show_file_preview', False):
                        with st.expander("File README Preview", expanded=True):
                            st.markdown(st.session_state['file_readme'])
            else:
                st.info("No code files found in project.")


if __name__ == '__main__':
    main()
