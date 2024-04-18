#!/bin/bash

# Loop 100 times
for i in {1..2}; do
  # Run the curl command
  curl -X 'POST' \
    'http://localhost:4557/events/book' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '[
      {
        "email": "marco@prova.it",
        "event_id": 2,
        "ticket_no": 3
      }
    ]' # Extract the message body using jq (assuming it's a JSON message)
  message=$(echo "$response" | jq -r '.message')
  printf "\n"
done

echo "Completed sending 100 booking requests."
