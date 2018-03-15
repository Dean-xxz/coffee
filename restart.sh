kill $(netstat -tlnp|grep 5555 |awk  '{print $7}'|awk -F '/' '{print $1}')
/home/coffee/py35env/bin/gunicorn  --error-logfile /tmp/coffee_gunicorn.log  -w 4 --bind 0.0.0.0:5555 coffee.wsgi:application -D
