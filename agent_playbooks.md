# Agent Playbooks (Starter)

Each section provides a 5–7 step guide and notes. Tailor to your org's policies.

## PAYMENT_METHOD_ERROR
1. Confirm payment method type and last 4 (never expose PAN/CVV).
2. Ask user to re-enter CVV and verify billing address.
3. If card expired, prompt to update expiry or add a new card.
4. Retry once after corrections (no more than 3 attempts/day).
5. Offer ACH/wire if card continues to fail.
6. Document steps and outcome in ticket.

## ACCOUNT_ERROR
1. Check AR/credit status and any holds in ERP.
2. If on hold, share next steps per policy (no charges allowed).
3. Coordinate with AR to remove hold when resolved.
4. Schedule follow-up; keep user informed.
5. Log audit trail with timestamps and agent ID.

## GATEWAY_TIMEOUT / NETWORK
1. Check payment partner status page and internal incident channel.
2. Auto-retry after 60–120s with exponential backoff (cap 3).
3. If persistent, stop retries and inform user; suggest alternate method.
4. Tag incident ID in audit log.

## STATEMENT_REFERENCE_ERROR
1. Refresh statements from ERP (force sync if available).
2. Validate statement ID and status (open/unpaid).
3. If just generated, wait 5–10 mins then retry.
4. If mismatch persists, escalate to billing support.

## DUPLICATE_TXN
1. Search for matching txn in last 24h by amount, account, and reference.
2. If found, present the existing receipt; do not re-charge.
3. Close as resolved and educate user on confirmation flow.

## SYSTEM_OUTAGE
1. Stop retries and display outage banner.
2. Create incident ticket; notify on-call.
3. Keep users updated with ETA; resume when resolved.

## LIMIT_EXCEEDED
1. Check policy thresholds for card and account.
2. Offer split payments if allowed; otherwise suggest ACH/wire.
3. Escalate for one-time exception if business approves.
