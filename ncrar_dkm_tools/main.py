from enaml.qt.qt_application import QtApplication
import enaml
with enaml.imports():
    from .srm.main_window import SRMAggregationWindow


def main_srm_aggregate():
    app = QtApplication()
    view = SRMAggregationWindow()
    view.show()
    app.start()
    return True
