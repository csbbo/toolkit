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
 _____           _ _  ___ _
|_   _|__   ___ | | |/ (_) |_
  | |/ _ \ / _ \| | ' /| | __|
  | | (_) | (_) | | . \| | |_
  |_|\___/ \___/|_|_|\_\_|\__|
Server running...
EOF

gunicorn toolkit.wsgi:application -c gunicorn_conf.py
