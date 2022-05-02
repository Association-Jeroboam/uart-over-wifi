tar -czvf build.tar.gz -C ../MotionBoardFirmware/firmware/src/hardware/robot ./cfg ./build/MotionBoard.bin
poetry run python uart_over_wifi/client.py --flash ./build.tar.gz $1
