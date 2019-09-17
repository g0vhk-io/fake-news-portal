from django import template


register = template.Library()

@register.filter(name='status_text')
def get_status_chinese(status):
    mapping = {'pending': '等待處理', 
               'processing': '處理中',
               'factchecked':'正確',
               'partially_wrong': '含錯誤信息',
               'wrong': '假新聞'}
    return mapping.get(status, '不明')


@register.filter(name='status_color')
def get_status_color(status):
    mapping = {'pending': 'dark', 
               'processing': 'info',
               'factchecked':'primary',
               'partially_wrong': 'warning',
               'wrong': 'danger'}
    return mapping.get(status, 'secondary')
