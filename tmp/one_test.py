import re

html = """
<?xml version="1.0" encoding="utf-8"?>
<root><![CDATA[<h3 class="psth cm">点评</h3>
<div class="pstl xs1 cl">
<div class="psta vm">
<a  href="space-uid-14297179.html" c="1"><img src="https://clubimg-p03-drcn.club.vmall.com/data/avatar/014/29/71/79_avatar_small.jpg?_t=1539504502" /></a>
<a  href="space-uid-14297179.html" class="xi2 xw1">以为很洒脱</a>
</div>
<div class="psti">
红豆香芋(相遇)奶茶&nbsp;
<span>
发表于 <span title="2019-11-21 20:06">昨天&nbsp;20:06</span>&nbsp;
<a href="forum.php?mod=misc&amp;action=comment&amp;tid=21972661&amp;pid=446197699&amp;topcid=27582199&amp;page=2" onclick="showWindow('comment', this.href, 'get', 0)">回复</a>&nbsp;

</span>
</div>
</div>
<div class="pstl xs1 cl">
<div class="psta vm">
<a  href="space-uid-8076985.html" c="1"><img src="https://clubimg-p03-drcn.club.vmall.com/data/avatar/008/07/69/85_avatar_small.jpg?_t=1539432749" /></a>
<a  href="space-uid-8076985.html" class="xi2 xw1">初见oc</a>
</div>
<div class="psti">
深圳走起！&nbsp;
<span>
发表于 <span title="2019-11-21 20:47">昨天&nbsp;20:47</span>&nbsp;
<a href="forum.php?mod=misc&amp;action=comment&amp;tid=21972661&amp;pid=446197699&amp;topcid=27583088&amp;page=2" onclick="showWindow('comment', this.href, 'get', 0)">回复</a>&nbsp;

</span>
</div>
</div>
<div class="pstl xs1 cl">
<div class="psta vm">
<a  href="space-uid-7051105.html" c="1"><img src="https://clubimg-p03-drcn.club.vmall.com/data/avatar/007/05/11/05_avatar_small.jpg?_t=1539604417" /></a>
<a  href="space-uid-7051105.html" class="xi2 xw1">hw206816</a>
</div>
<div class="psti">
希望。&nbsp;
<span>
发表于 <span title="2019-11-21 22:26">昨天&nbsp;22:26</span>&nbsp;
<a href="forum.php?mod=misc&amp;action=comment&amp;tid=21972661&amp;pid=446197699&amp;topcid=27585399&amp;page=2" onclick="showWindow('comment', this.href, 'get', 0)">回复</a>&nbsp;

</span>
</div>
</div>
<div class="pgs mbm mtn cl"><div class="pg"><a href="forum.php?mod=misc&action=commentmore&tid=21972661&pid=446197699&amp;page=1" class="prev" ajaxtarget="comment_446197699"  >&nbsp;&nbsp;</a><a href="forum.php?mod=misc&action=commentmore&tid=21972661&pid=446197699&amp;page=1" ajaxtarget="comment_446197699"  >1</a><strong>2</strong><a href="forum.php?mod=misc&action=commentmore&tid=21972661&pid=446197699&amp;page=3" ajaxtarget="comment_446197699"  >3</a><a href="forum.php?mod=misc&action=commentmore&tid=21972661&pid=446197699&amp;page=3" class="nxt" ajaxtarget="comment_446197699"  >下一页</a></div></div>]]></root>
"""
# html = re.search(r"<root><!\[CDATA\[(.*?)]]></root>", html).group(1)
info = re.search(r"<root><!\[CDATA\[(.*?)]]></root>", html, re.S).group(1)
print(info)
