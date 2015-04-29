from codecs import open

import click

from lic.manager import Manager


pass_manager = click.make_pass_decorator(Manager)


@click.group()
@click.pass_context
def cli(ctx):
    "Tool for create licensing your products"
    ctx.obj = Manager()


_list = list

@cli.command()
@click.argument('query', required=False, default=None)
@click.option('-n', '--by_nick', default=False, is_flag=True)
@pass_manager
def list(manager, query, by_nick):
    """
    List all the licenses whose name or (nick) match the query
    or all if there isn't query.
    """
    out = manager.list(query, by_nick)
    for l in out:
        print_attr('Title', l.title)
        print_attr('Nickname', l.nick)
        click.echo()


@cli.command()
@click.argument('query', required=True)
@click.option('-n', '--by_nick', default=False, is_flag=True)
@click.option('-o', '--out_path', default='./LICENSE')
@pass_manager
def write(manager, query, by_nick, out_path):
    """
    Write the license to output file
    """
    lic = manager.find_one(query, by_nick)
    with open(out_path, encoding='utf-8', mode='w') as file:
        click.echo(lic.filledbody, file=file)


@cli.command()
@click.argument('query', required=True)
@click.option('-n', '--by_nick', default=False, is_flag=True)
@pass_manager
def show(manager, query, by_nick):
    """
    Show the info of the license that better match the query
    """
    lic = manager.find_one(query, by_nick)

    print_attr('Title', lic.title)
    print_attr('Nick', lic.nick)
    print_attr('Category', lic.category)
    print_attr('Source', lic.source)
    print_attr('Required', lic.required)
    print_attr('Permitted', lic.permitted)
    print_attr('Forbidden', lic.forbidden)
    



def print_attr(name, val):
    click.secho(name + ': ', nl=False, fg='blue')

    if isinstance(val, _list):
        val = ', '.join(val)
    click.echo(val)



if __name__ == '__main__':
    cli()
