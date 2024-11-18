from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTableWidget, QTableWidgetItem
)

class StatSwingApp(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.data = data
        self.setWindowTitle("StatSwing Test")
        self.setGeometry(100, 100, 800, 600)
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.tabs.addTab(self.create_player_tab(), "Player Analytics")
        self.tabs.addTab(self.create_compare_tab(), "Compare Players")
    
    def create_player_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        #Team selection dropdown
        self.team_dropdown = QComboBox()
        self.team_dropdown.addItems(['All Teams'] + sorted(self.data['Team'].unique()))
        self.team_dropdown.currentTextChanged.connect(self.update_player_dropdown)

        #Player selection dropdown
        self.player_dropdown = QComboBox()
        self.update_player_dropdown('All Teams')
        self.player_dropdown.currentTextChanged.connect(self.update_player_stats)

        self.player_stats_table = QTableWidget()

        layout.addWidget(QLabel('Select Team:'))
        layout.addWidget(self.team_dropdown)
        layout.addWidget(QLabel('Select Player:'))
        layout.addWidget(self.player_dropdown)
        layout.addWidget(self.player_stats_table)

        tab.setLayout(layout)
        return tab
    
    def update_player_dropdown(self, team_name):
        if team_name == 'All Teams':
            filtered_data = self.data
        else:
            filtered_data = self.data[self.data['Team'] == team_name]
        self.player_dropdown.clear()
        self.player_dropdown.addItems(filtered_data['Name'].unique())
    
    def update_player_stats(self, player_name):
        player_data = self.data[self.data['Name'] == player_name]
        self.populate_table(self.player_stats_table, player_data)

    def create_compare_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        player1_layout = QHBoxLayout()
        self.player1_dropdown = QComboBox()
        self.player1_dropdown.addItems(self.data['Name'].unique())

        self.player2_dropdown = QComboBox()
        self.player2_dropdown.addItems(self.data['Name'].unique())

        player1_layout.addWidget(QLabel('Player 1:'))
        player1_layout.addWidget(self.player1_dropdown)
        player1_layout.addWidget(QLabel('Player 2:'))
        player1_layout.addWidget(self.player2_dropdown)

        layout.addLayout(player1_layout)

        self.player1_stats_table = QTableWidget()
        self.player2_stats_table = QTableWidget()

        layout.addWidget(QLabel('Player 1 Stats:'))
        layout.addWidget(self.player1_stats_table)
        layout.addWidget(QLabel('Player 2 Stats:'))
        layout.addWidget(self.player2_stats_table)

        self.player1_dropdown.currentTextChanged.connect(
            lambda: self.update_player_stats_comp(self.player1_stats_table, self.player1_dropdown.currentText())
        )
        self.player2_dropdown.currentTextChanged.connect(
            lambda: self.update_player_stats_comp(self.player2_stats_table, self.player2_dropdown.currentText())
        )

        tab.setLayout(layout)
        return tab
    
    def update_player_stats_comp(self, table, player_name):
        player_data = self.data[self.data['Name'] == player_name]
        self.populate_table(table, player_data)

    def populate_table(self, table, player_data):
        table.clear()
        table.setColumnCount(len(player_data.columns))
        table.setRowCount(len(player_data))
        table.setHorizontalHeaderLabels(player_data.columns)
        for row_idx, row in player_data.iterrows():
            for col_idx, val in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))
