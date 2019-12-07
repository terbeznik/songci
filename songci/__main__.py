import click
import json

from . import api
from .__version__ import __version__


@click.command()
@click.option("--version", is_flag=True)
@click.option("-i", "inputfilename", type=click.File(mode="r"), help="Input from list of proxies")
@click.option("-o", "outputfilename", type=click.File(mode="w"), help="Outputfilename to write summary as json")
@click.argument("proxies", nargs=-1)
def cli(version, inputfilename, outputfilename, proxies):
    proxies = list(proxies)
    if version:
        click.echo(__version__)

    if inputfilename:
        proxies += inputfilename.read().splitlines()

    if proxies:
        summary = api.check(proxies)

        if outputfilename:
            json.dump(summary, outputfilename, indent=4)


if __name__ == "__main__":
    cli()
