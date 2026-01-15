# Idempotency
The same event may arrive multiple times.  

Our system must say:  
 "I have already processed this".  
 
 This is why:  
 + Refrences are unique
 + Events are logged
 + Status updates are guarded

 We use universal unique identifier(uuid) to make our transactions idempotent by storing it in db.  
 