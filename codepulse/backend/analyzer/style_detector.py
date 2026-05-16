"""
Style Detector - Detects coding style patterns and conventions
"""

import re
from pathlib import Path
from typing import Dict, List
from collections import Counter


class StyleDetector:
    """Detects coding style and conventions"""

    def __init__(self, file_path: str):
        """
        Initialize Style Detector

        Args:
            file_path: Path to the code file
        """
        self.file_path = Path(file_path)
        self.content = None
        self.lines = []

    def read_file(self) -> bool:
        """Read the file content"""
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                self.content = f.read()
                self.lines = self.content.split('\n')
            return True
        except Exception as e:
            print(f"Error reading {self.file_path}: {e}")
            return False

    def detect_indentation(self) -> Dict[str, any]:
        """Detect indentation style (tabs vs spaces)"""
        if not self.content:
            if not self.read_file():
                return {}

        tabs = 0
        spaces_2 = 0
        spaces_4 = 0
        mixed = 0

        for line in self.lines:
            if not line.strip():
                continue

            leading_whitespace = line[:len(line) - len(line.lstrip())]

            if '\t' in leading_whitespace:
                if ' ' in leading_whitespace:
                    mixed += 1
                else:
                    tabs += 1
            elif leading_whitespace.startswith('  '):
                if leading_whitespace.startswith('    '):
                    spaces_4 += 1
                else:
                    spaces_2 += 1

        total = tabs + spaces_2 + spaces_4 + mixed

        if total == 0:
            style = 'none'
            consistency = 100
        elif mixed > total * 0.1:
            style = 'mixed'
            consistency = max(0, 100 - (mixed / total * 100))
        elif tabs > max(spaces_2, spaces_4):
            style = 'tabs'
            consistency = (tabs / total * 100) if total > 0 else 0
        elif spaces_4 > spaces_2:
            style = 'spaces_4'
            consistency = (spaces_4 / total * 100) if total > 0 else 0
        else:
            style = 'spaces_2'
            consistency = (spaces_2 / total * 100) if total > 0 else 0

        return {
            'style': style,
            'consistency': round(consistency, 1),
            'tabs_count': tabs,
            'spaces_2_count': spaces_2,
            'spaces_4_count': spaces_4,
            'mixed_count': mixed
        }

    def detect_naming_convention(self) -> Dict[str, any]:
        """Detect naming conventions (snake_case, camelCase, PascalCase)"""
        if not self.content:
            if not self.read_file():
                return {}

        # Patterns for different naming styles
        snake_case_pattern = r'\b[a-z]+_[a-z0-9_]+\b'
        camel_case_pattern = r'\b[a-z]+[A-Z][a-zA-Z0-9]*\b'
        pascal_case_pattern = r'\b[A-Z][a-zA-Z0-9]*\b'
        upper_case_pattern = r'\b[A-Z_][A-Z0-9_]+\b'

        snake_case_matches = len(re.findall(snake_case_pattern, self.content))
        camel_case_matches = len(re.findall(camel_case_pattern, self.content))
        pascal_case_matches = len(re.findall(pascal_case_pattern, self.content))
        upper_case_matches = len(re.findall(upper_case_pattern, self.content))

        total = snake_case_matches + camel_case_matches + pascal_case_matches + upper_case_matches

        if total == 0:
            dominant_style = 'none'
        else:
            styles = {
                'snake_case': snake_case_matches,
                'camelCase': camel_case_matches,
                'PascalCase': pascal_case_matches,
                'UPPER_CASE': upper_case_matches
            }
            dominant_style = max(styles, key=styles.get)

        return {
            'dominant_style': dominant_style,
            'snake_case': snake_case_matches,
            'camelCase': camel_case_matches,
            'PascalCase': pascal_case_matches,
            'UPPER_CASE': upper_case_matches
        }

    def detect_string_quotes(self) -> Dict[str, any]:
        """Detect string quote preference (single vs double)"""
        if not self.content:
            if not self.read_file():
                return {}

        single_quotes = len(re.findall(r"'[^']*'", self.content))
        double_quotes = len(re.findall(r'"[^"]*"', self.content))

        total = single_quotes + double_quotes

        if total == 0:
            preference = 'none'
            consistency = 100
        elif single_quotes > double_quotes:
            preference = 'single'
            consistency = (single_quotes / total * 100)
        elif double_quotes > single_quotes:
            preference = 'double'
            consistency = (double_quotes / total * 100)
        else:
            preference = 'mixed'
            consistency = 50

        return {
            'preference': preference,
            'consistency': round(consistency, 1),
            'single_quotes': single_quotes,
            'double_quotes': double_quotes
        }

    def calculate_comment_density(self) -> Dict[str, any]:
        """Calculate comment density and style"""
        if not self.content:
            if not self.read_file():
                return {}

        total_lines = len(self.lines)
        comment_lines = 0
        inline_comments = 0
        block_comments = 0

        for line in self.lines:
            stripped = line.strip()

            # Count comment lines
            if stripped.startswith('#') or stripped.startswith('//'):
                comment_lines += 1

            # Count inline comments
            if ' #' in line or ' //' in line:
                inline_comments += 1

            # Count block comment markers
            if stripped.startswith('/*') or stripped.startswith('"""') or stripped.startswith("'''"):
                block_comments += 1

        comment_ratio = (comment_lines / total_lines * 100) if total_lines > 0 else 0

        # Determine comment level
        if comment_ratio >= 20:
            level = 'high'
        elif comment_ratio >= 10:
            level = 'medium'
        elif comment_ratio >= 5:
            level = 'low'
        else:
            level = 'very_low'

        return {
            'comment_lines': comment_lines,
            'inline_comments': inline_comments,
            'block_comments': block_comments,
            'comment_ratio': round(comment_ratio, 2),
            'level': level
        }

    def detect_line_length(self) -> Dict[str, any]:
        """Analyze line length patterns"""
        if not self.content:
            if not self.read_file():
                return {}

        line_lengths = [len(line) for line in self.lines]

        if not line_lengths:
            return {}

        avg_length = sum(line_lengths) / len(line_lengths)
        max_length = max(line_lengths)

        # Count lines over common limits
        over_80 = sum(1 for l in line_lengths if l > 80)
        over_100 = sum(1 for l in line_lengths if l > 100)
        over_120 = sum(1 for l in line_lengths if l > 120)

        return {
            'average_length': round(avg_length, 1),
            'max_length': max_length,
            'over_80': over_80,
            'over_100': over_100,
            'over_120': over_120
        }

    def detect_import_style(self) -> Dict[str, any]:
        """Detect import organization style"""
        if not self.content:
            if not self.read_file():
                return {}

        import_lines = []
        from_lines = []

        for line in self.lines:
            stripped = line.strip()
            if stripped.startswith('import '):
                import_lines.append(stripped)
            elif stripped.startswith('from '):
                from_lines.append(stripped)

        total_imports = len(import_lines) + len(from_lines)

        return {
            'total_imports': total_imports,
            'import_statements': len(import_lines),
            'from_statements': len(from_lines),
            'style': 'from_preferred' if len(from_lines) > len(import_lines) else 'import_preferred'
        }

    def get_fingerprint(self) -> Dict:
        """
        Get complete style fingerprint

        Returns:
            Dictionary with all style information
        """
        if not self.content:
            if not self.read_file():
                return {}

        indentation = self.detect_indentation()
        naming = self.detect_naming_convention()
        quotes = self.detect_string_quotes()
        comments = self.calculate_comment_density()
        line_length = self.detect_line_length()
        imports = self.detect_import_style()

        # Calculate overall consistency score
        consistency_scores = [
            indentation.get('consistency', 0),
            quotes.get('consistency', 0)
        ]
        overall_consistency = sum(consistency_scores) / len(consistency_scores)

        return {
            'file': str(self.file_path),
            'indentation': indentation,
            'naming': naming,
            'quotes': quotes,
            'comments': comments,
            'line_length': line_length,
            'imports': imports,
            'overall_consistency': round(overall_consistency, 1)
        }

    def classify_personality(self, fingerprint: Dict = None) -> str:
        """
        Classify code personality based on style

        Returns:
            Personality type string
        """
        if fingerprint is None:
            fingerprint = self.get_fingerprint()

        if not fingerprint:
            return 'Unknown'

        # Extract key metrics
        comment_level = fingerprint['comments']['level']
        consistency = fingerprint['overall_consistency']
        indentation = fingerprint['indentation']['style']

        # Academic Researcher
        if comment_level in ['high', 'medium'] and consistency > 80:
            return 'Academic Researcher'

        # Enterprise Corporate
        if consistency > 90 and fingerprint['naming']['dominant_style'] == 'camelCase':
            return 'Enterprise Corporate'

        # Startup Hustle
        if comment_level in ['low', 'very_low'] and consistency < 70:
            return 'Startup Hustle'

        # Clean Coder
        if consistency > 85 and comment_level == 'medium':
            return 'Clean Coder'

        # Weekend Hacker
        if indentation == 'mixed' or consistency < 60:
            return 'Weekend Hacker'

        # Python Purist
        if fingerprint['naming']['dominant_style'] == 'snake_case' and consistency > 75:
            return 'Python Purist'

        return 'Pragmatic Developer'


if __name__ == '__main__':
    # Test the style detector
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("Usage: python style_detector.py <file_path>")
        sys.exit(1)

    detector = StyleDetector(file_path)
    fingerprint = detector.get_fingerprint()

    if fingerprint:
        print(f"\n🎨 Style Fingerprint: {fingerprint['file']}")
        print(f"{'='*60}")

        print(f"\n📏 Indentation:")
        ind = fingerprint['indentation']
        print(f"  Style: {ind['style']}")
        print(f"  Consistency: {ind['consistency']}%")

        print(f"\n✏️  Naming Convention:")
        naming = fingerprint['naming']
        print(f"  Dominant: {naming['dominant_style']}")
        print(f"  snake_case: {naming['snake_case']}")
        print(f"  camelCase: {naming['camelCase']}")
        print(f"  PascalCase: {naming['PascalCase']}")

        print(f"\n💬 Comments:")
        comments = fingerprint['comments']
        print(f"  Ratio: {comments['comment_ratio']}%")
        print(f"  Level: {comments['level']}")

        print(f"\n📐 Line Length:")
        length = fingerprint['line_length']
        print(f"  Average: {length['average_length']} chars")
        print(f"  Max: {length['max_length']} chars")
        print(f"  Over 80 chars: {length['over_80']} lines")

        print(f"\n📦 Imports:")
        imports = fingerprint['imports']
        print(f"  Total: {imports['total_imports']}")
        print(f"  Style: {imports['style']}")

        print(f"\n🎯 Overall Consistency: {fingerprint['overall_consistency']}%")

        personality = detector.classify_personality(fingerprint)
        print(f"\n🧬 Code Personality: {personality}")
