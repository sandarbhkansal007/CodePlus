"""
AST Parser - Parses Abstract Syntax Trees to extract code structure
"""

import ast
from typing import Dict, List, Optional
from pathlib import Path


class ASTParser:
    """Parses Python code to extract structural information"""

    def __init__(self, file_path: str):
        """
        Initialize AST Parser

        Args:
            file_path: Path to the Python file
        """
        self.file_path = Path(file_path)
        self.tree = None
        self.source_code = None

    def parse(self) -> bool:
        """
        Parse the Python file

        Returns:
            True if parsing successful, False otherwise
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                self.source_code = f.read()

            self.tree = ast.parse(self.source_code)
            return True
        except SyntaxError as e:
            print(f"Syntax error in {self.file_path}: {e}")
            return False
        except Exception as e:
            print(f"Error parsing {self.file_path}: {e}")
            return False

    def extract_imports(self) -> List[str]:
        """Extract all imports from the file"""
        if not self.tree:
            return []

        imports = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.append(node.module)

        return list(set(imports))  # Remove duplicates

    def extract_functions(self) -> List[Dict]:
        """Extract all function definitions"""
        if not self.tree:
            return []

        functions = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'line': node.lineno,
                    'args': [arg.arg for arg in node.args.args],
                    'docstring': ast.get_docstring(node),
                    'is_async': isinstance(node, ast.AsyncFunctionDef),
                    'decorators': [self._get_decorator_name(dec) for dec in node.decorator_list]
                }
                functions.append(func_info)

        return functions

    def extract_classes(self) -> List[Dict]:
        """Extract all class definitions"""
        if not self.tree:
            return []

        classes = []

        for node in ast.walk(self.tree):
            if isinstance(node, ast.ClassDef):
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        methods.append({
                            'name': item.name,
                            'line': item.lineno
                        })

                class_info = {
                    'name': node.name,
                    'line': node.lineno,
                    'bases': [self._get_name(base) for base in node.bases],
                    'methods': methods,
                    'docstring': ast.get_docstring(node),
                    'decorators': [self._get_decorator_name(dec) for dec in node.decorator_list]
                }
                classes.append(class_info)

        return classes

    def extract_global_variables(self) -> List[Dict]:
        """Extract global variable assignments"""
        if not self.tree:
            return []

        variables = []

        for node in self.tree.body:
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.append({
                            'name': target.id,
                            'line': node.lineno
                        })

        return variables

    def get_structure(self) -> Dict:
        """
        Get complete file structure

        Returns:
            Dictionary with all structural information
        """
        if not self.tree:
            if not self.parse():
                return {}

        return {
            'file': str(self.file_path),
            'imports': self.extract_imports(),
            'functions': self.extract_functions(),
            'classes': self.extract_classes(),
            'global_variables': self.extract_global_variables(),
            'has_main': self._has_main_block()
        }

    def _get_decorator_name(self, decorator) -> str:
        """Get decorator name as string"""
        if isinstance(decorator, ast.Name):
            return decorator.id
        elif isinstance(decorator, ast.Call):
            return self._get_name(decorator.func)
        return 'unknown'

    def _get_name(self, node) -> str:
        """Get name from various node types"""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return f"{self._get_name(node.value)}.{node.attr}"
        elif isinstance(node, ast.Call):
            return self._get_name(node.func)
        return 'unknown'

    def _has_main_block(self) -> bool:
        """Check if file has if __name__ == '__main__' block"""
        if not self.tree:
            return False

        for node in ast.walk(self.tree):
            if isinstance(node, ast.If):
                if isinstance(node.test, ast.Compare):
                    left = node.test.left
                    if isinstance(left, ast.Name) and left.id == '__name__':
                        return True

        return False


if __name__ == '__main__':
    # Test the AST parser
    import sys

    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        print("Usage: python ast_parser.py <file_path>")
        sys.exit(1)

    parser = ASTParser(file_path)
    structure = parser.get_structure()

    if structure:
        print(f"\n📄 File: {structure['file']}")
        print(f"{'='*60}")
        print(f"\n📦 Imports ({len(structure['imports'])}):")
        for imp in structure['imports']:
            print(f"  - {imp}")

        print(f"\n🔧 Functions ({len(structure['functions'])}):")
        for func in structure['functions']:
            args = ', '.join(func['args'])
            print(f"  - {func['name']}({args}) [Line {func['line']}]")
            if func['docstring']:
                print(f"    Doc: {func['docstring'][:50]}...")

        print(f"\n📦 Classes ({len(structure['classes'])}):")
        for cls in structure['classes']:
            print(f"  - {cls['name']} [Line {cls['line']}]")
            for method in cls['methods']:
                print(f"    - {method['name']}() [Line {method['line']}]")

        print(f"\n🌐 Global Variables ({len(structure['global_variables'])}):")
        for var in structure['global_variables']:
            print(f"  - {var['name']} [Line {var['line']}]")

        print(f"\n✅ Has main block: {structure['has_main']}")
