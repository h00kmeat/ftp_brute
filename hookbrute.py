import ftplib
import argparse
import asyncio


def file_read(path):
    with open(path, "r") as f:
        obj = f.readlines()
        for i in range(len(obj)):
            obj[i] = obj[i].rstrip()
        return obj


async def connect_to_ftp(ip, username, password, filter):

    try:
        with ftplib.FTP(ip, username, password) as ftp:
            print(f"Connected to FTP server {ip} with username {username}\n")
            print("/:")
            ftp.dir()
    except ftplib.all_errors as e:
        if not filter:
            print(f"FTP connection error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="hkFTP", description="FTP Connection Tool")
    parser.add_argument("target", metavar="IP", type=str, help="Target IP address")
    parser.add_argument(
        "-u", "--username", help="Username for login (optional)", default="anonymous"
    )
    parser.add_argument(
        "-p", "--password", help="Password for login (optional)", default="anonymous"
    )
    parser.add_argument(
        "-U",
        "--usernames",
        help="Path to a file containing usernames for brute-forcing",
    )
    parser.add_argument(
        "-P",
        "--passwords",
        help="Path to a file containing passwords for brute-forcing",
    )
    parser.add_argument(
        "-f",
        "--filter",
        action="store_const",
        const=True,
        help="Filtering output on code Error.",
    )

    args = parser.parse_args()
    usernames, passwords = [], []
    filter = args.filter

    if args.usernames:
        try:
            usernames = file_read(args.usernames)
        except FileNotFoundError:
            print(f"Error: Username file '{args.usernames}' not found.")
            exit(1)
    else:
        usernames = [args.username] if args.username else ["anonymous"]
    if args.passwords:
        try:
            passwords = file_read(args.passwords)

        except FileNotFoundError:
            print(f"Error: Username file '{args.passwords}' not found.")
            exit(1)
    else:
        passwords = [args.password] if args.password else ["anonymous"]
    for username in usernames:
        print(f"Trying username: {username}")
        for password in passwords:
            print(f"Trying password: {password}")
            asyncio.run(connect_to_ftp(args.target, username, password, filter))
