"""
Copyright (C) 2018 contributors listed in AUTHORS.

tvdisaggregator.py
~~~~~

Contains the class TVDisaggregator which is responsible for performing
the full disaggregation of the storage operation.
"""
import sys
import pandas as pd
import numpy as np

from storedisagg import ComponentCalculator

try:
    from tqdm import tqdm
except:
    # no fancy progress bars today
    tqdm = lambda x: x

class StDisaggregator():


    def __init__(self, df, eff, kind):

        self.eff = eff
        self.df = df
        self.kind = kind

    def run(self):

        # result dataframes
        self.df_full = None
        self.df_step_evts = None

        # aggregating dataframes
        self.df_full_all = pd.DataFrame()
        self.df_step_evts_all = pd.DataFrame()


        self.calc_internal_power()
        self.calc_state_of_charge()

        self.shift_profiles()
        self.set_small_to_zero()


        #

        erg = self.df.erg.values
#        erg[erg < 2e-4] = 0
        erg = np.diff(np.concatenate([np.array([erg[-1]]), erg]))
        self.df['ichg_fix'] = self.df['idch_fix'] = erg
        self.df['ichg'] = self.df.ichg_fix.where(self.df.ichg_fix > 0, 0)
        self.df['idch'] = - self.df.idch_fix.where(self.df.idch_fix < 0, 0)
#



        self.init_result_dfs()

        # calculate aggregate iterations
        self.iterate_event_aggregation()

        # get hourly components by looping over event rows
        self.loop_get_hourly_components()

        # calculate final results consisting in time differences and
        # component values
        self.calc_final_results()

        self.generate_stacked_tables()

    def calc_internal_power(self):

        self.df = self.df.rename(columns={'chg': 'echg',
                                          'dch': 'edch'})

        self.df['ichg'] = self.df['echg'] * np.sqrt(self.eff)
        self.df['idch'] = self.df['edch'] / np.sqrt(self.eff)

        # check equality
#        sum_chg = round(self.df.ichg.sum())
#        sum_dch = round(self.df.idch.sum())
#        assert sum_chg == sum_dch, \
#            'Charging doesn\'t match discharging: %f != %f'%(sum_chg, sum_dch)

    def calc_state_of_charge(self):
        '''
        Calculate state-of-charge column erg (units of energy)
        '''

        # calculate SOC
        self.df['erg'] = (self.df.ichg - self.df.idch).cumsum()

        # remove any offset such that the minimum of erg is 0
        self.df['erg'] -= self.df.erg.min()

    def shift_profiles(self):
        '''
        We want a point of zero state of charge to be at the very beginning.
        '''

        self.zero_sy = self.df.loc[self.df.erg == 0, 'sy'].iloc[-1]
        # shift zero erg to time slot zero
        df_2 = self.df.loc[self.df.sy > self.zero_sy]
        df_1 = self.df.loc[self.df.sy <= self.zero_sy]
        self.df = pd.concat([df_2, df_1], sort=True)

        # reset sy column
        self.df = self.df.rename(columns={'sy': 'sy_orig'})
        self.df = (self.df.reset_index(drop=True)
                          .reset_index()
                          .rename(columns={'index': 'sy'}))

    def set_small_to_zero(self):

        self.df.loc[self.df.idch.abs() < 1e-9, 'idch'] = 0
        self.df.loc[self.df.ichg.abs() < 1e-9, 'ichg'] = 0

    def init_result_dfs(self):

        # hourly dataframe df_full to be filled with hourly components
        self.df_full = self.df.rename(columns={'sy': 'slot'})
        for minmax in ['min', 'max']:
            self.df_full['slot_%s'%minmax] = self.df_full['slot']

        # step dataframe with 1 row per charging/discharging pair
        # this is iteration zero of the disaggregation
        self.df_step_evts = self.aggregate_events(self.df_full, 0)
        self.df_step_evts['iteration'] = 0



    def generate_stacked_tables(self):

        # stack df_full table
        self.df_full = self.df_full.drop(['idch', 'ichg'], axis=1) # residuals
        self.df_full = self.df_full.set_index([c for c in self.df_full.columns
                                               if not
                                               any(['_' + str(ii) in c
                                                    for ii in range(100)])])
        self.df_full.columns = [(int(c.split('_')[1]), c.split('_')[0])
                                for c in self.df_full.columns]

        self.df_full.columns = pd.MultiIndex.from_tuples(self.df_full.columns)
        self.df_full = self.df_full.stack(level=0)
        self.df_full = self.df_full.reset_index()

        self.df_full = self.df_full.rename(columns={[c for c in
                                                     self.df_full.columns
                                                     if 'level_' in c][0]:
                                                    'iteration'})
        self.df_full['kind'] = self.kind
        self.df_step_evts['kind'] = self.kind


    def calc_final_results(self):

        self.df_step_evts['time_diff_icd'] = (
                self.df_step_evts.wgt_center_erg_idch
                - self.df_step_evts.wgt_center_erg_ichg)
        self.df_step_evts['ival_comp_net'] = (
                self.df_step_evts.val_comp_idch
                - self.df_step_evts.val_comp_ichg)
        self.df_step_evts['eval_comp_net'] = (
                self.df_step_evts.val_comp_idch * np.sqrt(self.eff)
                - 1/np.sqrt(self.eff) * self.df_step_evts['val_comp_ichg'])

        self.df_step_evts['eff'] = self.eff

        tot_net_value_input = self.df_step_evts.eval_comp_net.sum()
        tot_net_value_disagg = ((self.df['idch'] * np.sqrt(self.eff)
                                 * self.df['mc']).sum()
                                - (self.df['ichg'] / np.sqrt(self.eff)
                                   * self.df['mc']).sum())
        print('Net value input: {}'.format(tot_net_value_input))
        print('Net value disagg: {}'.format(tot_net_value_disagg))
        print('Difference net value: {}'.format(tot_net_value_input
                                                - tot_net_value_disagg))
        sys.stdout.flush()


    def loop_get_hourly_components(self):

        irow =  0
        for irow in tqdm(range(len(self.df_step_evts))):
            dict_row = self.df_step_evts.iloc[irow].to_dict()

            base_str = '; kind = {}; event {} out of {}; slot ({}, {})'
            base_str = base_str.format(self.kind, dict_row['nevent'],
                                       self.df_step_evts.iloc[-1].nevent,
                                       dict_row['slot_min'],
                                       dict_row['slot_max'])

            mask_evt = self.df_step_evts.nevent == dict_row['nevent']
            iiter = dict_row['iteration']

            # select subset of hourly table
            smin = dict_row['slot_min']
            smax = dict_row['slot_max']
            df_slct = self.df_full.loc[smin:smax].copy()

            self.df_full.loc[smin:smax,
                        'nevent_' + str(int(iiter))] = dict_row['nevent']

            dr = 'idch'
            for dr in ['idch', 'ichg']:

                # select residual profile
                y = df_slct.copy()[dr]
                y.loc[y < 0] = 0
                y.loc[np.abs(y) < 1e-10] = 0

                val_tgt = dict_row['comp_' + dr]

                comp_col = dr + '_' + str(int(iiter))

                # get new component
                self.compcal = ComponentCalculator(y, val_tgt,
                                                            self.kind, dr)

                df_slct.loc[:, comp_col] = self.compcal.ycomp

                self.df_slct = df_slct
                self.comp_col = comp_col

                df_slct['wgt_slots_erg_' + dr] = (df_slct['slot']
                                                  * df_slct[comp_col])
                df_slct['value_' + dr] = df_slct['mc'] * df_slct[comp_col]

                self.df_step_evts.loc[mask_evt, 'wgt_center_erg_' + dr] = (
                    df_slct['wgt_slots_erg_' + dr].sum()
                    / df_slct[comp_col].sum())
                self.df_step_evts.loc[mask_evt, 'val_comp_' + dr] = (
                    df_slct['value_' + dr].sum())

                # subtract component from residual profile
                df_slct[dr] -= df_slct[dr + '_' + str(int(iiter))]

                self.df_full.loc[smin:smax, dr] = df_slct[dr]
                self.df_full.loc[smin:smax,
                            comp_col] = df_slct[dr + '_' + str(int(iiter))]


                mask_evt = self.df_step_evts.nevent == dict_row['nevent']
                self.df_step_evts.loc[mask_evt, dr + '_final'] = \
                        self.df_full.loc[smin:smax, comp_col].sum()

    def iterate_event_aggregation(self):
        '''
        Iterate block aggregation.

        Note: Iteration 0 corresponds to profile aggregation and is called
        separately.
        '''


        # copy first aggregated table as input to first iteration
        df_step_evts_add = self.df_step_evts.copy()
        iteration = 1
        while len(df_step_evts_add) > 1:

            df_step_evts_input = df_step_evts_add[['nevent', 'res_ichg',
                                                   'res_idch', 'slot_min',
                                                   'slot_max']]

            df_step_evts_input = df_step_evts_input.rename(
                                    columns={'nevent': 'slot',
                                             'res_ichg': 'ichg',
                                             'res_idch': 'idch'})
            nevent_offset = df_step_evts_input.slot.max()
            df_step_evts_add = self.aggregate_events(df_step_evts_input,
                                                     offset=nevent_offset)
            df_step_evts_add['iteration'] = int(iteration)
            iteration += 1

            if df_step_evts_add[['comp_ichg', 'comp_idch']].sum().sum() > 0:
                list_df = [self.df_step_evts, df_step_evts_add]
                self.df_step_evts = pd.concat(list_df, axis=0, sort=True)

        # comp_dch and comp_chg must add up to the original chg and dch
        print('Difference idch (events - total):',
              (self.df_step_evts['comp_idch'].sum()
               - self.df_full['idch'].sum()))
        print('Difference ichg (events - total):',
              (self.df_step_evts['comp_ichg'].sum()
               - self.df_full['ichg'].sum()))
        sys.stdout.flush()


        self.df_full['ichg_all'] = self.df_full.ichg
        self.df_full['idch_all'] = self.df_full.idch

        # sumcheck: all of these should be equal
        self.df_full[['ichg_all', 'idch_all', 'ichg', 'idch']].sum()

        self.df_step_evts = self.df_step_evts.reset_index(drop=True)


    def _add_dummy_rows(self, df):
        '''
        add first and last zero row
        '''

        dummy_0 = pd.DataFrame(np.array([[df.slot.min() - 1, 0, 0]]),
                               columns=['slot', 'ichg', 'idch'])
        dummy_end = pd.DataFrame(np.array([[df.slot.max() + 1, 0, 0]]),
                                 columns=['slot', 'ichg', 'idch'])

        list_dummy_slots = dummy_0.slot.tolist() + dummy_end.slot.tolist()

        return pd.concat([dummy_0, df, dummy_end], sort=True), list_dummy_slots


    def aggregate_events(self, df, offset=0):
        '''
        Aggregate components either from original profiles
        or subsequent residuals.

        Input dataframe columns: ['slot', 'ichg', 'idch']
        '''

        assert all(c in df.columns for c in ['slot', 'slot_min', 'slot_max',
                                             'ichg', 'idch']), \
                'aggregate_events: Incomplete input dataframe'


        df, list_dummy_rows = self._add_dummy_rows(df)

        # get onsets of charging/discharging events
        cut_0 = lambda x: max(x, 0)
        df.loc[:, 'ichg_bin'] = (df['ichg'] > 0).apply(int).diff().apply(cut_0)
        df.loc[:, 'idch_bin'] = (df['idch'] > 0).apply(int).diff().apply(cut_0)
                                                  # fillna due to diff
        df = df.loc[-df.slot.isin(list_dummy_rows)].fillna(0)

        # filter by onset charging/discharging
        col_slct = ['slot', 'ichg_bin', 'idch_bin']
        df_chgs = df.loc[(df.ichg_bin + df.idch_bin) > 0, col_slct]
        df_chgs = df_chgs.loc[(df_chgs.ichg_bin.shift(1) != df_chgs.ichg_bin) &
                              (df_chgs.idch_bin.shift(1) != df_chgs.idch_bin)]

        df = (df.drop(['ichg_bin', 'idch_bin'], axis=1)
                .join(df_chgs.set_index('slot'), on='slot')
                .fillna(0))

        df['nevent'] = df.ichg_bin.cumsum()
        df.loc[df['nevent'] == 0, ['nevent']] = 1
        df['nevent'] += offset

        # get total energy as well as min/max slot -> rows of df_step_evts
        def calc_events(dfevts, dr):
            dfevts = dfevts.reset_index()
            return dfevts.pivot_table(index=['nevent'],
                                      values=[dr, 'slot_min', 'slot_max'],
                                      aggfunc={dr: sum,
                                               'slot_min': min,
                                               'slot_max': max}).reset_index()

        list_df_cd = [df.groupby('nevent')
                        .apply(lambda x: calc_events(x, icd))
                        .reset_index(level=0, drop=True)
                        .reset_index() for icd in ['ichg', 'idch']]
        list_df_cd[1] = list_df_cd[1]['idch']

        df_evts = pd.concat(list_df_cd, axis=1)
        df_evts = df_evts.drop('index', axis=1)

        # calculate component energy from minima
        df_evts['min'] = df_evts[['ichg', 'idch']].min(axis=1)
        df_evts['comp_ichg'] = df_evts['comp_idch'] = df_evts['min']
        df_evts['res_ichg'] = df_evts['ichg'] - df_evts['comp_ichg']
        df_evts['res_idch'] = df_evts['idch'] - df_evts['comp_idch']

        df_evts.loc[df_evts.res_ichg < 1e-3, 'res_ichg'] = 0
        df_evts.loc[df_evts.res_idch < 1e-3, 'res_idch'] = 0

        return df_evts


    def final_tables_to_sql(self):
        ''' Writes the two result tables to the database. '''


        for itb in ['step_evts_all', 'full_all']:

            aql.joinon(self.db, ['pp', 'nd_id'], ['pp_id'],
                       [self.sc_out, itb], [self.sc, 'def_plant'])

            aql.joinon(self.db, ['nd'], ['nd_id'],
                       [self.sc_out, itb], [self.sc, 'def_node'])


