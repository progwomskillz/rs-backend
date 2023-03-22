from domain.utils import TypesHelper


class TestTypesHelper():
    def test_try_to_int_invalid(self):
        assert TypesHelper.try_to_int(None) is None
        assert TypesHelper.try_to_int({}) is None
        assert TypesHelper.try_to_int([]) is None
        assert TypesHelper.try_to_int("123test") is None

    def test_try_to_int(self):
        assert TypesHelper.try_to_int(128) == 128
        assert TypesHelper.try_to_int("512") == 512
