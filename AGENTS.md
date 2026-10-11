# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is an "Awesome" curated list repository focused on AI-driven development tools and resources. The repository maintains a comprehensive collection of AI tools, frameworks, libraries, and resources categorized by their use in software development workflow.

## Repository Structure

- `README.md` - Main awesome list with 13 categories and 100+ curated AI development resources
- `CONTRIBUTING.md` - Detailed contribution guidelines, format standards, and quality criteria
- `.gitignore` - Standard gitignore with specific exclusions for private files
- `CLAUDE_PROMPTS.md` - Private prompts file (excluded from git tracking)

## Content Management Standards

### Resource Entry Format
Each entry follows the strict format:
```markdown
- **[Tool Name](https://tool-url.com)** - Brief description of what the tool does
```

### Quality Criteria for Resources
Resources must be:
- **Relevant**: Directly related to AI-driven software development
- **Quality**: Well-maintained, documented, and useful to developers
- **Accessible**: Available for use (free, freemium, or paid)
- **Current**: Active and up-to-date (no abandoned projects)
- **Unique**: Not already listed or substantially different from existing entries

### Categories Structure
The list is organized into 13 main categories:
1. Code Generation & Assistance
2. Code Review & Analysis  
3. Testing & Quality Assurance
4. Documentation
5. DevOps & Deployment
6. Database & Data Management
7. Security
8. Project Management
9. Learning & Education
10. IDE Extensions & Plugins
11. APIs & SDKs
12. Research & Papers
13. Communities & Resources

Each category has subcategories that group similar tools together.

## Language Requirements

### Project Language Policy
**EVERYTHING in this project MUST be in English**, except for the following files (which may remain in French):
- `./CLAUDE.md`  
- `./CLAUDE_PROMPTS.md`

This includes:
- README.md (all content, descriptions, alerts) ✅ COMPLETED
- CONTRIBUTING.md
- All documentation files
- Issue templates and PR templates  
- GitHub Actions workflows
- Code comments and commit messages
- All resource descriptions and categories
- Scripts and their documentation
- All project files except the two mentioned above

**CRITICAL**: Any new content added to the project must be in English. This is to ensure international accessibility and maintain consistency across the repository.

## Content Guidelines

### When Adding Resources
- Maintain alphabetical order within each category/subcategory
- Descriptions should be under 100 characters when possible
- Focus on what the tool does, not just what it is
- Avoid marketing jargon
- Verify all links are functional
- Check for duplicates before adding

### Link Validation
All URLs must be functional and lead to the correct resource. Broken links should be updated or removed.

## Git Workflow & Branch Management

### Branch Strategy: GitHub Flow (ONLY)
This repository follows **GitHub Flow** exclusively:

- **Base Branch**: `main` (always deployable)
- **Feature Development**: Create short-lived branches from `main`
- **Pull Requests**: Required for ALL changes to main
- **Deployment**: Frequent deployments from `main`
- **Feature Flags**: Use for risky features

### Branch Naming Convention
Use clear, consistent naming patterns:
- `feat/<scope>-<short-description>` - New features
- `fix/<scope>-<short-description>` - Bug fixes  
- `docs/<short-description>` - Documentation changes
- `chore/<short-description>` - Maintenance tasks
- `refactor/<short-description>` - Code refactoring
- `test/<short-description>` - Test additions/fixes

**Rules**:
- Lowercase only, use hyphens `-`
- No spaces, accents, or special characters
- Keep under 50-72 characters
- Optionally prefix with issue ID: `1234-feat-oauth-device-flow`

### Branch Protection Rules
The `main` branch is protected with:
- **No direct pushes** - Pull Requests required
- **≥ 1 required review** before merging
- **Status checks required** - All CI/tests must pass
- **Linear history required** (optional)
- **Signed commits** (recommended)
- **CODEOWNERS** enforcement for automatic reviewers

### Protected Files
- `CLAUDE_PROMPTS.md` is in .gitignore and should never be committed
- `CLAUDE.md` is in .gitignore and should never be committed

### Git Configuration Requirements
**CRITICAL**: All Git activities MUST be performed with the following user configuration:
- **User**: josedacosta
- **Email**: contact@josedacosta.info

Ensure Git is properly configured before any commits:
```bash
git config user.name "josedacosta"
git config user.email "contact@josedacosta.info"
```

### Commit Message Standards: Conventional Commits
Follow the **Conventional Commits** specification:

**Format**: `<type>(<scope>): <description>`

**Types**:
- `feat` - New features
- `fix` - Bug fixes
- `docs` - Documentation changes
- `style` - Code style changes (formatting, no logic change)
- `refactor` - Code refactoring
- `test` - Test additions or modifications
- `chore` - Maintenance tasks
- `ci` - CI/CD changes
- `build` - Build system changes
- `perf` - Performance improvements

**Examples**:
- `feat(auth): add OAuth device flow support`
- `fix(links): update broken URLs in AI tools section`
- `docs: update contributing guidelines for new workflow`
- `chore: update dependencies to latest versions`

**Rules**:
- **ALL commit messages MUST be in English**
- Use imperative mood ("add" not "added")
- No period at the end of subject line
- Body optional, explain WHY not WHAT
- Footer for breaking changes: `BREAKING CHANGE: ...`
- Link issues: `Fixes #123`, `Closes #456`
- Never include Claude Code signatures or co-authored-by lines

### Pull Request Guidelines
- **Keep PRs small** (≤300 lines changed when possible)
- **Clear description** with context, solution, tests, and risks
- **Link related issues** using `Fixes #123` or `Closes #456`
- **Add screenshots/logs** when relevant
- **Respond quickly** to reviews
- **Use Squash & Merge** to maintain clean history

### Versioning & Releases
- **Semantic Versioning (SemVer)**: `vMAJOR.MINOR.PATCH`
- **Tag releases** and maintain human-readable CHANGELOG
- **Release notes** for significant updates
- **Breaking changes** clearly documented

## Maintenance Tasks

### Regular Maintenance
- Verify links are still functional
- Remove outdated or abandoned projects
- Update descriptions to reflect current tool capabilities
- Monitor for new tools in the AI development space
- Maintain alphabetical ordering when adding new entries

### Link Verification Requirement
**IMPORTANT**: After each addition or modification of resources in README.md, you MUST run the link verification script to ensure all URLs are functional:

```bash
# Quick check
./scripts/check-links.py

# With detailed report
./scripts/check-links.py --report

# Quiet mode (for automation)
./scripts/check-links.py --quiet
```

This script will:
- Extract all links from README.md automatically
- Test each URL for accessibility with proper rate limiting
- Generate colorized output showing results in real-time
- Create detailed markdown reports when requested
- Provide comprehensive success rate statistics
- Install dependencies automatically if needed

**Never commit changes without verifying link functionality first.**

The script is self-contained and requires no setup - just run it.

### Community Engagement
- Review and respond to issues promptly
- Evaluate pull requests against quality criteria
- Provide constructive feedback to contributors
- Recognize valuable contributions from the community

## Quality Assurance

When reviewing contributions or maintaining the list:
- Ensure tools are specifically AI-related for development workflows
- Verify tools are actively maintained (updated within the last year)
- Check that descriptions accurately reflect tool capabilities
- Maintain consistent formatting across all entries
- Preserve the educational value and usefulness of the curated list