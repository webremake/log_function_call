import allure
from functools import wraps
import types
import re




def humanify(name: str):
    return ' '.join(re.split('_+', name))


def step(fn):
    @wraps(fn)
    def fn_with_allure_step(*args, **kwargs):
        is_method = (
            isinstance(args[0], object)
            and isinstance(getattr(args[0], fn.__name__, None), types.MethodType)
        )

        args_to_log = args[1:] if is_method else args
        args_and_kwargs_to_log_as_strings = [
            *map(str, args_to_log),
            *[f'{key}={value}' for key, value in kwargs.items()]
        ]
        args_and_kwargs_string = (
            (': ' + ', '.join(map(str, args_and_kwargs_to_log_as_strings)))
            if args_and_kwargs_to_log_as_strings
            else ''
        )

        step_name = (
            (f'[{args[0].__class__.__name__}] ' if is_method else '')
            + humanify(fn.__name__)
            + args_and_kwargs_string
        )

        allure.step(step_name)(lambda: None)()

        return fn(*args, **kwargs)

    return fn_with_allure_step




@step
def add_numbers(a, b):
    return a + b


@step
def subtract_numbers(a, b):
    return a - b


def test_calculator():
    number1 = 10
    number2 = 5

    result1 = add_numbers(number1, number2)
    assert result1 == 15

    result2 = subtract_numbers(number1, number2)
    assert result2 == 5


class MyClass:
    def __init__(self, value):
        self.value = value

    @step
    def multiply(self, num):
        result = self.value * num
        return result


def test_class_method():
    obj = MyClass(5)
    result = obj.multiply(10)
    assert result == 50

if __name__ == '__main__':
    allure.severity(allure.severity_level.NORMAL)
    allure.feature('Calculator')
    allure.story('Addition and Subtraction')
    allure.title('Calculator Test')
    allure.description('Test the functionality of the calculator.')

    test_calculator()
    test_class_method()