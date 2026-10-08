"""
自定义业务指标
"""
from prometheus_client import Counter, Gauge, Histogram

#  Counter（只增计数器）
ORDERS_TOTAL = Counter(
    "demo_orders_total",           # 指标名，命名规范：<namespace>_<name>_total
    "Total number of orders created",
    labelnames=("type",),          # 维度：订单类型
)

# Gauge（瞬时值）
# 当前在线用户数
ACTIVE_USERS = Gauge(
    "demo_active_users",
    "Current number of simulated active users",
)

#  Histogram（分桶直方图）
# 业务耗时直方图。buckets 按业务经验设计：下单接口正常几十毫秒、慢到 2 秒就该告警。
ORDER_DURATION = Histogram(
    "demo_order_duration_seconds",
    "Order creation duration in seconds",
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.0, 3.0),
)

#  Summary 的分位数无法跨实例聚合，不做演示，需要分位数还是推荐使用 Histogram + histogram_quantile()
