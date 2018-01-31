from configparser import ConfigParser

import click

from financial_statements_downloader.data import Data
from financial_statements_downloader.downloader import download_data
from financial_statements_downloader.parser import parse

DB_FILE = 'db.json'
"""Database file name."""

CONFIG_FILE = 'config.cfg'
"""Config file name."""


@click.group(name='fsd')
@click.version_option(version='0.1', prog_name='fsd')
@click.pass_context
def cli(ctx):
    """Initializes common variables and stores them into context.

    :param ctx: click context
    """
    ctx.obj['data'] = Data(DB_FILE)

    config = ConfigParser()
    with open(CONFIG_FILE) as f:
        config.read_file(f)
    ctx.obj['config'] = config


@cli.command(help='Import ICOs from file, one ICO per line.')
@click.argument('file', type=click.Path(exists=True))
@click.pass_context
def import_icos(ctx, file: str):
    """Imports ICOs from file into database.

    File must contain one ICO per line.

    :param ctx: click context
    :param file: file path
    :type file: str
    """
    data = ctx.obj['data']

    data.import_icos(file)


@cli.command(help='Download documents for ICOs.')
@click.pass_context
def download(ctx):
    """Downloads documents for imported ICOs.

    :param ctx: click context
    """
    data = ctx.obj['data']
    config = ctx.obj['config']

    download_data(data, config)


@cli.command(help='Extract information from downloaded documents.')
@click.pass_context
def extract(ctx):
    """Extracts information specified in config file from downloaded documents.

    :param ctx: click context
    """
    data = ctx.obj['data']
    config = ctx.obj['config']

    parse(data, config)


def main():
    """Main function."""
    cli(obj={})
