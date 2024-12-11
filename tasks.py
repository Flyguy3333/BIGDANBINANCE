from celery_app import app

@app.task
def example_task():
    return "Task executed!"
