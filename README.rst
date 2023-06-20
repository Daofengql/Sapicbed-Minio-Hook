up2minio
========

这是基于 `sapic <https://github.com/sapicd/sapic>`_
的一个小的扩展模块，用来将上传的图片保存到 `Minio`中

安装
------

- 正式版本

    `$ pip install -U up2b2` #暂时不支持

- 开发版本

    `$ pip install -U git+https://github.com/Daofengql/Sapicbed-Minio-Hook.git@main`

开始使用
----------

此扩展请在部署 `sapic <https://github.com/sapicd/sapic>`_ 图床后使用，需要
其管理员进行添加扩展、设置钩子等操作。

添加：
^^^^^^^^

请在 **站点管理-钩子扩展** 中添加第三方钩子，输入模块名称：up2minio，
确认后提交即可加载这个模块（请在服务器先手动安装或Web上安装第三方包）。

配置：
^^^^^^^^

在 **站点管理-网站设置** 底部的钩子配置区域配置 minio 相关信息。

Bucket即桶名称，要求公开可读。

region为Minio服务端设置的节点名称

AccessKey为Minio服务端创建的对当前Bucket有权限的AK

Secret KEY为Minio服务端创建的对当前Bucket有权限的SK

endpoint为Minio服务端的S3API地址，如127.0.0.1:9000  不需要写请求协议的部分，默认会使用https来请求，暂不支持http请求，可以使用NGINX来反向代理你的s3api来解决问题

cdn domain 为自定义的CDN服务地址，通常为直接将endpoint作为源站建立的url，需要协议头，并且更具情况，在第一级目录上配置Bucket

存储根目录 在Minio Bucket里面的储存位置，不是Bucket name

使用：
^^^^^^^^

同样在 **站点管理-网站设置** 上传区域中选择存储后端为 `up2minio` 即可，
后续图片上传时将保存到minio。

上传图片的sender名称是：up2minio
