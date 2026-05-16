"""
Git Analyzer - Analyzes git history and activity
"""

import subprocess
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime, timedelta


class GitAnalyzer:
    """Analyzes git repository history and activity"""

    def __init__(self, repo_path: str):
        """
        Initialize Git Analyzer

        Args:
            repo_path: Path to the git repository
        """
        self.repo_path = Path(repo_path).resolve()

        if not self.is_git_repository():
            raise ValueError(f"Not a git repository: {repo_path}")

    def is_git_repository(self) -> bool:
        """Check if the path is a git repository"""
        git_dir = self.repo_path / '.git'
        return git_dir.exists() and git_dir.is_dir()

    def run_git_command(self, command: List[str]) -> Optional[str]:
        """
        Run a git command and return output

        Args:
            command: Git command as list of strings

        Returns:
            Command output or None if error
        """
        try:
            result = subprocess.run(
                ['git'] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return result.stdout.strip()
            else:
                print(f"Git command failed: {' '.join(command)}")
                print(f"Error: {result.stderr}")
                return None

        except subprocess.TimeoutExpired:
            print(f"Git command timed out: {' '.join(command)}")
            return None
        except Exception as e:
            print(f"Error running git command: {e}")
            return None

    def get_commit_count(self, days: int = 7) -> int:
        """
        Get number of commits in the last N days

        Args:
            days: Number of days to look back

        Returns:
            Number of commits
        """
        since_date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        output = self.run_git_command(['rev-list', '--count', f'--since={since_date}', 'HEAD'])

        if output:
            try:
                return int(output)
            except ValueError:
                return 0
        return 0

    def get_contributors(self) -> List[Dict]:
        """
        Get list of contributors with commit counts

        Returns:
            List of dictionaries with contributor info
        """
        output = self.run_git_command(['shortlog', '-sn', '--all', '--no-merges'])

        if not output:
            return []

        contributors = []
        for line in output.split('\n'):
            if line.strip():
                parts = line.strip().split('\t')
                if len(parts) == 2:
                    contributors.append({
                        'commits': int(parts[0]),
                        'name': parts[1]
                    })

        return contributors

    def get_total_commits(self) -> int:
        """Get total number of commits"""
        output = self.run_git_command(['rev-list', '--count', 'HEAD'])

        if output:
            try:
                return int(output)
            except ValueError:
                return 0
        return 0

    def get_branch_name(self) -> Optional[str]:
        """Get current branch name"""
        return self.run_git_command(['branch', '--show-current'])

    def get_file_change_frequency(self, limit: int = 10) -> List[Dict]:
        """
        Get files that change most frequently

        Args:
            limit: Number of files to return

        Returns:
            List of files with change counts
        """
        output = self.run_git_command(['log', '--format=format:', '--name-only', '--'])

        if not output:
            return []

        # Count file occurrences
        file_counts = {}
        for line in output.split('\n'):
            if line.strip():
                file_counts[line] = file_counts.get(line, 0) + 1

        # Sort and limit
        sorted_files = sorted(file_counts.items(), key=lambda x: x[1], reverse=True)[:limit]

        return [
            {'file': file, 'changes': count}
            for file, count in sorted_files
        ]

    def get_recent_commits(self, count: int = 5) -> List[Dict]:
        """
        Get recent commits

        Args:
            count: Number of commits to retrieve

        Returns:
            List of commit dictionaries
        """
        output = self.run_git_command([
            'log',
            f'-{count}',
            '--pretty=format:%H|%an|%ae|%at|%s'
        ])

        if not output:
            return []

        commits = []
        for line in output.split('\n'):
            if line.strip():
                parts = line.split('|')
                if len(parts) == 5:
                    commits.append({
                        'hash': parts[0][:8],
                        'author': parts[1],
                        'email': parts[2],
                        'timestamp': int(parts[3]),
                        'message': parts[4]
                    })

        return commits

    def get_first_commit_date(self) -> Optional[datetime]:
        """Get date of first commit"""
        output = self.run_git_command([
            'log',
            '--reverse',
            '--format=%at',
            '--max-count=1'
        ])

        if output:
            try:
                timestamp = int(output)
                return datetime.fromtimestamp(timestamp)
            except ValueError:
                return None
        return None

    def get_last_commit_date(self) -> Optional[datetime]:
        """Get date of last commit"""
        output = self.run_git_command([
            'log',
            '--format=%at',
            '--max-count=1'
        ])

        if output:
            try:
                timestamp = int(output)
                return datetime.fromtimestamp(timestamp)
            except ValueError:
                return None
        return None

    def calculate_activity_score(self) -> float:
        """
        Calculate activity score based on recent commits

        Returns:
            Score from 0-100
        """
        # Check commits in last 7 days
        recent_commits = self.get_commit_count(7)

        # 1+ commits per day = 100
        score = min((recent_commits / 7.0) * 100, 100)

        return round(score, 1)

    def get_repository_age_days(self) -> Optional[int]:
        """Get repository age in days"""
        first_commit = self.get_first_commit_date()

        if first_commit:
            age = datetime.now() - first_commit
            return age.days

        return None

    def get_analysis(self) -> Dict:
        """
        Get complete git analysis

        Returns:
            Dictionary with all git metrics
        """
        total_commits = self.get_total_commits()
        recent_commits = self.get_commit_count(7)
        contributors = self.get_contributors()
        branch = self.get_branch_name()
        hot_files = self.get_file_change_frequency(10)
        recent = self.get_recent_commits(5)
        age_days = self.get_repository_age_days()
        activity_score = self.calculate_activity_score()

        first_commit = self.get_first_commit_date()
        last_commit = self.get_last_commit_date()

        return {
            'repository_path': str(self.repo_path),
            'current_branch': branch,
            'total_commits': total_commits,
            'commits_last_7_days': recent_commits,
            'contributors': contributors,
            'contributor_count': len(contributors),
            'age_days': age_days,
            'first_commit': first_commit.isoformat() if first_commit else None,
            'last_commit': last_commit.isoformat() if last_commit else None,
            'activity_score': activity_score,
            'hot_files': hot_files,
            'recent_commits': recent
        }


if __name__ == '__main__':
    # Test the git analyzer
    import sys

    if len(sys.argv) > 1:
        repo_path = sys.argv[1]
    else:
        repo_path = '.'

    try:
        analyzer = GitAnalyzer(repo_path)
        analysis = analyzer.get_analysis()

        print(f"\n📊 Git Analysis: {analysis['repository_path']}")
        print(f"{'='*60}")
        print(f"Branch: {analysis['current_branch']}")
        print(f"Total Commits: {analysis['total_commits']:,}")
        print(f"Commits (Last 7 days): {analysis['commits_last_7_days']}")
        print(f"Activity Score: {analysis['activity_score']}/100")
        print(f"Repository Age: {analysis['age_days']} days")

        print(f"\n👥 Contributors ({analysis['contributor_count']}):")
        for contrib in analysis['contributors'][:5]:
            print(f"  - {contrib['name']}: {contrib['commits']} commits")

        if analysis['hot_files']:
            print(f"\n🔥 Hot Files (Most Changed):")
            for hot in analysis['hot_files'][:5]:
                print(f"  - {hot['file']}: {hot['changes']} changes")

        if analysis['recent_commits']:
            print(f"\n📝 Recent Commits:")
            for commit in analysis['recent_commits']:
                print(f"  - {commit['hash']}: {commit['message'][:50]}")

    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
