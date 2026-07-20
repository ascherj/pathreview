# Week 7 Journal

## Issue Link

Repository: https://github.com/eyobedmerhawi/pathreview

Assigned issue: **Issue #151 – Bias detector patterns are too narrow to match common phrasings**

## Issue Selection

I selected **Issue #151 (Tier 1)** because it matched my current familiarity with the codebase. The issue has a clearly defined scope and focuses on improving existing functionality instead of requiring major architectural changes. It gave me an opportunity to work with regular expressions, testing, and debugging while contributing a meaningful improvement.

## Problem Summary

The bias detector was missing several common educational bias statements because its matching patterns were too narrow. As a result, phrases such as "bootcamp graduates are not prepared" or "self-taught developers lack a strong technical foundation" were not consistently detected.

To fix this issue, I expanded the detector's regex patterns to recognize additional common educational bias phrasings and added regression tests to verify the new behavior. A successful fix ensures these statements are correctly identified while preserving existing functionality.