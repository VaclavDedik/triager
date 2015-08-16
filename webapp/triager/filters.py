from triager import app
from models import TrainStatus


@app.template_filter('canonize_alert')
def canonize_alert(value):
    """Bootstrap unreasonable alert names fix."""
    if value == 'error':
        return 'danger'
    elif value == 'message':
        return 'info'
    else:
        return value


@app.template_filter('readable_train_status')
def readable_train_status(value):
    if value == TrainStatus.FAILED:
        return "Failed"
    elif value == TrainStatus.NOT_TRAINED:
        return "Not trained"
    elif value == TrainStatus.TRAINED:
        return "Trained"
    elif value == TrainStatus.TRAINING:
        return "Training"
    else:
        return "/invalid value/"
