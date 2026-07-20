"""Tests for review_generator.py consolidation logic (issue #28).

These exercise the pure/static helpers directly, so they do not require an LLM
client, network access, or the ``ReviewGenerator`` to be instantiated.
"""

import pytest

from rag.generator.output_parser import FeedbackSection
from rag.generator.review_generator import ReviewGenerator


def _section(name: str, content: str, suggestions=None) -> FeedbackSection:
    return FeedbackSection(
        section_name=name,
        content=content,
        confidence=0.85,
        suggestions=suggestions or [],
    )


@pytest.mark.unit
class TestContentSimilarity:
    """Test suite for ReviewGenerator._content_similarity."""

    def test_identical_content_is_one(self):
        assert ReviewGenerator._content_similarity("python skills", "python skills") == 1.0

    def test_disjoint_content_is_zero(self):
        assert ReviewGenerator._content_similarity("python skills", "rust systems") == 0.0

    def test_both_empty_is_one(self):
        assert ReviewGenerator._content_similarity("", "") == 1.0

    def test_one_empty_is_zero(self):
        assert ReviewGenerator._content_similarity("python", "") == 0.0

    def test_partial_overlap_between_zero_and_one(self):
        # {a, b, c} vs {b, c, d}: intersection 2, union 4 -> 0.5
        sim = ReviewGenerator._content_similarity("a b c", "b c d")
        assert sim == pytest.approx(0.5)


@pytest.mark.unit
class TestConsolidateFeedback:
    """Test suite for ReviewGenerator._consolidate_feedback."""

    def test_empty_list_returns_empty(self):
        assert ReviewGenerator._consolidate_feedback([]) == []

    def test_single_section_unchanged(self):
        sections = [_section("skills", "Strong Python skills in backend projects")]
        result = ReviewGenerator._consolidate_feedback(sections)
        assert len(result) == 1
        assert result[0].section_name == "skills"

    def test_distinct_sections_all_kept(self):
        sections = [
            _section("skills", "Strong Python skills demonstrated in backend projects"),
            _section("docs", "Clear README files and thorough documentation everywhere"),
            _section("testing", "Consider adding automated CI pipelines for reliability"),
        ]
        result = ReviewGenerator._consolidate_feedback(sections)
        assert len(result) == 3

    def test_duplicate_content_consolidated(self):
        dup = "Strong Python skills demonstrated across multiple backend projects"
        sections = [
            _section("project_1", dup),
            _section("project_2", dup),
            _section("docs", "Clear README files and thorough documentation everywhere"),
        ]
        result = ReviewGenerator._consolidate_feedback(sections)
        # The two identical project sections collapse into one; docs is distinct.
        assert len(result) == 2
        assert result[0].section_name == "project_1"

    def test_near_duplicate_above_threshold_consolidated(self):
        # 9 shared tokens, union 11 -> ~0.82, above the 0.8 default threshold.
        sections = [
            _section("a", "The developer shows strong Python skills in three backend projects"),
            _section("b", "The developer shows strong Python skills in two backend projects"),
        ]
        result = ReviewGenerator._consolidate_feedback(sections)
        assert len(result) == 1

    def test_below_threshold_not_consolidated(self):
        sections = [
            _section("a", "Strong Python skills in backend projects"),
            _section("b", "Excellent documentation and accessibility in the frontend"),
        ]
        result = ReviewGenerator._consolidate_feedback(sections)
        assert len(result) == 2

    def test_duplicate_suggestions_merged_without_repeats(self):
        dup = "Strong Python skills demonstrated across multiple backend projects"
        sections = [
            _section("project_1", dup, ["Add type hints", "Write docstrings"]),
            _section("project_2", dup, ["Write docstrings", "Add CI"]),
        ]
        result = ReviewGenerator._consolidate_feedback(sections)
        assert len(result) == 1
        assert result[0].suggestions == ["Add type hints", "Write docstrings", "Add CI"]

    def test_threshold_is_configurable(self):
        sections = [
            _section("a", "Strong Python skills in backend projects"),
            _section("b", "Excellent documentation and accessibility in the frontend"),
        ]
        # A threshold of 0.0 treats everything as a duplicate of the first.
        result = ReviewGenerator._consolidate_feedback(sections, similarity_threshold=0.0)
        assert len(result) == 1
