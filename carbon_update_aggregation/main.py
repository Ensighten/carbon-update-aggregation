#!/usr/bin/env python
import argparse

import carbon_update_aggregation


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--storage-dir',
                        required=True,
                        help='Path to the whisper storage dir.')
    parser.add_argument('--conf-dir',
                        required=True,
                        help='Path to the Carbon configuration dir, which should include storage-aggregation.conf.')
    args = parser.parse_args()
    carbon_update_aggregation.update_storage_aggregations(args.storage_dir, args.conf_dir)