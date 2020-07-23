"""Script to split the dataset in shards."""

import os
import simplejson as json
import numpy as np
import pandas as pd


BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def shards(data, n_shard=10):
	for shard in np.array_split(data, n_shard):
		shard = [{"model": "api.application", 'pk': x, 'fields': y}
		 		 for x, y in shard.T.to_dict().items()]
		yield shard


def main(data):
	total = len(list(data.index))
	for i, shard in enumerate(shards(data)):
		f = f'shard_{i}.json'
		with open(os.path.join(BASE_PATH, 'models', f), 'w') as f:
			f.write(json.dumps(shard, ignore_nan=True))


if __name__ == '__main__':
	data = pd.read_csv(os.path.join(BASE_PATH, 'models', 'features_final.csv'))
	data.drop(columns='TARGET', inplace=True)
	data.columns = [x.lower() for x in data.columns]
	data.sort_values('sk_id_curr', inplace=True)
	main(data)
