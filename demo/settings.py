from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "demo-only-not-for-production"
DEBUG = False
ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.staticfiles",
    # django-prometheus 提供了
    #   1) /metrics 端点（django_prometheus.urls）
    #   2) Django 内置指标自动采集（迁移/数据库连接）
    #   3) 两个中间件（HTTP 请求指标）
    #   4) 让你自定义业务指标的 API（export_django_metrics / 直接用 prometheus_client）
    "django_prometheus",
    "ninja",
    "demo",
]

MIDDLEWARE = [
    # PrometheusBeforeMiddleware 必须放在第一个， 它在请求进入 Django 前记录时间戳/在进程内计数；
    "django_prometheus.middleware.PrometheusBeforeMiddleware",
    "django.middleware.common.CommonMiddleware",
    # PrometheusAfterMiddleware 必须放在最后一个——请求走完全部中间件和视图后，才能算出准确的耗时并完结直方图观测。
    "django_prometheus.middleware.PrometheusAfterMiddleware",
]

ROOT_URLCONF = "demo.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    },
]

WSGI_APPLICATION = "demo.wsgi.application"

# demo环境用 SQLite 文件库；django-prometheus 会自动暴露 django_migrations_applied_total 等数据库状态指标。
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# 不做静态文件收集
STATIC_URL = "static/"

# 关掉迁移自动导出
PROMETHEUS_EXPORT_MIGRATIONS = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

USE_TZ = True

