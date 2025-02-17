from lark import Lark, Token, Tree

from .column_type import BasicType, DUnion, Field, ListType, Map, ParseType, Struct
from .exceptions import *

parser = Lark.open("field_types.lark", rel_to=__file__, parser="lalr", start="type")


def traverse_tree(node):
    if isinstance(node, Tree):
        if node.data == "list":
            if len(node.children) != 1:
                raise StructureError(
                    f"Invalid array structure: expected 1 child, got: {len(node.children)}"
                )

            child = node.children[0]
            child_value = traverse_tree(child)

            if not isinstance(child_value, ParseType):
                raise NonTypeObjectError(f"Array got a non-type object: {child}")

            return ListType(child_value)

        elif node.data == "map":
            subtypes = []
            for child in node.children:
                child_value = traverse_tree(child)
                if not isinstance(child_value, ParseType):
                    raise NonTypeObjectError(f"Tuple got a non-type object: {child}")
                subtypes.append(child_value)
            return Map(subtypes[0], subtypes[1])

        elif node.data == "struct":
            fields = {}
            for child in node.children:
                value = traverse_tree(child)
                if isinstance(value, Field):
                    fields[value.name] = value.type_value
                else:
                    raise StructureError(f"Got an unexpected nested child: {value}")
            return Struct(fields)

        elif node.data == "union":
            fields = {}
            for child in node.children:
                value = traverse_tree(child)
                if isinstance(value, Field):
                    fields[value.name] = value.type_value
                else:
                    raise StructureError(f"Got an unexpected nested child: {value}")
            return DUnion(fields)

        elif node.data == "decimal":
            return BasicType(node.data)

        elif node.data == "field":
            if len(node.children) != 2:
                raise StructureError(f"Unexpected field structure: {node}")
            field_name_node, field_type_node = node.children
            field_name = traverse_tree(field_name_node)
            if not isinstance(field_name, str):
                raise UnexpectedTypeError(
                    f"Unexpected field name type: {type(field_name)}"
                )
            field_type = traverse_tree(field_type_node)
            if not isinstance(field_type, ParseType):
                raise UnexpectedTypeError(
                    f"Unexpected field type type: {type(field_type)}"
                )
            return Field(field_name, field_type)

        else:
            raise UnexpectedTypeError(f"Unexpected tree type: {node.data}")

    elif isinstance(node, Token):
        if node.type == "BASIC_TYPE":
            return BasicType(node.value)
        elif node.type == "FIELD_NAME":
            return node.value
        else:
            raise UnexpectedTypeError(f"Unexpected token type: {node.type}")

    else:
        raise UnexpectedTypeError(f"Unexpected node type: {type(node)}")
