import numpy as np


from data_loader import DataLoader

# TODO: Create a pandas dataframe to store all of this data
label_popularity = None  # label:str -> popularity_score:int
issues_map = None  # label:str -> issues:List
popularity_scores = None  # issue:Issue -> popularity_score:int

class DataProcess:
    """
    TODO: Description
    """
    
    def process_data(self):
        global popularity_scores, issues_map, label_popularity
        if popularity_scores is not None:
            return

        issues = DataLoader().get_issues()
        issues_map = {}
        density_scores = {}

        for issue in issues:
            # Append issues_map
            for label in issue.labels:
                issues_map.setdefault(label, []).append(issue)

            # Calculate density
            event_dates = [event.event_date for event in issue.events]
            if len(event_dates) > 1:
                first_event_date = min(event_dates)
                last_event_date = max(event_dates)
                time_span = (last_event_date - first_event_date).total_seconds()

                if time_span > 0:
                    # Events per second
                    density_scores[issue] = len(event_dates) / time_span
                else:
                    # Occurs when the only events pertain to the issue being created
                    density_scores[issue] = len(event_dates)
            else:
                # No density for issues with 0 or 1 events
                density_scores[issue] = 0

        # Calculate popularity (normalize density scores)
        min_density = min(density_scores.values())
        max_density = max(density_scores.values())
        popularity_scores = {}
        for issue, score in density_scores.items():
            popularity_scores[issue] = (score - min_density) / (max_density - min_density)
        
        label_popularity = {}
        labels_count = {}
        for issue, score in popularity_scores.items():
            for label in issue.labels:
                label_popularity.setdefault(label, 0)
                labels_count.setdefault(label, 0)
                label_popularity[label] += score
                labels_count[label] += 1
        
        for label, count in labels_count.items():
            label_popularity[label] = label_popularity[label] / count
        
        # Temporary plot for viewing
        import matplotlib
        matplotlib.use('Qt5Agg')  # Use the TkAgg backend for interactive plots
        import matplotlib.pyplot as plt

        labels = list(label_popularity.keys())
        densities = list(label_popularity.values())

        plt.figure(figsize=(20, 6))
        plt.bar(labels, densities, color='skyblue')

        plt.title("Average Popularity by Label")
        plt.xlabel("Label")
        plt.ylabel("Average Popularity")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    # Run for testing
    DataProcess().process_data()