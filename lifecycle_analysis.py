from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd

from data_loader import DataLoader
from model import Issue,Event
import config

class LifecycleAnalysis:

    # all_release_dates = ['2018-02-28','2018-03-01','2018-03-05','2018-03-08','2018-03-14','2018-03-16','2018-04-04','2018-04-14','2018-05-7','2018-05-28','2018-06-28','2018-10-17','2019-12-12','2020-10-01','2022-08-30','2022-12-09','2023-02-27','2023-05-19','2023-08-20','2023-11-03','2024-02-25']

    def __init__(self):
        """
        Constructor
        """
        # Parameter is passed in via command line (--user)
        self.USER:str = config.get_parameter('user')
    
    def run(self):

        issues:List[Issue] = DataLoader().get_issues()

        bug_dates = [issue.created_date.date() for issue in issues if 'kind/bug' in issue.labels]
        date_counts = Counter(bug_dates)

        # Create DF with bnumber of bugs per date 
        df = pd.DataFrame(date_counts.items(), columns=['Date', 'Count'])
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        df_filtered_dates = df[(df['Date'].dt.year == 2022) | (df['Date'].dt.year == 2023) | (df['Date'].dt.year == 2024)]
        
        # Release dates in 2022-2024
        release_dates = ['2022-08-30','2022-12-09','2023-02-27','2023-05-19','2023-08-20','2023-11-03','2024-02-25']
        release_dates = pd.to_datetime(release_dates)

        self.plot_issues_by_date(release_dates,df_filtered_dates)
        
    def plot_issues_by_date(self, release_dates, df_filtered_dates):
        for release in release_dates:
            plt.axvline(x=release, color='red', linestyle='--', linewidth=1)

        plt.bar(df_filtered_dates['Date'], df_filtered_dates['Count'])
        plt.xlabel('Date')
        plt.ylabel('Number of Bugs')
        plt.title('Number of Bugs by Date')

        plt.show()