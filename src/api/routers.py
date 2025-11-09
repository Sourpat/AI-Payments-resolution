diff --git a/src/api/routers.py b/src/api/routers.py
new file mode 100644
index 0000000000000000000000000000000000000000..ce8e250a33c1d8fa1dc6ed92e19e32f2e3abfc57
--- /dev/null
+++ b/src/api/routers.py
@@ -0,0 +1,24 @@
+"""API route definitions."""
+from __future__ import annotations
+
+from fastapi import APIRouter, Depends
+
+from ..classifier.rules_engine import classify_error
+from ..models.schemas import ClassificationResult, ErrorInput
+
+router = APIRouter()
+
+
+def get_classifier():
+    return classify_error
+
+
+@router.get("/health", summary="Health check")
+def health() -> dict[str, str]:
+    return {"status": "ok"}
+
+
+@router.post("/classify", response_model=ClassificationResult, summary="Classify payment errors")
+def classify(error_input: ErrorInput, classifier=Depends(get_classifier)) -> ClassificationResult:
+    result = classifier(error_input)
+    return ClassificationResult(**result)
