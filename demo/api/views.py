"""
业务 API：三个接口分别演示 Counter / Gauge / Histogram 的埋点方式。
"""
import random
import time

from ninja import Router

from demo.metrics import ACTIVE_USERS, ORDER_DURATION, ORDERS_TOTAL

router = Router()


@router.post("/order")
def create_order(request, type: str = "normal"):
    """下单接口：演示 Counter 埋点，业务动作发生就 inc()。"""
    # 模拟下单本身的耗时，同时被直方图观测
    with ORDER_DURATION.time():
        time.sleep(random.uniform(0.005, 0.08))
        # 真实项目会在这里写数据库/发消息
        ORDERS_TOTAL.labels(type=type).inc()   # <<< Counter：按 type 维度 +1

    return {"ok": True, "type": type}


@router.get("/stats")
def stats(request, delta: int = 1):
    """模拟“当前在线用户”波动：演示 Gauge 的 inc/dec/set。"""
    ACTIVE_USERS.inc(random.randint(0, 10) * delta)    # 随机上下浮动
    if ACTIVE_USERS._value.get() < 0:                  # 不允许负数
        ACTIVE_USERS.set(0)
    return {"active_users": ACTIVE_USERS._value.get()}


@router.get("/slow")
def slow(request, ms: int = 300):
    """手动制造慢请求：给 Grafana 面板和告警规则提供异常数据源。"""
    time.sleep(ms / 1000)
    return {"slept_ms": ms}
