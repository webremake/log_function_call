import os

import allure
import pytest


@pytest.hookimpl(trylast=True, hookwrapper=True)
def pytest_runtest_call(item):
    """Allure dynamic steps and features title"""
    yield
    allure.dynamic.title(" ".join(item.name.split("_")[1:]).capitalize())

    filename_with_extension = os.path.basename(item.location[0])
    filename_without_extension = os.path.splitext(filename_with_extension)[0]
    title = " ".join(filename_without_extension.split("_")[1:]).capitalize()
    allure.dynamic.feature(title)
