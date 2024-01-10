import requests
import csv

# Your access token
ACCESS_TOKEN = 'Replace with Access Token'

# The GroupMe group ID
GROUP_ID = 'Replace with Group ID'

# The base URL for the GroupMe API
BASE_URL = 'https://api.groupme.com/v3'

def get_group_members(group_id):
    members = {}
    response = requests.get(f'{BASE_URL}/groups/{group_id}', params={'token': ACCESS_TOKEN})
    if response.status_code == 200:
        data = response.json()['response']['members']
        for member in data:
            members[member['user_id']] = 0  # Initialize image count to 0 for each member
    else:
        print(f'Failed to fetch group members: {response.status_code}')
    return members

# Function to get messages from the GroupMe group
def get_messages(group_id):
    all_messages = []  # List to hold all messages
    params = {
        'token': ACCESS_TOKEN,
        'limit': 100  # Maximum number of messages per request
    }
    
    try:
        while True:
            response = requests.get(f'{BASE_URL}/groups/{group_id}/messages', params=params)
            if response.status_code == 200:
                data = response.json()['response']
                messages = data['messages']
                all_messages.extend(messages)

                if not data['count'] > len(all_messages):
                    break

                params['before_id'] = messages[-1]['id']
            else:
                print(f'Failed to fetch messages: {response.status_code}, {response.text}')
                break
    except Exception as e:
        print(f"An error occurred: {e}")

    return all_messages

# Function to count images sent by each pair
def count_images(messages, members):
    for message in messages:
        user_id = message['sender_id']
        if user_id in members:
            for attachment in message.get('attachments', []):
                if attachment['type'] == 'image':
                    members[user_id] += 1



# Main function to control the flow of the script.
def main():
    members = get_group_members(GROUP_ID)
    messages = get_messages(GROUP_ID)
    count_images(messages, members)

    with open('groupme_image_counts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['User ID', '# of Images Sent'])
        for user_id, count in members.items():
            writer.writerow([user_id, count])


if __name__ == "__main__":
    main()
