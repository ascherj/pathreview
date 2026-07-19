# scratch_repro.py
from safety.pii_scrubber import PIIScrubber

s = PIIScrubber()
print(repr(s.scrub("Call me at (555) 123-4567 or 555-123-4567")))
print(s.detect("Call me at (555) 123-4567"))
