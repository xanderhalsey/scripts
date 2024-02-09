#!/usr/bin/env python3

import csv
import requests
from datetime import datetime, timedelta

# Replace 'YOUR_TOKEN' with your GitHub PAT
GITHUB_TOKEN = 'YOUR_TOKEN'
HEADERS = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.v3+json',
}

def fetch_user_activity(username):
    url = f'https://api.github.com/users/{username}/events'
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # Raises any stored HTTPError
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {username}: {http_err}") 
        return "error"
    except Exception as err:
        print(f"Other error occurred for {username}: {err}") 
        return "error"

def check_activity_in_last_days(events, days=180):
    if events == "error":
        return "error"
    threshold_date = datetime.utcnow() - timedelta(days=days)
    for event in events:
        event_date = datetime.strptime(event['created_at'], "%Y-%m-%dT%H:%M:%SZ")
        if event_date > threshold_date:
            return "yes"
    return "no"

def main():
    input_filename = input("Enter the input CSV filename (including .csv): ")
    output_filename = 'user_activity.csv'
    
    with open(input_filename, newline='') as csvfile_in, open(output_filename, 'w', newline='') as csvfile_out:
        reader = csv.reader(csvfile_in)
        writer = csv.writer(csvfile_out)
        writer.writerow(['Username', 'Recent Activity'])

        for row in reader:
            username = row[0].strip()
            events = fetch_user_activity(username)
            activity_status = check_activity_in_last_days(events)
            writer.writerow([username, activity_status])
            print(f"Processed {username}: {activity_status}")

if __name__ == "__main__":
    main()
