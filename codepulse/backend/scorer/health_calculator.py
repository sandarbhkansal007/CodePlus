"""
Health Calculator - Calculates overall project health score
"""

from typing import Dict, List
import statistics


class HealthCalculator:
    """Calculates project health score from various metrics"""

    # Weights for different health components
    WEIGHTS = {
        'activity': 0.20,       # Git activity
        'quality': 0.25,        # Code complexity/quality
        'safety': 0.25,         # Security issues
        'documentation': 0.15,  # Comments and docs
        'organization': 0.15    # File structure
    }

    def __init__(self):
        """Initialize Health Calculator"""
        pass

    def calculate_activity_score(self, git_metrics: Dict) -> float:
        """
        Calculate activity score based on git metrics

        Args:
            git_metrics: Dictionary with git analysis results

        Returns:
            Score from 0-100
        """
        if not git_metrics:
            return 50.0

        # Use the pre-calculated activity score from git analyzer
        if 'activity_score' in git_metrics:
            return git_metrics['activity_score']

        # Fallback calculation
        commits_last_7_days = git_metrics.get('commits_last_7_days', 0)

        # 1+ commits per day = 100
        # 0 commits = 0
        score = min((commits_last_7_days / 7.0) * 100, 100)

        return round(score, 1)

    def calculate_quality_score(self, complexity_metrics: List[Dict]) -> float:
        """
        Calculate quality score based on code complexity

        Args:
            complexity_metrics: List of complexity metrics for all files

        Returns:
            Score from 0-100
        """
        if not complexity_metrics:
            return 70.0

        # Calculate average complexity across all files
        avg_complexities = []

        for file_metrics in complexity_metrics:
            if 'average_complexity' in file_metrics:
                avg_complexities.append(file_metrics['average_complexity'])

        if not avg_complexities:
            return 70.0

        overall_avg = statistics.mean(avg_complexities)

        # Scoring:
        # Complexity 1-5: 100
        # Complexity 5-10: 80-100
        # Complexity 10-15: 50-80
        # Complexity 15-20: 20-50
        # Complexity 20+: 0-20

        if overall_avg <= 5:
            score = 100
        elif overall_avg <= 10:
            score = 100 - ((overall_avg - 5) / 5.0 * 20)
        elif overall_avg <= 15:
            score = 80 - ((overall_avg - 10) / 5.0 * 30)
        elif overall_avg <= 20:
            score = 50 - ((overall_avg - 15) / 5.0 * 30)
        else:
            score = max(20 - ((overall_avg - 20) / 5.0 * 20), 0)

        return round(score, 1)

    def calculate_safety_score(self, complexity_metrics: List[Dict]) -> float:
        """
        Calculate safety score based on code smells and issues

        Args:
            complexity_metrics: List of complexity metrics for all files

        Returns:
            Score from 0-100
        """
        if not complexity_metrics:
            return 70.0

        total_smells = 0
        high_severity = 0
        medium_severity = 0

        for file_metrics in complexity_metrics:
            smells = file_metrics.get('code_smells', [])
            total_smells += len(smells)

            for smell in smells:
                if smell.get('severity') == 'high':
                    high_severity += 1
                elif smell.get('severity') == 'medium':
                    medium_severity += 1

        # Scoring based on issues found
        # 0 issues: 100
        # Each high severity: -10 points
        # Each medium severity: -5 points
        # Each low severity: -2 points

        score = 100
        score -= high_severity * 10
        score -= medium_severity * 5
        score -= (total_smells - high_severity - medium_severity) * 2

        return max(round(score, 1), 0)

    def calculate_documentation_score(self, file_metrics: List[Dict], style_metrics: List[Dict]) -> float:
        """
        Calculate documentation score based on comments

        Args:
            file_metrics: List of file analysis results
            style_metrics: List of style fingerprints

        Returns:
            Score from 0-100
        """
        if not file_metrics:
            return 50.0

        # Calculate overall comment ratio
        total_lines = sum(f['lines']['total'] for f in file_metrics)
        total_comments = sum(f['lines']['comments'] for f in file_metrics)

        if total_lines == 0:
            return 50.0

        comment_ratio = (total_comments / total_lines) * 100

        # Scoring:
        # 20%+ comments: 100
        # 15-20%: 85-100
        # 10-15%: 70-85
        # 5-10%: 50-70
        # 0-5%: 0-50

        if comment_ratio >= 20:
            score = 100
        elif comment_ratio >= 15:
            score = 85 + ((comment_ratio - 15) / 5.0 * 15)
        elif comment_ratio >= 10:
            score = 70 + ((comment_ratio - 10) / 5.0 * 15)
        elif comment_ratio >= 5:
            score = 50 + ((comment_ratio - 5) / 5.0 * 20)
        else:
            score = (comment_ratio / 5.0) * 50

        return round(score, 1)

    def calculate_organization_score(self, file_metrics: List[Dict], style_metrics: List[Dict]) -> float:
        """
        Calculate organization score based on file structure and consistency

        Args:
            file_metrics: List of file analysis results
            style_metrics: List of style fingerprints

        Returns:
            Score from 0-100
        """
        if not style_metrics:
            return 70.0

        # Calculate average consistency
        consistencies = []

        for style in style_metrics:
            if 'overall_consistency' in style:
                consistencies.append(style['overall_consistency'])

        if not consistencies:
            return 70.0

        avg_consistency = statistics.mean(consistencies)

        # Consistency directly maps to organization score
        return round(avg_consistency, 1)

    def calculate_health_score(self,
                               file_metrics: List[Dict],
                               complexity_metrics: List[Dict],
                               style_metrics: List[Dict],
                               git_metrics: Dict) -> Dict:
        """
        Calculate overall health score

        Args:
            file_metrics: List of file analysis results
            complexity_metrics: List of complexity metrics
            style_metrics: List of style fingerprints
            git_metrics: Git analysis results

        Returns:
            Dictionary with all scores and overall health
        """
        # Calculate component scores
        activity = self.calculate_activity_score(git_metrics)
        quality = self.calculate_quality_score(complexity_metrics)
        safety = self.calculate_safety_score(complexity_metrics)
        documentation = self.calculate_documentation_score(file_metrics, style_metrics)
        organization = self.calculate_organization_score(file_metrics, style_metrics)

        # Calculate weighted overall score
        overall = (
            activity * self.WEIGHTS['activity'] +
            quality * self.WEIGHTS['quality'] +
            safety * self.WEIGHTS['safety'] +
            documentation * self.WEIGHTS['documentation'] +
            organization * self.WEIGHTS['organization']
        )

        # Determine rating
        rating = self._get_rating(overall)

        return {
            'overall_score': round(overall, 1),
            'rating': rating,
            'components': {
                'activity': {
                    'score': activity,
                    'weight': self.WEIGHTS['activity'],
                    'description': 'Recent commits and development activity'
                },
                'quality': {
                    'score': quality,
                    'weight': self.WEIGHTS['quality'],
                    'description': 'Code complexity and maintainability'
                },
                'safety': {
                    'score': safety,
                    'weight': self.WEIGHTS['safety'],
                    'description': 'Code smells and potential issues'
                },
                'documentation': {
                    'score': documentation,
                    'weight': self.WEIGHTS['documentation'],
                    'description': 'Comments and documentation coverage'
                },
                'organization': {
                    'score': organization,
                    'weight': self.WEIGHTS['organization'],
                    'description': 'Code consistency and structure'
                }
            }
        }

    def _get_rating(self, score: float) -> str:
        """Get health rating from score"""
        if score >= 90:
            return 'excellent'
        elif score >= 80:
            return 'good'
        elif score >= 70:
            return 'fair'
        elif score >= 60:
            return 'needs_improvement'
        else:
            return 'poor'

    def get_health_insights(self, health_data: Dict) -> List[str]:
        """
        Generate insights based on health scores

        Args:
            health_data: Health score dictionary

        Returns:
            List of insight strings
        """
        insights = []
        components = health_data['components']

        # Check each component
        for component, data in components.items():
            score = data['score']

            if score < 50:
                insights.append(f"⚠️ {component.title()} is low ({score}/100). Consider improving {data['description'].lower()}.")
            elif score < 70:
                insights.append(f"⚡ {component.title()} could be better ({score}/100). {data['description']}.")
            elif score >= 90:
                insights.append(f"✅ {component.title()} is excellent ({score}/100)!")

        # Overall insights
        overall = health_data['overall_score']
        if overall >= 90:
            insights.insert(0, "🎉 Your code is in excellent health! Keep up the great work!")
        elif overall >= 80:
            insights.insert(0, "👍 Your code is healthy overall, with room for minor improvements.")
        elif overall >= 70:
            insights.insert(0, "📊 Your code health is fair. Focus on the lowest scoring areas.")
        elif overall >= 60:
            insights.insert(0, "⚠️ Your code needs attention. Prioritize improving safety and quality.")
        else:
            insights.insert(0, "🚨 Your code health is poor. Consider significant refactoring.")

        return insights


if __name__ == '__main__':
    # Test the health calculator
    calculator = HealthCalculator()

    # Sample data
    file_metrics = [
        {'lines': {'total': 100, 'code': 75, 'comments': 15, 'blank': 10}},
        {'lines': {'total': 150, 'code': 120, 'comments': 20, 'blank': 10}}
    ]

    complexity_metrics = [
        {'average_complexity': 6.5, 'code_smells': [
            {'severity': 'medium'},
            {'severity': 'low'}
        ]},
        {'average_complexity': 8.2, 'code_smells': []}
    ]

    style_metrics = [
        {'overall_consistency': 85.5},
        {'overall_consistency': 90.2}
    ]

    git_metrics = {
        'commits_last_7_days': 12,
        'activity_score': 85.0
    }

    health = calculator.calculate_health_score(
        file_metrics,
        complexity_metrics,
        style_metrics,
        git_metrics
    )

    print("\n📊 Health Score Report")
    print(f"{'='*60}")
    print(f"Overall Score: {health['overall_score']}/100")
    print(f"Rating: {health['rating'].upper()}")
    print(f"\nComponents:")
    for component, data in health['components'].items():
        print(f"  {component.title()}: {data['score']}/100 (weight: {data['weight']*100}%)")

    insights = calculator.get_health_insights(health)
    print(f"\n💡 Insights:")
    for insight in insights:
        print(f"  {insight}")
