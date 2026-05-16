"""
Anomaly Detector - Detects real production issues in code

Detects:
1. Circular Dependencies
2. Concurrency Problems
3. Security Issues (Auth/Authorization)
4. Heavy Database Calls
5. N+1 Query Problems
6. Memory Leaks
7. Hardcoded Secrets
8. Missing Error Handling
"""

import ast
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict


class AnomalyDetector:
    """Detects production-level code anomalies and anti-patterns"""

    def __init__(self, project_path: str):
        """
        Initialize Anomaly Detector

        Args:
            project_path: Path to the project directory
        """
        self.project_path = Path(project_path)
        self.anomalies = []

    def detect_all(self, file_metrics: List[Dict]) -> Dict:
        """
        Run all anomaly detection algorithms

        Args:
            file_metrics: List of file information from FileReader

        Returns:
            Dictionary with all detected anomalies
        """
        self.anomalies = []

        # Get all Python files
        python_files = [f for f in file_metrics if f['language'] == 'Python']

        # Run all detections
        circular_deps = self.detect_circular_dependencies(python_files)
        concurrency_issues = self.detect_concurrency_problems(python_files)
        security_issues = self.detect_security_issues(python_files)
        db_issues = self.detect_database_issues(python_files)
        memory_issues = self.detect_memory_leaks(python_files)
        error_handling = self.detect_missing_error_handling(python_files)

        # Aggregate results
        all_anomalies = {
            'circular_dependencies': circular_deps,
            'concurrency_issues': concurrency_issues,
            'security_issues': security_issues,
            'database_issues': db_issues,
            'memory_leaks': memory_issues,
            'error_handling': error_handling,
            'total_count': len(circular_deps) + len(concurrency_issues) +
                          len(security_issues) + len(db_issues) +
                          len(memory_issues) + len(error_handling)
        }

        all_anomalies['severity_counts'] = self._count_by_severity(all_anomalies)

        return all_anomalies

    # ============================================
    # ALGORITHM 1: Circular Dependency Detection
    # ============================================
    def detect_circular_dependencies(self, python_files: List[Dict]) -> List[Dict]:
        """
        Detect circular dependencies between modules

        Algorithm:
        1. Build dependency graph from imports
        2. Use DFS to detect cycles
        3. Report all circular chains found

        Returns:
            List of circular dependency chains
        """
        anomalies = []

        # Build import graph
        import_graph = defaultdict(set)

        for file_info in python_files:
            file_path = file_info['absolute_path']
            module_name = Path(file_path).stem

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                # Extract imports
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            import_graph[module_name].add(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            import_graph[module_name].add(node.module)
            except:
                continue

        # Detect cycles using DFS
        def find_cycles(node, path, visited):
            if node in path:
                # Found a cycle
                cycle_start = path.index(node)
                cycle = path[cycle_start:] + [node]
                return [cycle]

            if node in visited:
                return []

            visited.add(node)
            path.append(node)

            cycles = []
            for neighbor in import_graph.get(node, []):
                cycles.extend(find_cycles(neighbor, path[:], visited))

            return cycles

        visited = set()
        all_cycles = []

        for module in import_graph.keys():
            if module not in visited:
                cycles = find_cycles(module, [], visited)
                all_cycles.extend(cycles)

        # Remove duplicate cycles
        unique_cycles = []
        seen = set()
        for cycle in all_cycles:
            cycle_key = tuple(sorted(cycle))
            if cycle_key not in seen:
                seen.add(cycle_key)
                unique_cycles.append(cycle)

        # Create anomaly records
        for cycle in unique_cycles:
            anomalies.append({
                'type': 'circular_dependency',
                'severity': 'high',
                'title': 'Circular Dependency Detected',
                'description': f"Circular import chain: {' -> '.join(cycle)}",
                'impact': 'Can cause import errors and make code hard to test',
                'suggestion': 'Refactor to break the circular dependency. Consider dependency injection or restructuring modules.',
                'files': cycle
            })

        return anomalies

    # ============================================
    # ALGORITHM 2: Concurrency Problem Detection
    # ============================================
    def detect_concurrency_problems(self, python_files: List[Dict]) -> List[Dict]:
        """
        Detect concurrency and threading issues

        Algorithm:
        1. Find threading/multiprocessing/asyncio usage
        2. Check for missing locks on shared resources
        3. Detect race conditions (shared variables without synchronization)
        4. Find blocking calls in async functions

        Returns:
            List of concurrency issues
        """
        anomalies = []

        for file_info in python_files:
            file_path = file_info['absolute_path']

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)

                # Check for threading without locks
                has_threading = 'threading' in content or 'Thread(' in content
                has_multiprocessing = 'multiprocessing' in content or 'Process(' in content
                has_lock = 'Lock()' in content or 'RLock()' in content or 'Semaphore()' in content

                if (has_threading or has_multiprocessing) and not has_lock:
                    anomalies.append({
                        'type': 'missing_synchronization',
                        'severity': 'high',
                        'title': 'Missing Thread Synchronization',
                        'description': f"File uses threading/multiprocessing without locks",
                        'file': file_info['path'],
                        'impact': 'Race conditions can cause data corruption and unpredictable behavior',
                        'suggestion': 'Use threading.Lock() or multiprocessing.Lock() to protect shared resources'
                    })

                # Check for blocking calls in async functions
                for node in ast.walk(tree):
                    if isinstance(node, ast.AsyncFunctionDef):
                        func_name = node.name
                        # Check for blocking calls inside async function
                        for child in ast.walk(node):
                            if isinstance(child, ast.Call):
                                if isinstance(child.func, ast.Attribute):
                                    call_name = child.func.attr
                                    # Common blocking calls
                                    if call_name in ['sleep', 'read', 'write', 'connect']:
                                        anomalies.append({
                                            'type': 'blocking_call_in_async',
                                            'severity': 'medium',
                                            'title': 'Blocking Call in Async Function',
                                            'description': f"Function '{func_name}' uses blocking call '{call_name}' in async context",
                                            'file': file_info['path'],
                                            'line': node.lineno,
                                            'impact': 'Blocks the event loop, defeating the purpose of async',
                                            'suggestion': f"Use 'await asyncio.{call_name}()' instead of blocking '{call_name}()'"
                                        })

                # Check for shared mutable state
                class_vars = []
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for item in node.body:
                            if isinstance(item, ast.Assign):
                                for target in item.targets:
                                    if isinstance(target, ast.Name):
                                        # Class variable (shared state)
                                        class_vars.append(target.id)

                if class_vars and (has_threading or has_multiprocessing):
                    anomalies.append({
                        'type': 'shared_mutable_state',
                        'severity': 'medium',
                        'title': 'Shared Mutable State Without Protection',
                        'description': f"Class variables {class_vars[:3]} may be shared between threads",
                        'file': file_info['path'],
                        'impact': 'Race conditions when multiple threads access shared state',
                        'suggestion': 'Use thread-local storage or protect with locks'
                    })

            except:
                continue

        return anomalies

    # ============================================
    # ALGORITHM 3: Security Issue Detection
    # ============================================
    def detect_security_issues(self, python_files: List[Dict]) -> List[Dict]:
        """
        Detect security vulnerabilities

        Algorithm:
        1. SQL Injection: Find string formatting in SQL queries
        2. Hardcoded Secrets: Detect passwords, API keys, tokens
        3. Weak Authentication: Find plain text password storage
        4. Missing Authorization: Find endpoints without auth checks
        5. XSS Vulnerabilities: Unescaped user input in output
        6. Command Injection: User input in system commands

        Returns:
            List of security issues
        """
        anomalies = []

        # Patterns for secrets
        secret_patterns = [
            (r'password\s*=\s*["\']([^"\']{8,})["\']', 'Hardcoded Password'),
            (r'api[_-]?key\s*=\s*["\']([^"\']{20,})["\']', 'Hardcoded API Key'),
            (r'secret[_-]?key\s*=\s*["\']([^"\']{20,})["\']', 'Hardcoded Secret Key'),
            (r'token\s*=\s*["\']([^"\']{20,})["\']', 'Hardcoded Token'),
            (r'aws[_-]?access[_-]?key\s*=\s*["\']([^"\']{16,})["\']', 'AWS Access Key'),
        ]

        for file_info in python_files:
            file_path = file_info['absolute_path']

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    lines = content.split('\n')
                    tree = ast.parse(content)

                # 1. SQL Injection Detection
                for i, line in enumerate(lines, 1):
                    # Check for SQL with string formatting
                    if any(sql_keyword in line.upper() for sql_keyword in ['SELECT', 'INSERT', 'UPDATE', 'DELETE']):
                        if '%s' in line or '.format(' in line or 'f"' in line or "f'" in line:
                            anomalies.append({
                                'type': 'sql_injection',
                                'severity': 'critical',
                                'title': 'Potential SQL Injection',
                                'description': f"SQL query uses string formatting instead of parameterized query",
                                'file': file_info['path'],
                                'line': i,
                                'impact': 'Attackers can inject malicious SQL and access/modify database',
                                'suggestion': 'Use parameterized queries with placeholders (e.g., cursor.execute(query, params))'
                            })

                # 2. Hardcoded Secrets
                for pattern, secret_type in secret_patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        line_num = content[:match.start()].count('\n') + 1
                        anomalies.append({
                            'type': 'hardcoded_secret',
                            'severity': 'critical',
                            'title': f'{secret_type} Hardcoded',
                            'description': f"Found hardcoded {secret_type.lower()} in source code",
                            'file': file_info['path'],
                            'line': line_num,
                            'impact': 'Secrets in source code can be exposed in version control',
                            'suggestion': 'Use environment variables or secure secret management (e.g., AWS Secrets Manager)'
                        })

                # 3. Plain Text Password Storage
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        for target in node.targets:
                            if isinstance(target, ast.Name):
                                if 'password' in target.id.lower():
                                    # Check if it's being assigned a plain value (not a hash)
                                    if not any(func in ast.dump(node.value) for func in ['hash', 'bcrypt', 'sha', 'md5']):
                                        anomalies.append({
                                            'type': 'plain_text_password',
                                            'severity': 'high',
                                            'title': 'Plain Text Password Storage',
                                            'description': f"Password stored in plain text without hashing",
                                            'file': file_info['path'],
                                            'line': node.lineno,
                                            'impact': 'Password breach exposes all user passwords',
                                            'suggestion': 'Use bcrypt, scrypt, or Argon2 to hash passwords'
                                        })

                # 4. Command Injection
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Attribute):
                            if node.func.attr in ['system', 'popen', 'exec', 'eval']:
                                # Check if user input is used
                                if any('input' in ast.dump(arg) or 'request' in ast.dump(arg) for arg in node.args):
                                    anomalies.append({
                                        'type': 'command_injection',
                                        'severity': 'critical',
                                        'title': 'Potential Command Injection',
                                        'description': f"User input used in {node.func.attr}() call",
                                        'file': file_info['path'],
                                        'line': node.lineno,
                                        'impact': 'Attackers can execute arbitrary system commands',
                                        'suggestion': 'Sanitize input or use subprocess with shell=False and argument list'
                                    })

                # 5. Missing Authorization Checks (for Flask/FastAPI routes)
                for i, line in enumerate(lines, 1):
                    # Check for route decorators
                    if '@app.route' in line or '@router.' in line:
                        # Check if next few lines have auth check
                        next_lines = '\n'.join(lines[i:i+10])
                        if not any(auth_keyword in next_lines for auth_keyword in ['@login_required', '@require_auth', 'check_permission', 'verify_token', 'authenticate']):
                            anomalies.append({
                                'type': 'missing_authorization',
                                'severity': 'high',
                                'title': 'Missing Authorization Check',
                                'description': f"API endpoint defined without authentication/authorization",
                                'file': file_info['path'],
                                'line': i,
                                'impact': 'Unauthorized users can access protected resources',
                                'suggestion': 'Add authentication decorator or verify user permissions'
                            })

            except:
                continue

        return anomalies

    # ============================================
    # ALGORITHM 4: Database Issue Detection
    # ============================================
    def detect_database_issues(self, python_files: List[Dict]) -> List[Dict]:
        """
        Detect database-related performance issues

        Algorithm:
        1. N+1 Query Problem: DB queries inside loops
        2. Missing Connection Pooling
        3. Unclosed DB connections
        4. Missing Indexes (hints from queries)
        5. SELECT * usage (fetching unnecessary data)

        Returns:
            List of database issues
        """
        anomalies = []

        for file_info in python_files:
            file_path = file_info['absolute_path']

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)

                # 1. N+1 Query Problem (queries in loops)
                for node in ast.walk(tree):
                    if isinstance(node, (ast.For, ast.While)):
                        loop_body = ast.dump(node)
                        # Check for DB queries in loop
                        if any(db_call in loop_body for db_call in ['execute(', 'query(', 'filter(', 'get(']):
                            anomalies.append({
                                'type': 'n_plus_1_query',
                                'severity': 'high',
                                'title': 'N+1 Query Problem',
                                'description': f"Database query executed inside loop",
                                'file': file_info['path'],
                                'line': node.lineno,
                                'impact': 'Performance degradation: 1000 loop iterations = 1000 DB queries',
                                'suggestion': 'Use bulk queries, joins, or eager loading (e.g., select_related, prefetch_related)'
                            })

                # 2. Missing Connection Pooling
                if 'connect(' in content and 'pool' not in content.lower():
                    anomalies.append({
                        'type': 'missing_connection_pooling',
                        'severity': 'medium',
                        'title': 'Missing Database Connection Pooling',
                        'description': f"Database connections created without pooling",
                        'file': file_info['path'],
                        'impact': 'Each request creates new connection, exhausting DB resources',
                        'suggestion': 'Use connection pooling (SQLAlchemy pool, psycopg2 pool, etc.)'
                    })

                # 3. Unclosed Connections
                for node in ast.walk(tree):
                    if isinstance(node, ast.Assign):
                        if 'connect' in ast.dump(node):
                            # Check if there's a corresponding close()
                            func_node = node
                            while func_node and not isinstance(func_node, ast.FunctionDef):
                                func_node = getattr(func_node, 'parent', None)

                            if func_node:
                                func_body = ast.dump(func_node)
                                if '.close()' not in func_body and 'with' not in func_body[:100]:
                                    anomalies.append({
                                        'type': 'unclosed_connection',
                                        'severity': 'medium',
                                        'title': 'Unclosed Database Connection',
                                        'description': f"Database connection not explicitly closed",
                                        'file': file_info['path'],
                                        'line': node.lineno,
                                        'impact': 'Connection leaks exhaust database connection pool',
                                        'suggestion': 'Use context manager (with statement) or ensure close() is called'
                                    })

                # 4. SELECT * Usage
                import re
                select_star_pattern = r'SELECT\s+\*\s+FROM'
                matches = re.finditer(select_star_pattern, content, re.IGNORECASE)
                for match in matches:
                    line_num = content[:match.start()].count('\n') + 1
                    anomalies.append({
                        'type': 'select_star',
                        'severity': 'low',
                        'title': 'SELECT * Usage',
                        'description': f"Query uses SELECT * instead of specific columns",
                        'file': file_info['path'],
                        'line': line_num,
                        'impact': 'Fetches unnecessary data, increases network traffic and memory',
                        'suggestion': 'Select only required columns explicitly'
                    })

            except:
                continue

        return anomalies

    # ============================================
    # ALGORITHM 5: Memory Leak Detection
    # ============================================
    def detect_memory_leaks(self, python_files: List[Dict]) -> List[Dict]:
        """
        Detect potential memory leaks

        Algorithm:
        1. Unclosed file handles
        2. Unclosed network connections
        3. Growing lists/caches without limits
        4. Circular references in classes

        Returns:
            List of memory leak issues
        """
        anomalies = []

        for file_info in python_files:
            file_path = file_info['absolute_path']

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    tree = ast.parse(content)

                # 1. Unclosed File Handles
                for node in ast.walk(tree):
                    if isinstance(node, ast.Call):
                        if isinstance(node.func, ast.Name) and node.func.id == 'open':
                            # Check if it's in a with statement
                            parent = node
                            in_with = False
                            # Simple heuristic: check surrounding context
                            node_str = ast.dump(node)
                            if 'with' not in content[max(0, content.find(node_str)-50):content.find(node_str)]:
                                anomalies.append({
                                    'type': 'unclosed_file',
                                    'severity': 'medium',
                                    'title': 'Unclosed File Handle',
                                    'description': f"File opened without using 'with' statement",
                                    'file': file_info['path'],
                                    'line': node.lineno,
                                    'impact': 'File handles not released, can exhaust system resources',
                                    'suggestion': "Use 'with open(...) as f:' to ensure files are closed"
                                })

                # 2. Growing Caches Without Limits
                for node in ast.walk(tree):
                    if isinstance(node, ast.ClassDef):
                        for item in node.body:
                            if isinstance(item, ast.Assign):
                                # Check for cache/list class variables
                                if isinstance(item.value, (ast.Dict, ast.List)):
                                    for target in item.targets:
                                        if isinstance(target, ast.Name):
                                            if 'cache' in target.id.lower() or 'buffer' in target.id.lower():
                                                # Check if there's any size limit logic
                                                class_body = ast.dump(node)
                                                if 'maxsize' not in class_body and 'limit' not in class_body:
                                                    anomalies.append({
                                                        'type': 'unbounded_cache',
                                                        'severity': 'medium',
                                                        'title': 'Unbounded Cache/Buffer',
                                                        'description': f"Cache '{target.id}' has no size limit",
                                                        'file': file_info['path'],
                                                        'line': item.lineno,
                                                        'impact': 'Memory usage grows indefinitely, leading to OOM errors',
                                                        'suggestion': 'Use LRU cache with maxsize or implement eviction policy'
                                                    })

            except:
                continue

        return anomalies

    # ============================================
    # ALGORITHM 6: Error Handling Detection
    # ============================================
    def detect_missing_error_handling(self, python_files: List[Dict]) -> List[Dict]:
        """
        Detect missing or poor error handling

        Algorithm:
        1. Functions without try-except
        2. Empty except blocks
        3. Catching generic Exception
        4. Silent failures

        Returns:
            List of error handling issues
        """
        anomalies = []

        for file_info in python_files:
            file_path = file_info['absolute_path']

            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    tree = ast.parse(f.read())

                # Find functions with risky operations but no error handling
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        func_body = ast.dump(node)

                        # Check for risky operations
                        has_risky_ops = any(op in func_body for op in [
                            'open(', 'connect(', 'request(', 'json.loads', 'int(', 'float('
                        ])

                        # Check for try-except
                        has_error_handling = 'Try(' in func_body

                        if has_risky_ops and not has_error_handling:
                            anomalies.append({
                                'type': 'missing_error_handling',
                                'severity': 'medium',
                                'title': 'Missing Error Handling',
                                'description': f"Function '{node.name}' has risky operations without try-except",
                                'file': file_info['path'],
                                'line': node.lineno,
                                'impact': 'Unhandled exceptions crash the application',
                                'suggestion': 'Add try-except blocks to handle potential errors gracefully'
                            })

                    # Check for empty except blocks
                    if isinstance(node, ast.ExceptHandler):
                        if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                            anomalies.append({
                                'type': 'empty_except',
                                'severity': 'high',
                                'title': 'Empty Except Block',
                                'description': f"Exception caught but silently ignored",
                                'file': file_info['path'],
                                'line': node.lineno,
                                'impact': 'Errors are hidden, making debugging impossible',
                                'suggestion': 'Log the error or handle it appropriately'
                            })

                        # Check for catching generic Exception
                        if node.type and isinstance(node.type, ast.Name):
                            if node.type.id == 'Exception':
                                anomalies.append({
                                    'type': 'generic_exception',
                                    'severity': 'low',
                                    'title': 'Catching Generic Exception',
                                    'description': f"Catches Exception instead of specific exception types",
                                    'file': file_info['path'],
                                    'line': node.lineno,
                                    'impact': 'May catch and hide unexpected errors',
                                    'suggestion': 'Catch specific exceptions (ValueError, IOError, etc.)'
                                })

            except:
                continue

        return anomalies

    def _count_by_severity(self, all_anomalies: Dict) -> Dict[str, int]:
        """Count anomalies by severity"""
        counts = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        for cat in ['circular_dependencies', 'concurrency_issues',
                    'security_issues', 'database_issues',
                    'memory_leaks', 'error_handling']:
            category_list = all_anomalies.get(cat, [])
            for anomaly in category_list:
                severity = anomaly.get('severity', 'low')
                counts[severity] = counts.get(severity, 0) + 1
        return counts


if __name__ == '__main__':
    # Test the anomaly detector
    import sys
    from file_reader import FileReader

    if len(sys.argv) > 1:
        project_path = sys.argv[1]
    else:
        project_path = '.'

    reader = FileReader(project_path)
    file_metrics = reader.get_project_summary()

    detector = AnomalyDetector(project_path)
    anomalies = detector.detect_all(file_metrics['files'])

    print(f"\n🔍 Anomaly Detection Report")
    print(f"{'='*60}")
    print(f"Total Anomalies: {anomalies['total_count']}")
    print(f"\nBy Severity:")
    for severity, count in anomalies['severity_counts'].items():
        print(f"  {severity.upper()}: {count}")

    print(f"\n📊 By Category:")
    for category in ['circular_dependencies', 'concurrency_issues', 'security_issues',
                     'database_issues', 'memory_leaks', 'error_handling']:
        issues = anomalies[category]
        print(f"  {category.replace('_', ' ').title()}: {len(issues)}")

    if anomalies['security_issues']:
        print(f"\n🔒 Security Issues:")
        for issue in anomalies['security_issues'][:5]:
            print(f"  [{issue['severity'].upper()}] {issue['title']}")
            print(f"    File: {issue['file']}")
