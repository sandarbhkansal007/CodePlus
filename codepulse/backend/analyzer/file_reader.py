"""
File Reader - Scans directories and reads code files
"""

import os
from pathlib import Path
from typing import List, Dict, Optional
import fnmatch


class FileReader:
    """Reads and processes files from a project directory"""

    # File extensions we support
    SUPPORTED_LANGUAGES = {
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

    # Default patterns to ignore
    DEFAULT_IGNORE_PATTERNS = [
        '*.pyc',
        '__pycache__',
        '.git',
        '.gitignore',
        'node_modules',
        'venv',
        'env',
        '.env',
        'dist',
        'build',
        '.DS_Store',
        '*.min.js',
        '*.map',
        '.idea',
        '.vscode',
        'package-lock.json',
        'yarn.lock',
    ]

    def __init__(self, project_path: str, ignore_patterns: Optional[List[str]] = None):
        """
        Initialize FileReader

        Args:
            project_path: Path to the project directory
            ignore_patterns: Additional patterns to ignore
        """
        self.project_path = Path(project_path).resolve()
        self.ignore_patterns = self.DEFAULT_IGNORE_PATTERNS.copy()

        if ignore_patterns:
            self.ignore_patterns.extend(ignore_patterns)

        if not self.project_path.exists():
            raise ValueError(f"Project path does not exist: {project_path}")

        if not self.project_path.is_dir():
            raise ValueError(f"Project path is not a directory: {project_path}")

    def should_ignore(self, path: Path) -> bool:
        """Check if a path should be ignored"""
        path_str = str(path)
        name = path.name

        for pattern in self.ignore_patterns:
            if fnmatch.fnmatch(name, pattern) or fnmatch.fnmatch(path_str, f"*{pattern}*"):
                return True

        return False

    def detect_language(self, file_path: Path) -> Optional[str]:
        """Detect programming language from file extension"""
        suffix = file_path.suffix.lower()
        return self.SUPPORTED_LANGUAGES.get(suffix)

    def count_lines(self, file_path: Path) -> Dict[str, int]:
        """
        Count different types of lines in a file

        Returns:
            Dictionary with total, code, comment, and blank line counts
        """
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            total = len(lines)
            blank = 0
            comments = 0

            for line in lines:
                stripped = line.strip()

                if not stripped:
                    blank += 1
                elif stripped.startswith('#') or stripped.startswith('//') or \
                     stripped.startswith('/*') or stripped.startswith('*'):
                    comments += 1

            code = total - blank - comments

            return {
                'total': total,
                'code': code,
                'comments': comments,
                'blank': blank
            }
        except Exception as e:
            print(f"Error counting lines in {file_path}: {e}")
            return {'total': 0, 'code': 0, 'comments': 0, 'blank': 0}

    def read_file_content(self, file_path: Path) -> Optional[str]:
        """Read and return file content"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            return None

    def scan_directory(self) -> List[Dict]:
        """
        Scan the project directory and collect file information

        Returns:
            List of dictionaries containing file information
        """
        files_info = []

        for root, dirs, files in os.walk(self.project_path):
            # Remove ignored directories from the search
            dirs[:] = [d for d in dirs if not self.should_ignore(Path(root) / d)]

            for file in files:
                file_path = Path(root) / file

                # Skip ignored files
                if self.should_ignore(file_path):
                    continue

                # Detect language
                language = self.detect_language(file_path)

                # Only process supported files
                if not language:
                    continue

                # Get relative path
                rel_path = file_path.relative_to(self.project_path)

                # Count lines
                line_counts = self.count_lines(file_path)

                # Get file size
                file_size = file_path.stat().st_size

                files_info.append({
                    'path': str(rel_path),
                    'absolute_path': str(file_path),
                    'name': file_path.name,
                    'language': language,
                    'size': file_size,
                    'lines': line_counts
                })

        return files_info

    def get_project_summary(self) -> Dict:
        """
        Get a summary of the entire project

        Returns:
            Dictionary with project statistics
        """
        files_info = self.scan_directory()

        total_files = len(files_info)
        total_lines = sum(f['lines']['total'] for f in files_info)
        total_code_lines = sum(f['lines']['code'] for f in files_info)
        total_comment_lines = sum(f['lines']['comments'] for f in files_info)
        total_blank_lines = sum(f['lines']['blank'] for f in files_info)
        total_size = sum(f['size'] for f in files_info)

        # Count by language
        language_stats = {}
        for file_info in files_info:
            lang = file_info['language']
            if lang not in language_stats:
                language_stats[lang] = {
                    'files': 0,
                    'lines': 0,
                    'code': 0
                }

            language_stats[lang]['files'] += 1
            language_stats[lang]['lines'] += file_info['lines']['total']
            language_stats[lang]['code'] += file_info['lines']['code']

        return {
            'project_path': str(self.project_path),
            'total_files': total_files,
            'total_lines': total_lines,
            'code_lines': total_code_lines,
            'comment_lines': total_comment_lines,
            'blank_lines': total_blank_lines,
            'total_size': total_size,
            'language_stats': language_stats,
            'files': files_info
        }


if __name__ == '__main__':
    # Test the file reader
    import sys

    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = '.'

    reader = FileReader(project_path)
    summary = reader.get_project_summary()

    print(f"\n📊 Project Summary: {summary['project_path']}")
    print(f"{'='*60}")
    print(f"Total Files: {summary['total_files']}")
    print(f"Total Lines: {summary['total_lines']:,}")
    print(f"Code Lines: {summary['code_lines']:,}")
    print(f"Comment Lines: {summary['comment_lines']:,}")
    print(f"Blank Lines: {summary['blank_lines']:,}")
    print(f"Total Size: {summary['total_size']:,} bytes")
    print(f"\n📚 Languages:")
    for lang, stats in summary['language_stats'].items():
        print(f"  {lang}: {stats['files']} files, {stats['code']:,} lines")
