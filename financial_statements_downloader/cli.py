from configparser import ConfigParser

import click

from financial_statements_downloader.data import Data
from financial_statements_downloader.downloader import download_data

DB_FILE = 'db.json'
CONFIG_FILE = 'config.cfg'


@click.group(name='fsd')
@click.version_option(version='0.1', prog_name='fsd')
@click.pass_context
def cli(ctx):
    ctx.obj['data'] = Data(DB_FILE)

    config = ConfigParser()
    with open(CONFIG_FILE) as f:
        config.read_file(f)
    ctx.obj['config'] = config


@cli.command(help='Import ICOs from file, one ICO per line.')
@click.argument('file', type=click.Path(exists=True))
@click.pass_context
def import_icos(ctx, file):
    ctx.obj['data'].import_icos(file)


@cli.command(help='Download documents for ICOs.')
@click.pass_context
def download(ctx):
    data = ctx.obj['data']
    config = ctx.obj['config']

    download_data(data, config)


@cli.command(help='Extract information from downloaded documents.')
@click.pass_context
def extract(ctx):
    pass


def main():
    cli(obj={})
