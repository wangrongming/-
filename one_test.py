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
    hello()
