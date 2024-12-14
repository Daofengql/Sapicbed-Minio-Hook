# -*- coding: utf-8 -*-
"""
    up2minio
    ~~~~~

    Save uploaded pictures in Minio.

    :copyright: (c) 2023 by Hiroshi.tao.
    :license: Apache 2.0, see LICENSE for more details.
"""

__version__ = "0.0.2"
__author__ = "daofengqianlin"
__hookname__ = "up2minio"
__description__ = "将图片保存到minio"
__catalog__ = "upload"

from flask import g
from minio import Minio
from io import BytesIO
from posixpath import join
from mimetypes import guess_type
from utils._compat import string_types
from utils.tool import slash_join


intpl_localhooksetting = """
<div class="layui-col-xs12 layui-col-sm12 layui-col-md6">
    <fieldset class="layui-elem-field layui-field-title" style="margin-bottom: auto">
        <legend>
            Minio（{% if "up2minio" in g.site.upload_includes %}使用中{% else
            %}未使用{% endif %}）
        </legend>
        <div class="layui-field-box">
            <div class="layui-form-item">
                <label class="layui-form-label"><b style="color: red">*</b> Bucket</label>
                <div class="layui-input-block">
                    <input type="text" name="minio_bucket" value="{{ g.site.minio_bucket }}" placeholder="Minio服务的节点名称"
                        autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label"><b style="color: red">*</b> region</label>
                <div class="layui-input-block">
                    <input type="text" name="minio_reg" value="{{ g.site.minio_reg }}" placeholder="Minio服务的存储桶名称"
                        autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label"><b style="color: red">*</b> AccessKey</label>
                <div class="layui-input-block">
                    <input type="text" name="minio_AK" value="{{ g.site.minio_AK }}" placeholder="Minio服务的Access KEY"
                        autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label"><b style="color: red">*</b> Secret KEY</label>
                <div class="layui-input-block">
                    <input type="password" name="minio_SK" value="{{ g.site.minio_SK }}"
                        placeholder="BackBlaze B2 applicationKey" autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label">
                    <b style="color: red">*</b> endpoint
                </label>
                <div class="layui-input-block">
                    <input type="text" name="minio_ep" value="{{ g.site.minio_ep }}" placeholder="Minio服务的终结点"
                        autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label">
                    <b style="color: red">*</b> cdn domain
                </label>
                <div class="layui-input-block">
                    <input type="url" name="minio_cdn" value="{{ g.site.minio_cdn }}" placeholder="自定义CDN加速"
                        autocomplete="off" class="layui-input" />
                </div>
            </div>
            <div class="layui-form-item">
                <label class="layui-form-label">存储根目录</label>
                <div class="layui-input-block">
                    <input type="text" name="minio_basedir" value="{{ g.site.minio_basedir }}"
                        placeholder="图片存储到minio的基础目录，默认是根目录" autocomplete="off" class="layui-input" />
                </div>
            </div>
        </div>
    </fieldset>
</div>
"""


def get_bucket_obj()->Minio:
    sk = g.cfg.minio_SK
    ak = g.cfg.minio_AK
    endpoint = g.cfg.minio_ep
    region = g.cfg.minio_reg
    minio = Minio(
        endpoint=endpoint,
        access_key=ak,
        secret_key=sk,
        region=region
    )
    return minio


def upimg_save(**kwargs):
    res = dict(code=1)
    try:
        filename = kwargs["filename"]
        stream = kwargs["stream"]
        upload_path = kwargs.get("upload_path") or ""
        if not filename or not stream:
            return ValueError
    except (KeyError, ValueError):
        res.update(msg="Parameter error")
    else:
        name = g.cfg.minio_bucket
        cdn = g.cfg.minio_cdn

        basedir = g.cfg.minio_basedir or ""

        if not name or not basedir or not cdn:
            res.update(msg="The b2 parameter error")
            return res
        errmsg = "An unknown error occurred in the program"
        if isinstance(upload_path, string_types):
            if upload_path.startswith("/"):
                upload_path = upload_path.lstrip("/")
            if basedir.startswith("/"):
                basedir = basedir.lstrip("/")
            filepath = join(basedir, upload_path, filename)
            try:
                #: 使用Backblaze官方SDK上传
                minio = get_bucket_obj()
                if filename.endswith(".webp"):
                    mime_type = "image/webp"
                else:
                    mime_type, _ = guess_type(filename)
                file = minio.put_object(bucket_name=name, object_name=filepath, content_type=mime_type,data=BytesIO(stream),length=len(stream))
            except Exception as e:
                res.update(code=500, msg=str(e) or errmsg)
            else:
                src = slash_join(cdn, filepath)
                res.update(
                    code=0,
                    src=src,
                    basedir=basedir,
                    fileId=file.version_id
                )
        else:
            res.update(msg="The upload_path type error")
    return res


def upimg_delete(sha, upload_path, filename, basedir, save_result):
    basedir = g.cfg.minio_basedir or ""
    name = g.cfg.minio_bucket
    filepath = join(basedir or basedir, upload_path, filename)
    minio = get_bucket_obj()
    minio.remove_object(name,filepath)
