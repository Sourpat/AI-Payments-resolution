diff --git a/docs/architecture.md b/docs/architecture.md
new file mode 100644
index 0000000000000000000000000000000000000000..567ddc524abe23690fbc012c1034fbf3c760e85d
--- /dev/null
+++ b/docs/architecture.md
@@ -0,0 +1,22 @@
+# AI Payment Error Resolution Engine Architecture
+
+## Overview
+The system is a FastAPI service that exposes a small classification engine for payment errors. On startup the service loads a deterministic rulebook stored in `src/data/mappings.csv`. Each rule contains the provider code, regex hints, substring hints, category, and recommended guidance for support agents.
+
+## Flow
+1. **Request ingress**: Clients call `POST /classify` with the payment provider code and free-form error message.
+2. **Validation**: Pydantic models validate and coerce the payload into `ErrorInput`.
+3. **Rules engine**: The request is passed to `classify_error`. The engine evaluates rules in priority order:
+   - Provider code lookup (exact match).
+   - Regex hint evaluation using the `regex` library.
+   - Substring or fuzzy similarity check using `SequenceMatcher`.
+4. **Response shaping**: The selected rule is serialized into a `ClassificationResult` that contains the suggested user message, agent steps, confidence, and category.
+5. **Delivery**: FastAPI returns the JSON payload to the caller. The same pipeline is reused by the Streamlit demo via HTTP.
+
+## Components
+- `src/classifier/loader.py`: Reads CSV mappings and normalizes steps.
+- `src/classifier/rules_engine.py`: Implements the layered matching logic and exposes `classify_error`.
+- `src/api/main.py`: Creates the FastAPI application and ensures rules load on startup.
+- `src/api/routers.py`: Defines the HTTP routes.
+- `demo/streamlit_app.py`: Lightweight UI for manual testing.
+- `tests/`: Unit and integration coverage (20+ scenarios) verifying classifier behaviour.
