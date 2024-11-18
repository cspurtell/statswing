from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout, QHeaderView,
    QLabel, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QAbstractItemView
)
from qtrangeslider import QRangeSlider
from src.config import TEAM_NAME_MAPPING, STAT_MAPPING

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
        self.player_dropdown.currentTextChanged.connect(self.update_player_table)
        self.player_dropdown.currentTextChanged.connect(self.update_season_slider)

        #Season selection slider
        self.season_slider = QRangeSlider()
        self.season_slider_label = QLabel('Range: -')
        self.season_slider.setOrientation(Qt.Horizontal)
        self.season_slider.setRange(0, 0) #Placeholder values until years are determined
        self.season_slider.setValue((0, 0)) #Same
        self.season_slider.rangeChanged.connect(self.update_player_table)

        self.player_stats_table = QTableWidget()

        layout.addWidget(QLabel('Select Team:'))
        layout.addWidget(self.team_dropdown)
        layout.addWidget(QLabel('Select Player:'))
        layout.addWidget(self.player_dropdown)
        layout.addWidget(QLabel('Select Season(s):'))
        layout.addWidget(self.season_slider)
        layout.addWidget(self.season_slider_label)
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

    def update_season_slider(self):
        player_name = self.player_dropdown.currentText()
        if not player_name:
            self.season_slider.setRange(0, 0)
            self.season_slider.setValue(0, 0)
            self.season_slider.setEnabled(False)
            self.season_slider_label.setText('Range: -')
            return
        
        player_data = self.data[self.data['Name'] == player_name]

        if player_data.empty:
            self.season_slider.setRange(0, 0)
            self.season_slider.setValue(0, 0)
            self.season_slider.setEnabled(False)
            self.season_slider_label.setText('Range: -')
            return
    
        active_seasons = sorted(player_data['Season Year'].unique())
        min_year = active_seasons[0]
        max_year = active_seasons[-1]

        self.season_slider.setRange(min_year, max_year)
        self.season_slider.setValue((min_year, max_year))
        self.season_slider.setEnabled(True)
        self.season_slider_label.setText(f'Range: {min_year} - {max_year}')

    def update_player_table(self):
        player_name = self.player_dropdown.currentText()
        if not player_name:
            self.player_stats_table.clear()
            self.player_stats_table.setRowCount(0)
            self.player_stats_table.setColumnCount(0)
            self.player_stats_table.setHorizontalHeaderLabels([])
            return
        
        start_year, end_year = self.season_slider.value()
        
        filtered_data = self.data[
            (self.data['Name'] == player_name) &
            (self.data['Season Year'] >= int(start_year)) &
            (self.data['Season Year'] <= int(end_year))
        ]

        if filtered_data.empty:
            self.player_stats_table.clear()
            self.player_stats_table.setRowCount(0)
            self.player_stats_table.setColumnCount(0)
            self.player_stats_table.setHorizontalHeaderLabels(['No Data Available'])
            return
        
        agg_data = filtered_data.sum(numeric_only = True)

        stats = [
            (STAT_MAPPING.get(col, col), agg_data[col])
            for col in agg_data.index
            if col in STAT_MAPPING
        ]
        
        self.player_stats_table.clear()
        self.player_stats_table.setRowCount(len(stats))
        self.player_stats_table.setColumnCount(2) #Stat name and value
        self.player_stats_table.setHorizontalHeaderLabels(['Statistic', 'Value'])

        for row, (stat_name, value)in enumerate(stats):
            self.player_stats_table.setItem(row, 0, QTableWidgetItem(stat_name))
            self.player_stats_table.setItem(row, 1, QTableWidgetItem(f'{value:.2f}' if isinstance(value, float) else str(value)))

        self.player_stats_table.resizeColumnsToContents()
        self.player_stats_table.resizeRowsToContents()
        self.player_stats_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.player_stats_table.setEditTriggers(QAbstractItemView.NoEditTriggers)

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

        player1_data = self.data[self.data['Name'] == player1]
        player2_data = self.data[self.data['Name'] == player2]
        
        self.display_comparison(player1_data, player2_data)

    def display_comparison(self, player1_data, player2_data):
        if player1_data.empty or player2_data.empty:
            self.comparison_table.clear()
            self.comparison_table.setRowCount(0)
            self.comparison_table.setColumnCount(0)
            self.comparison_table.setHorizontalHeaderLabels([])
            return
        
        stats_columns = ['G', 'PA', 'HR', 'R'] #Need to fill this in with names for stats in data
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
    
