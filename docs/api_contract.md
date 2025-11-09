diff --git a/docs/api_contract.md b/docs/api_contract.md
new file mode 100644
index 0000000000000000000000000000000000000000..b60bf515972f85bbc0ac49418b9a2b2203ada5ff
--- /dev/null
+++ b/docs/api_contract.md
@@ -0,0 +1,34 @@
+# API Contract
+
+## GET /health
+- **Description**: Liveness probe.
+- **Response**: `200 OK`
+```json
+{"status": "ok"}
+```
+
+## POST /classify
+- **Description**: Classifies a payment error.
+- **Request Body**:
+```json
+{
+  "raw_code": "531",
+  "raw_message": "Account is not eligible"
+}
+```
+- **Response**: `200 OK`
+```json
+{
+  "category": "ACCOUNT_ERROR",
+  "user_message": "This account isn't eligible for online payments right now.",
+  "agent_steps": [
+    "Check account status/credit hold",
+    "Verify billing account mapping",
+    "If on hold, follow AR policy",
+    "Inform customer of next steps"
+  ],
+  "confidence": 1.0,
+  "source": "rules"
+}
+```
+- **Error Codes**: Validation errors handled by FastAPI/Pydantic (`422 Unprocessable Entity`).
