# -*- coding:utf-8 -*-
# author: JXF
# created: 2018-5-11

from rest_framework.pagination import PageNumberPagination
from collections import OrderedDict
from rest_framework.response import Response

# 分页处理
class Pagination(PageNumberPagination):
    # 默认每页显示数据条数
    page_size = 8
    # 获取url参数中设置的每页显示数据条数
    page_size_query_param = 'size'
    # 获取url中传入的页码
    page_query_param = 'page'
    # 每页最大显示数量
    max_page_size = 10

    def get_paginated_response(self, data):
        next = self.get_next_link()
        previous = self.get_previous_link()
        if next is None:
            next = ""
        if previous is None:
            previous = ""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', next),
            ('previous', previous),
            ('data', data),
            ('error', '0')
        ]))
