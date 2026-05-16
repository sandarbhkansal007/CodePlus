#!/usr/bin/env python3
"""
CodePulse Analyzer - Main script to analyze projects
"""

import sys
import json
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from analyzer.file_reader import FileReader
from analyzer.ast_parser import ASTParser
from analyzer.complexity import ComplexityCalculator
from analyzer.style_detector import StyleDetector
from analyzer.git_analyzer import GitAnalyzer
from analyzer.anomaly_detector import AnomalyDetector
from scorer.health_calculator import HealthCalculator
from scorer.personality import PersonalityClassifier


class CodePulseAnalyzer:
    """Main analyzer class that coordinates all analysis"""

    def __init__(self, project_path: str):
        """
        Initialize CodePulse Analyzer

        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path).resolve()

        if not self.project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")

        if not self.project_path.is_dir():
            raise ValueError(f"Project path is not a directory: {project_path}")

        print(f"🔍 Analyzing project: {self.project_path}")

    def analyze_files(self) -> Dict:
        """Analyze all files in the project"""
        print("\n📁 Scanning files...")

        reader = FileReader(str(self.project_path))
        summary = reader.get_project_summary()

        print(f"   Found {summary['total_files']} files")
        print(f"   Total lines: {summary['code_lines']:,}")

        return summary

    def analyze_python_files(self, file_metrics: Dict) -> tuple:
        """Analyze Python files for complexity and style"""
        print("\n🐍 Analyzing Python files...")

        complexity_results = []
        style_results = []

        python_files = [
            f for f in file_metrics['files']
            if f['language'] == 'Python'
        ]

        for i, file_info in enumerate(python_files, 1):
            file_path = file_info['absolute_path']

            # Show progress
            if i % 5 == 0 or i == len(python_files):
                print(f"   Processing {i}/{len(python_files)} files...", end='\r')

            try:
                # Complexity analysis
                complexity_calc = ComplexityCalculator(file_path)
                complexity_metrics = complexity_calc.get_metrics()
                if complexity_metrics:
                    complexity_results.append(complexity_metrics)

                # Style analysis
                style_detector = StyleDetector(file_path)
                style_fingerprint = style_detector.get_fingerprint()
                if style_fingerprint:
                    style_results.append(style_fingerprint)

            except Exception as e:
                print(f"\n   Warning: Error analyzing {file_info['path']}: {e}")
                continue

        print(f"\n   Analyzed {len(complexity_results)} Python files")

        return complexity_results, style_results

    def analyze_git_history(self) -> Optional[Dict]:
        """Analyze git repository history"""
        print("\n🔄 Analyzing git history...")

        try:
            git_analyzer = GitAnalyzer(str(self.project_path))
            git_metrics = git_analyzer.get_analysis()

            print(f"   Total commits: {git_metrics['total_commits']}")
            print(f"   Contributors: {git_metrics['contributor_count']}")
            print(f"   Commits (last 7 days): {git_metrics['commits_last_7_days']}")

            return git_metrics

        except ValueError as e:
            print(f"   ⚠️  Not a git repository: {e}")
            return None

    def detect_anomalies(self, file_metrics: Dict) -> Dict:
        """Detect production issues and anomalies"""
        print("\n🚨 Detecting anomalies...")

        detector = AnomalyDetector(str(self.project_path))
        anomalies = detector.detect_all(file_metrics['files'])

        print(f"   Total anomalies: {anomalies['total_count']}")
        if anomalies['severity_counts']['critical'] > 0:
            print(f"   🔴 Critical: {anomalies['severity_counts']['critical']}")
        if anomalies['severity_counts']['high'] > 0:
            print(f"   🟠 High: {anomalies['severity_counts']['high']}")
        if anomalies['severity_counts']['medium'] > 0:
            print(f"   🟡 Medium: {anomalies['severity_counts']['medium']}")

        return anomalies

    def calculate_health(self,
                        file_metrics: Dict,
                        complexity_results: list,
                        style_results: list,
                        git_metrics: Optional[Dict]) -> Dict:
        """Calculate health score"""
        print("\n💊 Calculating health score...")

        calculator = HealthCalculator()

        # Use empty dict if no git metrics
        if git_metrics is None:
            git_metrics = {'commits_last_7_days': 0, 'activity_score': 50.0}

        health_data = calculator.calculate_health_score(
            file_metrics['files'],
            complexity_results,
            style_results,
            git_metrics
        )

        print(f"   Overall health: {health_data['overall_score']}/100")
        print(f"   Rating: {health_data['rating'].upper()}")

        return health_data

    def classify_personality(self,
                            file_metrics: Dict,
                            complexity_results: list,
                            style_results: list) -> Dict:
        """Classify code personality"""
        print("\n🧬 Analyzing code personality...")

        classifier = PersonalityClassifier()

        personality_data = classifier.classify(
            file_metrics['files'],
            style_results,
            complexity_results
        )

        print(f"   Personality: {personality_data['personality']}")
        print(f"   Confidence: {personality_data['confidence']}%")

        return personality_data

    def analyze(self) -> Dict:
        """
        Run complete analysis

        Returns:
            Complete analysis results
        """
        start_time = datetime.now()

        # Analyze files
        file_metrics = self.analyze_files()

        # Analyze Python files specifically
        complexity_results, style_results = self.analyze_python_files(file_metrics)

        # Analyze git history
        git_metrics = self.analyze_git_history()

        # Calculate health score
        health_data = self.calculate_health(
            file_metrics,
            complexity_results,
            style_results,
            git_metrics
        )

        # Classify personality
        personality_data = self.classify_personality(
            file_metrics,
            complexity_results,
            style_results
        )

        # Detect anomalies
        anomalies = self.detect_anomalies(file_metrics)

        # Get insights
        calculator = HealthCalculator()
        insights = calculator.get_health_insights(health_data)

        # Get personality traits
        classifier = PersonalityClassifier()
        traits = classifier.get_personality_traits(personality_data['personality'])

        end_time = datetime.now()
        analysis_time = (end_time - start_time).total_seconds()

        print(f"\n✅ Analysis complete in {analysis_time:.1f} seconds")

        return {
            'project_path': str(self.project_path),
            'analysis_timestamp': datetime.now().isoformat(),
            'analysis_duration_seconds': analysis_time,
            'file_metrics': file_metrics,
            'health': health_data,
            'personality': personality_data,
            'personality_traits': traits,
            'insights': insights,
            'git_metrics': git_metrics,
            'anomalies': anomalies,
            'summary': {
                'total_files': file_metrics['total_files'],
                'total_lines': file_metrics['total_lines'],
                'code_lines': file_metrics['code_lines'],
                'health_score': health_data['overall_score'],
                'health_rating': health_data['rating'],
                'personality_type': personality_data['personality'],
                'total_anomalies': anomalies['total_count'],
                'critical_anomalies': anomalies['severity_counts']['critical']
            }
        }

    def print_report(self, results: Dict):
        """Print a formatted report"""
        print("\n" + "="*70)
        print("📊 CODEPULSE ANALYSIS REPORT")
        print("="*70)

        # Project info
        print(f"\n📁 Project: {results['project_path']}")
        print(f"🕐 Analyzed: {results['analysis_timestamp']}")

        # Summary
        summary = results['summary']
        print(f"\n📈 Summary:")
        print(f"   Files: {summary['total_files']}")
        print(f"   Lines of Code: {summary['code_lines']:,}")
        print(f"   Health Score: {summary['health_score']}/100")
        print(f"   Rating: {summary['health_rating'].upper()}")
        print(f"   Personality: {summary['personality_type']}")

        # Health components
        print(f"\n💊 Health Breakdown:")
        for component, data in results['health']['components'].items():
            bar_length = int(data['score'] / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)
            print(f"   {component.ljust(15)}: [{bar}] {data['score']:5.1f}/100")

        # Personality
        print(f"\n🧬 Code DNA:")
        print(f"   Type: {results['personality']['personality']}")
        print(f"   Confidence: {results['personality']['confidence']}%")
        print(f"   {results['personality']['description']}")

        print(f"\n   Traits:")
        for trait in results['personality_traits']:
            print(f"      • {trait}")

        # Metrics
        metrics = results['personality']['metrics']
        print(f"\n   Style Fingerprint:")
        print(f"      Comment Ratio: {metrics['comment_ratio']}%")
        print(f"      Consistency: {metrics['consistency']}%")
        print(f"      Avg Complexity: {metrics['complexity']}")
        print(f"      Naming: {metrics['naming_style']}")
        print(f"      Indentation: {metrics['indentation']}")

        # Git info
        if results['git_metrics']:
            git = results['git_metrics']
            print(f"\n🔄 Git Activity:")
            print(f"   Total Commits: {git['total_commits']:,}")
            print(f"   Recent Commits (7 days): {git['commits_last_7_days']}")
            print(f"   Contributors: {git['contributor_count']}")
            print(f"   Activity Score: {git['activity_score']}/100")

        # Insights
        print(f"\n💡 Insights:")
        for insight in results['insights']:
            print(f"   {insight}")

        print("\n" + "="*70)

    def save_results(self, results: Dict, output_path: str):
        """Save results to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        print(f"\n💾 Results saved to: {output_path}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python codepulse_analyzer.py <project_path> [--json output.json]")
        print("\nExample:")
        print("  python codepulse_analyzer.py /path/to/project")
        print("  python codepulse_analyzer.py /path/to/project --json results.json")
        sys.exit(1)

    project_path = sys.argv[1]

    # Check for JSON output
    json_output = None
    if '--json' in sys.argv:
        json_index = sys.argv.index('--json')
        if json_index + 1 < len(sys.argv):
            json_output = sys.argv[json_index + 1]

    try:
        # Run analysis
        analyzer = CodePulseAnalyzer(project_path)
        results = analyzer.analyze()

        # Print report
        analyzer.print_report(results)

        # Save JSON if requested
        if json_output:
            analyzer.save_results(results, json_output)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
