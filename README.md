# linkdump

post links, get atom feed.


## running it

- checkout this repo
- copy `docker-compose.prod.yaml.dist` to `docker-compose.prod.yaml`
- copy settings.prod.conf.dist` to `settings.prod.conf`
- add your config to these files 
- run `docker-compose -f docker-compose.prod.yml`
- get a shell on the service container (`docker-compose -f docker-compose.prod.yaml run service /bin/sh`) and setup the database: `flask db upgrade` 


## example nginx config
```
server {
        listen 80;
        listen [::]:80;

        error_log    /var/log/nginx/feeds.example.com.error.log;
        rewrite_log on;

        server_name feeds.example.com;

        include /etc/nginx/snippets/letsencrypt.conf;
        return 301 https://feeds.kwoh.de$request_uri;
}

server {

        rewrite_log on;

        listen 443 ssl;
        listen [::]:443 ssl;
        server_name feeds.example.com;

        ssl_certificate /etc/letsencrypt/live/feeds.example.com/fullchain.pem;
        ssl_certificate_key /etc/letsencrypt/live/feeds.example.com/privkey.pem;

        include /etc/nginx/snippets/letsencrypt.conf;

        location / {
                proxy_pass http://localhost:8080;
        }
}
```
