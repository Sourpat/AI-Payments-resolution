diff --git a/src/models/schemas.py b/src/models/schemas.py
new file mode 100644
index 0000000000000000000000000000000000000000..0ef14510856d16edf496590e517c29900b60a01a
--- /dev/null
+++ b/src/models/schemas.py
@@ -0,0 +1,17 @@
+"""Pydantic models for API payloads."""
+from __future__ import annotations
+
+from pydantic import BaseModel, Field
+
+
+class ErrorInput(BaseModel):
+    raw_code: str = Field("", description="Provider or internal error code.")
+    raw_message: str = Field("", description="Original error message text.")
+
+
+class ClassificationResult(BaseModel):
+    category: str
+    user_message: str
+    agent_steps: list[str]
+    confidence: float
+    source: str = "rules"
