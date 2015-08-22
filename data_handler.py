import sys
import pika
import json
import MySQLdb as db
import datetime
import logging

#logging.getLogger('pika').setLevel(logging.DEBUG)
logger = logging.getLogger('logger')
handler = logging.FileHandler('/home/gumidev/workspace/log/log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


credentials = pika.PlainCredentials('dev', 'dev')
parameters  = pika.ConnectionParameters(host='hostip', port=5672, credentials=credentials)
connection  = pika.BlockingConnection(parameters)
channel     = connection.channel()


channel.exchange_declare(exchange='exchange_name', type='fanout',durable=True)

result = channel.queue_declare('queue_name',durable=True,auto_delete=False)
queue_name = result.method.queue

print queue_name
channel.queue_bind(exchange ='exchange_name', queue = queue_name)

try:
    con = db.connect(host='hostip',port=3306, user = 'user',passwd='pas',db='DB_NAME');
    con.autocommit(True)  

    cur = con.cursor()
    cur.execute("SELECT VERSION()")
    ver = cur.fetchone()
    print " [*] Database version : %s " % ver
    cur.close()
except db.Error, e:
        print "Error %d: %s" % (e.args[0],e.args[1])
        logger.error('database connect')
        sys.exit(1)
finally:    
    pass
        if con:
            con.close()


print " [*] Waiting for messages. To exit press CTRL+C"



def callback(ch, method, properties, body):
    print " [x] Received %r\n\n" % (body)




if __name__ == '__main__':
    try:
        channel.basic_consume(callback, queue=queue_name, no_ack=True)
        channel.start_consuming()
    except (KeyboardInterrupt):#, SystemExit):
        print 'KeyboardInterrupt Program Exit....\n'
        logger.error('KeyboardInterrupt Program Exit....\n')
	channel.stop_consuming()
    connection.close()
    con.close()
    sys.exit(1)
