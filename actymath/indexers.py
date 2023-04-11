import numpy as np
from pandas.api.indexers import BaseIndexer


class SliceToEndIndexer(BaseIndexer):
    """
    Pandas custom indexer.

    This will return a slice from current index to the end.

    Usage example:
    indexer = SliceToEnd()
    dataframe['column'].rolling(indexer).sum()
    """

    def get_window_bounds(self, num_values, min_periods, center, closed, step):
        start = np.arange(num_values, dtype=np.int64)
        end = np.full(num_values, num_values, dtype=np.int64)
        return start, end


class SliceNIndexer(BaseIndexer):
    """
    Pandas custom indexer.

    This will return a slice from current index to include N further rows.

    Params:
    - n - a list or series of N values
    - offset - default=0 to add to the indices

    Usage example:
    indexer = SliceToN(n=df['window_size_column'])
    dataframe['column'].rolling(indexer).sum()
    """

    def get_window_bounds(self, num_values, min_periods, center, closed):
        try:
            offset = self.offset
        except:
            offset = 0
        start = np.empty(num_values, dtype=np.int64)
        end = np.empty(num_values, dtype=np.int64)
        for i in range(num_values):
            start[i] = i + offset
            if np.isnan(self.n[i]):
                end[i] = i + offset
            else:
                end[i] = i + offset + int(self.n[i])
        return start, end
