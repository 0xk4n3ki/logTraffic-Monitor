#!/bin/bash

API_KEY="251304ee5d9571dfdc4d85134ac55d4f4972d3f9a35a38745e316f3018876bcd"
URL="http://localhost:8000/api/logs/"

# Service names
services=("payment" "auth" "order" "email" "notification" "database" "cache" "api-gateway" "inventory" "shipping" "analytics" "search" "cdn" "user-service" "billing")

# Log levels
levels=("INFO" "WARNING" "ERROR" "DEBUG" "CRITICAL")

# Function to get messages for a service
get_messages() {
  local service=$1
  case $service in
    payment)
      echo "Payment processed successfully for order #ORDER_ID
Payment failed for order #ORDER_ID
Credit card declined for order #ORDER_ID
Refund processed for order #ORDER_ID
Payment gateway timeout
Delayed payment confirmation for order #ORDER_ID
Fraudulent transaction detected for user USER_NAME
Payment retry attempted for order #ORDER_ID
Currency conversion applied for order #ORDER_ID
Payment webhook received from Stripe"
      ;;
    auth)
      echo "User USER_NAME logged in successfully
Invalid login attempt for user USER_NAME
Password changed successfully for user USER_NAME
Token expired for user USER_NAME
Multiple failed login attempts detected
User USER_NAME logged out
2FA verification failed for user USER_NAME
Session created for user USER_NAME
OAuth token refreshed for user USER_NAME
Account locked due to suspicious activity"
      ;;
    order)
      echo "Order #ORDER_ID successfully created
Order #ORDER_ID dispatched
Order #ORDER_ID payment confirmed
Inventory shortage for product #PRODUCT_ID
Order #ORDER_ID failed due to invalid address
Order #ORDER_ID cancelled by user
Order #ORDER_ID status updated to delivered
Bulk order processing completed
Order validation failed for #ORDER_ID
Order #ORDER_ID assigned to warehouse"
      ;;
    email)
      echo "Welcome email sent to new user USER_NAME
Failed to send email to user EMAIL_ADDRESS
Email delivery delayed to user USER_NAME
Password reset email sent to EMAIL_ADDRESS
Order confirmation email delivered
Email bounce detected for EMAIL_ADDRESS
Newsletter sent to RANDOM_COUNT subscribers
Email template rendered successfully
SMTP connection failed
Promotional email queued for delivery"
      ;;
    notification)
      echo "Push notification sent to user USER_NAME
Failed to deliver SMS to user USER_NAME
Email notification queued for user USER_NAME
In-app notification delivered
Notification preferences updated for user USER_NAME
FCM token expired for device DEVICE_ID
Webhook notification sent successfully
Alert triggered for system downtime
Notification batch processed
SMS gateway rate limit exceeded"
      ;;
    database)
      echo "Database connection established
Query execution time exceeded RANDOM_MS ms
Connection pool exhausted
Database backup completed successfully
Deadlock detected in transaction
Index rebuild completed for table_name
Replication lag detected: RANDOM_SEC seconds
Database migration applied successfully
Slow query detected: SELECT * FROM users
Database health check passed"
      ;;
    cache)
      echo "Cache hit for key: user_USER_ID
Cache miss for key: product_PRODUCT_ID
Redis connection restored
Cache invalidation completed
Memory usage at RANDOM_PERCENT%
Cache eviction policy triggered
Cache cluster node added
TTL expired for RANDOM_COUNT keys
Cache warming completed
Redis connection timeout"
      ;;
    api-gateway)
      echo "Request routed to service SERVICE_NAME
Rate limit exceeded for IP IP_ADDRESS
API key validation failed
Circuit breaker opened for SERVICE_NAME
Request timeout after RANDOM_MS ms
CORS preflight request handled
API version deprecated warning
Load balancer health check passed
Gateway processing RANDOM_COUNT requests/sec
Upstream service unavailable"
      ;;
    inventory)
      echo "Stock level updated for product #PRODUCT_ID
Low stock alert for product #PRODUCT_ID
Inventory sync completed
Product #PRODUCT_ID out of stock
Restock order placed for RANDOM_COUNT items
Inventory audit completed
Warehouse transfer initiated
Product #PRODUCT_ID reserved for order #ORDER_ID
Inventory discrepancy detected
Bulk inventory import completed"
      ;;
    shipping)
      echo "Shipping label generated for order #ORDER_ID
Tracking number assigned: TRACKING_NUM
Package picked up by carrier
Delivery attempted for order #ORDER_ID
Shipping rate calculated: \$RANDOM_PRICE
Address validation failed
Package marked as delivered
Shipment delayed due to weather
Return shipment initiated
Carrier API timeout"
      ;;
    analytics)
      echo "Daily report generated
User behavior tracked for session SESSION_ID
Conversion event recorded
Analytics pipeline processing RANDOM_COUNT events
Dashboard metrics updated
A/B test results calculated
Pageview logged for /page/path
Funnel analysis completed
Real-time analytics stream started
Data warehouse sync completed"
      ;;
    search)
      echo "Search query executed: 'SEARCH_TERM'
Search index updated
Elasticsearch cluster healthy
Search suggestion generated
Query returned RANDOM_COUNT results
Search timeout after RANDOM_MS ms
Index optimization completed
Synonym dictionary updated
Search ranking recalculated
Autocomplete cache refreshed"
      ;;
    cdn)
      echo "Cache purge completed
Asset served from edge location LOCATION_ID
SSL certificate renewed
Origin server health check passed
CDN cache hit ratio: RANDOM_PERCENT%
DDoS protection activated
Image optimization completed
Geographic routing updated
Bandwidth limit approaching
Edge function executed successfully"
      ;;
    user-service)
      echo "User profile updated for USER_NAME
New user registered: USER_NAME
User preferences saved
Profile picture uploaded
Account verification email sent
User search completed
User deactivation requested
Privacy settings updated
User export data generated
Duplicate account detected"
      ;;
    billing)
      echo "Invoice generated for customer CUSTOMER_ID
Subscription renewed for USER_NAME
Payment method updated
Billing cycle completed
Proration calculated: \$RANDOM_PRICE
Credit applied to account
Failed to charge customer CUSTOMER_ID
Tax calculation completed
Refund issued for invoice #INVOICE_ID
Usage-based billing calculated"
      ;;
  esac
}

# Helper function to generate random values
random_order_id() {
  echo $((1000 + RANDOM % 9000))
}

random_product_id() {
  echo $((100 + RANDOM % 900))
}

random_user() {
  users=("john_doe" "jane_smith" "alice_wonder" "bob_builder" "charlie_brown" "dave_grohl" "eve_online" "frank_ocean" "grace_hopper" "henry_ford")
  echo "${users[$((RANDOM % ${#users[@]}))]}"
}

random_email() {
  domains=("example.com" "test.com" "mail.com" "demo.com")
  user=$(random_user)
  domain="${domains[$((RANDOM % ${#domains[@]}))]}"
  echo "${user}@${domain}"
}

random_ip() {
  echo "$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256)).$((RANDOM % 256))"
}

random_ms() {
  echo $((100 + RANDOM % 9900))
}

random_sec() {
  echo $((1 + RANDOM % 60))
}

random_percent() {
  echo $((1 + RANDOM % 100))
}

random_count() {
  echo $((10 + RANDOM % 990))
}

random_price() {
  echo "$((10 + RANDOM % 490)).$((RANDOM % 100))"
}

random_tracking() {
  echo "TRK$(date +%s)$RANDOM"
}

random_session() {
  echo "sess_$(echo $RANDOM$RANDOM | md5sum 2>/dev/null | cut -c1-16 || echo $RANDOM$RANDOM)"
}

random_device() {
  echo "dev_$(echo $RANDOM | md5sum 2>/dev/null | cut -c1-12 || echo $RANDOM)"
}

random_location() {
  locations=("us-east-1" "us-west-2" "eu-west-1" "ap-south-1" "ap-northeast-1")
  echo "${locations[$((RANDOM % ${#locations[@]}))]}"
}

random_search_term() {
  terms=("laptop" "phone" "shoes" "headphones" "watch" "camera" "tablet" "speaker")
  echo "${terms[$((RANDOM % ${#terms[@]}))]}"
}

# Function to generate a random log
generate_log() {
  # Pick random service
  service="${services[$((RANDOM % ${#services[@]}))]}"
  
  # Pick random level (weighted towards INFO)
  rand=$((RANDOM % 100))
  if [ $rand -lt 50 ]; then
    level="INFO"
  elif [ $rand -lt 75 ]; then
    level="WARNING"
  elif [ $rand -lt 90 ]; then
    level="ERROR"
  elif [ $rand -lt 97 ]; then
    level="DEBUG"
  else
    level="CRITICAL"
  fi
  
  # Get messages for this service
  mapfile -t msg_array < <(get_messages "$service")
  message="${msg_array[$((RANDOM % ${#msg_array[@]}))]}"
  
  # Replace placeholders
  message="${message//ORDER_ID/$(random_order_id)}"
  message="${message//PRODUCT_ID/$(random_product_id)}"
  message="${message//USER_NAME/$(random_user)}"
  message="${message//USER_ID/$(random_order_id)}"
  message="${message//EMAIL_ADDRESS/$(random_email)}"
  message="${message//IP_ADDRESS/$(random_ip)}"
  message="${message//RANDOM_MS/$(random_ms)}"
  message="${message//RANDOM_SEC/$(random_sec)}"
  message="${message//RANDOM_PERCENT/$(random_percent)}"
  message="${message//RANDOM_COUNT/$(random_count)}"
  message="${message//RANDOM_PRICE/$(random_price)}"
  message="${message//TRACKING_NUM/$(random_tracking)}"
  message="${message//SESSION_ID/$(random_session)}"
  message="${message//DEVICE_ID/$(random_device)}"
  message="${message//LOCATION_ID/$(random_location)}"
  message="${message//SEARCH_TERM/$(random_search_term)}"
  message="${message//SERVICE_NAME/${services[$((RANDOM % ${#services[@]}))]}}"
  message="${message//CUSTOMER_ID/CUST$(random_order_id)}"
  message="${message//INVOICE_ID/INV$(random_order_id)}"
  
  # Create JSON
  echo "{\"service_name\":\"$service\",\"log_level\":\"$level\",\"message\":\"$message\"}"
}

# Function to send log
send_log() {
  local log=$1
  local timestamp=$(date -Iseconds)
  
  response=$(curl -s -w "\n%{http_code}" -X POST "$URL" \
    -H "Content-Type: application/json" \
    -H "API-KEY: $API_KEY" \
    -d "$(echo "$log" | jq --arg timestamp "$timestamp" '. + {timestamp: $timestamp}')")
  
  http_code=$(echo "$response" | tail -n1)
  
  if [ "$http_code" -eq 200 ] || [ "$http_code" -eq 201 ]; then
    echo "✓ Sent: $(echo "$log" | jq -r '.service_name') - $(echo "$log" | jq -r '.log_level')"
  else
    echo "✗ Failed (HTTP $http_code): $(echo "$log" | jq -r '.service_name')"
  fi
}

# Main loop
echo "Starting log generator... (Press Ctrl+C to stop)"
echo "Sending 4-10 logs per second"
echo "----------------------------------------"

while true; do
  # Random number of logs per second (4-10)
  logs_this_second=$((4 + RANDOM % 7))
  
  for ((i=0; i<logs_this_second; i++)); do
    log=$(generate_log)
    send_log "$log" &
  done
  
  # Wait for background jobs to complete
  wait
  
  # Sleep for 1 second
  sleep 1
done