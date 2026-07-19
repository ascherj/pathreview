"""Tests for readme_scorer.py"""

import pytest

from agent.tools.readme_scorer import ReadmeScorer


@pytest.mark.unit
class TestReadmeScorer:
    """Test suite for ReadmeScorer."""

    @pytest.fixture
    def scorer(self):
        """Create a ReadmeScorer instance."""
        return ReadmeScorer()

    def test_readme_with_all_quality_signals(self, scorer):
        """Test README with all quality signals returns high score."""
        readme = """
# Project Name

PathReview is a comprehensive example application that analyzes software
projects and provides useful feedback to developers. It demonstrates how a
production-style service can organize documentation, testing, configuration,
deployment, and contribution workflows. The project is intended to serve as a
realistic reference implementation for contributors learning how large Python
applications are structured. Every component has been designed to encourage
clean architecture, maintainability, and collaboration while demonstrating
practical engineering techniques that can be reused in production systems.

## Project Overview

The application evaluates software projects and produces structured feedback
covering documentation quality, repository organization, testing practices,
configuration, and overall maintainability. Contributors can inspect scoring
results, understand why particular recommendations were generated, and improve
their projects through an iterative workflow. The design emphasizes
transparency, reproducibility, and developer experience while remaining easy to
extend with additional scoring tools and analysis modules in the future.

## Installation

Clone the repository and install the required dependencies before running the
application locally. Developers should also configure the required environment
variables and confirm that the database service is available.

```bash
git clone https://github.com/example/pathreview.git
cd pathreview
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Getting Started

After installation, initialize the database, configure environment variables,
and verify that required services are running. Starting with a clean
development environment reduces unexpected issues and helps contributors follow
the same workflow described throughout the documentation. The project includes
example configuration files that simplify local setup and provide sensible
defaults for development.

## Configuration

The application uses environment variables to configure database connections,
API credentials, logging preferences, and development settings. Contributors
should copy the example environment file, provide appropriate local values, and
avoid committing private credentials. Configuration validation happens during
startup so that missing values produce clear error messages instead of causing
unexpected failures later. Separate configurations can be used for local
development, automated testing, staging, and production deployments.

## Usage

Import the package and start the application using the provided command.
Additional examples explain how to submit data, review results, troubleshoot
common errors, and verify that each service is communicating correctly.

```python
import package

package.run()
```

Developers can interact with the application through the command line or HTTP
API depending on their workflow. Responses include structured metadata that
helps users understand how scores were generated and what recommendations are
most relevant for improving project quality.

## Features

- Automated project analysis
- Clear scoring and feedback
- Reliable tests and validation
- Contributor-friendly documentation
- Local development support
- Structured logging
- Extensible scoring framework
- REST API
- Database-backed persistence
- Modern Python architecture

## Architecture

The application separates its API, database, scoring tools, and user interface
into maintainable components. This structure helps contributors understand the
codebase, test changes independently, and extend features without affecting
unrelated functionality. Services communicate through clearly defined
interfaces, making individual modules easier to replace or improve without
introducing unnecessary coupling. The architecture also encourages thorough
testing by isolating business logic from framework-specific implementation
details.

## API Overview

The API provides endpoints for submitting projects, requesting analysis,
viewing scoring results, and checking service health. Each endpoint validates
incoming data and returns structured responses that are easy for clients to
process. Errors include useful status codes and messages so developers can
identify invalid requests quickly. The API documentation also includes example
payloads, expected responses, and descriptions of the most important fields.

## Testing

The project includes unit tests, integration tests, and validation tests for
the main scoring components. Unit tests check individual functions and classes
in isolation, while integration tests confirm that services communicate
correctly. Contributors should run the complete test suite before opening a
pull request. New behavior should include tests that demonstrate the expected
result and cover important edge cases. Test fixtures should accurately
represent the conditions described by their assertions.

```bash
pytest
```

## Development Workflow

Contributors should create a separate branch for each issue and keep changes
focused on the requested behavior. Before making changes, developers should
read the related tests and implementation files to understand the existing
design. After implementing a fix, they should run the targeted test first and
then run the complete relevant test file. Commit messages should clearly
explain the purpose of the change, and pull requests should include testing
evidence and a reference to the related issue.

## Deployment

The application can be deployed using a standard container-based workflow.
Production deployments should use secure environment variables, managed
database credentials, health checks, and structured logging. The deployment
process should run automated tests before publishing a new version. Rollback
procedures should also be documented so that a previous stable release can be
restored if a deployment introduces an unexpected problem.

## Troubleshooting

If the application does not start, confirm that dependencies are installed and
that required services are running. Database errors often indicate an
incorrect connection string or an unavailable PostgreSQL service. Import
errors usually mean that the virtual environment is not active or that
packages were installed using a different Python interpreter. Test failures
should be investigated by reading the first failure carefully and running the
affected test in isolation.

## Contributing

Contributions should follow the existing project structure and coding style.
Before submitting a pull request, contributors should review their Git diff,
remove unrelated changes, and confirm that all relevant tests pass. Pull
request descriptions should explain what changed, why the change was
necessary, and how the result was verified. Review feedback should be
addressed through focused commits whenever possible.

## Security

Sensitive information must never be stored directly in source code or
committed to the repository. API keys, passwords, and database credentials
should be provided through environment variables or an approved
secrets-management service. Dependencies should be reviewed regularly, and
security updates should be applied promptly. Error responses should provide
useful information without exposing private configuration values or internal
implementation details.

## Tech Stack

- Python 3.9
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pytest
- Docker

![Build Status](https://example.com/badge.svg)
![Coverage](https://example.com/coverage.svg)

## Live Demo

[Try it here](https://demo.example.com)

## Frequently Asked Questions

Developers commonly ask how to run the project locally, where configuration
values belong, and which tests should be executed before submitting changes.
The recommended approach is to activate the project virtual environment,
install the declared dependencies, configure PostgreSQL, and run the targeted
test followed by the complete relevant test suite. Additional questions can be
raised through the project's issue tracker.

## License

This project is provided as an educational example for demonstrating software
engineering practices, testing strategies, documentation quality, and open
source collaboration workflows. Contributors are encouraged to improve the
documentation, add tests, and submit well-scoped pull requests following the
project guidelines.
"""

        result = scorer.execute({"readme_content": readme})

        assert result.success is True
        data = result.data
        assert data["has_readme"] is True
        assert data["word_count"] > 100
        assert data["word_count_category"] == "comprehensive"
        assert data["has_installation_section"] is True
        assert data["has_usage_section"] is True
        assert data["has_badges"] is True
        assert data["has_demo_link"] is True
        assert data["has_tech_stack_section"] is True
        assert data["overall_score"] > 0.7  # Should be high

    def test_readme_with_no_content(self, scorer):
        """Test README with no content returns score of 0.0."""
        result = scorer.execute({"readme_content": ""})

        assert result.success is True
        data = result.data
        assert data["has_readme"] is False
        assert data["word_count"] == 0
        assert data["word_count_category"] == "minimal"
        assert data["overall_score"] == 0.0

    def test_readme_with_only_title(self, scorer):
        """Test README with only a title returns minimal word count category."""
        readme = "# Project Title"

        result = scorer.execute({"readme_content": readme})

        assert result.success is True
        data = result.data
        assert data["has_readme"] is True
        assert data["word_count"] < 100
        assert data["word_count_category"] == "minimal"
        assert data["overall_score"] < 0.3

    def test_word_count_category_minimal(self, scorer):
        """Test word_count_category: < 100 = minimal."""
        readme = "This is a very short readme with just a few words."

        result = scorer.execute({"readme_content": readme})

        data = result.data
        assert data["word_count"] < 100
        assert data["word_count_category"] == "minimal"

    def test_word_count_category_adequate(self, scorer):
        """Test word_count_category: 100-500 = adequate."""
        readme = " ".join(["word"] * 200)  # 200 words

        result = scorer.execute({"readme_content": readme})

        data = result.data
        assert 100 <= data["word_count"] <= 500
        assert data["word_count_category"] == "adequate"

    def test_word_count_category_comprehensive(self, scorer):
        """Test word_count_category: > 500 = comprehensive."""
        readme = " ".join(["word"] * 700)  # 700 words

        result = scorer.execute({"readme_content": readme})

        data = result.data
        assert data["word_count"] > 500
        assert data["word_count_category"] == "comprehensive"

    def test_installation_section_detection(self, scorer):
        """Test detection of installation section."""
        readme_with_install = """
        # Project
        ## Installation
        pip install package
        """

        result = scorer.execute({"readme_content": readme_with_install})
        assert result.data["has_installation_section"] is True

        readme_without_install = """
        # Project
        ## Description
        This is a project.
        """

        result = scorer.execute({"readme_content": readme_without_install})
        assert result.data["has_installation_section"] is False

    def test_usage_section_detection(self, scorer):
        """Test detection of usage section."""
        readme_with_usage = """
        # Project
        ## Usage
        Run the project like this...
        """

        result = scorer.execute({"readme_content": readme_with_usage})
        assert result.data["has_usage_section"] is True

    def test_setup_keyword_counts_as_installation(self, scorer):
        """Test that 'setup' keyword counts as installation."""
        readme = """
        # Project
        ## Getting Started
        Run setup.sh
        """

        result = scorer.execute({"readme_content": readme})
        # "Getting Started" matches the pattern
        assert (
            result.data["has_installation_section"] is True
            or result.data["has_usage_section"] is True
        )

    def test_quickstart_counts_as_usage(self, scorer):
        """Test that 'quickstart' counts as usage."""
        readme = """
        # Project
        ## Quickstart
        Quick example here
        """

        result = scorer.execute({"readme_content": readme})
        assert result.data["has_usage_section"] is True

    def test_badge_detection(self, scorer):
        """Test badge detection."""
        readme_with_badges = """
        ![Status](https://example.com/status.svg)
        ![License](https://example.com/license.svg)
        """

        result = scorer.execute({"readme_content": readme_with_badges})
        assert result.data["has_badges"] is True

    def test_demo_link_detection(self, scorer):
        """Test demo/live link detection."""
        readme_with_demo = """
        # Project
        [Live Demo](https://demo.example.com)
        """

        result = scorer.execute({"readme_content": readme_with_demo})
        assert result.data["has_demo_link"] is True

    def test_tech_stack_section_detection(self, scorer):
        """Test tech stack section detection."""
        readme_with_stack = """
        # Project
        ## Tech Stack
        - Python
        - FastAPI
        - PostgreSQL
        """

        result = scorer.execute({"readme_content": readme_with_stack})
        assert result.data["has_tech_stack_section"] is True

    def test_technologies_keyword_counts(self, scorer):
        """Test that 'Technologies' keyword counts as tech stack."""
        readme = """
        # Project
        ## Technologies
        Python, JavaScript, React
        """

        result = scorer.execute({"readme_content": readme})
        assert result.data["has_tech_stack_section"] is True

    def test_overall_score_calculation(self, scorer):
        """Test that overall score aggregates components."""
        readme = (
            """
        # Good README

        ## Installation
        Install it!

        ## Usage
        Use it!

        ## Tech Stack
        Python, JavaScript

        ![Build](https://example.com/build.svg)

        This readme has lots of content here.
        """
            * 3
        )  # Make it comprehensive

        result = scorer.execute({"readme_content": readme})

        data = result.data
        assert 0.0 <= data["overall_score"] <= 1.0
        # Multiple signals should yield higher score
        assert data["overall_score"] > 0.5

    def test_missing_readme_content_key(self, scorer):
        """Test handling of missing readme_content key."""
        result = scorer.execute({})

        assert result.success is True
        data = result.data
        assert data["has_readme"] is False

    def test_result_has_all_required_fields(self, scorer):
        """Test that result has all required fields."""
        result = scorer.execute({"readme_content": "# Test"})

        data = result.data
        assert "has_readme" in data
        assert "word_count" in data
        assert "word_count_category" in data
        assert "has_installation_section" in data
        assert "has_usage_section" in data
        assert "has_badges" in data
        assert "has_demo_link" in data
        assert "has_tech_stack_section" in data
        assert "overall_score" in data

    def test_case_insensitive_section_detection(self, scorer):
        """Test that section detection is case insensitive."""
        readme = """
        # Project
        ## INSTALLATION
        Install here
        """

        result = scorer.execute({"readme_content": readme})
        assert result.data["has_installation_section"] is True

    def test_whitespace_only_readme(self, scorer):
        """Test handling of whitespace-only README."""
        result = scorer.execute({"readme_content": "   \n\n   \t  "})

        data = result.data
        assert data["has_readme"] is False
        assert data["word_count"] == 0

    def test_example_keyword_counts_as_usage(self, scorer):
        """Test that 'Example' counts as usage section."""
        readme = """
        # Project
        ## Example
        Here's how to use it
        """

        result = scorer.execute({"readme_content": readme})
        assert result.data["has_usage_section"] is True

    def test_score_scales_with_word_count(self, scorer):
        """Test that longer READMEs get bonus in score."""
        short_readme = "# Title\nSmall content."
        long_readme = "# Title\n" + "Content paragraph. " * 100

        result_short = scorer.execute({"readme_content": short_readme})
        result_long = scorer.execute({"readme_content": long_readme})

        assert result_long.data["overall_score"] > result_short.data["overall_score"]

    def test_try_it_as_demo_indicator(self, scorer):
        """Test that 'try it' indicates demo link."""
        readme = "Check it out [try it here](https://example.com)"

        result = scorer.execute({"readme_content": readme})
        assert result.data["has_demo_link"] is True

    def test_built_with_counts_as_tech_stack(self, scorer):
        """Test that 'Built With' counts as tech stack."""
        readme = """
        # Project
        ## Built With
        - Python
        - FastAPI
        """

        result = scorer.execute({"readme_content": readme})
        assert result.data["has_tech_stack_section"] is True
