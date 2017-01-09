import argparse


def parseArgs():
    parser = argparse.ArgumentParser(
        description='Allegro server command.')
    parser.add_argument('-p', '--path', help='Database root path',
                        dest='databasePath', required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()

    if args.login != None:
        print("Login as {}".format(args.login))
        raise NotImplementedError()
    else:
        raise NotImplementedError()
