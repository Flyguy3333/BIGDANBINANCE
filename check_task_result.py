from celery.result import AsyncResult
from scripts.backtesting_pipeline import app

task_id = 'f7d3749c-324a-4f51-84f3-0331ae33531d'
result = AsyncResult(task_id, app=app)

if result.ready():
    print(f"Task Result: {result.result}")
else:
    print("Task is still processing.")
