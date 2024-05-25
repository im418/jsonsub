# Building
```ssh
docker-compose up -d --no-deps --build game_changer
```

# Nginx
```
        location /ghJGH876JGJG5opwdnmczhkjsa7T32o/ {
                proxy_pass http://127.0.0.1:20501/ghJGH876JGJG5opwdnmczhkjsa7T32/;
                proxy_read_timeout 1800;
                proxy_connect_timeout 1800;
                proxy_send_timeout 1800;
                send_timeout 1800;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header Connection "";
                proxy_http_version 1.1;
        }


        location /ghJGH876JGJG5opwdnmczhkjsa7T32/ {
                proxy_pass http://127.0.0.1:5000/full/http/127.0.0.1:20501/ghJGH876JGJG5opwdnmczhkjsa7T32/;
                proxy_read_timeout 1800;
                proxy_connect_timeout 1800;
                proxy_send_timeout 1800;
                send_timeout 1800;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
                proxy_set_header X-Forwarded-Proto $scheme;
                proxy_set_header Connection "";
                proxy_http_version 1.1;
        }
```
