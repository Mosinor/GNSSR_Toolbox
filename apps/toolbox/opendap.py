from pydap.client import open_url
import numpy as np


def generate_url(date, level, version):

    if version == "2":
        version = "v2.1"
    elif version == "3":
        version = "v3.0"

    opendap_url = []
    base_url = "https://podaac-opendap.jpl.nasa.gov/opendap/hyrax/allData/cygnss/"+level+"/"+version+"/"
    date_string = str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2)
    if version == "v2.1":
        v = "a21.d21"
    elif version == "v3.0":
        v = "a30.d31"

    if level == "L1":
        for satellite_number in range(8):
            specific_url = "/cyg0" + str(satellite_number+1) + ".ddmi.s" + date_string + "-000000-e" + date_string + "-235959.l1.power-brcs."+v+".nc"
            opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    elif level == "L2":
        specific_url = "/cyg.ddmi.s" + date_string + "-000000-e" + date_string + "-235959.l2.wind-mss."+v+".nc"
        opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    elif level == "L3":
        if version == "v2.1":
            v = "a10.d21"
        specific_url = "/cyg.ddmi.s" + date_string + "-003000-e" + date_string + "-233000.l3.grid-wind."+v+".nc"
        opendap_url.append(base_url + str(date.year) + "/" + str(date.timetuple().tm_yday).zfill(3) + specific_url)

    return opendap_url


def collect_dataset(url):
    try:
        dataset = open_url(url, output_grid=False, timeout=30)
    except:
        dataset = None
    return dataset


def define_dataset_keys(level):
    if level == "L1":
        keys = ['sample', 'ddm', 'spacecraft_id', 'spacecraft_num', 'ddm_source', 'ddm_time_type_selector', 'delay_resolution', 'dopp_resolution', 'ddm_timestamp_utc', 'ddm_timestamp_gps_week', 'ddm_timestamp_gps_sec', 'pvt_timestamp_utc', 'pvt_timestamp_gps_week', 'pvt_timestamp_gps_sec', 'att_timestamp_utc', 'att_timestamp_gps_week', 'att_timestamp_gps_sec', 'sc_pos_x', 'sc_pos_y', 'sc_pos_z', 'sc_vel_x', 'sc_vel_y', 'sc_vel_z', 'sc_pos_x_pvt', 'sc_pos_y_pvt', 'sc_pos_z_pvt', 'sc_vel_x_pvt', 'sc_vel_y_pvt', 'sc_vel_z_pvt', 'nst_att_status', 'sc_roll', 'sc_pitch', 'sc_yaw', 'sc_roll_att', 'sc_pitch_att', 'sc_yaw_att', 'sc_lat', 'sc_lon', 'sc_alt', 'zenith_sun_angle_az', 'zenith_sun_angle_decl', 'zenith_ant_bore_dir_x', 'zenith_ant_bore_dir_y', 'zenith_ant_bore_dir_z', 'rx_clk_bias', 'rx_clk_bias_rate', 'rx_clk_bias_pvt', 'rx_clk_bias_rate_pvt', 'lna_temp_nadir_starboard', 'lna_temp_nadir_port', 'lna_temp_zenith', 'ddm_end_time_offset', 'bit_ratio_hi_lo_starboard', 'bit_ratio_hi_lo_port', 'bit_null_offset_starboard', 'bit_null_offset_port', 'status_flags_one_hz', 'prn_code', 'sv_num', 'track_id', 'ddm_ant', 'zenith_code_phase', 'sp_ddmi_delay_correction', 'sp_ddmi_dopp_correction', 'add_range_to_sp', 'add_range_to_sp_pvt', 'sp_ddmi_dopp', 'sp_fsw_delay', 'sp_delay_error', 'sp_dopp_error', 'fsw_comp_delay_shift', 'fsw_comp_dopp_shift', 'prn_fig_of_merit', 'tx_clk_bias', 'sp_lat', 'sp_lon', 'sp_alt', 'sp_pos_x', 'sp_pos_y', 'sp_pos_z', 'sp_vel_x', 'sp_vel_y', 'sp_vel_z', 'sp_inc_angle', 'sp_theta_orbit', 'sp_az_orbit', 'sp_theta_body', 'sp_az_body', 'sp_rx_gain', 'gps_eirp', 'gps_tx_power_db_w', 'gps_ant_gain_db_i', 'gps_off_boresight_angle_deg', 'direct_signal_snr', 'ddm_snr', 'ddm_noise_floor', 'inst_gain', 'lna_noise_figure', 'rx_to_sp_range', 'tx_to_sp_range', 'tx_pos_x', 'tx_pos_y', 'tx_pos_z', 'tx_vel_x', 'tx_vel_y', 'tx_vel_z', 'bb_nearest', 'radiometric_antenna_temp', 'fresnel_coeff', 'ddm_nbrcs', 'ddm_les', 'nbrcs_scatter_area', 'les_scatter_area', 'brcs_ddm_peak_bin_delay_row', 'brcs_ddm_peak_bin_dopp_col', 'brcs_ddm_sp_bin_delay_row', 'brcs_ddm_sp_bin_dopp_col', 'ddm_brcs_uncert', 'quality_flags', 'raw_counts', 'power_digital', 'power_analog', 'brcs', 'eff_scatter']
    elif level == "L2":
        keys = ['111','aaaa']
    else:
        keys = ['Lol']



def clock_to_seconds(time):
    return sum(x * int(t) for x, t in zip([3600, 60, 1], str(time).split(":")))


# Filters the coordinate data based on user input and separates them into tracks.
def filter_valid_points_time_specific_level1(dataset, lats, lons, start_time, end_time):
    sat_num = np.array(dataset.spacecraft_num)
    track_list = []
    current_track = []
    previous_timestamp = -9
    previous_ddm = -9

    for ddm in range(4):
        sp_lat = np.array(dataset.sp_lat[start_time:end_time, ddm])
        sp_lon = np.array(dataset.sp_lon[start_time:end_time, ddm])
        for ddm_timestamp, latitude in enumerate(sp_lat):
            if min(lats) <= latitude <= max(lats):
                longitude = sp_lon[ddm_timestamp][0]
                if min(lons) <= longitude <= max(lons):
                    measure = [latitude[0], longitude, ddm_timestamp+start_time, ddm, int(sat_num)]
                    if not previous_timestamp + 1 == measure[2] or not measure[3] == previous_ddm:
                        track_list.append(current_track)
                        current_track = [measure]
                    else:
                        current_track.append(measure)

                    previous_ddm = measure[3]
                    previous_timestamp = measure[2]

    if track_list:
        del track_list[0]
        track_list.append(current_track)

    return track_list


# Filters the coordinate data based on user input and separates them into tracks.
#def filter_valid_points_time_specific_level2(dataset, lats, lons, start_time, end_time):
    #sat_num = np.array(dataset.spacecraft_num)
    #track_list = []
    #current_track = []
    #previous_timestamp = -9
    #previous_ddm = -9

    #for ddm in range(4):
    #    lat = np.array(dataset.lat.lat)
    #    lon = np.array(dataset.lon.lon)

        #for ddm_timestamp, latitude in enumerate(sp_lat):
        #    if min(lats) <= latitude <= max(lats):
        #        longitude = sp_lon[ddm_timestamp][0]
        #        if min(lons) <= longitude <= max(lons):
        #            measure = [latitude[0], longitude, ddm_timestamp+start_time, ddm, int(sat_num)]
        #            if not previous_timestamp + 1 == measure[2] or not measure[3] == previous_ddm:
        #                track_list.append(current_track)
        #                current_track = [measure]
        #            else:
        #                current_track.append(measure)
        #
        #            previous_ddm = measure[3]
        #           previous_timestamp = measure[2]

    #if track_list:
    #    del track_list[0]
    #    track_list.append(current_track)

    #return track_list
