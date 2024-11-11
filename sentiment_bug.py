import json
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sentiment_scores import SentimentScores

class SentimentAnalysisYearly:
    def __init__(self, json_file):
        self.json_file = json_file
        self.data = None
        self.df = None
        self.sentimentScores = SentimentScores()

    def load_data(self):
        # Load the JSON data
        with open(self.json_file, 'r') as f:
            self.data = json.load(f)

    # Function to categorize labels
    def categorize_labels(self, labels):
        bugs = ['bug', 'kind/bug', 'issue']
        for label in labels:
            if any(bug in label.lower() for bug in bugs):
                return 'Bug'
        return 'Other'

    def process_issues(self):
        # Extract relevant data into a list, including created_date and sentiment score
        issues_list = []
        for issue in self.data:
            labels = issue.get('labels', [])
            created_date = issue.get('created_date', 'Unknown')
            issueNumber = issue.get('number')
            category = self.categorize_labels(labels)
            
            # Append the data for Bugs only
            if category == "Bug":
                issues_list.append({
                    'CreatedDate': created_date,
                    'SentimentScore': self.sentimentScores.get_sentiment_score(issueNumber)
                })

        # Create a DataFrame from the list
        self.df = pd.DataFrame(issues_list)

    def prepare_data(self):
        # Convert the CreatedDate to datetime, ignoring invalid formats
        self.df['CreatedDate'] = pd.to_datetime(self.df['CreatedDate'], errors='coerce')

        # Filter out rows with NaT (invalid dates)
        self.df = self.df.dropna(subset=['CreatedDate'])

        # Extract the year from CreatedDate and add it as a new column
        self.df['Year'] = self.df['CreatedDate'].dt.year  # Extract the year

    def plot_3d_sentiment_vs_bugs(self):
        # Group by Year and calculate the number of bugs and average sentiment score
        yearly_bug_count = self.df.groupby('Year').size().reset_index(name='NumberOfBugs')
        yearly_avg_sentiment = self.df.groupby('Year')['SentimentScore'].mean().reset_index()

        # Merge the two dataframes on Year
        yearly_data = pd.merge(yearly_bug_count, yearly_avg_sentiment, on='Year')

        # Create a 3D plot
        fig = plt.figure(figsize=(10, 7))
        ax = fig.add_subplot(111, projection='3d')

        # Scatter plot: X = Year, Y = Number of Bugs, Z = Average Sentiment Score
        ax.scatter(yearly_data['Year'], yearly_data['NumberOfBugs'], yearly_data['SentimentScore'], color='blue')

        # Set labels for axes
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Bugs')
        ax.set_zlabel('Average Sentiment Score')

        # Customize and display the plot
        plt.title('3D Plot: Number of Bugs vs Average Sentiment Score per Year')
        plt.tight_layout()
        plt.show()

    def run(self):
        self.load_data()
        self.process_issues()
        self.prepare_data()
        self.plot_3d_sentiment_vs_bugs()

# Usage
if __name__ == "__main__":
    sentiment_analysis_yearly = SentimentAnalysisYearly('poetry_issues_all.json')
    sentiment_analysis_yearly.run()
