"""LLM-based review generation."""

from dataclasses import dataclass
from typing import Optional
import openai
import structlog

from .prompt_templates import get_template
from .output_parser import parse_review_output, FeedbackSection

logger = structlog.get_logger()


@dataclass
class ReviewConfig:
    """Configuration for review generation."""
    api_key: str
    base_url: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 2000


class ReviewGenerator:
    """Generate reviews using LLM (OpenAI API or OpenRouter)."""

    def __init__(self, config: ReviewConfig):
        """Initialize review generator.

        Args:
            config: ReviewConfig with API settings
        """
        self.config = config
        self.client = openai.OpenAI(
            api_key=config.api_key,
            base_url=config.base_url
        )

    def generate_section(self, section_name: str, context_chunks: list[dict],
                        profile_data: dict) -> FeedbackSection:
        """Generate feedback for a specific section.

        Args:
            section_name: Section name (skills_feedback, projects_feedback, etc.)
            context_chunks: Retrieved context chunks
            profile_data: Profile metadata

        Returns:
            FeedbackSection with generated content
        """
        # Get template
        template = get_template(section_name)

        # Format context
        context_text = self._format_context(context_chunks)
        github_username = profile_data.get("github_username", "")
        project_count = len(profile_data.get("projects", []))

        prompt = template.format(
            context=context_text,
            github_username=github_username,
            project_count=project_count
        )

        # Call LLM
        response = self.client.chat.completions.create(
            model=self.config.model,
            messages=[
                {"role": "system", "content": "You are an expert portfolio reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )

        content = response.choices[0].message.content

        # Parse output
        sections = parse_review_output(content)

        # Return first section or create default
        if sections:
            return sections[0]

        logger.warning("no_sections_parsed", section_name=section_name)
        return FeedbackSection(
            section_name=section_name,
            content=content,
            confidence=0.6,
            suggestions=[]
        )

    def generate_full_review(self, profile_data: dict,
                            retrieved_chunks: list[dict]) -> list[FeedbackSection]:
        """Generate complete review across all sections.

        Args:
            profile_data: Profile metadata and projects
            retrieved_chunks: Context chunks from retrieval

        Returns:
            List of FeedbackSections for all review areas
        """
        section_names = [
            "skills_feedback",
            "projects_feedback",
            "presentation_feedback",
            "gaps_feedback",
            "first_impression"
        ]

        all_sections = []

        for section_name in section_names:
            try:
                section = self.generate_section(
                    section_name, retrieved_chunks, profile_data
                )

                # Add source citations if available
                section = self._add_citations(section, retrieved_chunks)

                all_sections.append(section)
                logger.info("section_generated", section=section_name)

            except Exception as e:
                logger.error("section_generation_failed", section=section_name,
                           error=str(e))
                # Continue with remaining sections
                all_sections.append(FeedbackSection(
                    section_name=section_name,
                    content=f"Error generating {section_name}",
                    confidence=0.0,
                    suggestions=[]
                ))

        # Consolidate duplicates across similar projects
        all_sections = self._consolidate_feedback(all_sections)

        logger.info("full_review_generated", section_count=len(all_sections))
        return all_sections

    @staticmethod
    def _format_context(chunks: list[dict]) -> str:
        """Format retrieved chunks into context string.

        Args:
            chunks: List of retrieved chunks

        Returns:
            Formatted context string
        """
        parts = []
        for i, chunk in enumerate(chunks[:10], 1):  # Limit to 10 chunks
            source = chunk.get("metadata", {}).get("source_id", "unknown")
            score = chunk.get("score", 0)
            text = chunk.get("text", "")
            parts.append(f"[{i}] (relevance: {score:.2f}) Source: {source}\n{text}")

        return "\n\n".join(parts)

    @staticmethod
    def _add_citations(section: FeedbackSection,
                       retrieved_chunks: list[dict]) -> FeedbackSection:
        """Add source citations to feedback section.

        Args:
            section: Feedback section
            retrieved_chunks: Retrieved context chunks

        Returns:
            Updated section with citations
        """
        # Append sources if available
        if retrieved_chunks:
            sources = set()
            for chunk in retrieved_chunks[:5]:
                source = chunk.get("metadata", {}).get("source_id")
                if source:
                    sources.add(source)

            if sources:
                citation = f"\nSources: {', '.join(sorted(sources))}"
                section.content += citation

        return section

    @staticmethod
    def _content_similarity(a: str, b: str) -> float:
        """Jaccard similarity between two texts on their word sets.

        Args:
            a: First text
            b: Second text

        Returns:
            Similarity in 0.0-1.0 (1.0 = identical word sets, 0.0 = disjoint)
        """
        tokens_a = set(a.lower().split())
        tokens_b = set(b.lower().split())
        if not tokens_a and not tokens_b:
            return 1.0
        union = tokens_a | tokens_b
        if not union:
            return 0.0
        return len(tokens_a & tokens_b) / len(union)

    @staticmethod
    def _consolidate_feedback(
        sections: list[FeedbackSection], similarity_threshold: float = 0.8
    ) -> list[FeedbackSection]:
        """Consolidate near-duplicate feedback across sections.

        When a user has several projects in the same tech stack, the generator
        can emit near-identical observations in different sections. This keeps the
        first occurrence of each distinct piece of feedback and folds any duplicate
        section's suggestions into it, rather than repeating the same content.

        Args:
            sections: List of feedback sections
            similarity_threshold: Word-overlap ratio (0-1) at or above which two
                sections are treated as duplicates.

        Returns:
            Consolidated list of sections with duplicates merged.
        """
        consolidated: list[FeedbackSection] = []

        for section in sections:
            duplicate_of = None
            for kept in consolidated:
                if (
                    ReviewGenerator._content_similarity(section.content, kept.content)
                    >= similarity_threshold
                ):
                    duplicate_of = kept
                    break

            if duplicate_of is None:
                consolidated.append(section)
            else:
                # Fold the duplicate's suggestions into the kept section,
                # preserving order and dropping repeats.
                merged = list(
                    dict.fromkeys(duplicate_of.suggestions + section.suggestions)
                )
                duplicate_of.suggestions = merged
                logger.info(
                    "duplicate_feedback_consolidated",
                    dropped_section=section.section_name,
                    kept_section=duplicate_of.section_name,
                )

        return consolidated
