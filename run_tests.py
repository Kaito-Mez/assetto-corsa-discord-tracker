from tests import socket_tests
from tests import dao_tests
import main
import dao

if __name__ == "__main__":
    '''socket_tests.run_lap_completed_test(
        main.on_session_start,
        main.on_player_join, 
        main.on_car_info, 
        main.on_lap_completed,
        main.on_player_leave
        )'''

    dao = dao.Dao("laps.json")
    dao_tests.load_dataframe_test(dao)