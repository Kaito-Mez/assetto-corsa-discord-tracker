import random



def run_lap_completed_test(on_session_start, on_player_join, on_car_info, on_lap_completed, on_player_leave, on_session_end):
    '''Pass on_lap_completed() as a parameter'''

    session_data = {'version': 4, 'session_index': 1, 'current_session_index': 1, 'session_count': 3, 'server_name': 'Project D Prototype x:Len7PR', 'track': 'ks_brands_hatch', 'track_config': 'indy', 'name': random.choice(["Qualification", "Practice", "Race"]), 
                    'type': 2, 'time': 10, 'laps': 0, 'wait_time': 0, 'ambient_temp': 18, 'road_temp': 26, 'weather_graphics': 'sol_00_no_clouds_type=15_time=30655', 'elapsed_ms': 0}

    join_data = ({'car_id': 0})

    leave_data = ({'driver_name': 'A Tilted ~', 'driver_guid': '76561198249901870', 'car_id': 0, 'car_model': 'bksy_nissan_skyline_r34_z_tune', 'car_skin': '01_midnight_purple_3'})

    car_data = ({'car_id': 0, 'is_connected': True, 'car_model': 'bksy_nissan_skyline_r34_z_tune', 'car_skin': '01_midnight_purple_3', 'driver_name': 'A Tilted ~', 'driver_team': '', 'driver_guid': '76561198249901870'})

    lap_data = ({'car_id': 0, 'laptime': random.randrange(60000, 999999), 'cuts': 4, 'cars_count': 17, 'grip_level': 1, 'leaderboard': [{'car_id': 0, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 1, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 2, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 3, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 4, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 5, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 6, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 7, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 8, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 9, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 10, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 11, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 12, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 13, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 14, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 15, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 16, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}]})

    end_data = {"filename": None}

    on_session_start(session_data)
    on_player_join(join_data)
    on_car_info(car_data)
    on_lap_completed(lap_data)
    #on_player_leave(leave_data)
    on_session_end(end_data)
