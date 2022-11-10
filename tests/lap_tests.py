



def run_lap_completed_test(on_player_join, on_car_info, on_lap_completed):
    '''Pass on_lap_completed() as a parameter'''

    join_data = ({'car_id': 0})

    car_data = ({'car_id': 0, 'is_connected': True, 'car_model': 'bksy_nissan_skyline_r34_z_tune', 'car_skin': '01_midnight_purple_3', 'driver_name': 'A Tilted ~', 'driver_team': '', 'driver_guid': '76561198249901870'})

    lap_data = ({'car_id': 0, 'laptime': 103119, 'cuts': 4, 'cars_count': 17, 'grip_level': 1, 'leaderboard': [{'car_id': 0, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 1, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 2, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 3, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 4, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 5, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 6, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 7, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 8, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 9, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 10, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 11, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 12, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 13, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 14, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 15, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 16, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}]})

    
    on_player_join(join_data)
    on_car_info(car_data)
    on_lap_completed(lap_data)