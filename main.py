"""
Starter code for main.py

This file should take input from the user and call the
functions in sentiment_analysis.py

Replace this comment with one containing your full name,
student number, UWO username, the date, and a short
description of what this file does/contains.

You can NOT move the functions from sentiment_analysis.py
into this file. They must be defined in sentiment_analysis.py
"""

# Import the sentiment_analysis module
from sentiment_analysis import read_keywords, read_tweets, make_report, write_report

def main():
    try:
        # Input keyword filename
        keyword_filename = input("Input keyword filename (.tsv file): ")
        if not keyword_filename.endswith('.tsv'):
            raise TypeError("Keyword filename must have a tsv file extension!")

        # Input tweet filename
        tweet_filename = input("Input tweet filename (.csv file): ")
        if not tweet_filename.endswith('.csv'):
            raise TypeError("Tweet filename must have a csv file extension!")

        # Input report filename
        report_filename = input("Input filename to output report in (.txt file): ")
        if not report_filename.endswith('.txt'):
            raise TypeError("Report filename must have a txt file extension!")

        # Read keywords and tweets
        keyword_dict = read_keywords(keyword_filename)
        tweet_list = read_tweets(tweet_filename)

        if not keyword_dict or not tweet_list:
            raise TypeError("Tweet list or keyword dictionary is empty!")

        # Make report
        report = make_report(tweet_list, keyword_dict)

        # Write report
        write_report(report, report_filename)

    except TypeError as exception:
        print(f"Error: {exception}")

# Run the main function if this script is run directly
if __name__ == "__main__":
    main()
