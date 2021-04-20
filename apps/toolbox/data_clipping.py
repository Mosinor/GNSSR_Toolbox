from pydap.client import open_url
from pydap.cas.urs import setup_session
import numpy as np
import wget


def consecutive(data, stepsize=1):
    return np.split(data, np.where(np.diff(data) != stepsize)[0]+1)

opendap_url = 'https://podaac-opendap.jpl.nasa.gov/opendap/hyrax/allData/cygnss/L2/v2.1/2020/001/cyg.ddmi.s20200101-000000-e20200101-235959.l2.wind-mss.a21.d21.nc'

dataset = open_url(opendap_url)
print(dataset)

#latitude = dataset['sp_lat']
#longitude = dataset['sp_lon']

#location = [-24, 78, -18, 80]

#keys_l1 = ['sample', 'ddm', 'spacecraft_id', 'spacecraft_num', 'ddm_source', 'ddm_time_type_selector', 'delay_resolution', 'dopp_resolution', 'ddm_timestamp_utc', 'ddm_timestamp_gps_week', 'ddm_timestamp_gps_sec', 'pvt_timestamp_utc', 'pvt_timestamp_gps_week', 'pvt_timestamp_gps_sec', 'att_timestamp_utc', 'att_timestamp_gps_week', 'att_timestamp_gps_sec', 'sc_pos_x', 'sc_pos_y', 'sc_pos_z', 'sc_vel_x', 'sc_vel_y', 'sc_vel_z', 'sc_pos_x_pvt', 'sc_pos_y_pvt', 'sc_pos_z_pvt', 'sc_vel_x_pvt', 'sc_vel_y_pvt', 'sc_vel_z_pvt', 'nst_att_status', 'sc_roll', 'sc_pitch', 'sc_yaw', 'sc_roll_att', 'sc_pitch_att', 'sc_yaw_att', 'sc_lat', 'sc_lon', 'sc_alt', 'zenith_sun_angle_az', 'zenith_sun_angle_decl', 'zenith_ant_bore_dir_x', 'zenith_ant_bore_dir_y', 'zenith_ant_bore_dir_z', 'rx_clk_bias', 'rx_clk_bias_rate', 'rx_clk_bias_pvt', 'rx_clk_bias_rate_pvt', 'lna_temp_nadir_starboard', 'lna_temp_nadir_port', 'lna_temp_zenith', 'ddm_end_time_offset', 'bit_ratio_hi_lo_starboard', 'bit_ratio_hi_lo_port', 'bit_null_offset_starboard', 'bit_null_offset_port', 'status_flags_one_hz', 'prn_code', 'sv_num', 'track_id', 'ddm_ant', 'zenith_code_phase', 'sp_ddmi_delay_correction', 'sp_ddmi_dopp_correction', 'add_range_to_sp', 'add_range_to_sp_pvt', 'sp_ddmi_dopp', 'sp_fsw_delay', 'sp_delay_error', 'sp_dopp_error', 'fsw_comp_delay_shift', 'fsw_comp_dopp_shift', 'prn_fig_of_merit', 'tx_clk_bias', 'sp_lat', 'sp_lon', 'sp_alt', 'sp_pos_x', 'sp_pos_y', 'sp_pos_z', 'sp_vel_x', 'sp_vel_y', 'sp_vel_z', 'sp_inc_angle', 'sp_theta_orbit', 'sp_az_orbit', 'sp_theta_body', 'sp_az_body', 'sp_rx_gain', 'gps_eirp', 'gps_tx_power_db_w', 'gps_ant_gain_db_i', 'gps_off_boresight_angle_deg', 'direct_signal_snr', 'ddm_snr', 'ddm_noise_floor', 'inst_gain', 'lna_noise_figure', 'rx_to_sp_range', 'tx_to_sp_range', 'tx_pos_x', 'tx_pos_y', 'tx_pos_z', 'tx_vel_x', 'tx_vel_y', 'tx_vel_z', 'bb_nearest', 'radiometric_antenna_temp', 'fresnel_coeff', 'ddm_nbrcs', 'ddm_les', 'nbrcs_scatter_area', 'les_scatter_area', 'brcs_ddm_peak_bin_delay_row', 'brcs_ddm_peak_bin_dopp_col', 'brcs_ddm_sp_bin_delay_row', 'brcs_ddm_sp_bin_dopp_col', 'ddm_brcs_uncert', 'quality_flags', 'raw_counts', 'power_digital', 'power_analog', 'brcs', 'eff_scatter']

#a = (keys_l1[0], keys_l1[0])
#print(a)

#for key in keys_l1:
#    print(key, key)

"""
for ddm in range(1):
    sp_lat = np.array(latitude[:, ddm])
    sp_lon = np.array(longitude[:, ddm])

    indices, zero_array = np.where(
        (sp_lat[:] > location[0])
        & (sp_lon[:] < location[1])
        & (sp_lat[:] < location[2]) &
        (sp_lon[:] < location[3])
    )

    tracks = consecutive(indices)
 
    for track in tracks:
        print([track.min(), track.max()])
        link = opendap_url+".ascii?sp_lat["+str(track.min())+":"+str(track.max())+"]"+"["+str(ddm)+"],sp_lon["+str(track.min())+":"+str(track.max())+"]"+"["+str(ddm)+"]"
        wget.download(link)
    """

