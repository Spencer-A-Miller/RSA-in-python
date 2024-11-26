import os
import pathlib
import random
import pandas as pd
import pickle
import gzip

class FirstPrimesManager:
    def __init__(self, output_dir: str | pathlib.Path | None = r".\cached-first-primes"):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def import_csv(self, csv_path: str | pathlib.Path):
        self.df = pd.read_csv(csv_path, header=None)
        print("DataFrame imported successfully.")

    def cache_primes(self, file_name: str | pathlib.Path):
        if not hasattr(self, 'df'):
            raise ValueError("DataFrame not loaded. Please import a CSV first.")
        # Convert DataFrame to list of ints
        prime_list = self.df[0].tolist()
        cache_path = os.path.join(self.output_dir, f"{file_name}.pkl.gz")
        with gzip.open(cache_path, 'wb') as f:
            pickle.dump(prime_list, f, protocol=pickle.HIGHEST_PROTOCOL) 
            print(f"Prime list cached successfully at {cache_path}.")

    def load_cache(self, file_name: str | pathlib.Path) -> list: 
        cache_path = os.path.join(self.output_dir, f"{file_name}.pkl.gz")
        if not os.path.exists(cache_path): 
            raise FileNotFoundError(f"No cache found at {cache_path}.")
        with gzip.open(cache_path, 'rb') as f:
            prime_list = pickle.load(f)
            print(f"Prime list loaded successfully from {cache_path}.")
            return prime_list
