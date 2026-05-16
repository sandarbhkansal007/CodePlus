"""
Complexity Calculator - Calculates cyclomatic complexity and other metrics
"""

import ast
from typing import Dict, List
from pathlib import Path


class ComplexityCalculator:
    """Calculates code complexity metrics"""

    def __init__(self, file_path: str):
        """
        Initialize Complexity Calculator

        Args:
            file_path: Path to the Python file
        """
        self.file_path = Path(file_path)
        self.tree = None
        self.source_code = None

    def parse(self) -> bool:
        """Parse the Python file"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.source_code = f.read()

            self.tree = ast.parse(self.source_code)
            return True
        except Exception as e:
            print(f"Error parsing {self.file_path}: {e}")
            return False

    def calculate_cyclomatic_complexity(self, node=None) -> int:
        """
        Calculate cyclomatic complexity for a node

        Cyclomatic complexity = number of decision points + 1

        Decision points:
        - if, elif, else
        - for, while loops
        - except handlers
        - and, or operators
        - list/dict comprehensions
        """
        if node is None:
            if not self.tree:
                if not self.parse():
                    return 0
            node = self.tree

        complexity = 1  # Start with 1

        for child in ast.walk(node):
            # Decision structures
            if isinstance(child, (ast.If, ast.For, ast.While, ast.ExceptHandler)):
                complexity += 1

            # Boolean operators (and, or)
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1

            # Comprehensions
            elif isinstance(child, (ast.ListComp, ast.DictComp, ast.SetComp)):
                complexity += 1

            # Ternary operator
            elif isinstance(child, ast.IfExp):
                complexity += 1

        return complexity

    def calculate_function_complexity(self) -> List[Dict]:
        """Calculate complexity for each function"""
        if not self.tree:
            if not self.parse():
                return []

        function_complexities = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                complexity = self.calculate_cyclomatic_complexity(node)
                function_complexities.append({
                    'name': node.name,
                    'line': node.lineno,
                    'complexity': complexity,
                    'rating': self._get_complexity_rating(complexity)
                })

        return function_complexities

    def calculate_nesting_depth(self) -> int:
        """Calculate maximum nesting depth"""
        if not self.tree:
            if not self.parse():
                return 0

        max_depth = 0

        def get_depth(node, current_depth=0):
            nonlocal max_depth
            max_depth = max(max_depth, current_depth)

            for child in ast.iter_child_nodes(node):
                # Increase depth for control structures
                if isinstance(child, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
                    get_depth(child, current_depth + 1)
                else:
                    get_depth(child, current_depth)

        get_depth(self.tree)
        return max_depth

    def count_functions_and_classes(self) -> Dict[str, int]:
        """Count number of functions and classes"""
        if not self.tree:
            if not self.parse():
                return {'functions': 0, 'classes': 0, 'methods': 0}

        functions = 0
        classes = 0
        methods = 0

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                # Check if it's a method (inside a class)
                for parent in ast.walk(self.tree):
                    if isinstance(parent, ast.ClassDef):
                        if node in ast.walk(parent):
                            methods += 1
                            break
                else:
                    functions += 1

            elif isinstance(node, ast.ClassDef):
                classes += 1

        return {
            'functions': functions,
            'classes': classes,
            'methods': methods
        }

    def detect_code_smells(self) -> List[Dict]:
        """Detect common code smells"""
        if not self.tree:
            if not self.parse():
                return []

        smells = []

        # Check for long functions
        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                func_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0

                # Long function (>50 lines)
                if func_lines > 50:
                    smells.append({
                        'type': 'long_function',
                        'name': node.name,
                        'line': node.lineno,
                        'severity': 'medium',
                        'message': f"Function '{node.name}' is {func_lines} lines long (>50)"
                    })

                # Too many parameters (>5)
                num_params = len(node.args.args)
                if num_params > 5:
                    smells.append({
                        'type': 'too_many_parameters',
                        'name': node.name,
                        'line': node.lineno,
                        'severity': 'low',
                        'message': f"Function '{node.name}' has {num_params} parameters (>5)"
                    })

                # High complexity
                complexity = self.calculate_cyclomatic_complexity(node)
                if complexity > 10:
                    smells.append({
                        'type': 'high_complexity',
                        'name': node.name,
                        'line': node.lineno,
                        'severity': 'high',
                        'message': f"Function '{node.name}' has complexity {complexity} (>10)"
                    })

            # Large class (>500 lines)
            elif isinstance(node, ast.ClassDef):
                class_lines = node.end_lineno - node.lineno if hasattr(node, 'end_lineno') else 0
                if class_lines > 500:
                    smells.append({
                        'type': 'large_class',
                        'name': node.name,
                        'line': node.lineno,
                        'severity': 'medium',
                        'message': f"Class '{node.name}' is {class_lines} lines long (>500)"
                    })

        # Deep nesting
        max_depth = self.calculate_nesting_depth()
        if max_depth > 4:
            smells.append({
                'type': 'deep_nesting',
                'name': 'file',
                'line': 0,
                'severity': 'medium',
                'message': f"Maximum nesting depth is {max_depth} (>4)"
            })

        return smells

    def get_metrics(self) -> Dict:
        """
        Get all complexity metrics

        Returns:
            Dictionary with all metrics
        """
        if not self.tree:
            if not self.parse():
                return {}

        file_complexity = self.calculate_cyclomatic_complexity()
        function_complexities = self.calculate_function_complexity()
        counts = self.count_functions_and_classes()
        nesting_depth = self.calculate_nesting_depth()
        code_smells = self.detect_code_smells()

        # Calculate average complexity
        if function_complexities:
            avg_complexity = sum(f['complexity'] for f in function_complexities) / len(function_complexities)
        else:
            avg_complexity = file_complexity

        return {
            'file': str(self.file_path),
            'file_complexity': file_complexity,
            'average_complexity': round(avg_complexity, 2),
            'max_nesting_depth': nesting_depth,
            'function_count': counts['functions'],
            'class_count': counts['classes'],
            'method_count': counts['methods'],
            'function_complexities': function_complexities,
            'code_smells': code_smells,
            'quality_rating': self._get_quality_rating(avg_complexity, nesting_depth, len(code_smells))
        }

    def _get_complexity_rating(self, complexity: int) -> str:
        """Get complexity rating"""
        if complexity <= 5:
            return 'simple'
        elif complexity <= 10:
            return 'moderate'
        elif complexity <= 20:
            return 'complex'
        else:
            return 'very_complex'

    def _get_quality_rating(self, avg_complexity: float, nesting: int, smells: int) -> str:
        """Get overall quality rating"""
        score = 0

        # Complexity scoring
        if avg_complexity <= 5:
            score += 3
        elif avg_complexity <= 10:
            score += 2
        elif avg_complexity <= 15:
            score += 1

        # Nesting scoring
        if nesting <= 3:
            score += 3
        elif nesting <= 4:
            score += 2
        elif nesting <= 5:
            score += 1

        # Code smells scoring
        if smells == 0:
            score += 3
        elif smells <= 2:
            score += 2
        elif smells <= 5:
            score += 1

        # Overall rating
        if score >= 8:
            return 'excellent'
        elif score >= 6:
            return 'good'
        elif score >= 4:
            return 'fair'
        else:
            return 'poor'


if __name__ == '__main__':
    # Test the complexity calculator
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("Usage: python complexity.py <file_path>")
        sys.exit(1)

    calc = ComplexityCalculator(file_path)
    metrics = calc.get_metrics()

    if metrics:
        print(f"\n📊 Complexity Metrics: {metrics['file']}")
        print(f"{'='*60}")
        print(f"File Complexity: {metrics['file_complexity']}")
        print(f"Average Complexity: {metrics['average_complexity']}")
        print(f"Max Nesting Depth: {metrics['max_nesting_depth']}")
        print(f"Functions: {metrics['function_count']}")
        print(f"Classes: {metrics['class_count']}")
        print(f"Methods: {metrics['method_count']}")
        print(f"Quality Rating: {metrics['quality_rating'].upper()}")

        if metrics['function_complexities']:
            print(f"\n🔧 Function Complexities:")
            for func in metrics['function_complexities']:
                print(f"  - {func['name']}: {func['complexity']} ({func['rating']})")

        if metrics['code_smells']:
            print(f"\n⚠️  Code Smells ({len(metrics['code_smells'])}):")
            for smell in metrics['code_smells']:
                print(f"  - [{smell['severity'].upper()}] {smell['message']}")
