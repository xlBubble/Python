# /bin/python3.5
# _*_coding:utf-8 _*_
from aliyunsdkcore import client
from aliyunsdkrds.request.v20140815.DescribeDatabasesRequest import DescribeDatabasesRequest
from aliyunsdkdts.request.v20180801.CreateMigrationJobRequest import CreateMigrationJobRequest
from aliyunsdkdts.request.v20180801.ConfigureMigrationJobRequest import ConfigureMigrationJobRequest
# from aliyunsdkdts.request.v20180801.DescribeMigrationJobStatusRequest import DescribeMigrationJobStatusRequest
from aliyunsdkdts.request.v20180801.StartMigrationJobRequest import StartMigrationJobRequest
from aliyunsdkrds.request.v20140815.DeleteDatabaseRequest import DeleteDatabaseRequest
from aliyunsdkcore.request import CommonRequest
import json
import logging
import gaojing
import time
import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))
with open("config.json", 'r') as f:
    params = json.load(f)
f.close()

clt = client.AcsClient(params['id'], params['key'], params['region'])
migration_job_name = params['migration_job_name']

sourceRDSId = params["sourceRDS"]["id"]
sourceRDSAccount = params["sourceRDS"]["account"]
sourceRDSPassword = params["sourceRDS"]["password"]
sourceDBName = params["sourceRDS"]["sourceDB"]

targetRDSId = params["targetRDS"]["id"]
targetRDSAccount = params["targetRDS"]["account"]
targetRDSPassword = params["targetRDS"]["password"]
targetDBName = params["targetRDS"]["targetDB"]

migration_object = [{
    "DBName": sourceDBName,
    "NewDBName": targetDBName
}
]

file_date = time.strftime("%Y%m%d", time.localtime())
filename = 'log/accesslog' + '_' + file_date + '.txt'
logging.basicConfig(level=logging.INFO,
                    filename=filename,
                    filemode='a',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                    )


def delete_database():
    logging.info("正在删除数据库：%s.%s" % (targetRDSId, targetDBName))
    try:
        request = DeleteDatabaseRequest()
        request.set_accept_format('json')
        request.set_version('2014-08-15')
        request.set_DBInstanceId(targetRDSId)
        request.set_DBName(targetDBName)
        response = clt.do_action_with_exception(request)
        response_detail = json.loads(response.decode('utf-8'))
        return response_detail
    except Exception as e:
        logging.error(e)


def show_database():
    request = DescribeDatabasesRequest()
    request.set_accept_format('json')
    request.set_version('2014-08-15')
    request.set_DBInstanceId(targetRDSId)
    try:
        response = clt.do_action_with_exception(request)
        response_detail = json.loads(response.decode('utf8'))['Databases']['Database']
        return response_detail
    except Exception as e:
        logging.error(e)


def create_migration_job():
    logging.info("创建迁移实例")
    request = CreateMigrationJobRequest()
    request.set_accept_format('json')
    request.set_version('2018-08-01')
    request.set_Region(params['region'])
    request.set_MigrationJobClass('medium')
    try:
        response = clt.do_action_with_exception(request)
        response_detail = json.loads(response.decode('utf8'))['MigrationJobId']
        logging.info("迁移任务ID: %s" % response_detail)
        return response_detail
    except Exception as e:
        logging.error(e)


def config_migration_job(migration_job_id):
    logging.info('开始迁移配置')
    request = ConfigureMigrationJobRequest()
    request.set_version('2018-08-01')
    request.set_accept_format('json')
    request.set_MigrationJobId(migration_job_id)
    request.set_MigrationJobName(migration_job_name)
    # 配置源库
    request.set_SourceEndpointInstanceType('RDS')
    request.add_query_param("SourceEndpointRegion", params['region'])
    request.set_SourceEndpointInstanceID(sourceRDSId)
    request.set_SourceEndpointEngineName('MySQL')
    request.set_SourceEndpointUserName(sourceRDSAccount)
    request.set_SourceEndpointPassword(sourceRDSPassword)
    # 配置目标库
    request.set_DestinationEndpointInstanceType('RDS')
    request.set_DestinationEndpointRegion(params['region'])
    request.set_DestinationEndpointInstanceID(targetRDSId)
    request.set_DestinationEndpointEngineName('MySQL')
    request.set_DestinationEndpointUserName(targetRDSAccount)
    request.set_DestinationEndpointPassword(targetRDSPassword)
    # 迁移类型
    request.set_MigrationModeStructureIntialization("true")
    request.set_MigrationModeDataIntialization("true")
    request.set_MigrationModeDataSynchronization("false")
    # 待迁移对象
    request.set_MigrationObject(json.dumps(migration_object))
    try:
        response = clt.do_action_with_exception(request)
        response_detail = json.loads(response.decode('utf8'))
        return response_detail
    except Exception as e:
        logging.error(e)


def show_migration_status(migration_job_id):
    try:
        request = CommonRequest(domain='dts.aliyuncs.com', version='2018-08-01',
                                action_name='DescribeMigrationJobStatus')
        request.add_query_param('MigrationJobId', migration_job_id)
        request.add_query_param('PageNumber', '1')
        request.add_query_param('PageSize', '30')
        response = clt.do_action_with_exception(request)
        response_detail = json.loads(response.decode('utf8'))['MigrationJobStatus']
        return response_detail
    except Exception as e:
        logging.error(e)


def start_migration_job(migration_job_id):
    logging.info("启动迁移任务")
    request = StartMigrationJobRequest()
    request.set_version('2018-08-01')
    request.set_accept_format('json')
    request.set_MigrationJobId(migration_job_id)
    try:
        response = clt.do_action_with_exception(request)
        response_detail = json.loads(response.decode('utf8'))  # type: object
        print(response_detail)
        return response_detail
    except Exception as e:
        logging.error(e)


'''
迁移任务状态，取值包括：
NotStarted : 表示未启动 
Prechecking : 表示预检查中 
PrecheckFailed : 表示预检查失败 
Migrating : 表示迁移中 
Suspengding : 表示暂停中
MigrationFailed : 表示迁移失败 
Finished : 表示完成
'''


def get_db_list(db_info):
    db_list = []
    for db in db_info:
        db_list.append(db['DBName'])
    logging.info("database in %s ：%s" % (targetRDSId, db_list))
    return db_list


def check_migration():
    migration_job_id = create_migration_job()
    config_migration_job(migration_job_id)
    if not True:
        value = "Failed(迁移配置失败)"
        logging.error(value)
        gaojing.main(value, filename)
    while True:
        status = show_migration_status(migration_job_id)
        if status == 'PrecheckFailed':
            value = "Failed(预检查失败)"
            logging.error(value)
            gaojing.main(value, filename)
            break
        elif status == 'MigrationFailed':
            value = "Failed(迁移失败)"
            logging.error(value)
            gaojing.main(value, filename)
            break
        elif status == 'NotStarted':
            value = "NotStarted(未启动)"
            logging.error(value)
            gaojing.main(value, filename)
            break
        elif status == 'Suspengding':
            value = "Subpending(暂停中)"
            logging.error(value)
            gaojing.main(value, filename)
            break
        elif status == 'Finished':
            value = "Success"
            logging.info(value)
            get_db_list(show_database())
            gaojing.main(value, filename)
            break
        else:
            logging.info(status)
            time.sleep(1800)
            continue


if __name__ == '__main__':
    logging.info("数据库迁移：%s.%s TO %s.%s " % (sourceRDSId, sourceDBName, targetRDSId, targetDBName))
    gaojing.main("start", filename)
    db_list = get_db_list(show_database())
    if targetDBName not in db_list:
        logging.error("数据库不存在")
        # 开始迁移
        check_migration()
    else:
        # 删除数据库
        delete_database()
        time.sleep(5)
        db_list = get_db_list(show_database())
        if targetDBName in db_list:
            logging.info("ATTENTION: DATABASE %s still exists!" % params['targetRDS']['targetDB'])
            logging.error("数据库未删除")
            gaojing.main("Failed(数据库未删除)", filename)
            exit(1)
        else:
            # 开始迁移
            check_migration()