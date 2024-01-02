"""
Starter code for sentiment_analysis.py
Your function headers must match this file exactly.
You should only have function definitions in this file.
No code should be outside of a function in this file.

Replace this comment with one containing your full name,
student number, UWO username, the date, and a short
description of what this file does/contains.

Each function should have at least one comment documenting
what it does and the arguments it takes.
"""


def read_keywords(keyword_file_name):
    try:
        with open(keyword_file_name, 'r') as file:
            keyword_dict = {}

            for line in file:
                # Split the line into keyword and score using tab as the delimiter
                keyword, score_str = line.strip().split('\t', 1)

                # Make the score be an integer
                score = int(score_str)

                # Store the keyword and score in the empty dictionary
                # Replace multiple spaces in the keyword with a single space
                keyword = ' '.join(keyword.split())

                keyword_dict[keyword] = score

            return keyword_dict
    except IOError:
        print(f"Could not open file {keyword_file_name}!")
        return {}


# Call the function
#read_and_print_keywords()
    # Add your code here
	# Should return a dict of keywords.


def clean_tweet_text(tweet_text):
    """
    Clean the tweet text by removing non-English letters and converting to lowercase.

    Parameters:
    - tweet_text (str): The input tweet text.

    Returns:
    - str: Cleaned tweet text with only English letters and spaces, converted to lowercase.
    """
    # Use a generator expression to iterate through each character in tweet_text
    cleaned_text = ''.join(char.lower() if char.isalpha() or char.isspace() else '' for char in tweet_text)

    # Remove extra spaces by splitting the cleaned_text and joining with a single space
    cleaned_text = ' '.join(cleaned_text.split())

    # Return the cleaned text
    return cleaned_text


# Add your code here
	# Should return a string with the clean tweet text.


def calc_sentiment(tweet_text, keyword_dict):
    # Split the tweet text into individual words
    words = tweet_text.split()

    # Initialize sentiment score
    sentiment_score = 0

    # Calculate sentiment score based on keywords
    for word in words:
        # Check if the word is in the keyword dictionary
        if word in keyword_dict:
            sentiment_score += keyword_dict[word]

    return sentiment_score
# Should return an integer value.


def classify(score):
    if score > 0:
        return "positive"
    elif score < 0:
        return "negative"
    else:
        return "neutral"
# Should return a string.


def read_tweets(tweet_file_name):
    try:
        # Open the file in read mode
        with open(tweet_file_name, 'r') as file:
            # Initialize an empty list to store dictionaries
            tweets_list = []

            # Iterate through each line in the file
            for line in file:
                # Split the line into fields using comma as the delimiter
                fields = line.strip().split(',')

                # Create a dictionary with keys from the table in Section 3.1.2
                tweet_dict = {
                    'date': fields[0],
                    'text': clean_tweet_text(fields[1]),
                    'user': fields[2],
                    'retweet': int(fields[3]),
                    'favorite': int(fields[4]),
                    'lang': fields[5],
                    'country': fields[6] if fields[6] != 'NULL' else 'NULL',
                    'state': fields[7] if fields[7] != 'NULL' else 'NULL',
                    'city': fields[8] if fields[8] != 'NULL' else 'NULL',
                    'lat': float(fields[9]) if fields[9] != 'NULL' else 'NULL',
                    'lon': float(fields[10]) if fields[10] != 'NULL' else 'NULL'
                }

                # Append the dictionary to the list
                tweets_list.append(tweet_dict)

            # Return the list of dictionaries
            return tweets_list
    except IOError:
        # Handle IOError (file not found)
        print(f"Could not open file {tweet_file_name}!")
        return []
# Add your code here
# Should return a list with a dictionary for each tweet.


def make_report(tweet_list, keyword_dict):
    report = {
        'avg_favorite': 'NAN',
        'avg_retweet': 'NAN',
        'avg_sentiment': 'NAN',
        'num_favorite': 0,
        'num_negative': 0,
        'num_neutral': 0,
        'num_positive': 0,
        'num_retweet': 0,
        'num_tweets': 0,
        'top_five': ''
    }

    if not tweet_list:
        return report

    sentiment_sum = 0
    favorite_sum = 0
    retweet_sum = 0
    countries_sentiment = {}

    for tweet in tweet_list:
        num_favorite = tweet['favorite']
        num_retweet = tweet['retweet']
        sentiment_score = calc_sentiment(tweet['text'], keyword_dict)

        sentiment_sum += sentiment_score
        report['num_tweets'] += 1

        if num_favorite > 0:
            favorite_sum += sentiment_score
            report['num_favorite'] += 1

        if num_retweet > 0:
            retweet_sum += sentiment_score
            report['num_retweet'] += 1

        if sentiment_score < 0:
            report['num_negative'] += 1
        elif sentiment_score > 0:
            report['num_positive'] += 1
        else:
            report['num_neutral'] += 1

        country = tweet['country']
        if country != 'NULL':
            if country not in countries_sentiment:
                countries_sentiment[country] = [sentiment_score, 1]
            else:
                countries_sentiment[country][0] += sentiment_score
                countries_sentiment[country][1] += 1

    if report['num_favorite'] > 0:
        report['avg_favorite'] = round(favorite_sum / report['num_favorite'], 2)

    if report['num_retweet'] > 0:
        report['avg_retweet'] = round(retweet_sum / report['num_retweet'], 2)

    if report['num_tweets'] > 0:
        report['avg_sentiment'] = round(sentiment_sum / report['num_tweets'], 2)

    sorted_countries = sorted(countries_sentiment.items(), key=lambda x: x[1][0] / x[1][1], reverse=True)
    top_five_countries = [country[0] for country in sorted_countries[:5]]
    report['top_five'] = ', '.join(top_five_countries)

    return report

# Should return a dictionary containing the report values.

def write_report(report, output_file):
    try:
        with open(output_file, 'w') as file:
            file.write("Average sentiment of all tweets: {:.2f}\n".format(report['avg_sentiment']))  # Corrected line
            file.write("Total Number of Tweets: {}\n".format(report['num_tweets']))
            file.write("Number of Positive Tweets: {}\n".format(report['num_positive']))
            file.write("Number of Negative Tweets: {}\n".format(report['num_negative']))
            file.write("Number of Neutral Tweets: {}\n".format(report['num_neutral']))
            file.write("Number of Favorited Tweets: {}\n".format(report['num_favorite']))
            file.write("Average Favorite Sentiment: {:.2f}\n".format(report['avg_favorite']))
            file.write("Number of Retweeted Tweets: {}\n".format(report['num_retweet']))
            file.write("Average Retweet Sentiment: {:.2f}\n".format(report['avg_retweet']))
            file.write("Top Five Countries: {}\n".format(report['top_five']))

        print("Wrote report to {}".format(output_file))
    except IOError:
        print("Could not open file {}".format(output_file))





# Should write the report to the output_file.
