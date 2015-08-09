from triager import app


@app.template_filter('canonize_alert')
def canonize_alert(value):
    """Bootstrap unreasonable alert names fix."""
    if value == 'error':
        return 'danger'
    elif value == 'message':
        return 'info'
    else:
        return value
