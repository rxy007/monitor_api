## 此服务是定时监控线上api接口是否正常 如果接口出现异常 则发邮件通知

使用方法 编写py文件 放到tasks目录即可 主程序会定时更新添加和删除的任务

## 定时监控的实现参考tasks下现有的例子 其中cron 和 run这两个属性是必须的 

## 部署方式

source /opt/envir/minicoda3/bin/activate

###开始任务

./deploy

./deploy start

###重新开始

./deploy restart


###停止任务

./deploy stop
#### 此项目已经部署到新测试环境的/appletree/nlp_service/service/monitor_api目录下了


