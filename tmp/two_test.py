# "element": element,
# "comment": comment,
# "reply": "",
# page_source
item = {
    "comment": {'page_source': 'nihao', "other": "other"},
    "element": {'page_source': 'nihao'},
    "reply": ""
}

comment = item.get("comment", "")
element = item.get("element", "")
reply = item.get("reply", "")
if comment:
    comment.pop('page_source', None)
if element:
    element.pop('page_source', None)
if reply:
    reply.pop('page_source', None)

print(item)
