# -*- coding:utf-8 -*-

from django.template import Library
from types import FunctionType

register = Library()


def table_body(result_list, list_display, ygadmin_obj):
    for row in result_list:
        if list_display == "__all__":
            yield [str(row), ]
        else:
            yield [name(ygadmin_obj, obj=row) if isinstance(name, FunctionType) else getattr(row, name) for name in
                   list_display]


def table_head(list_display, ygadmin_obj):
    if list_display == "__all__":
        yield "对象列表"
    else:
        for item in list_display:
            if isinstance(item, FunctionType):
                yield item(ygadmin_obj, is_header=True)
            else:
                yield ygadmin_obj.model_class._meta.get_field(item).verbose_name


# @register.simple_tag
@register.inclusion_tag("yg/md.html")
def func(result_list, list_display, ygadmin_obj):
    tbody = table_body(result_list, list_display, ygadmin_obj)
    thead = table_head(list_display, ygadmin_obj)

    return {"tbody": tbody, "thead": thead}


