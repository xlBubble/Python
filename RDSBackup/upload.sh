#!/bin/bash
#date:2019-06-03 15:25:30
#auth:xule
#usage:download backup_url and upload it to oss
#version: v1.0

FILEPATH=$1
URL=$2
FILENAME=`echo ${URL##*/}|awk -F? '{print $1}'`
LOGFILE=baklog\_`date +%Y%m%d`
BAKPATH=tmp
LOGPATH=logs
BUCKET=oss://roadoordsbackup/full

if [ $USER != root ];then echo "`date +%F' '%T` - $0 - DEBUG: 请使用root用户执行" >> $LOGPATH/$LOGFILE;exit 1; fi
[ -d $FILEPATH/$BAKPATH  ] || mkdir -p $FILEPATH/$BAKPATH
[ -d $FILEPATH/$LOGPATH  ] || mkdir $FILEPATH/$LOGPATH

cd $FILEPATH

# '%(asctime)s - %(filename)s - %(levelname)s: %(message)s'
upload(){
	echo "`date +%F' '%T` - $0 - INFO: 正在上传文件：$FILENAME" >> $LOGPATH/$LOGFILE
	./ossutil64 cp --retry-times=100 --disable-crc64  $1 $BUCKET/$FILENAME &> /dev/null
	if [ $? == 0 ];then
		echo "`date +%F' '%T` - $0 - INFO: 上传成功" >> $LOGPATH/$LOGFILE
	else
		echo "`date +%F' '%T` - $0 - ERROR: 上传失败" >> $LOGPATH/$LOGFILE
	fi
}


download(){
	if [ -f "$BAKPATH/$FILENAME" ];then
		echo "`date +%F' '%T` - $0 - INFO: 文件已下载" >> $LOGPATH/$LOGFILE
		flag=`./ossutil64 stat $BUCKET/$FILENAME &>>/dev/null;echo $?`
		if [ $flag == 0 ];then
			echo "`date +%F' '%T` - $0 - INFO: 文件已上传" >> $LOGPATH/$LOGFILE
		else
			upload $BAKPATH/$FILENAME
		fi
	else
		echo "`date +%F' '%T` - $0 - INFO: 正在下载文件：$FILENAME" >> $LOGPATH/$LOGFILE
		wget  -c -t 100 "$URL" -O $BAKPATH/$FILENAME &>/dev/null
		if [ $? == 0 ];then
			echo "`date +%F' '%T` - $0 - INFO: 下载完成" >> $LOGPATH/$LOGFILE
		else
			echo "`date +%F' '%T` - $0 - ERROR: 下载失败" >> $LOGPATH/$LOGFILE
			exit 1
		fi
		upload $BAKPATH/$FILENAME
	fi
}
download