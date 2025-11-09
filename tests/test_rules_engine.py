diff --git a/tests/test_rules_engine.py b/tests/test_rules_engine.py
new file mode 100644
index 0000000000000000000000000000000000000000..8468743b44882452b71323bbcafc84108763bb50
--- /dev/null
+++ b/tests/test_rules_engine.py
@@ -0,0 +1,151 @@
+"""Unit tests for the rules engine."""
+from __future__ import annotations
+
+import math
+
+import pytest
+
+from src.classifier.rules_engine import classify_error, RulesEngine
+from src.classifier.loader import load_rules
+
+
+@pytest.fixture(scope="module")
+def engine() -> RulesEngine:
+    return RulesEngine(load_rules())
+
+
+def assert_result(result, category, confidence):
+    assert result["category"] == category
+    assert math.isclose(result["confidence"], confidence, rel_tol=1e-6)
+    assert result["source"] == "rules"
+
+
+def test_exact_provider_code_match(engine):
+    result = engine.classify("530", "any")
+    assert_result(result, "STATEMENT_REFERENCE_ERROR", 1.0)
+
+
+def test_exact_provider_code_case_insensitive(engine):
+    result = engine.classify("card_expired", "Payment failed")
+    assert_result(result, "PAYMENT_METHOD_ERROR", 1.0)
+
+
+def test_regex_timeout_match(engine):
+    result = engine.classify("", "Gateway timed out after 30s")
+    assert_result(result, "GATEWAY_TIMEOUT", 0.95)
+
+
+def test_regex_do_not_honor_match(engine):
+    result = engine.classify("", "Bank returned Do Not Honor status")
+    assert_result(result, "PAYMENT_POLICY_ERROR", 0.95)
+
+
+def test_regex_insufficient_funds_match(engine):
+    result = engine.classify("", "insufficient funds for transaction")
+    assert_result(result, "PAYMENT_METHOD_ERROR", 0.95)
+
+
+def test_regex_3ds_match(engine):
+    result = engine.classify("", "3DS authentication required")
+    assert_result(result, "PAYMENT_POLICY_ERROR", 0.95)
+
+
+def test_regex_cvv_match(engine):
+    result = engine.classify("", "Security code (cvv) mismatch")
+    assert_result(result, "PAYMENT_METHOD_ERROR", 0.95)
+
+
+def test_substring_match_statement(engine):
+    result = engine.classify("", "Issue with statement reference in request")
+    assert_result(result, "STATEMENT_REFERENCE_ERROR", 0.85)
+
+
+def test_substring_match_account(engine):
+    result = engine.classify("", "Account eligible flag missing")
+    assert_result(result, "ACCOUNT_ERROR", 0.85)
+
+
+def test_substring_match_token(engine):
+    result = engine.classify("", "token invalid due to rotation")
+    assert_result(result, "PAYMENT_METHOD_ERROR", 0.85)
+
+
+def test_substring_match_gateway_down(engine):
+    result = engine.classify("", "gateway down reported by monitor")
+    assert_result(result, "SYSTEM_OUTAGE", 0.85)
+
+
+def test_substring_match_network_glitch(engine):
+    result = engine.classify("", "network glitch observed during retries")
+    assert_result(result, "GATEWAY_TIMEOUT", 0.85)
+
+
+def test_fuzzy_match_close_phrase(engine):
+    result = engine.classify("", "card is almost expire soon")
+    assert_result(result, "PAYMENT_METHOD_ERROR", 0.85)
+
+
+def test_unknown_when_no_match(engine):
+    result = engine.classify("", "completely unrelated error")
+    assert_result(result, "UNKNOWN", 0.0)
+    assert result["agent_steps"] == []
+
+
+def test_unknown_when_empty_inputs(engine):
+    result = engine.classify("", "")
+    assert_result(result, "UNKNOWN", 0.0)
+
+
+def test_classify_error_accepts_dict():
+    result = classify_error({"raw_code": "AVS_MISMATCH", "raw_message": ""})
+    assert_result(result, "PAYMENT_METHOD_ERROR", 1.0)
+
+
+def test_classify_error_accepts_object():
+    class Payload:
+        raw_code = "INSUFFICIENT_FUNDS"
+        raw_message = ""
+
+    result = classify_error(Payload())
+    assert_result(result, "PAYMENT_METHOD_ERROR", 1.0)
+
+
+def test_provider_code_precedence(engine):
+    result = engine.classify("TOKEN_INVALID", "Token invalid message")
+    assert_result(result, "PAYMENT_METHOD_ERROR", 1.0)
+
+
+def test_regex_precedence_over_substring(engine):
+    result = engine.classify("", "Timeout response but also duplicate payment")
+    assert_result(result, "GATEWAY_TIMEOUT", 0.95)
+
+
+def test_substring_fallback_when_regex_missing(engine):
+    result = engine.classify("", "autopay eligible check failed")
+    assert_result(result, "AUTOPAY_ELIGIBILITY", 0.85)
+
+
+def test_confidence_exact_match_is_highest(engine):
+    exact = engine.classify("GATEWAY_DOWN", "gateway down message")
+    regex_result = engine.classify("", "gateway down due to outage")
+    assert exact["confidence"] > regex_result["confidence"]
+
+
+def test_agent_steps_returned(engine):
+    result = engine.classify("LIMIT_EXCEEDED", "limit exceeded message")
+    assert result["agent_steps"]
+
+
+def test_rules_engine_loads_rules():
+    engine = RulesEngine()
+    assert len(engine.rules) >= 10
+
+
+def test_sequence_match_threshold(engine):
+    result = engine.classify("", "This is about gating down")
+    assert_result(result, "SYSTEM_OUTAGE", 0.85)
+
+
+def test_multiple_regex_patterns(engine):
+    result = engine.classify("", "Payment had no response from gateway")
+    assert_result(result, "GATEWAY_TIMEOUT", 0.95)
