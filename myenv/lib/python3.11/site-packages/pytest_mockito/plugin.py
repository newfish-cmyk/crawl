
import pytest


@pytest.fixture
def unstub_():
    from mockito import unstub
    yield unstub
    unstub()

@pytest.fixture
def unstub(unstub_):
    from mockito import verifyStubbedInvocationsAreUsed
    yield unstub_

    verifyStubbedInvocationsAreUsed()


@pytest.fixture
def when(unstub):
    from mockito import when
    yield when


@pytest.fixture
def when2(unstub):
    from mockito import when2
    yield when2


@pytest.fixture
def expect(unstub):
    from mockito import expect, verifyNoUnwantedInteractions
    yield expect
    verifyNoUnwantedInteractions()


@pytest.fixture
def patch(unstub):
    from mockito import patch
    yield patch


@pytest.fixture
def spy2(unstub):
    from mockito import spy2
    yield spy2
