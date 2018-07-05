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
        next_link = self.get_next_link()
        previous = self.get_previous_link()
        if next_link is None:
            next_link = ""
        if previous is None:
            previous = ""
        now = self.page.number
        if self.page.paginator.count >= now * self.page_size:
            number = self.page_size
        else:
            number = self.page.paginator.count - self.page_size * (now - 1)
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('number', number),
            ('next', next_link),
            ('previous', previous),
            ('data', data),
            ('error', '0')
        ]))
