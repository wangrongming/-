import click


@click.group()
@click.pass_context
def cli(ctx):
    click.echo(ctx)


@cli.command()
@click.pass_context
def sync(ctx):
    click.echo('Debug is %s' % (ctx.obj['DEBUG'] and 'on' or 'off'))


if __name__ == '__main__':
    cli()
