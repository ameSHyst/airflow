FRUIT=$1 # $1 = 입력변수 중 첫 번째 입력변수
if [ $FRUIT == APPLE ]; then
	echo "You selected Apple!"
elif [ $FRUIT == ORANGE ]; then
	echo "You selected Orange!"
elif [ $FRUIT == GRAPE ]; then
	echo "You selected Grape!"
else
	echo "You selected other Fruit!"
fi
