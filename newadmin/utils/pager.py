# -*- coding:utf-8 -*-

class PageInfo(object):
    def __init__(self,current_page,all_count,base_url,page_param_dict,per_page=10,show_page=11):
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.per_page = per_page
        self.all_count = all_count
        a,b = divmod(all_count,per_page)
        if b:
            a += 1
        self.all_pager = a
        self.show_page = show_page
        self.base_url = base_url
        self.page_param_dict = page_param_dict

    @property
    def start(self):
        return (self.current_page-1) * self.per_page

    @property
    def end(self):
        return self.current_page * self.per_page

    def pager(self):
        # v = '<a href="/custom.html?page=1">1</a>'
        # return v
        page_list = []
        half = (self.show_page) // 2
        # 如果数据总页数 < 11
        if self.all_pager < self.show_page:
            begin = 1
            stop = self.all_pager + 1
        # 如果数据总页数 > 11
        else:
            # 如果当前页 <= 5，永远显示1，11
            if self.current_page <= half:

                begin = 1
                stop = self.show_page + 1
            else:
                if self.current_page + half > self.all_pager:
                    # begin = self.current_page - half
                    begin = self.all_pager - self.show_page + 1
                    stop = self.all_pager + 1
                else:
                    begin = self.current_page - half
                    stop = self.current_page + half + 1
        if self.current_page <= 1:
            prev = '<li><a href="#">上一页</a></li>'
        else:
            self.page_param_dict["page"] = self.current_page-1
            prev = '<li><a href="{}?{}">上一页</a></li>'.format(self.base_url,self.page_param_dict.urlencode())
        page_list.append(prev)

        for i in range(begin,stop):
            self.page_param_dict["page"] = i
            if i == self.current_page:
                tmp = '<li class="active"><a href="{}?{}">{}</a></li>'.format(self.base_url,self.page_param_dict.urlencode(),i)
            else:
                tmp = '<li><a href="{}?{}">{}</a></li>'.format(self.base_url,self.page_param_dict.urlencode(),i)
            page_list.append(tmp)

        if self.current_page >= self.all_pager:
            after = '<li><a href="#">下一页</a></li>'
        else:
            self.page_param_dict["page"] = self.current_page+1
            after = '<li><a href="{}?{}">下一页</a></li>'.format(self.base_url,self.page_param_dict)
        page_list.append(after)

        # if self.current_page >= self.all_pager:
        #     after = '<li><a href="#">下一页</a></li><span>（{start}-{end}/共{total}）</span>'.format(
        #         start=self.start+1 if self.start<self.all_count else self.all_count,
        #         end=self.end if self.end<self.all_count else self.all_count,
        #         total=self.all_count)
        # else:
        #     after = '<li><a href="{url}?page={next_page}">下一页</a></li><span>（{start}-{end}/共{total}）</span>'.format(
        #         url=self.base_url,
        #         next_page=self.current_page+1,
        #         start=self.start+1 if self.start<self.all_count else self.all_count,
        #         end=self.end if self.end<self.all_count else self.all_count,
        #         total=self.all_count
        #     )
        # page_list.append(after)

        return " ".join(page_list)