diff --git a/tests/test_api.py b/tests/test_api.py
new file mode 100644
index 0000000000000000000000000000000000000000..39e223b27341ca404c201320c8714b0ff9718ae7
--- /dev/null
+++ b/tests/test_api.py
@@ -0,0 +1,47 @@
+"""API contract tests."""
+from __future__ import annotations
+
+from fastapi.testclient import TestClient
+
+from src.api.main import app
+
+client = TestClient(app)
+
+
+def test_health_endpoint():
+    response = client.get("/health")
+    assert response.status_code == 200
+    assert response.json() == {"status": "ok"}
+
+
+def test_root_endpoint():
+    response = client.get("/")
+    assert response.status_code == 200
+    assert response.json()["message"].startswith("AI Payment Error")
+
+
+def test_classify_endpoint_exact():
+    payload = {"raw_code": "531", "raw_message": "ignored"}
+    response = client.post("/classify", json=payload)
+    assert response.status_code == 200
+    body = response.json()
+    assert body["category"] == "ACCOUNT_ERROR"
+    assert body["confidence"] == 1.0
+
+
+def test_classify_endpoint_regex():
+    payload = {"raw_code": "", "raw_message": "Payment duplicate already processed"}
+    response = client.post("/classify", json=payload)
+    assert response.status_code == 200
+    body = response.json()
+    assert body["category"] == "DUPLICATE_TXN"
+    assert body["confidence"] == 0.95
+
+
+def test_classify_endpoint_unknown():
+    payload = {"raw_code": "", "raw_message": "mystery"}
+    response = client.post("/classify", json=payload)
+    assert response.status_code == 200
+    body = response.json()
+    assert body["category"] == "UNKNOWN"
+    assert body["confidence"] == 0.0
