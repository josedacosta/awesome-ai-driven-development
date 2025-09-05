# 🛠️ Scripts Directory

This directory contains utility scripts for maintaining the Awesome AI-Driven Development repository.

## 🔗 Link Checker (`check-links.py`)

A **simple, self-contained** Python script that extracts all links from README.md and verifies their functionality.

### ✨ Features
- ✅ **Self-contained** - Automatically installs dependencies if needed
- 🌐 **Comprehensive** - Tests all HTTP/HTTPS links in README.md
- 🎨 **Colorized output** - Easy-to-read colored terminal output
- 📊 **Detailed reports** - Generate markdown reports with statistics
- ⏱️ **Rate limiting** - Respectful delays between requests
- 🎯 **Smart filtering** - Ignores anchor links and relative paths

### 🚀 Quick Start

```bash
# Basic usage - check all links
./scripts/check-links.py

# Generate a detailed report
./scripts/check-links.py --report

# Quiet mode (for CI/CD)
./scripts/check-links.py --quiet
```

### 📋 Usage Options

```bash
./scripts/check-links.py [OPTIONS]

Options:
  --readme PATH      Path to README.md file (default: README.md)
  --timeout SECONDS  Request timeout (default: 10)
  --delay SECONDS    Delay between requests (default: 0.5)
  --report          Generate timestamped report in reports/
  --output FILE     Custom output file for report
  --quiet           Minimal output mode
  --help            Show detailed help
```

### 📊 Sample Output

#### ✅ Success Example:
```
🔗 Awesome AI-Driven Development - Link Checker
==================================================
🔍 Extracting links from README.md...
📋 Found 157 links to check
🔗 Checking links...
  [  1/157] https://github.com/features/copilot
    ✅ OK (200) - 0.45s
  [  2/157] https://aws.amazon.com/codewhisperer/
    ✅ OK (200) - 0.62s
  ...

==================================================
📊 SUMMARY: 155/157 links working (98.7%)
⚠️ 2 redirected links found
✅ All links are working perfectly!
```

#### ❌ Error Example:
```
🔗 Awesome AI-Driven Development - Link Checker
==================================================
...
  [ 85/157] https://broken-link.example.com
    ❌ ERROR - Connection failed
  ...

==================================================
📊 SUMMARY: 148/157 links working (94.3%)
❌ 7 broken links found
⚠️ 2 redirected links found
📄 Detailed report with broken links saved to: reports/link_check_20241204_143022.md
```

### 📄 Generated Reports

Reports include:
- **📊 Summary statistics** (total, working, errors, success rate)
- **❌ Broken links section** with line numbers and error details
- **⚠️ Redirected links** with original and final URLs
- **🕒 Timestamp** and metadata

### 🤖 Automatic Features

- **📦 Dependency Management**: Automatically installs `requests` if missing
- **📁 Directory Creation**: Creates `reports/` directory as needed
- **⏰ Timestamp Reports**: Auto-names reports with date/time
- **🚪 Exit Codes**: Returns 0 for success, 1 if broken links found

### 🔧 Requirements

- **Python 3.6+** (built-in modules + automatic `requests` installation)
- **No manual setup** - everything is handled automatically

### 🤖 CI/CD Integration

Perfect for automated workflows:

```yaml
# GitHub Actions example
- name: Check Links
  run: ./scripts/check-links.py --quiet
  
- name: Generate Report on Failure
  if: failure()
  run: ./scripts/check-links.py --report
```

**Exit codes:**
- `0` - All links working
- `1` - Broken links found

### 💡 Usage Tips

- **Rate limiting**: Use `--delay 1.0` for slower checking
- **Custom timeout**: Use `--timeout 15` for slow servers
- **Debugging**: Use `--report` to get detailed error information
- **CI/CD**: Use `--quiet` to reduce output noise

### 🔧 Advanced Examples

```bash
# Check with custom settings
./scripts/check-links.py --timeout 15 --delay 1.0

# Save report to specific file
./scripts/check-links.py --output my-report.md

# Check different markdown file
./scripts/check-links.py --readme docs/LINKS.md

# Quiet check for automation
./scripts/check-links.py --quiet && echo "All links OK"
```

## 🚀 Development

The script is designed to be:
- **📝 Self-documenting** - Clear code with docstrings
- **🔧 Easily modifiable** - Modular class structure
- **🧪 Testable** - Separate methods for each function
- **🛡️ Robust** - Comprehensive error handling

## 🔗 Integration

This script integrates with:
- **GitHub Actions** workflows
- **Pre-commit** hooks
- **CI/CD** pipelines
- **Manual** maintenance tasks

## 💭 Philosophy

**Simple is better than complex** - One script that does everything you need for link checking in an awesome list, with zero configuration required.