import argparse
import select
import socket
import sys

if __name__ != "__main__":
    sys.exit()

try:
    p = argparse.ArgumentParser(description="parameters for auditor")
    p.add_argument('-s', type=str, help='server address of the daemon', default='localhost')
    p.add_argument('-p', type=int, help='port number of the daemon', required=True)
    p.add_argument('-d', type=str, help='test packet defined inside a string', default='')
    p.add_argument('-m', type=bool, help='if true, send the packet in raw binary', default=True)
    p.add_argument('-w', type=bool, help='wait for data receivable', default=False)
    p.add_argument('-t', type=int, help='timeout for the data receivable', default=5)
    p.add_argument('-c', type=int, help='override buffer size for bytes readable', default=1024)
    args = p.parse_args()
except:
    print('required port parameter missing')
    sys.exit()

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((args.s, args.p))
        if len(args.d):
            s.sendall(args.d if not args.m else args.d.encode('utf-8'))
        if args.w:
            peek_for_read_event = select.select([s], [], [], args.t)
            if peek_for_read_event[0]:
                data = s.recv(args.c)
                print(f"data receivable: {data.decode('utf-8') if args.m else data}")
            else:
                print("no data receivable within timeout interval")
        s.close()
except Exception as e:
    print(f"error: {e}")
