import json
from collections import Counter, defaultdict
import pandas as pd
from datetime import datetime, timezone, timedelta

# Load JSON data
def load_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data

# Analyze data and create a sender_id to name mapping
def analyze_data(messages, swear_words, debug_users):
    swear_count = Counter()
    likes_count = Counter()
    total_word_count = Counter()
    unique_word_set = {}  # Change from count to set
    sender_id_to_name = {}
    debug_data = {user: {'total_words': [], 'unique_words': set()} for user in debug_users}

    for message in messages:
        sender_id = message['sender_id']
        sender_name = message['name']

        # Exclude 'groupme' user and map sender_id to name if not already done
        if sender_id != 'system' and sender_id not in sender_id_to_name:
            sender_id_to_name[sender_id] = sender_name
        
        # Counting swears and words for lexical diversity
        text = message.get('text')
        if text and sender_id != 'system':
            words = text.lower().split()  # Convert to lowercase
            total_word_count[sender_id] += len(words)  # Count all words
            if sender_id not in unique_word_set:
                unique_word_set[sender_id] = set()
            unique_word_set[sender_id].update(words)  # Store unique words

            if sender_name in debug_users:
                debug_data[sender_name]['total_words'].extend(words)
                debug_data[sender_name]['unique_words'].update(words)

            for word in words:
                if word in swear_words:
                    swear_count[sender_id] += 1

        # Counting likes
        if sender_id != 'system':
            for liked_by in message['favorited_by']:
                likes_count[liked_by] += 1

    # Debug: Print debug data for specific users
    for user, data in debug_data.items():
        print(f"User: {user}, Total Words: {len(data['total_words'])}, Unique Words: {len(data['unique_words'])}")
        print(f"Total Words: {data['total_words']}")
        print(f"Unique Words: {data['unique_words']}")

    swear_word_percentage = {sender_id: (swear_count[sender_id] / total_word_count[sender_id] * 100) if total_word_count[sender_id] > 0 else 0 for sender_id in total_word_count}


    # Calculate lexical diversity
    lexical_diversity = {sender_id: len(unique_word_set[sender_id]) / total_word_count[sender_id] 
                         if total_word_count[sender_id] > 0 else 0 
                         for sender_id in total_word_count}

    return swear_count, likes_count, lexical_diversity, sender_id_to_name, swear_word_percentage

# Function to count name changes
def count_name_changes(messages):
    name_changes = defaultdict(set)
    for message in messages:
        sender_id = message['sender_id']
        sender_name = message['name']
        name_changes[sender_id].add(sender_name)

    # Count the number of different names used by each sender_id
    name_change_count = {sender_id: len(names) - 1 for sender_id, names in name_changes.items()}
    return name_change_count

# Function to count messages for each user
def count_messages(messages):
    message_count = Counter()
    for message in messages:
        sender_id = message['sender_id']
        message_count[sender_id] += 1
    return message_count

# Function to count messages and calculate average message length
def count_messages_and_average_length(messages):
    message_count = Counter()
    total_length = Counter()

    for message in messages:
        sender_id = message['sender_id']
        text = message.get('text')  # Get the text
        text = text if text is not None else ''  # Ensure text is not None
        message_count[sender_id] += 1
        total_length[sender_id] += len(text)

    # Calculate average message length
    average_length = {sender_id: total_length[sender_id] / message_count[sender_id] if message_count[sender_id] > 0 else 0 for sender_id in message_count}
    
    return message_count, average_length

# Function to determine who each individual likes the most
def find_favorite_targets(messages, id_to_name):
    likes_given = defaultdict(Counter)

    for message in messages:
        sender_id = message['sender_id']
        liked_by_users = message['favorited_by']
        for user in liked_by_users:
            likes_given[user][sender_id] += 1

    # Find out the sender who received the most likes from each user
    favorite_targets = {}
    for user, likes in likes_given.items():
        favorite_sender_id = max(likes, key=likes.get)
        favorite_sender_name = id_to_name.get(favorite_sender_id, favorite_sender_id)
        favorite_targets[id_to_name.get(user, user)] = favorite_sender_name

    return favorite_targets

# Function to count the total number of likes received by each user
def count_likes_received(messages):
    likes_received = Counter()

    for message in messages:
        sender_id = message['sender_id']
        number_of_likes = len(message['favorited_by'])
        likes_received[sender_id] += number_of_likes

    return likes_received

# Function to count messages sent between 2 AM and 4 AM
def count_messages_in_time_range(messages, start_hour, end_hour, utc_offset=-6):
    message_count = Counter()
    for message in messages:
        sender_id = message['sender_id']
        timestamp = message['created_at']
        # Adjust for Central Time
        adjusted_time = datetime.fromtimestamp(timestamp, timezone.utc) + timedelta(hours=utc_offset)
        
        if start_hour <= adjusted_time.hour < end_hour:
            message_count[sender_id] += 1

    return message_count

def calculate_percentage_in_time_range(messages, start_hour, end_hour, utc_offset):
    total_message_count = Counter()
    time_range_message_count = Counter()

    for message in messages:
        sender_id = message['sender_id']
        timestamp = message['created_at']
        adjusted_time = datetime.fromtimestamp(timestamp, timezone.utc) + timedelta(hours=utc_offset)
        
        total_message_count[sender_id] += 1
        if start_hour <= adjusted_time.hour < end_hour:
            time_range_message_count[sender_id] += 1

    # Calculate percentage
    percentage_in_time_range = {sender_id: (time_range_message_count[sender_id] / total_message_count[sender_id] * 100) if total_message_count[sender_id] > 0 else 0 for sender_id in total_message_count}

    return percentage_in_time_range

# Main function to run analytics
def run_analytics(file_path, excluded_users):
    messages = load_data(file_path)

    # Basic list of swear words (extend this list as needed)
    swear_words = {'damn', 'hell', 'shit', 'fuck', 'cunt', 'ass', 'cock', 'pussy', 'bitch'}  # Add more words here

    # Users to debug
    debug_users = []

    swears, likes, diversity, id_to_name, swear_percentage = analyze_data(messages, swear_words, debug_users)
    name_changes = count_name_changes(messages)
    message_counts, average_message_length = count_messages_and_average_length(messages)

    # Find out who each user likes
    likes_details = defaultdict(lambda: defaultdict(int))  # Nested dictionary to store likes details

    for message in messages:
        sender_id = message['sender_id']
        for liked_by in message['favorited_by']:
            if sender_id not in excluded_users and liked_by not in excluded_users:
                sender_name = id_to_name.get(sender_id, sender_id)
                liked_by_name = id_to_name.get(liked_by, liked_by)
                likes_details[sender_name][liked_by_name] += 1

    # Flatten the likes details to a list of tuples
    likes_flattened = [(sender, receiver, likes) for sender, receivers in likes_details.items() for receiver, likes in receivers.items()]

    # Convert the likes details to a DataFrame
    likes_df = pd.DataFrame(likes_flattened, columns=['Sender', 'Receiver', 'Likes'])


    # Replace sender_id with names and exclude specific users in the counters
    swears = {id_to_name.get(sender_id, sender_id): count for sender_id, count in swears.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    likes = {id_to_name.get(sender_id, sender_id): count for sender_id, count in likes.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    diversity = {id_to_name.get(sender_id, sender_id): value for sender_id, value in diversity.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    name_change_counts = {id_to_name.get(sender_id, sender_id): count for sender_id, count in name_changes.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    message_counts = {id_to_name.get(sender_id, sender_id): count for sender_id, count in message_counts.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    average_message_length = {id_to_name.get(sender_id, sender_id): length for sender_id, length in average_message_length.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    favorite_targets = find_favorite_targets(messages, id_to_name)
    likes_received = count_likes_received(messages)
    likes_received = {id_to_name.get(sender_id, sender_id): count for sender_id, count in likes_received.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    messages_2_to_4_am_central = count_messages_in_time_range(messages, 2, 4, utc_offset=-6)
    messages_2_to_4_am_central = {id_to_name.get(sender_id, sender_id): count for sender_id, count in messages_2_to_4_am_central.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    messages_6_to_8_am_central = count_messages_in_time_range(messages, 6, 8, utc_offset=-6)
    messages_6_to_8_am_central = {id_to_name.get(sender_id, sender_id): count for sender_id, count in messages_6_to_8_am_central.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    percentage_2_to_4_am_central = calculate_percentage_in_time_range(messages, 2, 4, utc_offset=-6)
    percentage_6_to_8_am_central = calculate_percentage_in_time_range(messages, 6, 8, utc_offset=-6)
    percentage_2_to_4_am_central = {id_to_name.get(sender_id, sender_id): percent for sender_id, percent in percentage_2_to_4_am_central.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    percentage_6_to_8_am_central = {id_to_name.get(sender_id, sender_id): percent for sender_id, percent in percentage_6_to_8_am_central.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}
    swear_percentage = {id_to_name.get(sender_id, sender_id): percent for sender_id, percent in swear_percentage.items() if id_to_name.get(sender_id, sender_id) not in excluded_users}


    # Creating a DataFrame
    data = {'Mess_Count': message_counts, 'Avg_Mess_Len': average_message_length, 'Swear_Count': swears, "%_Swear": swear_percentage, 'Likes_Given': likes, 'Likes_Taken': likes_received, 'Lex_Div': diversity, 'Name_Change': name_change_counts, 'Fav': favorite_targets, 'Night_Owl': percentage_2_to_4_am_central,'Early_Bird': percentage_6_to_8_am_central}
    df = pd.DataFrame.from_dict(data, orient='index').fillna(0).transpose()

    df = df[~df.index.isin(excluded_users)]
    likes_df = likes_df[~likes_df['Sender'].isin(excluded_users)]
    likes_df = likes_df[~likes_df['Receiver'].isin(excluded_users)]

    #print(likes_df)
    return(df, likes_df)




