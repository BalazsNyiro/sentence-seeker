#!/usr/bin/env bash

# unfortunately the current solution in sentence_seeker.py:
# httpd = HTTPServer((Prg["ServerHost"], Prg["ServerPort"]), ui_html.SimpleHTTPRequestHandler)
# httpd.serve_forever()
# stop working after two/three days.

# until I debug the problem, this script restart the htttp server daily.

# start it from the root dir of sentence_seeker.py
# install daemon on your linux os to execute it
while true
do
  PID=$(ps aux | grep "sentence-seeker.py" | grep -v "grep" | awk '{print $2}')
  kill -9 $PID
  ./sentence-seeker.py --ui html &

  date
  echo "sleep..."
  sleep 86400
  echo "sleep end..."

done
