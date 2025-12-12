import argparse

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dashboard start")
    parser.add_argument(
            '--fetch-data',
            action='store_true',
            help='Download datas from the USGS API before starting the dashboard.',
        )
    
    parser.add_argument(
            '--start-time',
            type=str,
            default=None,
            help='Start date in YYYY-MM-DD format.',
        )

    parser.add_argument(
            '--end-time',
            type=str,
            default=None,
            help='End date in YYYY-MM-DD format.',
        )
    return parser.parse_args()
