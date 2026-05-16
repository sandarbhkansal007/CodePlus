"""
Project Comparator - Compares two projects
"""

from typing import Dict


class ProjectComparator:
    """Compares two project analyses"""

    def __init__(self):
        """Initialize Project Comparator"""
        pass

    def compare_health(self, project1: Dict, project2: Dict) -> Dict:
        """
        Compare health scores of two projects

        Args:
            project1: First project's health data
            project2: Second project's health data

        Returns:
            Comparison dictionary
        """
        score1 = project1.get('overall_score', 0)
        score2 = project2.get('overall_score', 0)

        difference = score2 - score1
        percent_diff = (difference / score1 * 100) if score1 > 0 else 0

        return {
            'project1_score': score1,
            'project2_score': score2,
            'difference': round(difference, 1),
            'percent_difference': round(percent_diff, 1),
            'winner': 'project2' if score2 > score1 else 'project1' if score1 > score2 else 'tie'
        }

    def compare_personalities(self, personality1: str, personality2: str) -> Dict:
        """
        Compare two personality types

        Args:
            personality1: First personality type
            personality2: Second personality type

        Returns:
            Comparison dictionary
        """
        similarity_map = {
            ('Academic Researcher', 'Clean Coder'): 75,
            ('Academic Researcher', 'Python Purist'): 70,
            ('Enterprise Corporate', 'Clean Coder'): 80,
            ('Startup Hustle', 'Weekend Hacker'): 65,
            ('Startup Hustle', 'Pragmatic Developer'): 60,
            ('Clean Coder', 'Python Purist'): 85,
            ('Python Purist', 'Pragmatic Developer'): 70
        }

        # Check both directions
        key1 = (personality1, personality2)
        key2 = (personality2, personality1)

        similarity = similarity_map.get(key1, similarity_map.get(key2, 50))

        if personality1 == personality2:
            similarity = 100

        return {
            'personality1': personality1,
            'personality2': personality2,
            'similarity': similarity,
            'match': 'exact' if personality1 == personality2 else 'similar' if similarity > 70 else 'different'
        }

    def compare_metrics(self, metrics1: Dict, metrics2: Dict) -> Dict:
        """
        Compare basic metrics between projects

        Args:
            metrics1: First project's metrics
            metrics2: Second project's metrics

        Returns:
            Comparison dictionary
        """
        comparisons = {}

        # Compare lines of code
        loc1 = metrics1.get('code_lines', 0)
        loc2 = metrics2.get('code_lines', 0)
        comparisons['lines_of_code'] = {
            'project1': loc1,
            'project2': loc2,
            'difference': loc2 - loc1,
            'larger': 'project2' if loc2 > loc1 else 'project1'
        }

        # Compare file count
        files1 = metrics1.get('total_files', 0)
        files2 = metrics2.get('total_files', 0)
        comparisons['file_count'] = {
            'project1': files1,
            'project2': files2,
            'difference': files2 - files1,
            'more': 'project2' if files2 > files1 else 'project1'
        }

        # Compare languages
        langs1 = set(metrics1.get('language_stats', {}).keys())
        langs2 = set(metrics2.get('language_stats', {}).keys())
        comparisons['languages'] = {
            'project1_only': list(langs1 - langs2),
            'project2_only': list(langs2 - langs1),
            'common': list(langs1 & langs2)
        }

        return comparisons


if __name__ == '__main__':
    # Test the comparator
    comparator = ProjectComparator()

    health1 = {'overall_score': 78.5}
    health2 = {'overall_score': 85.2}

    comparison = comparator.compare_health(health1, health2)
    print("\n📊 Health Comparison")
    print(f"{'='*60}")
    print(f"Project 1: {comparison['project1_score']}")
    print(f"Project 2: {comparison['project2_score']}")
    print(f"Difference: {comparison['difference']} ({comparison['percent_difference']}%)")
    print(f"Winner: {comparison['winner']}")
