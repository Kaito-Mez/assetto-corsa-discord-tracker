import main
if __name__ == "__main__":

    lap_data = str({'car_id': 0, 'laptime': 103119, 'cuts': 4, 'cars_count': 17, 'grip_level': 1, 'leaderboard': [{'car_id': 0, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 1, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 2, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 3, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 4, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 5, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 6, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 7, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 8, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 9, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 10, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 11, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 12, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 13, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}, {'car_id': 14, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 15, 'laptime': 999999999, 'laps': 0, 'completed': False}, {'car_id': 16, 'laptime': 999999999, 
                    'laps': 0, 'completed': False}]})

    main.on_lap_completed(lap_data)