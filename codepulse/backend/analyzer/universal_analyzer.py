"""
Universal Analyzer - Basic code analysis for all languages
"""

import re
from pathlib import Path
from typing import Dict, List


class UniversalAnalyzer:
    """Provides basic code analysis for any programming language"""

    def __init__(self, file_path: str):
        """Initialize with file path"""
        self.file_path = Path(file_path)
        self.language = self._detect_language()

    def _detect_language(self) -> str:
        """Detect language from file extension"""
        ext_map = {
            '.py': 'Python',
            '.js': 'JavaScript',
            '.jsx': 'JavaScript',
            '.ts': 'TypeScript',
            '.tsx': 'TypeScript',
            '.java': 'Java',
            '.cpp': 'C++',
            '.c': 'C',
            '.h': 'C/C++',
            '.cs': 'C#',
            '.go': 'Go',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin',
            '.rs': 'Rust',
        }
        return ext_map.get(self.file_path.suffix.lower(), 'Unknown')

    def analyze_complexity(self) -> Dict:
        """
        Analyze basic complexity using pattern matching
        Works for all languages
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            # Count basic patterns that indicate complexity
            function_count = self._count_functions(content)
            class_count = self._count_classes(content)
            conditional_count = self._count_conditionals(content)
            loop_count = self._count_loops(content)
            nesting_depth = self._estimate_nesting_depth(content)

            # Calculate estimated complexity score
            complexity_score = (
                function_count * 2 +
                conditional_count * 1.5 +
                loop_count * 2 +
                nesting_depth * 3
            ) / max(function_count, 1)

            return {
                'file': str(self.file_path),
                'language': self.language,
                'function_count': function_count,
                'class_count': class_count,
                'conditional_count': conditional_count,
                'loop_count': loop_count,
                'estimated_complexity': round(complexity_score, 1),
                'max_nesting_depth': nesting_depth,
                'quality_rating': self._get_quality_rating(complexity_score),
            }
        except Exception as e:
            return None

    def _count_functions(self, content: str) -> int:
        """Count functions across different languages"""
        patterns = [
            r'\bfunction\s+\w+',  # JavaScript
            r'\bdef\s+\w+',  # Python, Ruby
            r'\bfunc\s+\w+',  # Go, Swift
            r'\bfn\s+\w+',  # Rust
            r'\b(?:public|private|protected)?\s*\w+\s+\w+\s*\(',  # Java, C#, C++
            r'\bsub\s+\w+',  # Perl
        ]
        total = 0
        for pattern in patterns:
            total += len(re.findall(pattern, content))
        return max(total, 1)  # At least 1

    def _count_classes(self, content: str) -> int:
        """Count class definitions"""
        patterns = [
            r'\bclass\s+\w+',  # Most languages
            r'\bstruct\s+\w+',  # C, C++, Go, Rust
            r'\binterface\s+\w+',  # Java, TypeScript, Go
        ]
        total = 0
        for pattern in patterns:
            total += len(re.findall(pattern, content))
        return total

    def _count_conditionals(self, content: str) -> int:
        """Count conditional statements"""
        patterns = [
            r'\bif\s*\(',
            r'\belse\s+if\s*\(',
            r'\belif\s*\(',
            r'\bswitch\s*\(',
            r'\bcase\s+',
            r'\bmatch\s+',  # Rust
            r'\?\s*.*\s*:',  # Ternary operators
        ]
        total = 0
        for pattern in patterns:
            total += len(re.findall(pattern, content))
        return total

    def _count_loops(self, content: str) -> int:
        """Count loop statements"""
        patterns = [
            r'\bfor\s*\(',
            r'\bwhile\s*\(',
            r'\bdo\s*\{',
            r'\bforeach\s*\(',
            r'\.map\s*\(',
            r'\.filter\s*\(',
            r'\.forEach\s*\(',
        ]
        total = 0
        for pattern in patterns:
            total += len(re.findall(pattern, content))
        return total

    def _estimate_nesting_depth(self, content: str) -> int:
        """Estimate maximum nesting depth by counting braces"""
        max_depth = 0
        current_depth = 0

        for char in content:
            if char in '{([':
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif char in '})]':
                current_depth = max(0, current_depth - 1)

        return max_depth

    def _get_quality_rating(self, complexity: float) -> str:
        """Get quality rating based on complexity"""
        if complexity < 5:
            return 'excellent'
        elif complexity < 10:
            return 'good'
        elif complexity < 15:
            return 'fair'
        else:
            return 'poor'

    def analyze_style(self) -> Dict:
        """
        Analyze basic style patterns
        Works for all languages
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            # Detect indentation style
            indentation = self._detect_indentation(lines)

            # Detect naming convention
            with open(self.file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            naming = self._detect_naming_style(content)

            # Calculate line length consistency
            line_lengths = [len(line.rstrip()) for line in lines if line.strip()]
            avg_line_length = sum(line_lengths) / len(line_lengths) if line_lengths else 0
            long_lines = sum(1 for length in line_lengths if length > 100)

            return {
                'file': str(self.file_path),
                'language': self.language,
                'indentation': indentation,
                'naming_style': naming,
                'average_line_length': round(avg_line_length, 1),
                'long_lines_count': long_lines,
                'total_lines': len(lines),
            }
        except Exception as e:
            return None

    def _detect_indentation(self, lines: List[str]) -> Dict:
        """Detect indentation style (tabs vs spaces)"""
        tab_count = 0
        space_count = 0

        for line in lines:
            if line.startswith('\t'):
                tab_count += 1
            elif line.startswith('    ') or line.startswith('  '):
                space_count += 1

        if tab_count > space_count:
            style = 'tabs'
        elif space_count > 0:
            # Detect 2 vs 4 spaces
            space_2 = sum(1 for line in lines if line.startswith('  ') and not line.startswith('    '))
            space_4 = sum(1 for line in lines if line.startswith('    '))
            style = 'spaces_4' if space_4 > space_2 else 'spaces_2'
        else:
            style = 'unknown'

        return {
            'style': style,
            'tabs': tab_count,
            'spaces': space_count,
        }

    def _detect_naming_style(self, content: str) -> str:
        """Detect dominant naming convention"""
        # Count different naming patterns
        snake_case = len(re.findall(r'\b[a-z]+_[a-z_]+\b', content))
        camel_case = len(re.findall(r'\b[a-z]+[A-Z][a-zA-Z]*\b', content))
        pascal_case = len(re.findall(r'\b[A-Z][a-z]+[A-Z][a-zA-Z]*\b', content))

        styles = {
            'snake_case': snake_case,
            'camelCase': camel_case,
            'PascalCase': pascal_case,
        }

        dominant = max(styles.items(), key=lambda x: x[1])
        return dominant[0] if dominant[1] > 0 else 'mixed'


if __name__ == '__main__':
    # Test the analyzer
    import sys
    if len(sys.argv) > 1:
        analyzer = UniversalAnalyzer(sys.argv[1])

        print("\n=== Complexity Analysis ===")
        complexity = analyzer.analyze_complexity()
        if complexity:
            for key, value in complexity.items():
                print(f"{key}: {value}")

        print("\n=== Style Analysis ===")
        style = analyzer.analyze_style()
        if style:
            for key, value in style.items():
                print(f"{key}: {value}")
