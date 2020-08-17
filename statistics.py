import pandas as pd


class DataSet(object):
    def __init__(self, data: dict):
        self.columns = list(data.keys())
        self.data = pd.DataFrame(data=data)
        self.number_lines = len(self.get_column_data(self.columns[0]))

    def __str__(self):
        return str(self.data.head(n=self.number_lines))

    def get_column_data(self, column: str):
        return self.data[column]

    def get_row_data(self):
        pass

    def get_column_sum(self, column: str):
        column_data = self.get_column_data(column=column)
        s = 0
        for row in column_data:
            if (not isinstance(row, int)) or (not isinstance(row, float)):
                row = float(row)
            s += row
        return s

    def get_column_mean(self, column: str):
        return self.get_column_sum(column=column) / self.number_lines

    def get_deviations(self, column: str):
        column_data = self.get_column_data(column=column)
        mean = self.get_column_mean(column=column)
        deviations = []
        for row in column_data:
            if (not isinstance(row, int)) or (not isinstance(row, float)):
                row = float(row)
            deviations.append(row - mean)
        return deviations

    def apply_function_to_column(self, column: str, f):
        pass

    def plot_comparative_graph(self):
        pass

    def get_column_population_std(self, column: str):
        deviations = self.get_deviations(column=column)
        square_deviations = [d ** 2 for d in deviations]
        deviations_mean = sum(square_deviations) / len(deviations)
        return deviations_mean ** (1 / 2)

    def get_column_sample_std(self, column: str):
        deviations = self.get_deviations(column=column)
        square_deviations = [d ** 2 for d in deviations]
        deviations_mean = sum(square_deviations) / (len(deviations) - 1)
        return deviations_mean ** (1 / 2)

    def get_column_population_var(self, column: str):
        return self.get_column_population_std(column=column) ** 2

    def get_column_sample_var(self, column: str):
        return self.get_column_sample_std(column=column) ** 2

    def get_sample_std_mean_deviation(self, column: str):
        return self.get_column_sample_std(column=column) / (self.number_lines ** (1/2))

    def get_population_std_mean_deviation(self, column: str):
        return self.get_column_population_std(column=column) / (self.number_lines ** (1 / 2))
