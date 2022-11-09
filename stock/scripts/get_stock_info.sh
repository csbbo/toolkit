#! /bin/bash

# shellcheck disable=SC2071
if [[ $# < 1 ]]; then
    echo "Useage: v <query1> <query2> ..."
    # shellcheck disable=SC2242
    exit -1
fi

is_first="true"
for i in $*
do
    if [[ $is_first == "true" ]]; then
        # 删除换行符, 中文编码, ...
        param+="?search="`echo $i | tr -d '\n' | xxd -plain | sed 's/\(..\)/%\1/g'`
    else
        param+="&search="`echo $i | tr -d '\n' | xxd -plain | sed 's/\(..\)/%\1/g'`
    fi
    is_first="false"
done
#curl "http://127.0.0.1:8000/api/stock/stock/info/"$param
curl "http://60.205.223.161:9000/api/stock/stock/info/"$param
echo ""
