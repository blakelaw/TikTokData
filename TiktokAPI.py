import httpx
import pandas as pd
import time
import datetime
import random

# Function to fetch trend data for a given hashtag
def fetch_trend_data(hashtag):
    # URL and query parameters
    url = "https://ads.tiktok.com/creative_radar_api/v1/popular_trend/hashtag/detail"
    params = {
        "period": "1095", # 1095 days is 3 years
        "hashtag_name": hashtag,
        "country_code": "US"
    }

    # Custom variables. Acccess through Inspect > Network tab then find each in your request header
    COOKIE = ""
    WEBID = ""
    USERSIGN = ""
    ANONID = ""

    # Custom headers
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Anonymous-User-Id": ANONID,
        "Cookie": COOKIE,
        "Dnt": "1",
        "Lang": "en",
        "Referer": f"https://ads.tiktok.com/business/creativecenter/hashtag/{hashtag}/pc/en?countryCode=US&period=7",
        "Sec-Ch-Ua": '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"macOS"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "Timestamp": "1702755403",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "User-Sign": USERSIGN,
        "Web-Id": WEBID
    }

    # Send the GET request
    response = httpx.get(url, headers=headers, params=params)

    # Extract 'trend' data from 'info'
    trend_data = response.json()['data']['info']['trend']

    return trend_data

# Hashtags to analyze
hashtags = ['looksmaxxing', 'mewing', 'mogger', 'pslgod', 'seanopry', 'jordanbarrett', 'chicolachowski']

# Dictionary to store dataframes for each hashtag
dfs = {}

# Fetch and store data for each hashtag
for hashtag in hashtags:
    trend_data = fetch_trend_data(hashtag)
    df = pd.DataFrame(trend_data)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df = df.set_index('time')
    dfs[hashtag] = df

    # Add random delay between 0.8 and 1.2 seconds
    delay = random.uniform(0.8, 1.2)
    time.sleep(delay)

# Combine dataframes
combined_df = pd.concat([dfs[hashtag]['value'] for hashtag in hashtags], axis=1)

# Set new column names
combined_df.columns = hashtags

# Save to CSV
current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"hashtag_trends_{current_time}.csv"
combined_df.to_csv(filename, index_label='time')
# Combine dataframes
combined_df = pd.concat([dfs[hashtag]['value'] for hashtag in hashtags], axis=1)

# Set new column names
combined_df.columns = hashtags

# Add average column
combined_df['average'] = combined_df.mean(axis=1)

# Save to CSV
current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
filename = f"hashtag_trends_{current_time}.csv"
combined_df.to_csv(filename, index_label='time')
