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

with open("config.json", 'r') as f:
    params = json.load(f)

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
    "DBName":  sourceDBName,
    "NewDBName": targetDBName
    }
]


logging.basicConfig(level=logging.DEBUG,
                    filename='accesslog.txt',
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
        exit(1)
    pass


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
        exit(1)


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
    # request.set_SourceEndpointInstanceType('LocalInstance')
    # request.set_SourceEndpointEngineName('MySQL')
    # request.set_SourceEndpointRegion('cn-shanghai')
    # request.set_SourceEndpointIP('119.28.132.236')
    # request.set_SourceEndpointPort('3306')
    # request.set_SourceEndpointUserName('root')
    # request.set_SourceEndpointPassword('51idc.coM')
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
        request = CommonRequest(domain='dts.aliyuncs.com', version='2018-08-01', action_name='DescribeMigrationJobStatus')
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


if __name__ == '__main__':
    with open('accesslog.txt', 'w') as file:
        file.truncate()
    logging.info("数据库迁移：%s.%s TO %s.%s " % (sourceRDSId, sourceDBName, targetRDSId, targetDBName))
    get_db_list(show_database())
    # 删除数据库
    logging.debug(delete_database())
    time.sleep(5)
    db_list = get_db_list(show_database())
    if targetDBName in db_list:
        logging.info("ATTENTION: DATABASE %s still exists!" % params['targetRDS']['targetDB'])
        logging.error("数据库未删除")
        gaojing.main("Failed(数据库未删除)")
        exit(1)
    else:
        # 开始迁移
        migration_job_id = create_migration_job()
        config_migration_job(migration_job_id)
        while True:
            #precheck_status = show_migration_status(migration_job_id)['PrecheckStatus']['Status']
            #structure_initialization_status = show_migration_status(migration_job_id)['StructureInitializationStatus']['Status']
            #data_nitialization_status = show_migration_status(migration_job_id)['DataInitializationStatus']['Status']
            #logging.info("预检查：%s,结构迁移：%s,全量迁移：%s" %(precheck_status, structure_initialization_status, data_nitialization_status))
            status = show_migration_status(migration_job_id)
            if status == 'PrecheckFailed':
                value = "Failed(预检查失败)"
                logging.error(value)
                gaojing.main(value)
                break
            elif status == 'MigrationFailed':
                value = "Failed(迁移失败)"
                logging.error(value)
                gaojing.main(value)
                break
            elif status == 'Finished':
                print("i am ok")
                value = "Success"
                logging.info(value)
                get_db_list(show_database())
                gaojing.main(value)
                break
            else:
                logging.info(status)
                time.sleep(60)
                continue
