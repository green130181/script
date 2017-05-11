for((i=1;i<1000000;i++))
do
    echo "in" $i
    adb shell monkey -v 5000000
done
