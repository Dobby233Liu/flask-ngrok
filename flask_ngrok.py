from google.colab.output import eval_js

def start_proxy(port):
    address = ""
    try:
        address = eval_js("google.colab.kernel.proxyPort(%s)" % str(port))
    except:
        print(" * Failed to get address to proxy URL")
        return
    if address == "":
        print(" * Failed to get address to proxy URL")
        return
    print(f" * Port exposed to address {address}")

def hook_proxy_helper(app, *args, **kwargs):
    """
    The provided Flask app will be exposed through Google Cloud when run.
    The address to the app will then be printed to stdout.
    :param app: a Flask application object
    :return: None
    """

    old_run = app.run

    def new_run(*args, **kwargs):
        import threading
        port = kwargs.get('port', 5000)
        thread = threading.Timer(1, start_proxy, args=(port,))
        thread.setDaemon(True)
        thread.start()
        old_run(*args, **kwargs)
    app.run = new_run
