from enaml.qt.qt_application import QtApplication
import enaml

def make_shortcuts():
    import os
    import sys
    from pyshortcuts import make_shortcut, platform
    bindir = 'bin'
    if platform.startswith('win'):
        bindir = 'Scripts'

    shortcut = make_shortcut(
        os.path.normpath(os.path.join(sys.prefix, bindir, 'srm-aggregate')),
        name='SRM aggregate',
        folder='NCRAR',
        description='SRM aggregation tool for Konrad-Martin lab',
        terminal=True,
        desktop=False,
        startmenu=True,
    )

    shortcut = make_shortcut(
        os.path.normpath(os.path.join(sys.prefix, bindir, 'srm-test')),
        name='SRM test',
        folder='NCRAR',
        description='SRM aggregation tool for Konrad-Martin lab',
        terminal=True,
        desktop=False,
        startmenu=True,
    )


def main_test():
    print('Hello world')
    input()


def main_srm_aggregate():
    with enaml.imports():
        from .srm.main_window import SRMAggregationWindow
    app = QtApplication()
    view = SRMAggregationWindow()
    view.show()
    app.start()
    return True


def main_wbmemr_aggregate():
    with enaml.imports():
        from .wbmemr.main_window import WBMEMRAggregationWindow
    app = QtApplication()
    view = WBMEMRAggregationWindow()
    view.show()
    app.start()
    return True
