#!/bin/bash
actions=("start" "restart" "stop")
action="start"
pidFile="_pid"

if [ "$1" != "" ] && [ "$1" = "-h" ]; then
    echo "./deploy.sh [action]"
    echo "action: start, clone, restart, stop"
    echo "action default start"
    exit 0
fi

if [ "$#" -gt "1" ]; then
    echo "最多支持一个参数"
    exit 1
elif [ "$#" -eq "1" ]; then
    action=$1
fi



start() {
    echo "启动定时任务..."
    python main.py &
    echo "启动成功."

}

stop() {
    echo "开始停止模型..."
    if [ -e $pidFile ]; then
        while read line
        do
            kill -9 $line
        done < $pidFile

        rm -rf _pid
    fi
    echo "模型已停止."
}

check

if [ $action = "start" ]; then
    start
elif [ $action = "stop" ]; then
    stop
elif [ $action = "restart" ]; then
    stop
    start
fi
