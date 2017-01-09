import argparse


def parseArgs():
    parser = argparse.ArgumentParser(
        description='Allegro client command.')
    parser.add_argument('-l', '--login', help='Client login',
                        dest='login', default=None)
    # TODO: make some security
    parser.add_argument('-p', '--password', help='Client password',
                        dest='password', required=False)
    parser.add_argument('-s', '--server-ip', help='Server ID address',
                        dest='serverIp', default='127.0.0.1')
    return parser.parse_args()

if __name__ == "__main__":
    args = parseArgs()

    if args.login != None:
        print("Login as {}".format(args.login))
        raise NotImplementedError()
    else:
        raise NotImplementedError()
