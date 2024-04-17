#!/bin/bash

# Loop 100 times
for i in {1..100}; do
  # Run the curl command
  curl -X 'POST' \
    'http://localhost:4557/events/book' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '[
      {
        "email": "carlo@prova.it",
        "event_id": 2,
        "ticket_no": 3
      },
      {
        "email": "marco@prova.it",
        "event_id": 3,
        "ticket_no": 2
      },
      {
        "email": "marco@prova.it",
        "event_id": 1,
        "ticket_no": 1
      }
    ]' # Extract the message body using jq (assuming it's a JSON message)
  message=$(echo "$response" | jq -r '.message')
  printf "\n"

  # Print the message (if it exists)
  if [[ ! -z "$message" ]]; then
    echo "Request number $i: Message - $message"
  fi
done

echo "Completed sending 100 booking requests."
