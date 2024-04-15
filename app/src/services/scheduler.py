from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler(
    # jobstores={
    #     "default": RedisJobStore(db=2, host="127.0.0.1", port=6379, password="test")
    # }
)


@scheduler.scheduled_job("cron", second=0)
async def cron_task_test():
    print("task is run...")
