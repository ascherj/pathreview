"""Parse GitHub Actions workflow files and detect CI/CD skills."""

import yaml

from .base import BaseParser, ParseResult


class WorkflowParser(BaseParser):
    """Parse a GitHub Actions workflow file and detect CI/CD skills.

    The parser reads the workflow YAML. It finds the marketplace actions and the
    shell commands in each job. It maps them to CI/CD skills. It returns the
    skills and the workflow metadata in a ParseResult.
    """

    # A marketplace action prefix maps to one CI/CD skill.
    ACTION_SKILLS = {
        "actions/checkout": "GitHub Actions",
        "actions/upload-artifact": "GitHub Actions",
        "actions/download-artifact": "GitHub Actions",
        "actions/cache": "GitHub Actions",
        "actions/setup-python": "Python CI",
        "actions/setup-node": "Node.js CI",
        "actions/setup-java": "Java CI",
        "actions/setup-go": "Go CI",
        "actions/setup-dotnet": ".NET CI",
        "docker/build-push-action": "Docker",
        "docker/login-action": "Docker",
        "docker/setup-buildx-action": "Docker",
        "aws-actions": "AWS",
        "azure/": "Azure",
        "google-github-actions": "GCP",
        "hashicorp/setup-terraform": "Terraform",
        "codecov/codecov-action": "Code Coverage",
    }

    # A shell command substring in a run step maps to one CI/CD skill.
    RUN_SKILLS = {
        "pytest": "Testing",
        "npm test": "Testing",
        "npm run test": "Testing",
        "yarn test": "Testing",
        "go test": "Testing",
        "make test": "Testing",
        "docker build": "Docker",
        "docker push": "Docker",
        "docker compose": "Docker",
        "docker-compose": "Docker",
        "kubectl": "Kubernetes",
        "helm ": "Kubernetes",
        "terraform ": "Terraform",
        "ansible": "Ansible",
        "flake8": "Linting",
        "ruff": "Linting",
        "black": "Linting",
        "eslint": "Linting",
        "mypy": "Type Checking",
    }

    def parse(self, content: str | bytes) -> ParseResult:
        """Parse workflow content and detect CI/CD skills.

        Args:
            content: The workflow YAML text, as str or bytes.

        Returns:
            A ParseResult. The metadata holds the detected skills, the triggers,
            the actions, and the job count.

        Raises:
            ValueError: If the content is not a valid workflow mapping.
        """
        if isinstance(content, bytes):
            content = content.decode("utf-8")

        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as exc:
            raise ValueError(f"Invalid workflow YAML: {exc}") from exc

        if not isinstance(data, dict):
            raise ValueError("Workflow content must be a YAML mapping.")

        jobs = data.get("jobs")
        if not isinstance(jobs, dict):
            raise ValueError("Workflow must define a 'jobs' mapping.")

        skills: set[str] = {"GitHub Actions"}  # A valid workflow always uses GitHub Actions.
        actions_used: list[str] = []

        for job in jobs.values():
            if not isinstance(job, dict):
                continue
            steps = job.get("steps")
            if not isinstance(steps, list):
                continue
            for step in steps:
                if not isinstance(step, dict):
                    continue
                self._scan_uses(step.get("uses"), skills, actions_used)
                self._scan_run(step.get("run"), skills)

        metadata = {
            "ci_cd_skills": sorted(skills),
            "triggers": self._extract_triggers(data),
            "actions_used": actions_used,
            "job_count": len(jobs),
        }

        return ParseResult(
            text=self._summary(metadata),
            metadata=metadata,
            source_type="github_actions_workflow",
        )

    def _scan_uses(self, uses: object, skills: set, actions_used: list) -> None:
        """Map a step 'uses' action to a skill."""
        if not isinstance(uses, str):
            return
        action = uses.split("@", 1)[0].strip()
        actions_used.append(action)
        for prefix, skill in self.ACTION_SKILLS.items():
            if action.startswith(prefix):
                skills.add(skill)

    def _scan_run(self, run: object, skills: set) -> None:
        """Map a step 'run' command to a skill."""
        if not isinstance(run, str):
            return
        run_lower = run.lower()
        for needle, skill in self.RUN_SKILLS.items():
            if needle in run_lower:
                skills.add(skill)

    @staticmethod
    def _extract_triggers(data: dict) -> list[str]:
        """Return the workflow trigger events.

        YAML reads a bare 'on' key as the boolean True. The parser checks both
        the string key and the boolean key.
        """
        raw = data.get("on", data.get(True))
        if isinstance(raw, str):
            return [raw]
        if isinstance(raw, list):
            return [str(item) for item in raw]
        if isinstance(raw, dict):
            return [str(key) for key in raw]
        return []

    @staticmethod
    def _summary(metadata: dict) -> str:
        """Build a short text summary of the workflow."""
        skills = ", ".join(metadata["ci_cd_skills"]) or "none"
        triggers = ", ".join(metadata["triggers"]) or "none"
        return (
            f"GitHub Actions workflow with {metadata['job_count']} job(s). "
            f"Triggers: {triggers}. CI/CD skills: {skills}."
        )
