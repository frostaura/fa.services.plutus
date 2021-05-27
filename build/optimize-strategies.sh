while getopts e: flag
do
    case "${flag}" in
        e) epochs=${OPTARG};;
    esac
done

echo "Initialing hyperopts for all strategies with $epochs epochs."