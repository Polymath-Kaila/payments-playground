### 1.CRAETED
+ Payment intent is created internally
+ No external provider contacted yet
+ Refrence generated
+ Safe to retry craetion

Example:  
User clicks `pay`, backend creates a record.  
we do not charge at this state.

---

### 2.PENDING
+ External provider has been contacted
+ Money not confirmed
+ Waiting for provider event(webhook)

Example:  
- M-Pesa STK Push sent
- Paystack checkout initialized

This state can last for seconds or minutes.  

---

### 3.SUCCESS
+ Provider confirms money was recieved
+ Verified via webhook or API verification
+ Irreversible(usually)

Only this state unlocks features.  

---

### 4. Failed
+ User canceled
+ Insufficient funds
+ Timeout
+ Provider error
  
---

## Payment Movement between States
This is never frontend actions.  

Only backend-controlled events:  

| Event                | Source   |
| -------------------- | -------- |
| STK push sent        | Backend  |
| Webhook received     | Provider |
| Verification success | Backend  |
| Verification failure | Backend  |


---

## Significance of PENDING state
It exit because:  
+ Networks fail
+ Phones go offline
+ Providers retry later
+ Money moves slower than code

If we skip `PENDING` we will:  
+ Double-credit users
+ Lose money
+ Create race conditions

---

A payment state must only change through a controlled function.  
Not views.  
Not serializers.  
Not admin edits.  

## Strategy to tackling it
We introduce:  
+ A service layer
+ A transition function
+ Automatic event creation
+ transition validation

We must prevent edge cases like, double refund, double charge etc.  

---
## STATES ALLOWED TRANSITIONS
| From              | To | Allowed? |
| ----------------- | -- | -------- |
| CREATED → PENDING | ✅  |          |
| PENDING → SUCCESS | ✅  |          |
| PENDING → FAILED  | ✅  |          |
| CREATED → SUCCESS | ❌  |          |
| SUCCESS → PENDING | ❌  |          |
| FAILED → SUCCESS  | ❌  |          |

---
We handle this explicitly in a service file say base.py because:  
1. In views we handle http requests so any code can modify state.  
2. In serializers we handle validations and they should be readonly so business logic will interfere with our state machine.  
