import pandas as pd
import numpy as np

from sportsreference.nfl.boxscore import Boxscores, Boxscore

class NFLSeasonDatasetCreator:
    def get_nfl_schedule(self):
        week_list = list(range(1, 18))
        nfl_schedule = pd.DataFrame()
        year = 2019

        for week in week_list:
            week_str = str(week)
            year_str = str(year)
            date = week_str + "-" + year_str
            week_results = Boxscores(week, year)

            week_results_df = pd.DataFrame()
            for game in week_results.games[date]:
                game_results = pd.DataFrame(game, index=[0])[
                    ['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name', 'winning_abbr']]
                game_results['week'] = week
                week_results_df = pd.concat([week_results_df, game_results])

            nfl_schedule = pd.concat([nfl_schedule, week_results_df]).reset_index().drop(columns='index')

        return nfl_schedule

    def game_stats_cleanup(self, game_df, game_stats):
        try:
            away_team_df = game_df[['away_name', 'away_abbr', 'away_score']].rename(
                columns={'away_name': 'team_name', 'away_abbr': 'team_abbr', 'away_score': 'score'})
            home_team_df = game_df[['home_name', 'home_abbr', 'home_score']].rename(
                columns={'home_name': 'team_name', 'home_abbr': 'team_abbr', 'home_score': 'score'})
            try:
                if game_df.loc[0, 'away_score'] > game_df.loc[0, 'home_score']:
                    away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won': [1], 'game_lost': [0]}),
                                            left_index=True, right_index=True)
                    home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won': [0], 'game_lost': [1]}),
                                            left_index=True, right_index=True)
                elif game_df.loc[0, 'away_score'] < game_df.loc[0, 'home_score']:
                    away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won': [0], 'game_lost': [1]}),
                                            left_index=True, right_index=True)
                    home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won': [1], 'game_lost': [0]}),
                                            left_index=True, right_index=True)
                else:
                    away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won': [0], 'game_lost': [0]}),
                                            left_index=True, right_index=True)
                    home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won': [0], 'game_lost': [0]}),
                                            left_index=True, right_index=True)
            except TypeError:
                away_team_df = pd.merge(away_team_df, pd.DataFrame({'game_won': [np.nan], 'game_lost': [np.nan]}),
                                        left_index=True, right_index=True)
                home_team_df = pd.merge(home_team_df, pd.DataFrame({'game_won': [np.nan], 'game_lost': [np.nan]}),
                                        left_index=True, right_index=True)

            away_stats_df = game_stats.dataframe[['away_first_downs', 'away_fourth_down_attempts',
                                                  'away_fourth_down_conversions', 'away_fumbles', 'away_fumbles_lost',
                                                  'away_interceptions', 'away_net_pass_yards', 'away_pass_attempts',
                                                  'away_pass_completions', 'away_pass_touchdowns', 'away_pass_yards',
                                                  'away_penalties', 'away_points', 'away_rush_attempts',
                                                  'away_rush_touchdowns', 'away_rush_yards', 'away_third_down_attempts',
                                                  'away_third_down_conversions', 'away_time_of_possession',
                                                  'away_times_sacked', 'away_total_yards', 'away_turnovers',
                                                  'away_yards_from_penalties',
                                                  'away_yards_lost_from_sacks']].reset_index().drop(
                columns='index').rename(columns={
                'away_first_downs': 'first_downs', 'away_fourth_down_attempts': 'fourth_down_attempts',
                'away_fourth_down_conversions': 'fourth_down_conversions', 'away_fumbles': 'fumbles',
                'away_fumbles_lost': 'fumbles_lost',
                'away_interceptions': 'interceptions', 'away_net_pass_yards': 'net_pass_yards',
                'away_pass_attempts': 'pass_attempts',
                'away_pass_completions': 'pass_completions', 'away_pass_touchdowns': 'pass_touchdowns',
                'away_pass_yards': 'pass_yards',
                'away_penalties': 'penalties', 'away_points': 'points', 'away_rush_attempts': 'rush_attempts',
                'away_rush_touchdowns': 'rush_touchdowns', 'away_rush_yards': 'rush_yards',
                'away_third_down_attempts': 'third_down_attempts',
                'away_third_down_conversions': 'third_down_conversions',
                'away_time_of_possession': 'time_of_possession',
                'away_times_sacked': 'times_sacked', 'away_total_yards': 'total_yards', 'away_turnovers': 'turnovers',
                'away_yards_from_penalties': 'yards_from_penalties',
                'away_yards_lost_from_sacks': 'yards_lost_from_sacks'})

            home_stats_df = game_stats.dataframe[['home_first_downs', 'home_fourth_down_attempts',
                                                  'home_fourth_down_conversions', 'home_fumbles', 'home_fumbles_lost',
                                                  'home_interceptions', 'home_net_pass_yards', 'home_pass_attempts',
                                                  'home_pass_completions', 'home_pass_touchdowns', 'home_pass_yards',
                                                  'home_penalties', 'home_points', 'home_rush_attempts',
                                                  'home_rush_touchdowns', 'home_rush_yards', 'home_third_down_attempts',
                                                  'home_third_down_conversions', 'home_time_of_possession',
                                                  'home_times_sacked', 'home_total_yards', 'home_turnovers',
                                                  'home_yards_from_penalties',
                                                  'home_yards_lost_from_sacks']].reset_index().drop(
                columns='index').rename(columns={
                'home_first_downs': 'first_downs', 'home_fourth_down_attempts': 'fourth_down_attempts',
                'home_fourth_down_conversions': 'fourth_down_conversions', 'home_fumbles': 'fumbles',
                'home_fumbles_lost': 'fumbles_lost',
                'home_interceptions': 'interceptions', 'home_net_pass_yards': 'net_pass_yards',
                'home_pass_attempts': 'pass_attempts',
                'home_pass_completions': 'pass_completions', 'home_pass_touchdowns': 'pass_touchdowns',
                'home_pass_yards': 'pass_yards',
                'home_penalties': 'penalties', 'home_points': 'points', 'home_rush_attempts': 'rush_attempts',
                'home_rush_touchdowns': 'rush_touchdowns', 'home_rush_yards': 'rush_yards',
                'home_third_down_attempts': 'third_down_attempts',
                'home_third_down_conversions': 'third_down_conversions',
                'home_time_of_possession': 'time_of_possession',
                'home_times_sacked': 'times_sacked', 'home_total_yards': 'total_yards', 'home_turnovers': 'turnovers',
                'home_yards_from_penalties': 'yards_from_penalties',
                'home_yards_lost_from_sacks': 'yards_lost_from_sacks'})

            away_team_df = pd.merge(away_team_df, away_stats_df, left_index=True, right_index=True)
            home_team_df = pd.merge(home_team_df, home_stats_df, left_index=True, right_index=True)
            try:
                away_team_df['time_of_possession'] = (int(away_team_df['time_of_possession'].loc[0][0:2]) * 60) + int(
                    away_team_df['time_of_possession'].loc[0][3:5])
                home_team_df['time_of_possession'] = (int(home_team_df['time_of_possession'].loc[0][0:2]) * 60) + int(
                    home_team_df['time_of_possession'].loc[0][3:5])
            except TypeError:
                away_team_df['time_of_possession'] = np.nan
                home_team_df['time_of_possession'] = np.nan
        except TypeError:
            away_team_df = pd.DataFrame()
            home_team_df = pd.DataFrame()
        return away_team_df, home_team_df

    def get_game_stats_for_season(self):
        week_list = list(range(1, 18))
        nfl_game_stats = pd.DataFrame()
        year = 2019

        for week in week_list:
            week_str = str(week)
            year_str = str(year)
            date = week_str + "-" + year_str
            week_results = Boxscores(week, year)

            week_stats_df = pd.DataFrame()
            for game in week_results.games[date]:
                game_id = game['boxscore']
                game_stats = Boxscore(game_id)
                game_results = pd.DataFrame(game, index=[0])

                away_team_stats, home_team_stats = self.game_stats_cleanup(game_results, game_stats)
                away_team_stats['week'] = week
                home_team_stats['week'] = week
                week_stats_df = pd.concat([week_stats_df, away_team_stats])
                week_stats_df = pd.concat([week_stats_df, home_team_stats])

            nfl_game_stats = pd.concat([nfl_game_stats, week_stats_df])

        return nfl_game_stats

    # loops through all the weeks we have collected
    # It sums various statistics for each week
    # averages the rest of the statistics over the weeks
    # Wins and Losses are now a win percentage
    # 3rd and 4th down conversions are now percentages as well
    def agg_weekly_data(self, schedule_df, weeks_games_df, current_week, weeks):
        schedule_df = schedule_df[schedule_df.week < current_week]

        agg_games_df = pd.DataFrame()

        for w in range(1, len(weeks)):

            games_df = schedule_df[schedule_df.week == weeks[w]]
            agg_weekly_df = weeks_games_df[
                weeks_games_df.week < weeks[w]].drop(columns=['score', 'week', 'game_won', 'game_lost']).groupby(
                    by=["team_name", "team_abbr"]).mean().reset_index()
            win_loss_df = weeks_games_df[weeks_games_df.week < weeks[w]][
                ["team_name", "team_abbr", 'game_won', 'game_lost']].groupby(
                by=["team_name", "team_abbr"]).sum().reset_index()
            try:
                win_loss_df['win_perc'] = win_loss_df['game_won'] / (win_loss_df['game_won'] + win_loss_df['game_lost'])
            except ZeroDivisionError:
                win_loss_df['win_perc'] = 0

            win_loss_df = win_loss_df.drop(columns=['game_won', 'game_lost'])

            try:
                agg_weekly_df['fourth_down_perc'] = agg_weekly_df['fourth_down_conversions'] / agg_weekly_df[
                    'fourth_down_attempts']
            except ZeroDivisionError:
                agg_weekly_df['fourth_down_perc'] = 0
            agg_weekly_df['fourth_down_perc'] = agg_weekly_df['fourth_down_perc'].fillna(0)

            try:
                agg_weekly_df['third_down_perc'] = agg_weekly_df['third_down_conversions'] / agg_weekly_df[
                    'third_down_attempts']
            except ZeroDivisionError:
                agg_weekly_df['third_down_perc'] = 0
            agg_weekly_df['third_down_perc'] = agg_weekly_df['third_down_perc'].fillna(0)

            agg_weekly_df = agg_weekly_df.drop(
                columns=['fourth_down_attempts', 'fourth_down_conversions', 'third_down_attempts',
                         'third_down_conversions'])
            agg_weekly_df = pd.merge(win_loss_df, agg_weekly_df, left_on=['team_name', 'team_abbr'],
                                     right_on=['team_name', 'team_abbr'])

            away_df = pd.merge(games_df, agg_weekly_df, how='inner', left_on=['away_name', 'away_abbr'],
                               right_on=['team_name', 'team_abbr']).drop(columns=['team_name', 'team_abbr']).rename(
                columns={
                    'win_perc': 'away_win_perc',
                    'first_downs': 'away_first_downs', 'fumbles': 'away_fumbles', 'fumbles_lost': 'away_fumbles_lost',
                    'interceptions': 'away_interceptions',
                    'net_pass_yards': 'away_net_pass_yards', 'pass_attempts': 'away_pass_attempts',
                    'pass_completions': 'away_pass_completions',
                    'pass_touchdowns': 'away_pass_touchdowns', 'pass_yards': 'away_pass_yards',
                    'penalties': 'away_penalties', 'points': 'away_points', 'rush_attempts': 'away_rush_attempts',
                    'rush_touchdowns': 'away_rush_touchdowns', 'rush_yards': 'away_rush_yards',
                    'time_of_possession': 'away_time_of_possession', 'times_sacked': 'away_times_sacked',
                    'total_yards': 'away_total_yards', 'turnovers': 'away_turnovers',
                    'yards_from_penalties': 'away_yards_from_penalties',
                    'yards_lost_from_sacks': 'away_yards_lost_from_sacks', 'fourth_down_perc': 'away_fourth_down_perc',
                    'third_down_perc': 'away_third_down_perc'})

            home_df = pd.merge(games_df, agg_weekly_df, how='inner', left_on=['home_name', 'home_abbr'],
                               right_on=['team_name', 'team_abbr']).drop(columns=['team_name', 'team_abbr']).rename(
                columns={
                    'win_perc': 'home_win_perc',
                    'first_downs': 'home_first_downs', 'fumbles': 'home_fumbles', 'fumbles_lost': 'home_fumbles_lost',
                    'interceptions': 'home_interceptions',
                    'net_pass_yards': 'home_net_pass_yards', 'pass_attempts': 'home_pass_attempts',
                    'pass_completions': 'home_pass_completions',
                    'pass_touchdowns': 'home_pass_touchdowns', 'pass_yards': 'home_pass_yards',
                    'penalties': 'home_penalties', 'points': 'home_points', 'rush_attempts': 'home_rush_attempts',
                    'rush_touchdowns': 'home_rush_touchdowns', 'rush_yards': 'home_rush_yards',
                    'time_of_possession': 'home_time_of_possession', 'times_sacked': 'home_times_sacked',
                    'total_yards': 'home_total_yards', 'turnovers': 'home_turnovers',
                    'yards_from_penalties': 'home_yards_from_penalties',
                    'yards_lost_from_sacks': 'home_yards_lost_from_sacks', 'fourth_down_perc': 'home_fourth_down_perc',
                    'third_down_perc': 'home_third_down_perc'})

            agg_weekly_df = pd.merge(away_df, home_df,
                                     left_on=['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
                                              'winning_abbr', 'week'],
                                     right_on=['away_name', 'away_abbr', 'home_name', 'home_abbr', 'winning_name',
                                               'winning_abbr', 'week'])

            agg_weekly_df['win_perc_dif'] = agg_weekly_df['away_win_perc'] - agg_weekly_df['home_win_perc']
            agg_weekly_df['first_downs_dif'] = agg_weekly_df['away_first_downs'] - agg_weekly_df['home_first_downs']
            agg_weekly_df['fumbles_dif'] = agg_weekly_df['away_fumbles'] - agg_weekly_df['home_fumbles']
            agg_weekly_df['interceptions_dif'] = agg_weekly_df['away_interceptions'] - agg_weekly_df[
                'home_interceptions']
            agg_weekly_df['net_pass_yards_dif'] = agg_weekly_df['away_net_pass_yards'] - agg_weekly_df[
                'home_net_pass_yards']
            agg_weekly_df['pass_attempts_dif'] = agg_weekly_df['away_pass_attempts'] - agg_weekly_df[
                'home_pass_attempts']
            agg_weekly_df['pass_completions_dif'] = agg_weekly_df['away_pass_completions'] - agg_weekly_df[
                'home_pass_completions']
            agg_weekly_df['pass_touchdowns_dif'] = agg_weekly_df['away_pass_touchdowns'] - agg_weekly_df[
                'home_pass_touchdowns']
            agg_weekly_df['pass_yards_dif'] = agg_weekly_df['away_pass_yards'] - agg_weekly_df['home_pass_yards']
            agg_weekly_df['penalties_dif'] = agg_weekly_df['away_penalties'] - agg_weekly_df['home_penalties']
            agg_weekly_df['points_dif'] = agg_weekly_df['away_points'] - agg_weekly_df['home_points']
            agg_weekly_df['rush_attempts_dif'] = agg_weekly_df['away_rush_attempts'] - agg_weekly_df[
                'home_rush_attempts']
            agg_weekly_df['rush_touchdowns_dif'] = agg_weekly_df['away_rush_touchdowns'] - agg_weekly_df[
                'home_rush_touchdowns']
            agg_weekly_df['rush_yards_dif'] = agg_weekly_df['away_rush_yards'] - agg_weekly_df['home_rush_yards']
            agg_weekly_df['time_of_possession_dif'] = agg_weekly_df['away_time_of_possession'] - agg_weekly_df[
                'home_time_of_possession']
            agg_weekly_df['times_sacked_dif'] = agg_weekly_df['away_times_sacked'] - agg_weekly_df['home_times_sacked']
            agg_weekly_df['total_yards_dif'] = agg_weekly_df['away_total_yards'] - agg_weekly_df['home_total_yards']
            agg_weekly_df['turnovers_dif'] = agg_weekly_df['away_turnovers'] - agg_weekly_df['home_turnovers']
            agg_weekly_df['yards_from_penalties_dif'] = agg_weekly_df['away_yards_from_penalties'] - agg_weekly_df[
                'home_yards_from_penalties']
            agg_weekly_df['yards_lost_from_sacks_dif'] = agg_weekly_df['away_yards_lost_from_sacks'] - agg_weekly_df[
                'home_yards_lost_from_sacks']
            agg_weekly_df['fourth_down_perc_dif'] = agg_weekly_df['away_fourth_down_perc'] - agg_weekly_df[
                'home_fourth_down_perc']
            agg_weekly_df['third_down_perc_dif'] = agg_weekly_df['away_third_down_perc'] - agg_weekly_df[
                'home_third_down_perc']

            agg_weekly_df = agg_weekly_df.drop(columns=['away_win_perc',
                                                        'away_first_downs', 'away_fumbles', 'away_fumbles_lost',
                                                        'away_interceptions',
                                                        'away_net_pass_yards', 'away_pass_attempts',
                                                        'away_pass_completions',
                                                        'away_pass_touchdowns', 'away_pass_yards', 'away_penalties',
                                                        'away_points', 'away_rush_attempts',
                                                        'away_rush_touchdowns', 'away_rush_yards',
                                                        'away_time_of_possession', 'away_times_sacked',
                                                        'away_total_yards', 'away_turnovers',
                                                        'away_yards_from_penalties',
                                                        'away_yards_lost_from_sacks', 'away_fourth_down_perc',
                                                        'away_third_down_perc', 'home_win_perc',
                                                        'home_first_downs', 'home_fumbles', 'home_fumbles_lost',
                                                        'home_interceptions',
                                                        'home_net_pass_yards', 'home_pass_attempts',
                                                        'home_pass_completions',
                                                        'home_pass_touchdowns', 'home_pass_yards', 'home_penalties',
                                                        'home_points', 'home_rush_attempts',
                                                        'home_rush_touchdowns', 'home_rush_yards',
                                                        'home_time_of_possession', 'home_times_sacked',
                                                        'home_total_yards', 'home_turnovers',
                                                        'home_yards_from_penalties',
                                                        'home_yards_lost_from_sacks', 'home_fourth_down_perc',
                                                        'home_third_down_perc'])

            if agg_weekly_df['winning_name'].isnull().values.any() and weeks > 3:
                agg_weekly_df['result'] = np.nan
                print(f"Week {weeks} games have not finished yet.")
            else:
                agg_weekly_df['result'] = agg_weekly_df['winning_name'] == agg_weekly_df['away_name']
                agg_weekly_df['result'] = agg_weekly_df['result'].astype('float')
            agg_weekly_df = agg_weekly_df.drop(columns=['winning_name', 'winning_abbr'])
            agg_games_df = pd.concat([agg_games_df, agg_weekly_df])
        agg_games_df = agg_games_df.reset_index().drop(columns='index')
        agg_games_df = agg_games_df.drop(index=20, axis=0)

        return agg_games_df

    def create_dataset(self):
        current_week = 18
        weeks = list(range(1, current_week + 1))
        nfl_schedule_df = self.get_nfl_schedule()
        game_stats_for_season = self.get_game_stats_for_season()
        aggregated_game_stats_for_season = self.agg_weekly_data(nfl_schedule_df, game_stats_for_season, current_week, weeks)
        # these rows are removed because they have NaN values in the win percentage (bug due to teams with a tie and
        # no wins)
        aggregated_game_stats_for_season.drop(3, axis=0, inplace=True)
        aggregated_game_stats_for_season.drop(10, axis=0, inplace=True)
        self.convert_df_to_csv(aggregated_game_stats_for_season)

    def convert_df_to_csv(self, dataset):
        dataset.to_csv("2019-NFL-Season-Dataset.csv")


if __name__ == '__main__':
    NFl2019Season = NFLSeasonDatasetCreator()
    NFl2019Season.create_dataset()
