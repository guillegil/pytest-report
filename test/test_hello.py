
import pytest
import pytest_report

from advanced_logger import log

def test_error():
    log.init_term_handler('myterm', level='info')

    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')
    log.info('LOG LINE TO SEE IF IS DISPLAYED IN THE TB')

    print("This is gonna break everything")
    