# Platomini-fastapi-service

## 快速开始
1. 安装docker
2. 进入该仓库目录，逐行运行下面的代码
```shell
docker pull registry.baidubce.com/paddlepaddle/paddle:2.4.2
docker tag registry.baidubce.com/paddlepaddle/paddle:2.4.2 plato:2.4.2
docker build -t plato:1.0 .
docker-compose up -d
```
3.暴露服务器或或主机的9006端口（云服务器设置安全组，个人主机设置防火墙准入规则）
4.通过浏览器 IP[替换为自己服务器的IP]:9006/docs 查看api使用规则
