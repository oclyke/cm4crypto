#!/usr/bin/env python3

import serial
import argparse
import time
import asyncio

async def main(args):
  print(args)


  start = time.time()
  async def heartbeet():
    while True:
      print('test alive. elapsed: ', time.time() - start)
      await asyncio.sleep(5)
  
  async def recorder():
    with serial.Serial(args.port, args.baud, timeout=0) as ser:
      print('connecting to port: ', ser.name)

      with open(args.out, 'wb') as f:
        print('starting test!')
        ser.write(b'00')
        while True:
          s = ser.read(1024)
          if len(s):
            f.write(s)
          await asyncio.sleep(0)

  # todo: better handling of exceptions
  G = asyncio.gather(recorder(), heartbeet())
  try:
    await G
  except KeyboardInterrupt:
    G.cancel()
  
  print('test ended')


# when run as the main script:
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Parallel Network Ping Utility')

  parser.add_argument('-p', dest='port', required=True, help='serial port to connect over')
  parser.add_argument('-b', dest='baud', default=115200, help='baud rate at which to connect')
  parser.add_argument('out', help='output file')

  args = parser.parse_args()
  asyncio.run(main(args))
