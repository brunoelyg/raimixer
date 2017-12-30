import sys
from PyQt5.QtWidgets import (
        QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QPushButton, QApplication,
        QGroupBox, QLabel, QLineEdit, QSpinBox, QComboBox, QTextBrowser,
        QCheckBox, QMainWindow
)
from PyQt5.QtGui import QFont, QFontMetrics
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

# TODO: simplify the var names in the private methods
# TODO: settings: RPC data and wallet list
# TODO: connect with raimixer and make it work
# TODO: progress bar
# TODO: tooltips

XXX_TEST_ACCOUNT = 'xrb_3zq1yrhgij8ix35yf1khehzwfiz9ojjotndtqprpyymixxwxnkhn44qgqmy5'


def _units_combo():
    units_combo = QComboBox()
    units_combo.addItem('XRB/MRAI')
    units_combo.addItem('KRAI')
    return units_combo


class RaimixerGUI(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        central_wid = QWidget(self)
        self.setCentralWidget(central_wid)

        self.main_layout = QVBoxLayout()
        central_wid.setLayout(self.main_layout)

        self.create_accounts_box()

        self.mixwallet_layout = QHBoxLayout()
        self.create_mix_box()
        self.create_walletstatus_box()
        self.main_layout.addLayout(self.mixwallet_layout)

        self.create_buttons_box()
        self.create_log_box()
        # XXX wallet online and unlock status

        self.setWindowTitle('RaiMixer')

    def create_accounts_box(self):
        accounts_groupbox = QGroupBox()
        accounts_layout = QVBoxLayout()

        # XXX minimum width for 64 chars
        source_lbl = QLabel('Source:')
        # Set to default account or a list selector
        source_combo = QComboBox()
        source_combo.addItem(XXX_TEST_ACCOUNT)
        accounts_layout.addWidget(source_lbl)
        accounts_layout.addWidget(source_combo)

        dest_lbl = QLabel('Destination:')
        dest_edit = QLineEdit(XXX_TEST_ACCOUNT)
        self._resize_to_content(dest_edit)
        dest_edit.setText('')
        dest_edit.setPlaceholderText('Destination account')
        accounts_layout.addWidget(dest_lbl)
        accounts_layout.addWidget(dest_edit)

        amount_lbl = QLabel('Amount:')
        amount_hbox = QHBoxLayout()
        amount_edit = QLineEdit('')
        amount_edit.setPlaceholderText('Amount to send')
        accounts_layout.addWidget(amount_lbl)
        units_combo = _units_combo()
        amount_hbox.addWidget(amount_edit)
        amount_hbox.addWidget(units_combo)
        accounts_layout.addLayout(amount_hbox)

        incamount_check = QCheckBox('Increase needed amount (helps masking transaction, '
                                    'excess returns to account)')
        incamount_edit = QLineEdit('')
        incamount_edit.setPlaceholderText('Amount to increase')
        incamount_edit.setEnabled(False)
        incamount_check.stateChanged.connect(
                lambda: incamount_edit.setEnabled(incamount_check.isChecked())
        )
        accounts_layout.addWidget(incamount_check)
        accounts_layout.addWidget(incamount_edit)

        accounts_groupbox.setLayout(accounts_layout)
        self.main_layout.addWidget(accounts_groupbox)

    def create_mix_box(self):
        mix_groupbox = QGroupBox('Mixing')
        mix_layout = QFormLayout()

        mix_numaccounts_lbl = QLabel('Accounts:')
        mix_numaccounts_spin = QSpinBox()
        # XXX set default from settings
        mix_numaccounts_spin.setValue(4)
        mix_layout.addRow(mix_numaccounts_lbl, mix_numaccounts_spin)

        mix_numrounds_lbl = QLabel('Rounds:')
        mix_numrounds_spin = QSpinBox()
        mix_numrounds_spin.setValue(2)
        mix_layout.addRow(mix_numrounds_lbl, mix_numrounds_spin)

        mix_groupbox.setLayout(mix_layout)
        self.mixwallet_layout.addWidget(mix_groupbox)

    def create_walletstatus_box(self):
        walletstatus_groupbox = QGroupBox('Wallet Status')
        walletstatus_layout = QFormLayout()

        connected_lbl = QLabel('Connected:')
        # XXX
        connected_lbl_dyn = QLabel('Yes')
        walletstatus_layout.addRow(connected_lbl, connected_lbl_dyn)

        unlocked_lbl = QLabel('Unlocked:')
        # XXX
        unlocked_lbl_dyn = QLabel('Yes')
        walletstatus_layout.addRow(unlocked_lbl, unlocked_lbl_dyn)

        walletstatus_groupbox.setLayout(walletstatus_layout)
        self.mixwallet_layout.addWidget(walletstatus_groupbox)

    def create_buttons_box(self):
        buttons_groupbox = QGroupBox()
        buttons_layout = QHBoxLayout()

        mix_btn = QPushButton('Mix!')
        settings_btn = QPushButton('Settings')

        def _show_config():
            c = ConfigWindow(self)
            c.show()

        settings_btn.clicked.connect(_show_config)
        buttons_layout.addWidget(mix_btn)
        buttons_layout.addWidget(settings_btn)

        buttons_groupbox.setLayout(buttons_layout)
        self.main_layout.addWidget(buttons_groupbox)

    def create_log_box(self):
        self.log_groupbox = QGroupBox('Output')
        log_layout = QVBoxLayout()

        log_text = QTextBrowser()
        log_layout.addWidget(log_text)
        self.log_groupbox.setLayout(log_layout)
        self.main_layout.addWidget(self.log_groupbox)
        self.log_groupbox.setHidden(True)

    def _resize_to_content(self, line_edit):
        text = line_edit.text()
        font = QFont('', 0)
        fm = QFontMetrics(font)
        pixelsWide = fm.width(text)
        pixelsHigh = fm.height()
        line_edit.setFixedSize(pixelsWide, pixelsHigh)


class ConfigWindow(QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        central_wid = QWidget(self)
        self.setCentralWidget(central_wid)

        self.main_layout = QVBoxLayout()
        central_wid.setLayout(self.main_layout)

        self.create_connect_box()
        self.create_mixingdefs_box()

        unit_groupbox = QGroupBox('Default Unit')
        unit_hbox = QHBoxLayout()
        unit_combo = _units_combo()
        unit_hbox.addWidget(unit_combo)
        unit_groupbox.setLayout(unit_hbox)
        self.main_layout.addWidget(unit_groupbox)

        self.create_buttons_box()
        self.setWindowTitle('Settings')

    def create_connect_box(self):
        connect_groupbox = QGroupBox("Node / Wallet's RPC Connection")
        connect_layout = QVBoxLayout()

        addr_lbl = QLabel('Address:')
        # XXX read from settings json
        addr_edit = QLineEdit('::1')
        connect_layout.addWidget(addr_lbl)
        connect_layout.addWidget(addr_edit)

        port_lbl = QLabel('Port:')
        # XXX ditto
        port_edit = QLineEdit('7076')
        connect_layout.addWidget(port_lbl)
        connect_layout.addWidget(port_edit)

        connect_groupbox.setLayout(connect_layout)
        self.main_layout.addWidget(connect_groupbox)

    def create_mixingdefs_box(self):
        mix_groupbox = QGroupBox('Mixing Defaults')
        mix_layout = QFormLayout()

        mix_numaccounts_lbl = QLabel('Accounts:')
        mix_numaccounts_spin = QSpinBox()
        # XXX set default from settings
        mix_numaccounts_spin.setValue(4)
        mix_layout.addRow(mix_numaccounts_lbl, mix_numaccounts_spin)

        mix_numrounds_lbl = QLabel('Rounds:')
        mix_numrounds_spin = QSpinBox()
        mix_numrounds_spin.setValue(2)
        mix_layout.addRow(mix_numrounds_lbl, mix_numrounds_spin)

        mix_groupbox.setLayout(mix_layout)
        self.main_layout.addWidget(mix_groupbox)

    def create_buttons_box(self):
        buttons_groupbox = QGroupBox()
        buttons_layout = QHBoxLayout()

        apply_btn = QPushButton('Apply')
        cancel_btn = QPushButton('Cancel')
        buttons_layout.addWidget(apply_btn)
        buttons_layout.addWidget(cancel_btn)

        buttons_groupbox.setLayout(buttons_layout)
        self.main_layout.addWidget(buttons_groupbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    # app.setApplicationName('RaiMixer')
    gui = RaimixerGUI()
    gui.show()
    # settings = ConfigWindow()
    sys.exit(app.exec_())