#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import logging.config
import sys

import click

logger = logging.getLogger(__name__)
LOG_FORMAT = ('%(asctime)-15s [%(levelname)-7s]: '
              '%(message)s (%(filename)s:%(lineno)s)')


@click.command()
@click.option('--debug/--no-debug', default=False)
@click.option('--logging-config')
def run(debug, logging_config):
    logging.basicConfig(
        format=LOG_FORMAT,
        level=logging.DEBUG if debug else logging.INFO)
    if logging_config:
        try:
            logging.config.fileConfig(
                fname=logging_config,
                disable_existing_loggers=False)
        except (KeyError, ValueError, TypeError,
                AttributeError, ImportError) as e:
            logger.info(f'Error with the logging config file: {e}')

    logger.debug('debug')
    logger.info('info')
    print('foobar')
    return 0


if __name__ == '__main__':
    sys.exit(run())
