import pandas as pd

class PerformanceResultsLogger:
    def __init__(self):
        self.results = []
        self.test_counter = 1

    def log_result(self, result_dict):
        result_with_id = {
            'Test Number': self.test_counter,
            **result_dict
        }
        self.results.append(result_with_id)
        self.test_counter += 1

    def get_dataframe(self):
        return pd.DataFrame(self.results)

    def save_to_csv(self, filepath='performance_results.csv'):
        results_df = self.get_dataframe()
        results_df.to_csv(filepath, index=False)
        print(f'Results saved to {filepath}')
