#!/usr/bin/env python3
"""
Created by Jianshu Zhao (jansuechao@gmail.com)
This script uses FastANI output to generate a PHYLIP distance matrix suitable for tree/headmap et.al.
"""

import argparse
import sys


def get_arguments():
    parser = argparse.ArgumentParser(description='Distance matrix from pairwise identities')

    parser.add_argument('identities', type=str,
                        help='FastANI output file (or similarly formatted file with three '
                             'whitespace-delimited columns of assembly 1, assembly 2, percent '
                             'identity')

    parser.add_argument('--max_dist', type=float, required=False, default=1.0,
                        help='Maximum allowed genomic distance')

    args = parser.parse_args()
    return args


def main():
    args = get_arguments()

    clusters = set()
    distances = {}

    print('', file=sys.stderr)
    print('Convert FastANI distances to PHYLIP matrix', file=sys.stderr)
    print('------------------------------------------------', file=sys.stderr)

    fastani_output_filename = args.identities

    with open(fastani_output_filename, 'rt') as fastani_output:
        for line in fastani_output:
            parts = line.strip().split()
            cluster_1 = parts[0]
            cluster_2 = parts[1]
            ani = float(parts[2])
            if cluster_1 == cluster_2:
                distance = 1.0
            else:
                distance = ani / 100.0
            clusters.add(cluster_1)
            clusters.add(cluster_2)
            add_distance(distances, cluster_1, cluster_2, distance)
            add_distance(distances, cluster_2, cluster_1, distance)
    print('Found {} clusters and {} distances'.format(len(clusters), len(distances)),
          file=sys.stderr)

    print(len(clusters))
    clusters = sorted(clusters)
    for i in clusters:
        print(i, end='')
        for j in clusters:
            print('\t', end='')
            try:
                distance = distances[(i, j)]
            except KeyError:
                distance = args.max_dist
            if distance > args.max_dist:
                distance = args.max_dist
            print('%.6f' % distance, end='')
        print()
    print('', file=sys.stderr)


def add_distance(distances, cluster_1, cluster_2, distance):
    # If this is the first time we've seen this pair, then we just add it to the dictionary.
    if (cluster_1, cluster_2) not in distances:
        distances[(cluster_1, cluster_2)] = distance
    # If we've seen this pair before (the other way around), then we make sure the distances are
    # close (sanity check) and then save the mean distance.
    else:
        assert abs(distance - distances[(cluster_1, cluster_2)]) < 0.1
        distances[(cluster_1, cluster_2)] = (distances[(cluster_1, cluster_2)] + distance) / 2.0


if __name__ == '__main__':
    main()
