pkill monetdb
pkill mserver5
./exec.sh

python3 YeSQL_MonetDB/cffi_wrappers/build.py
python3 YeSQL_MonetDB/monetdb.py -d fldb -H localhost -P 50000 -u monetdb -p monetdb