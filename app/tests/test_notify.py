from unittest.mock import MagicMock, call
from app.notification import notify


def notifier(item, result):
    return 'notifier output'


def rule():
    return [1, 2, 3]


def even(x):
    return x % 2 == 0


def odd(x):
    return x % 2 == 1


def test_notify_calls_rules():
    def dumb_notifier(item, result):
        pass

    rule = MagicMock(return_value=[])
    notify(rule=rule, notifiers=dumb_notifier)
    rule.assert_called_once_with()


def test_notify_calls_notifier():
    notifier = MagicMock(return_value='notifier')
    notify(rule=rule, notifiers=notifier)
    # there is only one notifier, hence it always recieves None as the
    # second parameter
    notifier.assert_has_calls([call(1, None), call(2, None), call(3, None)])


def test_notify_iterates_list_of_notifier():
    notifier = MagicMock(return_value='First Notifier')
    second_notifier = MagicMock(return_value='Second Notifier')
    notify(rule=rule, notifiers=[notifier, second_notifier])
    notifier.assert_has_calls([call(1, None), call(2, None), call(3, None)])
    second_notifier.assert_has_calls([call(1, 'First Notifier'),
                                      call(2, 'First Notifier'),
                                      call(3, 'First Notifier')])


def test_notify_filters_items():
    notifier = MagicMock(return_value='First Notifier')
    notify(rule=rule, notifiers=notifier, filters=even)
    notifier.assert_called_once_with(2, None)


def test_notify_iterates_list_of_filters():
    notifier = MagicMock(return_value='First Notifier')
    notify(rule=rule, notifiers=notifier, filters=[even, odd])
    notifier.assert_not_called()


def test_notify_calls_success_cb():
    success_cb = MagicMock(return_value='success')
    notify(rule=rule, notifiers=notifier, filters=even, success=success_cb)
    # success callback should be called only for even numbers with
    # a number and notifier output
    success_cb.assert_called_once_with(2, 'notifier output')


def test_notify_iterates_list_of_success_cb():
    success_cb = MagicMock(return_value='success')
    second_success_cb = MagicMock(return_value='second success')
    notify(rule=rule, notifiers=notifier, filters=even,
           success=[success_cb, second_success_cb])

    success_cb.assert_called_once_with(2, 'notifier output')
    # second callback recieves "transformed" notifier output
    second_success_cb.assert_called_once_with(2, 'success')


def test_notify_calls_failure_cb():
    def faulty_notifier(item, result):
        if item % 2 == 0:
            raise Exception
        return result

    failure = MagicMock(return_value=None)
    notify(rule=rule, notifiers=faulty_notifier, failure=failure)

    # call_args[0] returns tuple of positional arguments
    args = failure.call_args[0]
    assert args[0] == 2
    assert isinstance(args[1], Exception)
