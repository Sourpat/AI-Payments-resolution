diff --git a/README.md b/README.md
new file mode 100644
index 0000000000000000000000000000000000000000..1e71d23d86ce967ef464512171541e5f2b033ce5
--- /dev/null
+++ b/README.md
@@ -0,0 +1,37 @@
+# AI Payment Error Resolution Engine
+
+Phase 1 delivery for a rules-driven error classifier built with FastAPI.
+
+## Features
+- Deterministic rules engine backed by `mappings.csv` with provider, regex, and substring hints.
+- REST API with `/health` and `/classify` endpoints.
+- Pydantic models for request/response validation.
+- 20+ unit tests covering rule priority paths and API contract.
+- Streamlit demo client for interactive testing.
+
+## Getting Started
+1. **Install dependencies**
+   ```bash
+   python3.10 -m venv .venv
+   source .venv/bin/activate
+   pip install -r requirements.txt
+   ```
+2. **Run the API**
+   ```bash
+   uvicorn src.api.main:app --reload
+   ```
+3. **Run tests**
+   ```bash
+   pytest
+   ```
+4. **Launch Streamlit demo**
+   ```bash
+   streamlit run demo/streamlit_app.py
+   ```
+
+## Configuration
+- Rules are stored in `src/data/mappings.csv`. Updating the CSV updates classification behaviour instantly at service start.
+
+## Future Work
+- Introduce ML-based embeddings for fallback classification.
+- Add caching (Redis) and feedback logging.
