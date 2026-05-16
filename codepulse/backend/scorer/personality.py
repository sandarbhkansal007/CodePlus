"""
Personality Classifier - Classifies code personality
"""

from typing import Dict, List
import statistics


class PersonalityClassifier:
    """Classifies code personality based on various metrics"""

    # Personality types and their characteristics
    PERSONALITIES = {
        'Academic Researcher': {
            'comment_ratio': (15, 100),
            'consistency': (80, 100),
            'complexity': (1, 10),
            'description': 'Well-documented, clean code with thoughtful structure'
        },
        'Enterprise Corporate': {
            'comment_ratio': (10, 25),
            'consistency': (85, 100),
            'complexity': (1, 12),
            'description': 'Highly structured, follows strict conventions'
        },
        'Startup Hustle': {
            'comment_ratio': (0, 10),
            'consistency': (0, 70),
            'complexity': (5, 20),
            'description': 'Fast-moving, pragmatic, some technical debt'
        },
        'Clean Coder': {
            'comment_ratio': (8, 20),
            'consistency': (80, 100),
            'complexity': (1, 8),
            'description': 'Excellent code quality, simple and maintainable'
        },
        'Weekend Hacker': {
            'comment_ratio': (0, 15),
            'consistency': (0, 60),
            'complexity': (5, 25),
            'description': 'Experimental, mixed styles, learning as you go'
        },
        'Python Purist': {
            'comment_ratio': (10, 20),
            'consistency': (75, 100),
            'complexity': (1, 10),
            'description': 'Pythonic code, follows PEP 8, snake_case naming'
        },
        'Pragmatic Developer': {
            'comment_ratio': (5, 15),
            'consistency': (60, 85),
            'complexity': (5, 15),
            'description': 'Balanced approach, gets things done'
        }
    }

    def __init__(self):
        """Initialize Personality Classifier"""
        pass

    def calculate_metrics(self,
                         file_metrics: List[Dict],
                         style_metrics: List[Dict],
                         complexity_metrics: List[Dict]) -> Dict:
        """
        Calculate aggregate metrics for personality classification

        Returns:
            Dictionary with calculated metrics
        """
        # Calculate comment ratio
        total_lines = sum(f['lines']['total'] for f in file_metrics) if file_metrics else 0
        total_comments = sum(f['lines']['comments'] for f in file_metrics) if file_metrics else 0
        comment_ratio = (total_comments / total_lines * 100) if total_lines > 0 else 0

        # Calculate average consistency
        consistencies = [s['overall_consistency'] for s in style_metrics if 'overall_consistency' in s]
        avg_consistency = statistics.mean(consistencies) if consistencies else 70.0

        # Calculate average complexity
        complexities = [c['average_complexity'] for c in complexity_metrics if 'average_complexity' in c]
        avg_complexity = statistics.mean(complexities) if complexities else 8.0

        # Detect naming style
        naming_styles = {}
        for style in style_metrics:
            if 'naming' in style and 'dominant_style' in style['naming']:
                dominant = style['naming']['dominant_style']
                naming_styles[dominant] = naming_styles.get(dominant, 0) + 1

        dominant_naming = max(naming_styles.items(), key=lambda x: x[1])[0] if naming_styles else 'unknown'

        # Detect indentation style
        indentation_styles = {}
        for style in style_metrics:
            if 'indentation' in style and 'style' in style['indentation']:
                indent_style = style['indentation']['style']
                indentation_styles[indent_style] = indentation_styles.get(indent_style, 0) + 1

        dominant_indentation = max(indentation_styles.items(), key=lambda x: x[1])[0] if indentation_styles else 'unknown'

        return {
            'comment_ratio': round(comment_ratio, 2),
            'consistency': round(avg_consistency, 2),
            'complexity': round(avg_complexity, 2),
            'naming_style': dominant_naming,
            'indentation': dominant_indentation
        }

    def classify(self,
                file_metrics: List[Dict],
                style_metrics: List[Dict],
                complexity_metrics: List[Dict]) -> Dict:
        """
        Classify code personality

        Returns:
            Dictionary with personality type and details
        """
        metrics = self.calculate_metrics(file_metrics, style_metrics, complexity_metrics)

        # Score each personality type
        scores = {}

        for personality, characteristics in self.PERSONALITIES.items():
            score = 0

            # Comment ratio match
            comment_min, comment_max = characteristics['comment_ratio']
            if comment_min <= metrics['comment_ratio'] <= comment_max:
                score += 3

            # Consistency match
            consist_min, consist_max = characteristics['consistency']
            if consist_min <= metrics['consistency'] <= consist_max:
                score += 3

            # Complexity match
            complex_min, complex_max = characteristics['complexity']
            if complex_min <= metrics['complexity'] <= complex_max:
                score += 3

            # Special bonuses
            if personality == 'Python Purist' and metrics['naming_style'] == 'snake_case':
                score += 2

            if personality == 'Enterprise Corporate' and metrics['naming_style'] == 'camelCase':
                score += 2

            if personality == 'Weekend Hacker' and metrics['indentation'] == 'mixed':
                score += 2

            if personality == 'Startup Hustle' and metrics['comment_ratio'] < 8:
                score += 1

            scores[personality] = score

        # Get best match
        best_personality = max(scores.items(), key=lambda x: x[1])[0]
        confidence = scores[best_personality] / 9.0  # Max score is 9

        return {
            'personality': best_personality,
            'confidence': round(confidence * 100, 1),
            'description': self.PERSONALITIES[best_personality]['description'],
            'metrics': metrics,
            'all_scores': scores
        }

    def get_personality_traits(self, personality: str) -> List[str]:
        """Get list of traits for a personality type"""
        trait_map = {
            'Academic Researcher': [
                'Well-documented code',
                'Complex algorithms',
                'Formal naming conventions',
                'Thoughtful structure',
                'Minimal external dependencies'
            ],
            'Enterprise Corporate': [
                'Strict coding standards',
                'Extensive documentation',
                'Design patterns',
                'Slow to change',
                'Process-oriented'
            ],
            'Startup Hustle': [
                'Fast iteration',
                'Quick fixes',
                'External libraries',
                'Technical debt',
                'Results-focused'
            ],
            'Clean Coder': [
                'Simple solutions',
                'Readable code',
                'Well-tested',
                'Refactored regularly',
                'SOLID principles'
            ],
            'Weekend Hacker': [
                'Experimental',
                'Mixed styles',
                'Creative naming',
                'Learning focused',
                'Irregular patterns'
            ],
            'Python Purist': [
                'Pythonic code',
                'PEP 8 compliant',
                'Snake case naming',
                'List comprehensions',
                'Standard library preferred'
            ],
            'Pragmatic Developer': [
                'Balanced approach',
                'Gets things done',
                'Reasonable documentation',
                'Moderate complexity',
                'Practical solutions'
            ]
        }

        return trait_map.get(personality, [])

    def compare_personalities(self, personality1: str, personality2: str) -> Dict:
        """Compare two personality types"""
        chars1 = self.PERSONALITIES.get(personality1, {})
        chars2 = self.PERSONALITIES.get(personality2, {})

        # Calculate similarity based on characteristic ranges
        similarities = []

        for key in ['comment_ratio', 'consistency', 'complexity']:
            if key in chars1 and key in chars2:
                range1 = chars1[key]
                range2 = chars2[key]

                # Calculate overlap
                overlap_start = max(range1[0], range2[0])
                overlap_end = min(range1[1], range2[1])

                if overlap_end > overlap_start:
                    overlap = overlap_end - overlap_start
                    total_range = max(range1[1], range2[1]) - min(range1[0], range2[0])
                    similarity = (overlap / total_range) * 100
                    similarities.append(similarity)

        avg_similarity = statistics.mean(similarities) if similarities else 0

        return {
            'similarity': round(avg_similarity, 1),
            'personality1': personality1,
            'personality2': personality2,
            'description1': chars1.get('description', ''),
            'description2': chars2.get('description', '')
        }


if __name__ == '__main__':
    # Test the personality classifier
    classifier = PersonalityClassifier()

    # Sample data
    file_metrics = [
        {'lines': {'total': 100, 'code': 75, 'comments': 18, 'blank': 7}},
        {'lines': {'total': 150, 'code': 120, 'comments': 22, 'blank': 8}}
    ]

    style_metrics = [
        {
            'overall_consistency': 87.5,
            'naming': {'dominant_style': 'snake_case'},
            'indentation': {'style': 'spaces_4'}
        },
        {
            'overall_consistency': 92.0,
            'naming': {'dominant_style': 'snake_case'},
            'indentation': {'style': 'spaces_4'}
        }
    ]

    complexity_metrics = [
        {'average_complexity': 6.5},
        {'average_complexity': 7.8}
    ]

    result = classifier.classify(file_metrics, style_metrics, complexity_metrics)

    print("\n🧬 Code Personality Analysis")
    print(f"{'='*60}")
    print(f"Personality: {result['personality']}")
    print(f"Confidence: {result['confidence']}%")
    print(f"Description: {result['description']}")
    print(f"\nMetrics:")
    print(f"  Comment Ratio: {result['metrics']['comment_ratio']}%")
    print(f"  Consistency: {result['metrics']['consistency']}%")
    print(f"  Complexity: {result['metrics']['complexity']}")
    print(f"  Naming Style: {result['metrics']['naming_style']}")
    print(f"  Indentation: {result['metrics']['indentation']}")

    traits = classifier.get_personality_traits(result['personality'])
    print(f"\n✨ Personality Traits:")
    for trait in traits:
        print(f"  - {trait}")
