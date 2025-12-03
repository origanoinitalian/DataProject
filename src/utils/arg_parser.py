import argparse

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dashboard start")
    parser.add_argument(
            '--fetch-data',
            action='store_true',
            help='Download datas from the USGS API before starting the dashboard.'
        )
    return parser.parse_args()
