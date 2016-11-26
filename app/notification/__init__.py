def notify(rule=None, notifiers=None, filters=None, success=None,
           failure=None):
    # do nothing if there is no rule or notifier - fail silently
    # success and failure callbacks can be omitted though
    if rule is None or notifiers is None:
        return

    if filters is None:
        filters = []

    if success is None:
        success = []

    # we accept either a function or a list of functions as notifiers, filters
    # and filters. Hence, we need to wrap single function in a list
    if callable(notifiers):
        notifiers = [notifiers]

    if callable(filters):
        filters = [filters]

    if callable(success):
        success = [success]

    # main loop
    results = []
    for item in rule():
        if all(map(lambda x: x(item), filters)):
            result = None
            for notifier in notifiers:
                try:
                    result = notifier(item, result)
                    for success_cb in success:
                        result = success_cb(item, result)
                    results.append(result)
                except Exception as e:
                    if callable(failure):
                        failure(item, e)

    return results
