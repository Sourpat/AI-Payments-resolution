diff --git a/src/classifier/rules_engine.py b/src/classifier/rules_engine.py
new file mode 100644
index 0000000000000000000000000000000000000000..2bace2f5ddd2250829e1e816f52424c4cd05cd94
--- /dev/null
+++ b/src/classifier/rules_engine.py
@@ -0,0 +1,114 @@
+"""Rules-based classifier for payment error resolution."""
+from __future__ import annotations
+
+from dataclasses import dataclass
+from difflib import SequenceMatcher
+from typing import Any, Dict, Iterable, List, Optional
+
+import regex
+
+from .loader import Rule, load_rules
+
+
+@dataclass
+class MatchResult:
+    rule: Rule
+    confidence: float
+
+
+class RulesEngine:
+    """Core rules engine that performs layered matching."""
+
+    def __init__(self, rules: Optional[Iterable[Rule]] = None) -> None:
+        self.rules: List[Rule] = list(rules) if rules is not None else load_rules()
+        self._provider_index = {
+            rule.provider_code.lower(): rule for rule in self.rules if rule.provider_code
+        }
+
+    def classify(self, raw_code: str, raw_message: str) -> Dict[str, Any]:
+        raw_code = (raw_code or "").strip()
+        raw_message = (raw_message or "").strip()
+
+        match = (
+            self._match_provider_code(raw_code)
+            or self._match_regex(raw_message)
+            or self._match_substring_or_fuzzy(raw_message)
+        )
+
+        if match:
+            return {
+                "category": match.rule.category or "UNKNOWN",
+                "user_message": match.rule.user_message,
+                "agent_steps": match.rule.agent_steps,
+                "confidence": match.confidence,
+                "source": "rules",
+            }
+        return {
+            "category": "UNKNOWN",
+            "user_message": "",
+            "agent_steps": [],
+            "confidence": 0.0,
+            "source": "rules",
+        }
+
+    def _match_provider_code(self, raw_code: str) -> Optional[MatchResult]:
+        if not raw_code:
+            return None
+        rule = self._provider_index.get(raw_code.lower())
+        if rule:
+            return MatchResult(rule=rule, confidence=1.0)
+        return None
+
+    def _match_regex(self, raw_message: str) -> Optional[MatchResult]:
+        if not raw_message:
+            return None
+        for rule in self.rules:
+            if not rule.regex_hint:
+                continue
+            pattern = regex.compile(rule.regex_hint, regex.IGNORECASE)
+            if pattern.search(raw_message):
+                return MatchResult(rule=rule, confidence=0.95)
+        return None
+
+    def _match_substring_or_fuzzy(self, raw_message: str) -> Optional[MatchResult]:
+        if not raw_message:
+            return None
+        message_lower = raw_message.lower()
+        best_ratio = 0.0
+        best_rule: Optional[Rule] = None
+        for rule in self.rules:
+            hint = rule.substring_hint.lower() if rule.substring_hint else ""
+            if hint and hint in message_lower:
+                return MatchResult(rule=rule, confidence=0.85)
+            if hint:
+                ratio = SequenceMatcher(None, hint, message_lower).ratio()
+                if ratio > best_ratio:
+                    best_ratio = ratio
+                    best_rule = rule
+        if best_rule and best_ratio >= 0.6:
+            return MatchResult(rule=best_rule, confidence=0.85)
+        return None
+
+
+_engine = RulesEngine()
+
+
+def classify_error(error_input: Any) -> Dict[str, Any]:
+    """Public API for classifying errors.
+
+    ``error_input`` may be a mapping or object with ``raw_code`` and ``raw_message``.
+    """
+
+    raw_code = ""
+    raw_message = ""
+    if isinstance(error_input, dict):
+        raw_code = error_input.get("raw_code", "")
+        raw_message = error_input.get("raw_message", "")
+    else:
+        raw_code = getattr(error_input, "raw_code", "")
+        raw_message = getattr(error_input, "raw_message", "")
+
+    return _engine.classify(raw_code, raw_message)
+
+
+__all__ = ["RulesEngine", "classify_error"]
