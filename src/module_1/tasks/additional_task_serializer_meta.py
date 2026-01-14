from typing import get_origin


class SerializerCreationError(Exception):
    def __str__(self):
        return "You must add at least one annotated field!"


class SerializerAnnotationMissedError(Exception):
    def __init__(self, attr_name):
        self.attr_name = attr_name

    def __str__(self):
        return (
            "All fields must be annotated! " + f"Not annotated field '{self.attr_name}'"
        )


class SerializerAnnotationMismatchTypesError(Exception):
    def __init__(self, attr_name, direction, target_type, provided_value):
        self.attr_name = attr_name
        self.direction = direction
        self.target_type = target_type
        self.provided_value = provided_value

    def __str__(self):
        return (
            f"Field type ({self.attr_name}: <{self.target_type.__name__}>) "
            + f"did not match {self.direction} type ({self.provided_value}: "
            + f"<{type(self.provided_value).__name__}>)!"
        )


class SerializerHeterogeneousCollectionsError(Exception):
    def __init__(self, attr_name, provided_type):
        self.attr_name = attr_name
        self.provided_type = provided_type

    def __str__(self):
        return (
            "You cant use heterogeneous collections "
            + "(list, tuple, dict, set, frozenset)! "
            + f"Using '{self.attr_name}' "
            + f"with type <{self.provided_type.__name__}>"
        )


class SerializerMissingRequiredField(Exception):
    def __init__(self, field_name, log_path, class_name):
        self.field_name = field_name
        self.log_path = log_path
        self.class_name = class_name

    def __str__(self):
        return (
            f"Field '{self.field_name}' is required, but not provided in "
            + f"<{
                self.log_path + ': ' + f'!{self.class_name}!'
                if self.log_path
                else self.class_name
            }>"
        )


class SerializerMeta(type):
    def __new__(mcs, name, bases, attrs):
        if name == "BaseSerializer":
            return type.__new__(mcs, name, bases, attrs)

        if "__annotations__" not in attrs:
            raise SerializerCreationError

        annotations = attrs["__annotations__"]
        SerializerMeta.validate_annotations(annotations)

        init_values = {}

        for attr in attrs:
            if not attr.startswith("__"):
                if not callable(attrs[attr]):
                    if attr not in annotations:
                        raise SerializerAnnotationMissedError(attr)

                    elif annotations[attr] is not type(attrs[attr]):
                        if not (
                            annotations[attr] is float and type(attrs[attr]) is int
                        ):
                            raise SerializerAnnotationMismatchTypesError(
                                attr, "placeholder", annotations[attr], attrs[attr]
                            )
                        else:
                            init_values[attr] = attrs[attr]
                    else:
                        init_values[attr] = attrs[attr]

        attrs["__init__"] = SerializerMeta.create_init_method()
        attrs["serialize"] = SerializerMeta.create_serialize_method()
        attrs["deserialize"] = SerializerMeta.create_deserialize_method()
        attrs["_init_values"] = init_values

        return type.__new__(mcs, name, bases, attrs)

    @staticmethod
    def validate_annotations(annotations):
        heterogeneous_collections = {list, tuple, dict, set, frozenset}

        for attr in annotations:
            if (
                annotations[attr] in heterogeneous_collections
                or get_origin(annotations[attr]) in heterogeneous_collections
            ):
                raise SerializerHeterogeneousCollectionsError(attr, annotations[attr])

    @staticmethod
    def create_init_method():
        def init(self, *args, **kwargs):
            log_path = None
            if args and not kwargs:
                kwargs = args[0]
                if len(args) > 1:
                    log_path = args[1]

            for field in self.__class__.__annotations__:
                value = kwargs.get(field, self._init_values.get(field))

                if value is None:
                    raise SerializerMissingRequiredField(
                        field, log_path, self.__class__.__name__
                    )

                if self.__class__.__annotations__[field] is not type(value):
                    if not (
                        self.__class__.__annotations__[field] is float
                        and type(value) is int
                    ):
                        raise SerializerAnnotationMismatchTypesError(
                            field,
                            "provided",
                            self.__class__.__annotations__[field],
                            value,
                        )

                setattr(self, field, value)

        return init

    @staticmethod
    def create_serialize_method():
        def serialize(self) -> dict:
            data = {}
            fields = self.__class__.__annotations__

            for attr in fields:
                data[attr] = getattr(self, attr)

                if type(fields[attr]) is SerializerMeta:
                    data[attr] = data[attr].serialize()

            return data

        return serialize

    @staticmethod
    def create_deserialize_method():
        @classmethod
        def deserialize(cls, attrs, *, log_path=None):
            attrs = {**attrs}
            for field in attrs:
                if field in cls.__annotations__:
                    if type(cls.__annotations__[field]) is SerializerMeta:
                        attrs[field] = cls.__annotations__[field].deserialize(
                            attrs[field],
                            log_path=(
                                log_path + ": " + cls.__name__
                                if log_path
                                else cls.__name__
                            ),
                        )

                    attrs[field] = attrs.get(field, cls._init_values.get(field))

            return cls(attrs, log_path)

        return deserialize


class BaseSerializer(metaclass=SerializerMeta):
    pass
