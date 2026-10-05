#!/usr/bin/env python3
"""Quick test to verify the JSON array fix works."""

import json
import sys

from rag.generator.output_parser import FeedbackSection, parse_review_output


def test_json_array_fallback() -> bool:
    """Test that JSON array is handled gracefully."""
    json_array = json.dumps(["First feedback item", "Second feedback item"])

    print("Input: JSON array")
    print(f"  {json_array}")
    print()

    try:
        result = parse_review_output(json_array)
        print("✓ Success - no crash")
        print(f"  Result type: {type(result)}")
        print(f"  Result length: {len(result)}")

        if result:
            section = result[0]
            print(f"  First section name: {section.section_name}")
            print(f"  First section type: {type(section).__name__}")
            assert isinstance(section, FeedbackSection), "Result should be FeedbackSection"
            assert isinstance(result, list), "Result should be a list"

        print()
        print("✓ Test PASSED - JSON array handled gracefully")
        return True

    except Exception as e:
        print(f"✗ Test FAILED with error: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_json_array_fallback()
    sys.exit(0 if success else 1)
