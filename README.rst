up2minio - Sapic 图床的 Minio 存储钩子扩展
==============================================

**许可证**: 本项目基于 `Apache 2.0 许可证 <https://www.apache.org/licenses/LICENSE-2.0>`_ 开源，您可以自由使用、修改和分发本项目，但需保留原始版权声明及许可证信息。

---

简介
----

``up2minio`` 是基于 `Sapic <https://github.com/daofengqianlin/Sapic>`_ 的一个扩展模块，用于将上传的图片保存到自建的 ``Minio`` 对象存储中。它支持通过 Minio 的 S3 兼容 API 上传图片，并提供必要的配置与管理功能。

---

安装
----

正式 ‖ 开发版本
^^^^^^^^^^^^^^^^

开发版本安装
`````````````
运行以下命令安装开发版本：

.. code-block:: bash

    pip install -U git+https://github.com/Daofengql/Sapicbed-Minio-Hook.git@main

---

开始使用
--------

环境准备
^^^^^^^^^

1. 部署并运行 `Sapic 图床 <https://github.com/daofengqianlin/Sapic>`_。
2. 确保 Minio 服务已搭建并配置了所需的存储桶（Bucket）。

添加扩展
^^^^^^^^^

1. 登录 Sapic 站点管理员后台。
2. 进入 **站点管理 > 钩子扩展** 页面。
3. 添加钩子扩展：
   - **模块名称**：输入 ``up2minio``。
   - 提交保存后，模块会被加载（请确保扩展模块已通过 pip 安装到服务器）。

配置扩展
^^^^^^^^^

1. 进入 **站点管理 > 网站设置** 页面。
2. 在页面底部的钩子配置区域，填写 Minio 的相关信息：
   - **Bucket**：Minio 存储桶名称（需公开可读）。
   - **Region**：Minio 服务端的节点名称。
   - **AccessKey**：对存储桶有权限的 Access Key。
   - **SecretKey**：对存储桶有权限的 Secret Key。
   - **Endpoint**：Minio 服务的 S3 API 地址（如 ``127.0.0.1:9000``，无需包含协议头）。
   - **CDN Domain**：自定义 CDN 加速域名，需包含协议头，例如 ``https://cdn.example.com``。
   - **存储根目录**：图片存储在存储桶内的路径（非存储桶名称）。

启用存储后端
^^^^^^^^^^^^^

1. 在 **站点管理 > 网站设置 > 上传区域** 页面。
2. 设置存储后端为 ``up2minio``。
3. 保存设置后，所有上传的图片将存储到 Minio。

---

功能特点
--------

1. **扩展性**：基于 Sapic 的钩子架构，可无缝集成。
2. **支持自定义 CDN**：通过配置 CDN 域名优化访问速度。
3. **存储路径灵活**：支持自定义 Minio 存储根目录。
4. **安全性**：通过 AK/SK 验证访问，确保数据安全。

---

API 方法
--------

``get_bucket_obj()``
^^^^^^^^^^^^^^^^^^^^
返回 Minio 客户端对象。

- **用途**：初始化 Minio 客户端。

``upimg_save(**kwargs)``
^^^^^^^^^^^^^^^^^^^^^^^^
上传图片到 Minio。

- **参数**：
  - ``filename``：图片文件名。
  - ``stream``：图片文件流。
  - ``upload_path``：上传路径。
- **返回**：字典，包含上传结果（``src`` 为图片的完整 URL）。

``upimg_delete(sha, upload_path, filename, basedir, save_result)``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

删除存储在 Minio 中的图片。

- **参数**：
  - ``sha``：图片的哈希值。
  - ``upload_path``：上传路径。
  - ``filename``：图片文件名。
  - ``basedir``：存储根目录。
  - ``save_result``：保存时的结果。
- **返回**：无。

---

注意事项
--------

1. **HTTPS 限制**：目前仅支持 HTTPS，若 Minio 不支持 HTTPS，请使用 Nginx 配置反向代理解决。
2. **存储桶权限**：存储桶需设置为公开可读，以便图片能被外部访问。
3. **路径配置**：
   - **Bucket** 和 **存储根目录** 配置正确，否则会导致文件存储失败。
4. **CDN 配置**：若未配置 CDN 域名，将直接使用 Minio Endpoint 地址。

---

示例配置
--------

- **Bucket**: ``my-images``
- **Region**: ``us-east-1``
- **AccessKey**: ``your-access-key``
- **SecretKey**: ``your-secret-key``
- **Endpoint**: ``minio.example.com:9000``
- **CDN Domain**: ``https://cdn.example.com``
- **存储根目录**: ``uploads/images``

---

许可证
------

本项目基于 `Apache 2.0 许可证 <https://www.apache.org/licenses/LICENSE-2.0>`_ 发布，用户可自由使用、修改和分发，但需保留原始版权声明及许可证信息。

---
