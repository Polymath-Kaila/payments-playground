## Flow

```pgsql
Client
  ↓
POST /api/payments/initiate/
  ↓
Create PaymentTransaction (CREATED)
  ↓
Call provider API
  ↓
Store raw request
  ↓
Transition → PENDING
  ↓
Return reference to client
```
## Design Rule
+ Views do not talk to providers
+ Views do not change status
+ Views delegate to services