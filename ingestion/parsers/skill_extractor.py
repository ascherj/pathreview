import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class SkillDetection:
    """Result of detecting a skill."""
    name: str
    category: str
    confidence: float
    evidence: list[str]


class SkillExtractor:
    """Extract skills from source code and documentation."""

    PYTHON_KEYWORDS = {
        "import",
        "from",
        "def",
        "class",
        "async",
        "await",
        "yield",
        "lambda",
        "with",
    }

    JS_TS_KEYWORDS = {
        "import",
        "export",
        "require",
        "const",
        "let",
        "var",
        "function",
        "async",
        "await",
        "class",
    }

    REACT_INDICATORS = {
        "import React",
        "useState",
        "useEffect",
        "useContext",
        "useReducer",
        "useCallback",
        "useMemo",
        "useRef",
        "createContext",
        "ReactDOM.render",
        ".jsx",
        ".tsx",
    }

    FRAMEWORKS = {
        "django": ("Python", 0.95),
        "flask": ("Python", 0.95),
        "fastapi": ("Python", 0.95),
        "sqlalchemy": ("Python", 0.85),
        "numpy": ("Python", 0.85),
        "pandas": ("Python", 0.85),
        "scikit-learn": ("Python", 0.85),
        "tensorflow": ("Python", 0.85),
        "pytorch": ("Python", 0.85),
        "express": ("JavaScript", 0.95),
        "next.js": ("JavaScript", 0.95),
        "react": ("JavaScript", 0.95),
        "vue": ("JavaScript", 0.95),
        "angular": ("JavaScript", 0.95),
        "svelte": ("JavaScript", 0.85),
        "webpack": ("JavaScript", 0.85),
        "vite": ("JavaScript", 0.85),
        "rollup": ("JavaScript", 0.85),
        "jest": ("JavaScript", 0.80),
        "mocha": ("JavaScript", 0.80),
    }

    DATABASES = {
        "PostgreSQL": (0.95, ["postgresql", "postgres", "psycopg2", "psycopg"]),
        "MySQL": (0.95, ["mysql", "mysql2"]),
        "MongoDB": (0.95, ["mongodb", "mongo"]),
        "Redis": (0.90, ["redis"]),
        "Elasticsearch": (0.90, ["elasticsearch", "es"]),
        "DynamoDB": (0.90, ["dynamodb"]),
        "Firebase": (0.85, ["firebase"]),
        "Cassandra": (0.85, ["cassandra"]),
        "Oracle": (0.85, ["oracle"]),
    }

    TOOLS = {
        "Docker": (0.95, ["docker", "dockerfile", "docker-compose"]),
        "Kubernetes": (0.95, ["kubernetes", "kubectl", "helm", "apiVersion:", "kind:"]),
        "Git": (0.90, ["git"]),
        "GitHub": (0.90, ["github"]),
        "GitLab": (0.90, ["gitlab"]),
        "AWS": (0.90, ["aws", "boto3", "s3", "ec2", "lambda"]),
        "GCP": (0.90, ["gcp", "google.cloud", "googleapis"]),
        "Azure": (0.90, ["azure"]),
        "CI/CD": (0.85, ["ci/cd", "circleci", "github actions", "gitlab ci", "jenkins"]),
        "Jenkins": (0.85, ["jenkins"]),
        "Terraform": (0.85, ["terraform"]),
        "Ansible": (0.85, ["ansible"]),
    }

    def extract_skills(self, text: str, filename: Optional[str] = None) -> list[SkillDetection]:
        """
        Extract skills from source code or documentation text.

        Args:
            text: The source text to analyze
            filename: Optional filename for extension-based detection

        Returns:
            List of detected skills with confidence scores
        """
        detected_skills = {}

        # Detect languages first
        self._detect_languages(text, filename, detected_skills)

        # Detect frameworks and libraries
        self._detect_frameworks(text, detected_skills)

        # Detect React specifically
        self._detect_react(text, detected_skills)

        # Detect databases
        self._detect_databases(text, detected_skills)

        # Detect tools
        self._detect_tools(text, detected_skills)

        # Sort by confidence
        return sorted(
            detected_skills.values(),
            key=lambda x: x.confidence,
            reverse=True,
        )

    def _detect_languages(
        self,
        text: str,
        filename: Optional[str],
        skills_dict: dict,
    ) -> None:
        """Detect programming languages."""
        text_lower = text.lower()

        # Python detection
        python_evidence = []
        if ".py" in str(filename or "").lower():
            python_evidence.append("Python file extension (.py)")
        if re.search(r"\bimport\s+\w+", text):
            python_evidence.append("Python import statements")
        if re.search(r"\bdef\s+\w+\s*\(", text):
            python_evidence.append("Python function definitions")
        if re.search(r":\s*(int|str|float|bool|list|dict)", text):
            python_evidence.append("Python type annotations")
        if "requirements.txt" in text_lower:
            python_evidence.append("requirements.txt found")

        if python_evidence:
            skills_dict["Python"] = SkillDetection(
                name="Python",
                category="Language",
                confidence=min(0.95, 0.6 + len(python_evidence) * 0.1),
                evidence=python_evidence,
            )

        # JavaScript/TypeScript detection
        js_evidence = []
        ts_evidence = []
        filename_lower = str(filename or "").lower()

        if ".js" in filename_lower:
            js_evidence.append("JavaScript file extension (.js)")
        if ".ts" in filename_lower or ".tsx" in filename_lower:
            ts_evidence.append("TypeScript file extension (.ts/.tsx)")

        if re.search(r"\bimport\s+", text):
            js_evidence.append("CommonJS or ES6 imports")
        if re.search(r"\brequire\s*\(", text):
            js_evidence.append("CommonJS require calls")
        if "package.json" in text_lower:
            js_evidence.append("package.json found")

        # TypeScript-specific indicators
        if re.search(r"\bexport\s+(interface|type|enum|class)\b", text_lower):
            ts_evidence.append("TypeScript export interface/type/enum/class")
        if re.search(r"\bPromise<", text):
            ts_evidence.append("TypeScript Promise generic")
        if re.search(r":\s*(string|number|boolean|any|unknown|void|never|readonly)\b", text_lower):
            ts_evidence.append("TypeScript type annotation")
        if re.search(r"\bimplements\s+\w+", text_lower):
            ts_evidence.append("TypeScript implements keyword")

        if ts_evidence:
            skills_dict["TypeScript"] = SkillDetection(
                name="TypeScript",
                category="Language",
                confidence=min(0.95, 0.6 + len(ts_evidence) * 0.1),
                evidence=ts_evidence,
            )
        elif js_evidence:
            skills_dict["JavaScript"] = SkillDetection(
                name="JavaScript",
                category="Language",
                confidence=min(0.95, 0.6 + len(js_evidence) * 0.1),
                evidence=js_evidence,
            )

        # Other languages by extension
        extension_langs = {
            ".java": ("Java", 0.95),
            ".cpp": ("C++", 0.95),
            ".cs": ("C#", 0.95),
            ".go": ("Go", 0.95),
            ".rs": ("Rust", 0.95),
            ".rb": ("Ruby", 0.95),
            ".php": ("PHP", 0.95),
            ".swift": ("Swift", 0.95),
        }

        filename_lower = str(filename or "").lower()
        for ext, (lang, confidence) in extension_langs.items():
            if ext in filename_lower:
                skills_dict[lang] = SkillDetection(
                    name=lang,
                    category="Language",
                    confidence=confidence,
                    evidence=[f"{lang} file extension"],
                )

    def _detect_frameworks(self, text: str, skills_dict: dict) -> None:
        """Detect frameworks and libraries."""
        text_lower = text.lower()

        for framework, (category, confidence) in self.FRAMEWORKS.items():
            if framework in text_lower:
                display_name = framework.title()
                if display_name not in skills_dict:
                    skills_dict[display_name] = SkillDetection(
                        name=display_name,
                        category=category,
                        confidence=confidence,
                        evidence=[f"Found '{framework}' in content"],
                    )

    def _detect_react(self, text: str, skills_dict: dict) -> None:
        """Detect React specifically."""
        text_lower = text.lower()
        react_evidence = []

        for indicator in self.REACT_INDICATORS:
            if indicator.lower() in text_lower:
                react_evidence.append(indicator)

        if react_evidence:
            skills_dict["React"] = SkillDetection(
                name="React",
                category="Framework",
                confidence=min(0.99, 0.7 + len(react_evidence) * 0.05),
                evidence=react_evidence,
            )

    def _detect_databases(self, text: str, skills_dict: dict) -> None:
        """Detect databases."""
        text_lower = text.lower()

        for display_name, (confidence, keywords) in self.DATABASES.items():
            if any(keyword in text_lower for keyword in keywords):
                if display_name not in skills_dict:
                    skills_dict[display_name] = SkillDetection(
                        name=display_name,
                        category="Database",
                        confidence=confidence,
                        evidence=[f"Found '{keywords[0]}' reference in content"],
                    )

    def _detect_tools(self, text: str, skills_dict: dict) -> None:
        """Detect tools and DevOps technologies."""
        text_lower = text.lower()

        for display_name, (confidence, keywords) in self.TOOLS.items():
            found = False

            if display_name == "Docker":
                if any(keyword in text_lower for keyword in keywords):
                    found = True
                elif re.search(r"^\s*from\s+[\w\-./:]+", text_lower, re.MULTILINE):
                    found = True
                elif re.search(r"^\s*version\s*:\s*['\"]?\d+\.\d+['\"]?", text_lower, re.MULTILINE) and \
                    re.search(r"^\s*services\s*:\s*$", text_lower, re.MULTILINE):
                    found = True
            else:
                if any(keyword in text_lower for keyword in keywords):
                    found = True

            if found and display_name not in skills_dict:
                skills_dict[display_name] = SkillDetection(
                    name=display_name,
                    category="Tool",
                    confidence=confidence,
                    evidence=[f"Found '{display_name}' reference in content"],
                )
