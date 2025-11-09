diff --git a/demo/streamlit_app.py b/demo/streamlit_app.py
new file mode 100644
index 0000000000000000000000000000000000000000..6f30264adc4bec2c8b09b3594d61e30ad5f4ce8a
--- /dev/null
+++ b/demo/streamlit_app.py
@@ -0,0 +1,40 @@
+"""Streamlit demo for the AI Payment Error Resolution Engine."""
+from __future__ import annotations
+
+import os
+
+import requests
+import streamlit as st
+
+API_URL = os.getenv("API_URL", "http://localhost:8000")
+
+st.set_page_config(page_title="AI Payment Error Resolution Demo", layout="centered")
+st.title("AI Payment Error Resolution Engine")
+
+st.sidebar.header("API Settings")
+api_url = st.sidebar.text_input("FastAPI base URL", value=API_URL)
+
+st.header("Classify Payment Error")
+with st.form("classification_form"):
+    raw_code = st.text_input("Provider / Internal Code", placeholder="e.g. INSUFFICIENT_FUNDS")
+    raw_message = st.text_area(
+        "Error Message",
+        placeholder="Paste the raw gateway response or support note here",
+    )
+    submitted = st.form_submit_button("Classify")
+
+if submitted:
+    try:
+        response = requests.post(f"{api_url}/classify", json={"raw_code": raw_code, "raw_message": raw_message})
+        response.raise_for_status()
+        payload = response.json()
+        st.success(f"Category: {payload['category']} (confidence {payload['confidence']:.2f})")
+        st.write("**User Message**")
+        st.info(payload.get("user_message", ""))
+        st.write("**Agent Steps**")
+        for step in payload.get("agent_steps", []):
+            st.write(f"- {step}")
+    except requests.RequestException as exc:
+        st.error(f"Failed to contact API: {exc}")
+else:
+    st.caption("Provide an error code or message and press classify to see the recommendation.")
