import unittest

from additional_task_serializer_meta import (
    BaseSerializer,
    SerializerAnnotationMismatchTypesError,
    SerializerAnnotationMissedError,
    SerializerCreationError,
    SerializerHeterogeneousCollectionsError,
    SerializerMeta,
    SerializerMissingRequiredField,
)


class TestSerializer(unittest.TestCase):
    def assertEqualNotIs(self, a, b, msg=None):
        self.assertEqual(a, b, msg=msg)
        self.assertIsNot(a, b, msg=msg)

    def test_serializer_creation_types(self):
        class Types(BaseSerializer):
            b: bool
            i: int
            f: float
            s: str

            b_ph: bool = True
            i_ph: int = 314
            f_ph: float = 2.71
            s_ph: str = "Hello world!"

    def test_serialization_correctness(self):
        # Rondon is ze kapitaru of ze Gureite Buritan
        class Simple(BaseSerializer):
            required: str
            optional: str = "placeholder"

        simple = Simple(required="value")
        data = simple.serialize()
        simple2 = Simple(data)
        data2 = simple2.serialize()

        self.assertEqualNotIs(data, data2)
        self.assertIsNot(simple, simple2)

        data3 = {**data}
        del data3["optional"]

        simple3 = Simple(data3)
        self.assertEqual(simple3.optional, "placeholder")

    def test_neg_mismatch_types(self):
        with self.assertRaises(SerializerAnnotationMismatchTypesError):

            class WrongMismatch(BaseSerializer):
                wrong: str = 15

    def test_neg_mismatch_types_float_to_int(self):
        with self.assertRaises(SerializerAnnotationMismatchTypesError):

            class WrongFloatToInt(BaseSerializer):
                wrong: int = 15.5

    def test_pos_mismatch_types_int_to_float(self):
        class CorrectIntToFloat(BaseSerializer):
            wrong: float = 15

    def test_serializer_creation_nested(self):
        class WalletSerializer(BaseSerializer):
            uuid: int
            balance: float = 0

        class UserSerializer(BaseSerializer):
            username: str
            password: str
            wallet: WalletSerializer

        self.assertIs(type(WalletSerializer), SerializerMeta)
        self.assertIs(type(UserSerializer), SerializerMeta)

        wallet = WalletSerializer(uuid=1, balance=100)

        user = UserSerializer(username="me", password="123456", wallet=wallet)
        data = user.serialize()

        user2 = UserSerializer.deserialize(data)
        data2 = user2.serialize()

        self.assertEqualNotIs(data, data2)
        self.assertIsNot(user, user2)

    def test_neg_no_fields(self):
        with self.assertRaises(SerializerCreationError):

            class WrongNoFields(BaseSerializer):
                pass

    def test_neg_no_annotation_field(self):
        with self.assertRaises(SerializerCreationError):

            class WrongNoAnnotation(BaseSerializer):
                wrong = 0

    def test_neg_some_no_annotation_field(self):
        with self.assertRaises(SerializerAnnotationMissedError):

            class WrongSomeNoAnnotation(BaseSerializer):
                annot: str
                another: int = 12
                wrong = 0

    def test_neg_try_to_use_collection(self):
        with self.assertRaises(SerializerHeterogeneousCollectionsError):

            class WrongUsingList(BaseSerializer):
                wrong: list

        with self.assertRaises(SerializerHeterogeneousCollectionsError):

            class WrongUsingTypedList(BaseSerializer):
                wrong: list[int]

        with self.assertRaises(SerializerHeterogeneousCollectionsError):

            class WrongUsingListOfLists(BaseSerializer):
                wrong: list[list[int]]

        with self.assertRaises(SerializerHeterogeneousCollectionsError):

            class WrongUsingTuple(BaseSerializer):
                wrong: tuple

        with self.assertRaises(SerializerHeterogeneousCollectionsError):

            class WrongUsingSet(BaseSerializer):
                wrong: set

        with self.assertRaises(SerializerHeterogeneousCollectionsError):

            class WrongUsingFrozenset(BaseSerializer):
                wrong: frozenset

        with self.assertRaises(SerializerHeterogeneousCollectionsError):

            class WrongUsingDict(BaseSerializer):
                wrong: dict

        with self.assertRaises(SerializerHeterogeneousCollectionsError):

            class WrongUsingTypedDict(BaseSerializer):
                wrong: dict[str, float]

    def test_neg_try_create_no_args(self):
        class Correct(BaseSerializer):
            optional: int = 10
            required: str

        with self.assertRaises(SerializerMissingRequiredField):
            Correct()  # 'required' not provided

    def test_neg_wrong_deserialize_data(self):
        class Inner(BaseSerializer):
            optional: int = 10
            required: float

        class Middle(BaseSerializer):
            optional: int = 100
            required: Inner

        class Outer(BaseSerializer):
            optional: int = 1000
            required: Middle

        inner = Inner(required=10)
        middle = Middle(required=inner)
        outer = Outer(required=middle)
        data_outer = outer.serialize()
        del data_outer["required"]["required"]["required"]

        with self.assertRaises(SerializerMissingRequiredField):
            Outer.deserialize(data_outer)


if __name__ == "__main__":
    unittest.main()
