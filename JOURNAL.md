# Journal — Issue #152

## Investigation
I located the faithfulness checker in `faithfulness_checker.py`.

The checker currently requires at least two meaningful overlapping words:

```python
return len(meaningful_overlap) >= 2