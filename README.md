### 潜在问题
- 暂时使用debug=true否则无法加载静态文件
- 使用以下代码会定期卡死
    ```bash
    gunicorn --bind 127.0.0.1:8000 clipboard.wsgi:application
    ```
  改为这样就不会卡死
    ```bash
    gunicorn --bind 127.0.0.1:8000 clipboard.wsgi:application --log-level=debug --workers=3 --threads=3 --worker-connections=1000
    ```