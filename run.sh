#Reading app.conf and cd'ing into App folder
for line in $(cat $(dirname -- "$0")/app.conf)
do
        case "$line" in
                */home*) AppDir="$line" ;;
        esac
done
cd $AppDir

echo "Exported RPIGPIO pin factory and Display"
export GPIOZERO_PIN_FACTORY=RPiGPIO
export DISPLAY=":0"
sleep 2

echo "Taking power into my hands ;D"
python3 powerInMyHands.py &

echo "Starting application"
python3 main.py &
unclutter &
(sleep 30 && python3 mouse_off.py) &
sleep 3 && midori -e fullscreen http://0.0.0.0:8080/ 
