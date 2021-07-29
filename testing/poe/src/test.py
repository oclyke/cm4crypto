#!/usr/bin/env python3

import time
import json
import argparse
import math
from collections import namedtuple
import os
from korad import kel103

def main(args):

  # load configuration
  with open(args.config, 'r') as f:
    config_dict = json.loads(f.read())
  
  # convert config to tuple
  cfgtuple = namedtuple('config', config_dict)
  config = cfgtuple(**config_dict)
  
  # connect to device
  kel = kel103.kel103(args.local, args.remote, 18190)
  kel.checkDevice()
  kel.setOutput(False)

  # apply test configuration
  if config.mode == 'power':
    kel.setPower(config.value)
  elif config.mode == 'voltage':
    kel.setVolt(config.value)
  elif config.mode == 'current':
    kel.setCurrent(config.value)
  else:
    raise Exception('unknown test mode: ', config.mode)
  
  # generate logfile
  START_TIME = time.time()
  LOGFILE = os.path.join(args.outdir, config.name + '-' + str(math.floor(START_TIME)) + '.json')
  
  def log(entry, total_entries):
    if not len(entry):
      raise Exception('zero length entry!')

    with open(LOGFILE, 'br+') as f:
      f.seek( -7, 2) # _whence == 2 to indicate seeking from end of file
      
      if total_entries != 0:
        f.write(b',')
      f.write(b'\n    ')
      
      # write entry (nonzero len already ensured)
      f.write(entry)

      # write the new end of the file
      f.write(b'\n  ]\n}\n')

  def get_elapsed_seconds():
    return time.time() - START_TIME

  def get_sample():
    return {
      'headers': ('elapsed time', 'current', 'voltage', 'power'),
      'units': ('s', 'A', 'V', 'W'),
      'values': (get_elapsed_seconds(), kel.measureCurrent(), kel.measureVolt(), kel.measurePower()),
    }

  # initialize contents
  sample = get_sample()
  del sample['values']
  metadata = {
    'config': config_dict,
    'format': sample,
  }
  initial_content = {
    'meta': metadata,
    'entries': []
  }

  # prepare logfile
  with open(LOGFILE, 'bw') as f:
    f.write(bytearray(json.dumps(initial_content, indent=2), 'utf-8'))
    f.seek( -3 ,2)
    f.write(b'\n  ]\n}\n')

  # run the test
  stop_reason = None
  delay = 1/config.rate # seconds
  count = 0
  consecutive_sample_failures = 0
  kel.setOutput(True)
  while True:
    try:

      # get a sample retrying immediately on failure up to consecutive limit
      while True:
        try:
          sample = get_sample()
          break
        except Exception as e:
          print(e)
          consecutive_sample_failures += 1
          if consecutive_sample_failures >  CONSECUTIVE_SAMPLE_FAILURE_LIMIT:
            raise Exception('Too many consecutive sample failures')

      log(bytearray(json.dumps(sample['values']), 'utf-8'), count)
      count += 1
      time.sleep(delay)

    except KeyboardInterrupt:
      print('stopping test')
      break
    
    except Exception as e:
      stop_reason = e
      break

  print('shutting down')

  kel.setOutput(False)
  kel.endComm()

  print('test stopped')

  if stop_reason is not None:
    raise stop_reason

  print('test complete')



# when run as the main script:
if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Parallel Network Ping Utility')

  parser.add_argument('-l', dest='local', required=True, help='ip address of local (your pc) ethernet/wifi interface')
  parser.add_argument('-r', dest='remote', required=True, help='ip address of device (kel103) ethernet interface on network')
  parser.add_argument('-o', dest='outdir', default='.', help='output directory for test')
  parser.add_argument('-c', dest='config', default='$\{outdir\}/config.json', help='configuration file for the test')

  args = parser.parse_args()
  main(args)
