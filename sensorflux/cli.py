#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys

import click

logger = logging.getLogger(__name__)
LOG_FORMAT = ('%(asctime)-15s [%(levelname)-7s]: '
              '%(message)s (%(filename)s:%(lineno)s)')


@click.command()
@click.option('--debug/--no-debug', default=False)
def run(debug):
    logging.basicConfig(
        format=LOG_FORMAT,
        level=logging.DEBUG if debug else logging.INFO)
    logger.debug('debug')
    logger.info('info')
    print('foobar')
    return 0


if __name__ == '__main__':
    sys.exit(run())
