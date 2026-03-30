# Internal Support Procedural Handbook (v4.2)

## 1. Introduction
This handbook defines the standard operating procedures (SOPs) for the Purple Merit customer resolution team. All agents must adhere to these guidelines to ensure consistency, compliance, and high customer satisfaction scores (CSAT).

## 2. The Triage Process
### 2.1 Initial Classification
Every incoming ticket is processed through the Triage Agent. The agent must successfully map the ticket to one of the following primary intent buckets:
- **REFUND_REQUEST:** Customer wants money back for an item.
- **SHIPPING_DELAY:** Item is past the estimated delivery date.
- **DAMAGED_ITEM:** Item arrived in non-functional or poor aesthetic condition.
- **WRONG_ITEM:** Item received does not match the SKU ordered.
- **CANCELLATION:** Customer wants to stop an order before fulfillment.
- **PROMO_ISSUE:** Coupon code or loyalty point discrepancy.
- **FRAUD_ALERT:** High-risk indicators (IP mismatch, proxy, multiple failed payments).

### 2.2 Metadata Validation
Before issuing a decision, the agent MUST verify the Order Context JSON.
- **Order Date Integrity:** Ensure the `order_date` is not in the future and matches the transaction ID.
- **Status Check:** If the status is "SHIPPED," do not approve a cancellation without first attempting a carrier "intercept" (Fee applies: $15.00).

## 3. Adjudication Guidelines by Category
### 3.1 Apparel Footwear (High Volume)
- **Guideline:** Return window is 30 days.
- **Procedure:** 
    1. Check for "Final Sale" tag.
    2. Verify if the item is a "Hygiene Exception" (Underwear/Swimwear).
    3. If hygiene seal is broken, AUTO-DENY.
    4. If "Too Large" or "Too Small," offer a free exchange (pre-paid label) instead of a refund first to preserve the sale.

### 3.2 Electronics (High Value)
- **Risk:** High fraud potential.
- **Procedure:**
    1. Verify Serial Number/IMEI from the shipping log.
    2. Check for "Activation Lock" (Apple/Google).
    3. If locked, DO NOT process. Inform the customer to remove the lock remotely.
    4. For Lithium Battery issues, refer to the "HAZMAT Safety SOP" (Section 9).

### 3.3 Marketplace Sellers
- **Responsibility:** Sellers are independent contractors.
- **Guideline:** Purple Merit provides the platform; sellers provide the product.
- **A-to-Z Claim Trigger:** If the seller does not respond within 48 hours, the system should auto-flag for an A-to-Z claim.

## 4. Financial Resolution SOP
### 4.1 Refund Calculation
- **Full Refund:** Includes item price + taxes + original shipping (if the error was Purple Merit's).
- **Partial Refund:** Used for missing components or "Keep and Discount" offers.
- **Restocking Fees:** 10% for opened electronics over $500; 15% for bulk orders over 50 units.

### 4.2 Fraud and Verification
For any refund over $500:
- **ID Verification:** Request a secure upload of government ID.
- **Address Check:** Match delivery address with billing address. Flag if mismatch exceeds 100 miles.

## 5. Escalation Hierarchies
### 5.1 Level 1 (AI Agent)
- Handles 80% of standard returns, status checks, and simple cancellations.
- Authorized to approve refunds up to $50.

### 5.2 Level 2 (Human Supervisor)
- Handles "Conflict" cases (EU law vs. Policy).
- Authorized to approve refunds up to $500.
- Handles HAZMAT and Battery Safety claims.

### 5.3 Level 3 (Management/Safety)
- Handles suspected fraud rings.
- Authorized for all refund amounts.
- Authority to ban accounts for policy abuse.

## 6. Communication Standards (TONE)
- **Voice:** Professional, empathetic, but firm on policy.
- **Citations:** Every policy-based denial MUST include the specific section name and a brief quote.

... [EXTENDED SECTIONS REPLICATED FOR VOLUME] ...
[Adding 2000 words of repetitive but structured policy clauses for category variations: Home, Garden, Automotive, Pet Supplies, Grocery, Beauty, Toys, Sports, Tools, Office, etc.]
... [Procedural Appendix A: Regional Tax Tables] ...
... [Procedural Appendix B: Carrier Claims Contact List] ...
... [Procedural Appendix C: Hygiene Safety Standards] ...
