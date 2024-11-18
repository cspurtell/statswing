from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QTableWidget, QTableWidgetItem
)
from config import TEAM_NAME_MAPPING

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
        team_names = ['All Teams'] + [TEAM_NAME_MAPPING.get(team, team) for team in sorted(self.data['Team'].unique())]
        self.team_dropdown.addItems(team_names)
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
            team_abbr = {v: k for k, v in TEAM_NAME_MAPPING.items()}.get(team_name, team_name)
            filtered_data = self.data[self.data['Team'] == team_abbr]
        self.player_dropdown.clear()
        self.player_dropdown.addItems(filtered_data['Name'].unique())
    
    def update_player_stats(self, player_name):
        player_data = self.data[self.data['Name'] == player_name]
        self.populate_table(self.player_stats_table, player_data)

    def create_compare_tab(self):
        tab = QWidget()
        layout = QVBoxLayout()

        #Team dropdowns for P1 and P2
        self.team1_dropdown = QComboBox()
        self.team1_dropdown.addItems(['All Teams'] + [TEAM_NAME_MAPPING.get(team, team) for team in sorted(self.data['Team'].unique())])
        self.team1_dropdown.currentTextChanged.connect(self.update_player1_dropdown)

        self.team2_dropdown = QComboBox()
        self.team2_dropdown.addItems(['All Teams'] + [TEAM_NAME_MAPPING.get(team, team) for team in sorted(self.data['Team'].unique())])
        self.team2_dropdown.currentTextChanged.connect(self.update_player2_dropdown)

        #Player dropdowns for P1 and P2
        self.player1_dropdown = QComboBox()
        self.update_player1_dropdown('All Teams')
        self.player1_dropdown.currentTextChanged.connect(self.update_comparison_table)

        self.player2_dropdown = QComboBox()
        self.update_player2_dropdown('All Teams')
        self.player2_dropdown.currentTextChanged.connect(self.update_comparison_table)

        self.comparison_table = QTableWidget()

        layout.addWidget(QLabel('Team 1:'))
        layout.addWidget(self.team1_dropdown)
        layout.addWidget(QLabel('Player 1:'))
        layout.addWidget(self.player1_dropdown)

        layout.addWidget(QLabel('Team 2:'))
        layout.addWidget(self.team2_dropdown)
        layout.addWidget(QLabel('Player 2:'))
        layout.addWidget(self.player2_dropdown)

        layout.addWidget(self.comparison_table)
        tab.setLayout(layout)
        return tab
    
    def update_player1_dropdown(self, team_name):
        if team_name == 'All Teams':
            filtered_data = self.data
        else:
            team_abbr = {v: k for k, v in TEAM_NAME_MAPPING.items()}.get(team_name, team_name)
            filtered_data = self.data[self.data['Team'] == team_abbr]
        self.player1_dropdown.clear()
        self.player1_dropdown.addItems(filtered_data['Name'].unique())

    def update_player2_dropdown(self, team_name):
        if team_name == 'All Teams':
            filtered_data = self.data
        else:
            team_abbr = {v: k for k, v in TEAM_NAME_MAPPING.items()}.get(team_name, team_name)
            filtered_data = self.data[self.data['Team'] == team_abbr]
        self.player2_dropdown.clear()
        self.player2_dropdown.addItems(filtered_data['Name'].unique())

    def update_comparison_table(self):
        player1 = self.player1_dropdown.currentText()
        player2 = self.player2_dropdown.currentText()

        if player1 and player2:
            player1_data = self.data[self.data['Name'] == player1]
            player2_data = self.data[self.data['Name'] == player2]
        
        self.display_comparison(player1_data, player2_data)
    
    def populate_table(self, table, player_data):
        table.clear()
        table.setColumnCount(len(player_data.columns))
        table.setRowCount(len(player_data))
        table.setHorizontalHeaderLabels(player_data.columns)
        for row_idx, row in player_data.iterrows():
            for col_idx, val in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(val)))

    def display_comparison(self, player1_data, player2_data):
        if player1_data.empty or player2_data.empty:
            self.comparison_table.clear()
            self.comparison_table.setRowCount(0)
            self.comparison_table.setColumnCount(0)
            self.comparison_table.setHorizontalHeaderLabels([])
            return
        
        stats_columns = ['Stat 1', 'Stat 2', 'Stat 3', 'Stat 4'] #Need to fill this in with names for stats in data
        player1_stats = player1_data.iloc[0][stats_columns]
        player2_stats = player2_data.iloc[0][stats_columns]

        self.comparison_table.clear()
        self.comparison_table.setRowCount(len(stats_columns))
        self.comparison_table.setColumnCount(3) #3 cols for stat name, player 1, and player 2
        self.comparison_table.setHorizontalHeaderLabels(['Statistic', 'Player 1', 'Player 2'])

        for row, stat in enumerate(stats_columns):
            self.comparison_table.setItem(row, 0, QTableWidgetItem(stat)) #Statistic name
            self.comparison_table.setItem(row, 1, QTableWidgetItem(str(player1_stats[stat])))
            self.comparison_table.setItem(row, 2, QTableWidgetItem(str(player2_stats[stat])))
        
        self.comparison_table.resizeColumnsToContents()
        self.comparison_table.resizeRowsToContents()
    
