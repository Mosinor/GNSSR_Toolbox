from bootstrap_datepicker_plus import DatePickerInput, TimePickerInput, DateTimePickerInput
from leaflet.forms.widgets import LeafletWidget
from django.contrib.gis import forms


keys_l1 = ['sample', 'ddm', 'spacecraft_id', 'spacecraft_num', 'ddm_source', 'ddm_time_type_selector',
           'delay_resolution', 'dopp_resolution', 'ddm_timestamp_utc', 'ddm_timestamp_gps_week',
           'ddm_timestamp_gps_sec', 'pvt_timestamp_utc', 'pvt_timestamp_gps_week', 'pvt_timestamp_gps_sec',
           'att_timestamp_utc', 'att_timestamp_gps_week', 'att_timestamp_gps_sec', 'sc_pos_x', 'sc_pos_y', 'sc_pos_z',
           'sc_vel_x', 'sc_vel_y', 'sc_vel_z', 'sc_pos_x_pvt', 'sc_pos_y_pvt', 'sc_pos_z_pvt', 'sc_vel_x_pvt',
           'sc_vel_y_pvt', 'sc_vel_z_pvt', 'nst_att_status', 'sc_roll', 'sc_pitch', 'sc_yaw', 'sc_roll_att',
           'sc_pitch_att', 'sc_yaw_att', 'sc_lat', 'sc_lon', 'sc_alt', 'zenith_sun_angle_az', 'zenith_sun_angle_decl',
           'zenith_ant_bore_dir_x', 'zenith_ant_bore_dir_y', 'zenith_ant_bore_dir_z', 'rx_clk_bias', 'rx_clk_bias_rate',
           'rx_clk_bias_pvt', 'rx_clk_bias_rate_pvt', 'lna_temp_nadir_starboard', 'lna_temp_nadir_port',
           'lna_temp_zenith', 'ddm_end_time_offset', 'bit_ratio_hi_lo_starboard', 'bit_ratio_hi_lo_port',
           'bit_null_offset_starboard', 'bit_null_offset_port', 'status_flags_one_hz', 'prn_code', 'sv_num', 'track_id',
           'ddm_ant', 'zenith_code_phase', 'sp_ddmi_delay_correction', 'sp_ddmi_dopp_correction', 'add_range_to_sp',
           'add_range_to_sp_pvt', 'sp_ddmi_dopp', 'sp_fsw_delay', 'sp_delay_error', 'sp_dopp_error',
           'fsw_comp_delay_shift', 'fsw_comp_dopp_shift', 'prn_fig_of_merit', 'tx_clk_bias', 'sp_lat', 'sp_lon',
           'sp_alt', 'sp_pos_x', 'sp_pos_y', 'sp_pos_z', 'sp_vel_x', 'sp_vel_y', 'sp_vel_z', 'sp_inc_angle',
           'sp_theta_orbit', 'sp_az_orbit', 'sp_theta_body', 'sp_az_body', 'sp_rx_gain', 'gps_eirp',
           'gps_tx_power_db_w', 'gps_ant_gain_db_i', 'gps_off_boresight_angle_deg', 'direct_signal_snr', 'ddm_snr',
           'ddm_noise_floor', 'inst_gain', 'lna_noise_figure', 'rx_to_sp_range', 'tx_to_sp_range', 'tx_pos_x',
           'tx_pos_y', 'tx_pos_z', 'tx_vel_x', 'tx_vel_y', 'tx_vel_z', 'bb_nearest', 'radiometric_antenna_temp',
           'fresnel_coeff', 'ddm_nbrcs', 'ddm_les', 'nbrcs_scatter_area', 'les_scatter_area',
           'brcs_ddm_peak_bin_delay_row', 'brcs_ddm_peak_bin_dopp_col', 'brcs_ddm_sp_bin_delay_row',
           'brcs_ddm_sp_bin_dopp_col', 'ddm_brcs_uncert', 'quality_flags', 'raw_counts', 'power_digital',
           'power_analog', 'brcs', 'eff_scatter']

keys_l2 = ['sample', 'ddm', 'averaged_l1', 'ddm_source', 'spacecraft_id', 'spacecraft_num', 'prn_code', 'sv_num',
           'antenna', 'sample_time', 'lat', 'lon', 'sc_lat', 'sc_lon', 'sc_alt', 'wind_speed', 'fds_nbrcs_wind_speed',
           'fds_les_wind_speed', 'yslf_nbrcs_wind_speed', 'yslf_les_wind_speed', 'yslf_nbrcs_wind_speed_uncertainty',
           'yslf_les_wind_speed_uncertainty', 'wind_speed_uncertainty', 'azimuth_angle', 'mean_square_slope',
           'mean_square_slope_uncertainty', 'incidence_angle', 'nbrcs_mean', 'les_mean', 'range_corr_gain',
           'fresnel_coeff', 'num_ddms_utilized', 'sample_flags', 'fds_sample_flags', 'yslf_sample_flags',
           'sum_neg_brcs_value_used_for_nbrcs_flags', 'ddm_obs_utilized_flag', 'ddm_sample_index',
           'ddm_num_averaged_l1', 'ddm_channel', 'ddm_les', 'ddm_nbrcs']

keys_l3 = ['time', 'lat', 'lon', 'wind_speed', 'wind_speed_uncertainty', 'num_wind_speed_samples', 'yslf_wind_speed',
           'yslf_wind_speed_uncertainty', 'num_yslf_wind_speed_samples', 'mean_square_slope',
           'mean_square_slope_uncertainty', 'num_mss_samples']


class TrackDemoTool(forms.Form):
    grid = forms.PolygonField(widget=LeafletWidget(), required=False)
    coordinate_a = forms.CharField()
    coordinate_b = forms.CharField()
    date = forms.DateField(widget=DatePickerInput().start_of('event days'))
    start_time = forms.TimeField(widget=TimePickerInput().start_of('event days'))
    end_time = forms.TimeField(widget=TimePickerInput().start_of('event days'))
    level = forms.ChoiceField(choices=[('L1', 'L1'), ('L2', 'L2'), ('L3', 'L3')])
    version = forms.ChoiceField(choices=[('v2.1', 'v2.1'), ('v3.0', 'v3.0')])

    def clean(self):
        cleaned_data = super(TrackDemoTool, self).clean()


class DataClippingTool(forms.Form):
    grid = forms.PolygonField(widget=LeafletWidget(), required=False)
    coordinate_a = forms.CharField()
    coordinate_b = forms.CharField()
    start_date = forms.DateTimeField(widget=DateTimePickerInput().start_of('event days'))
    end_date = forms.DateTimeField(widget=DateTimePickerInput().start_of('event days'))
    level = forms.ChoiceField(choices=[('1', 'L1'), ('2', 'L2'), ('3', 'L3')])
    version = forms.ChoiceField(choices=[('2', 'v2.1'), ('3', 'v3.0')])
    keys_level1 = forms.MultipleChoiceField(choices=[(key, key) for key in keys_l1])
    keys_level2 = forms.MultipleChoiceField(choices=[(key, key) for key in keys_l2])
    keys_level3 = forms.MultipleChoiceField(choices=[(key, key) for key in keys_l3])

    def clean(self):
        cleaned_data = super(DataClippingTool, self).clean()
