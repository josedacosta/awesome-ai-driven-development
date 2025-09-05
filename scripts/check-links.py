#!/usr/bin/env python3
"""
🔗 Link Checker for Awesome AI-Driven Development
Simple, self-contained script to verify all links in README.md

Usage:
    ./scripts/check-links.py                    # Basic check
    ./scripts/check-links.py --quiet            # Minimal output
    ./scripts/check-links.py --report           # Generate report
    ./scripts/check-links.py --help             # Show help
"""

import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple

import requests


# ANSI color codes
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    CYAN = '\033[0;36m'
    WHITE = '\033[1;37m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_colored(text, color=Colors.RESET):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.RESET}")


def check_dependencies():
    """Check and install required dependencies"""
    try:
        import requests
        return True
    except ImportError:
        print_colored("📦 Installing required dependency: requests", Colors.YELLOW)
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'requests'])
            print_colored("✅ Successfully installed requests", Colors.GREEN)
            return True
        except subprocess.CalledProcessError:
            print_colored("❌ Failed to install requests. Please install manually:", Colors.RED)
            print("   pip3 install requests")
            return False


class LinkChecker:
    def __init__(self, readme_path: str = "README.md", timeout: int = 10, delay: float = 0.5):
        self.readme_path = Path(readme_path)
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; Awesome-AI-Link-Checker/1.0; +https://github.com/josedacosta/awesome-ai-driven-development)'
        })

    def extract_links(self) -> List[Tuple[str, str, int]]:
        """Extract all markdown links from README.md"""
        if not self.readme_path.exists():
            print_colored(f"❌ Error: {self.readme_path} not found", Colors.RED)
            return []

        with open(self.readme_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Regex pattern to match markdown links: [text](url)
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        links = []

        for line_num, line in enumerate(content.split('\n'), 1):
            matches = re.findall(link_pattern, line)
            for text, url in matches:
                # Filter out anchor links and relative links
                if not url.startswith('#') and not url.startswith('./') and not url.startswith('../'):
                    # Handle incomplete URLs
                    if url.startswith('//'):
                        url = 'https:' + url
                    elif not url.startswith(('http://', 'https://')):
                        continue  # Skip non-HTTP links
                    links.append((text, url, line_num))

        return links

    def check_link(self, url: str) -> Dict[str, any]:
        """Check if a single link is functional"""
        result = {
            'url': url,
            'status': 'unknown',
            'status_code': None,
            'response_time': None,
            'error': None,
            'redirect_url': None
        }

        # Skip certain domains that consistently block automated requests
        blocked_domains = ['openai.com', 'anthropic.com']
        from urllib.parse import urlparse
        parsed_url = urlparse(url)
        if any(domain in parsed_url.netloc for domain in blocked_domains):
            result['status'] = 'blocked'
            result['error'] = 'Domain blocks automated requests - likely working for humans'
            return result

        try:
            start_time = time.time()
            response = self.session.get(url, timeout=self.timeout, allow_redirects=True)
            response_time = round(time.time() - start_time, 2)

            result['status_code'] = response.status_code
            result['response_time'] = response_time

            if response.status_code == 200:
                result['status'] = 'ok'
            elif 300 <= response.status_code < 400:
                result['status'] = 'redirect'
                result['redirect_url'] = response.url
            elif response.status_code == 403 and 'openai.com' in url:
                result['status'] = 'blocked'
                result['error'] = 'OpenAI blocks automated requests - likely working for humans'
            elif 400 <= response.status_code < 500:
                result['status'] = 'client_error'
            elif 500 <= response.status_code < 600:
                result['status'] = 'server_error'
            else:
                result['status'] = 'unknown_status'

        except requests.exceptions.Timeout:
            result['status'] = 'timeout'
            result['error'] = f'Timeout after {self.timeout}s'
        except requests.exceptions.ConnectionError:
            result['status'] = 'connection_error'
            result['error'] = 'Connection failed'
        except requests.exceptions.RequestException as e:
            result['status'] = 'error'
            result['error'] = str(e)
        except Exception as e:
            result['status'] = 'error'
            result['error'] = f'Unexpected error: {str(e)}'

        return result

    def check_all_links(self, verbose: bool = True) -> Dict[str, any]:
        """Check all links and return results"""
        print_colored("🔍 Extracting links from README.md...", Colors.CYAN)
        links = self.extract_links()

        if not links:
            print_colored("❌ No links found in README.md", Colors.RED)
            return {'total': 0, 'results': [], 'summary': {}}

        print_colored(f"📋 Found {len(links)} links to check", Colors.BLUE)

        if verbose:
            print_colored("🔗 Checking links...", Colors.CYAN)

        results = []
        summary = {
            'total': len(links),
            'ok': 0,
            'errors': 0,
            'warnings': 0,
            'checked_at': datetime.now().isoformat()
        }

        for i, (text, url, line_num) in enumerate(links, 1):
            if verbose:
                # Truncate long URLs for display
                display_url = url if len(url) <= 60 else url[:57] + "..."
                print(f"  [{i:3d}/{len(links)}] {display_url}")

            result = self.check_link(url)
            result.update({
                'text': text,
                'line_number': line_num
            })
            results.append(result)

            # Update summary and show status
            if result['status'] == 'ok':
                summary['ok'] += 1
                if verbose:
                    print_colored(f"    ✅ OK ({result['status_code']}) - {result['response_time']}s", Colors.GREEN)
            elif result['status'] == 'redirect':
                summary['warnings'] += 1
                if verbose:
                    print_colored(f"    ⚠️  REDIRECT ({result['status_code']}) - {result['response_time']}s",
                                  Colors.YELLOW)
            elif result['status'] == 'blocked':
                summary['warnings'] += 1
                if verbose:
                    print_colored(f"    ⚠️  BLOCKED - {result['error']}", Colors.YELLOW)
            else:
                summary['errors'] += 1
                if verbose:
                    error_msg = result.get('error', f"Status: {result['status']}")
                    print_colored(f"    ❌ ERROR - {error_msg}", Colors.RED)

            # Rate limiting
            time.sleep(self.delay)

        return {
            'total': len(links),
            'results': results,
            'summary': summary
        }

    def generate_report(self, results: Dict[str, any]) -> str:
        """Generate a detailed text report"""
        report = []
        report.append("# 🔗 Link Check Report")
        report.append(f"Generated on: {results['summary']['checked_at']}")
        report.append("")

        # Summary
        summary = results['summary']
        report.append("## 📊 Summary")
        report.append(f"- **Total Links**: {summary['total']}")
        report.append(f"- **✅ Working**: {summary['ok']}")
        report.append(f"- **⚠️ Warnings**: {summary['warnings']}")
        report.append(f"- **❌ Errors**: {summary['errors']}")

        success_rate = round((summary['ok'] / summary['total']) * 100, 1) if summary['total'] > 0 else 0
        report.append(f"- **📈 Success Rate**: {success_rate}%")
        report.append("")

        # Detailed results
        errors = [r for r in results['results'] if r['status'] not in ['ok', 'redirect']]
        warnings = [r for r in results['results'] if r['status'] == 'redirect']

        if errors:
            report.append("## ❌ Broken Links")
            for result in errors:
                report.append(f"- **Line {result['line_number']}**: [{result['text']}]({result['url']})")
                report.append(f"  - Status: {result['status']}")
                if result['error']:
                    report.append(f"  - Error: {result['error']}")
                report.append("")

        if warnings:
            report.append("## ⚠️ Redirected Links")
            for result in warnings:
                report.append(f"- **Line {result['line_number']}**: [{result['text']}]({result['url']})")
                report.append(f"  - Redirects to: {result['redirect_url']}")
                report.append("")

        return '\n'.join(report)

    def save_report(self, results: Dict[str, any], output_file: str):
        """Save report to file"""
        report = self.generate_report(results)

        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print_colored(f"📄 Report saved to: {output_path}", Colors.BLUE)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='🔗 Check all links in README.md',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ./scripts/check-links.py                     # Basic check
  ./scripts/check-links.py --quiet             # Minimal output
  ./scripts/check-links.py --report            # Generate timestamped report
  ./scripts/check-links.py --timeout 15        # Custom timeout
        """
    )

    parser.add_argument('--readme', default='README.md',
                        help='Path to README.md file (default: README.md)')
    parser.add_argument('--timeout', type=int, default=10,
                        help='Request timeout in seconds (default: 10)')
    parser.add_argument('--delay', type=float, default=0.5,
                        help='Delay between requests in seconds (default: 0.5)')
    parser.add_argument('--report', action='store_true',
                        help='Generate a detailed report in reports/ directory')
    parser.add_argument('--output',
                        help='Custom output file for report')
    parser.add_argument('--quiet', action='store_true',
                        help='Quiet mode with minimal output')

    args = parser.parse_args()

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Re-import requests after potential installation

    # Print header
    if not args.quiet:
        print_colored("🔗 Awesome AI-Driven Development - Link Checker", Colors.BOLD + Colors.CYAN)
        print_colored("=" * 50, Colors.CYAN)

    # Initialize checker
    checker = LinkChecker(args.readme, args.timeout, args.delay)

    # Check if README exists
    if not Path(args.readme).exists():
        print_colored(f"❌ Error: {args.readme} not found", Colors.RED)
        sys.exit(1)

    # Run checks
    results = checker.check_all_links(verbose=not args.quiet)

    # Print summary
    if not args.quiet:
        print_colored("\n" + "=" * 50, Colors.CYAN)
        summary = results['summary']
        success_rate = round((summary['ok'] / summary['total']) * 100, 1) if summary['total'] > 0 else 0

        print_colored(f"📊 SUMMARY: {summary['ok']}/{summary['total']} links working ({success_rate}%)", Colors.BOLD)

        if summary['errors'] > 0:
            print_colored(f"❌ {summary['errors']} broken links found", Colors.RED)
        if summary['warnings'] > 0:
            print_colored(f"⚠️  {summary['warnings']} redirected links found", Colors.YELLOW)

        if summary['errors'] == 0 and summary['warnings'] == 0:
            print_colored("✅ All links are working perfectly!", Colors.GREEN)

    # Generate report if requested
    if args.report or args.output:
        if args.output:
            output_file = args.output
        else:
            # Auto-generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"reports/link_check_{timestamp}.md"

        checker.save_report(results, output_file)

        if not args.quiet:
            if results['summary']['errors'] > 0:
                print_colored(f"📄 Detailed report with broken links saved to: {output_file}", Colors.YELLOW)
            else:
                print_colored(f"📄 Report saved to: {output_file}", Colors.BLUE)

    # Exit with appropriate code
    if results['summary']['errors'] > 0:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
