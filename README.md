# python-daemon
python command daemon(mysql,rabbitmq)

참고 
http://blog.scphillips.com/posts/2013/07/getting-a-python-script-to-run-in-the-background-as-a-service-on-boot/


sudo chmod 755 consumer.py

sudo cp consumer.sh /etc/init.d

sudo chmod 755 /etc/init.d/consumer.sh

sudo chmod +x /etc/init.d/consumer.sh

sudo /etc/init.d/consumer.sh start

ps -ef | grep consumer

// 부팅시 시작
sudo update-rc.d consumer.sh defaults

// 서비스 제거
sudo update-rc.d -f consumer.sh remove

// 스크립트 변경 후 Reload
sudo systemctl daemon-reload


// 실행 확인
ps -ef | grep consumer.sh