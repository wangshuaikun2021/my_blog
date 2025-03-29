# Django 博客项目部署指南

## 1. 项目配置

### 1.1 创建生产环境配置文件
创建 `settings_prod.py`：
```python
from .settings import *

# 关闭调试模式
DEBUG = False

# 允许访问的主机
ALLOWED_HOSTS = ['*']  # 在生产环境中应该设置具体的域名

# 数据库配置
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blogdb',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}

# 静态文件配置
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# 安全设置
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1年
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 1.2 创建依赖管理文件
创建 `requirements.txt`：
```txt
Django==5.1.7
mysqlclient==2.2.4
gunicorn==21.2.0
whitenoise==6.6.0
python-dotenv==1.0.1
```

## 2. 部署方式

### 2.1 使用云服务器部署

#### 2.1.1 准备工作
1. 购买云服务器（阿里云、腾讯云等）
2. 安装必要的软件：
```bash
sudo apt update
sudo apt install python3 python3-pip nginx mysql-server
```

#### 2.1.2 配置 MySQL
```bash
sudo mysql_secure_installation
sudo mysql -u root -p
```

在 MySQL 中执行：
```sql
CREATE DATABASE blogdb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'bloguser'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON blogdb.* TO 'bloguser'@'localhost';
FLUSH PRIVILEGES;
```

#### 2.1.3 部署项目
1. 上传项目代码到服务器
2. 安装依赖：
```bash
pip install -r requirements.txt
```

3. 收集静态文件：
```bash
python manage.py collectstatic
```

4. 配置 Nginx（创建 `/etc/nginx/sites-available/blog`）：
```nginx
server {
    listen 80;
    server_name your_domain.com;  # 替换为你的域名

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/your/project/staticfiles;
    }
    
    location / {
        proxy_set_header Host $http_host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8000;
    }
}
```

5. 启用 Nginx 配置：
```bash
sudo ln -s /etc/nginx/sites-available/blog /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

6. 使用 gunicorn 启动应用：
```bash
gunicorn my_blog.wsgi:application
```

### 2.2 使用 Docker 部署

#### 2.2.1 创建 Dockerfile
```dockerfile
FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "my_blog.wsgi:application", "--bind", "0.0.0.0:8000"]
```

#### 2.2.2 创建 docker-compose.yml
```yaml
version: '3'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      - DJANGO_SETTINGS_MODULE=my_blog.settings_prod

  db:
    image: mysql:8.0
    environment:
      - MYSQL_DATABASE=blogdb
      - MYSQL_USER=root
      - MYSQL_PASSWORD=root
      - MYSQL_ROOT_PASSWORD=root
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

#### 2.2.3 启动服务
```bash
docker-compose up -d
```

## 3. 安全建议

1. 使用 HTTPS
   - 申请 SSL 证书（可以使用 Let's Encrypt）
   - 配置 Nginx 支持 HTTPS

2. 数据库安全
   - 定期备份数据库
   - 使用强密码
   - 限制数据库访问IP

3. 服务器安全
   - 配置防火墙
   - 定期更新系统和依赖包
   - 设置监控和日志

4. 应用安全
   - 使用环境变量管理敏感信息
   - 定期更新 Django 和依赖包
   - 配置 CSRF 和 XSS 防护

## 4. 性能优化

1. 静态文件
   - 使用 CDN 加速静态文件
   - 配置静态文件缓存

2. 数据库
   - 添加适当的索引
   - 优化查询性能

3. 缓存
   - 使用 Redis 或 Memcached 缓存
   - 配置 Django 缓存

## 5. 维护建议

1. 监控
   - 设置服务器监控
   - 配置应用日志
   - 设置告警机制

2. 备份
   - 定期备份数据库
   - 备份项目代码
   - 测试备份恢复

3. 更新
   - 定期更新依赖包
   - 测试更新后的功能
   - 制定回滚计划 