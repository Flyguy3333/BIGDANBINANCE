from celery import Celery

app = Celery(
    'backtesting_pipeline',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/0'
)

@app.task
def example_task():
    return "Task executed!"