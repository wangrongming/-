import click


@click.command()
@click.option('--count', default=2, help='Number of greetings.')
@click.option('--name', prompt='Your name', help='The person to greet.')
@click.option('--password', default='', type=str, help='Number of greetings.')
def hello(count, name, password):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo('Hello %s! %s' % (name, password))


if __name__ == '__main__':
    # hello()
    print(repr(r"""京东当天到，17号，成都<br><img class="BDE_Image" src="https://imgsa.baidu.com/forum/w%3D580/sign=1a36a1749d58d109c4e3a9bae159ccd0/a53e1295a4c27d1e1579f9ce14d5ad6eddc43864.jpg" size="328689" changedsize="true" width="560" height="746" size="328689">', 'post_no': 1, 'type': '0', 'comment_num': 0, 'is_fold': 0, 'props': None, 'post_index': 0, 'pb_tpoint': None}}, 'source_code': '<div class="d_post_content j_d_post_content " id="post_content_127961898402" style="display:;">            京东当天到，17号，成都<br/><img changedsize="true" class="BDE_Image" height="746" size="328689" src="https://imgsa.baidu.com/forum/w%3D580/sign=1a36a1749d58d109c4e3a9bae159ccd0/a53e1295a4c27d1e1579f9ce14d5ad6eddc43864.jpg" width="560"/></div>"""))