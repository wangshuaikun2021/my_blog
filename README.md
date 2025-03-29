# Django 博客系统

一个使用 Django 开发的个人博客系统，支持用户注册、登录、发布博客、评论等功能。

## 功能特点

- 用户认证（注册、登录、退出）
- 博客发布（支持富文本编辑）
- 博客评论
- 博客搜索
- 分类管理

## 技术栈

- Python 3.11
- Django 5.1.7
- MySQL 8.0
- Bootstrap 5
- WangEditor（富文本编辑器）

## 安装说明

1. 克隆项目
```bash
git clone https://github.com/wangshuaikun2021/my_blog.git
cd my_blog
```

2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. 安装依赖
```bash
pip install -r requirements.txt
```

4. 配置数据库
- 创建 MySQL 数据库
- 修改 `settings.py` 中的数据库配置

5. 运行迁移
```bash
python manage.py migrate
```

6. 启动开发服务器
```bash
python manage.py runserver
```

## 部署说明

详细的部署说明请参考 [deploy_guide.md](deploy_guide.md)

## 作者

- 王帅坤
- 北京科技大学

## 许可证

MIT License 