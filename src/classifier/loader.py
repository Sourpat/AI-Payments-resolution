diff --git a/src/classifier/loader.py b/src/classifier/loader.py
new file mode 100644
index 0000000000000000000000000000000000000000..bf9265b2f18db1d2052d9115f0fd70b31eb48efd
--- /dev/null
+++ b/src/classifier/loader.py
@@ -0,0 +1,69 @@
+"""Utilities for loading rules from CSV mappings."""
+from __future__ import annotations
+
+from dataclasses import dataclass
+from pathlib import Path
+from typing import List, Optional
+
+import csv
+
+
+@dataclass
+class Rule:
+    """Data representation of a single classification rule."""
+
+    provider_code: str
+    source: str
+    regex_hint: str
+    substring_hint: str
+    category: str
+    user_message: str
+    agent_steps: List[str]
+
+
+def _get_default_mapping_path() -> Path:
+    return Path(__file__).resolve().parents[1] / "data" / "mappings.csv"
+
+
+def _normalize_step(step: str) -> str:
+    cleaned = step.strip()
+    if not cleaned:
+        return ""
+    # Remove common numbering prefixes like "1)" or "1."
+    if len(cleaned) > 2 and cleaned[0].isdigit() and cleaned[1] in {")", ".", ":"}:
+        cleaned = cleaned[2:].strip()
+    return cleaned
+
+
+def load_rules(path: Optional[Path] = None) -> List[Rule]:
+    """Load the set of rules from ``mappings.csv``."""
+
+    csv_path = path or _get_default_mapping_path()
+    if not csv_path.exists():
+        raise FileNotFoundError(f"Mapping file not found at {csv_path}")
+
+    rules: List[Rule] = []
+    with csv_path.open(newline="", encoding="utf-8") as handle:
+        reader = csv.DictReader(handle)
+        for row in reader:
+            agent_steps_raw = row.get("agent_steps", "")
+            steps = [
+                _normalize_step(step)
+                for step in agent_steps_raw.split(";")
+                if _normalize_step(step)
+            ]
+            rules.append(
+                Rule(
+                    provider_code=row.get("provider_code", "").strip(),
+                    source=row.get("source", "").strip(),
+                    regex_hint=row.get("regex_hint", "").strip(),
+                    substring_hint=row.get("substring_hint", "").strip(),
+                    category=row.get("category", "").strip(),
+                    user_message=row.get("user_message", "").strip(),
+                    agent_steps=steps,
+                )
+            )
+    return rules
+
+
+__all__ = ["Rule", "load_rules"]
