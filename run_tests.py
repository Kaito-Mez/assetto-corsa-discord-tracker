from tests import lap_tests
import main

if __name__ == "__main__":
    lap_tests.run_lap_completed_test(main.on_player_join, main.on_car_info, main.on_lap_completed)