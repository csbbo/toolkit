#! /bin/bash

echo -e "\033[31m - run databases migrate \033[0m"
while :; do
    if python3 manage.py migrate; then
        break
    fi
    sleep 1
done

echo -e "\033[31m - run sync stock scheduler server \033[0m"
python3 manage.py sync_stock_scheduler 2>&1 &

# todo: 切换成toolkit
cat <<-'EOF'
   ____  _          ____
  / ___|| | ___   _| __ )  _____  __
  \___ \| |/ / | | |  _ \ / _ \ \/ /
   ___) |   <| |_| | |_) | (_) >  <
  |____/|_|\_\\__, |____/ \___/_/\_\
              |___/
Server running...
EOF

gunicorn toolkit.wsgi:application -c gunicorn_conf.py
