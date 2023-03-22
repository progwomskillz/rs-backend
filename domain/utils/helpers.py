class TypesHelper():
    @staticmethod
    def try_to_int(value):
        try:
            return int(value)
        except ValueError:
            return None
        except TypeError:
            return None
