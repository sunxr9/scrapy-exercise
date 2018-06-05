# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals
import pickle

from django.db import models
import redis
r = redis.Redis()


class Model(object):
    @classmethod
    def get(cls, **kwargs):
        pass
        cache_key = '%s - %s' % (cls.__name__, next(iter(kwargs.values())))
        cache_obj = r.get(cache_key)
        if not cache_obj:
            cache_obj = cls.objects.get(**kwargs)
            r.set(cache_key, pickle.dumps(cache_obj))
        else:
            cache_obj = pickle.loads(cache_obj)
        return cache_obj


class Code(models.Model, Model):
    code_id = models.BigAutoField(primary_key=True)
    phone = models.BigIntegerField()
    code = models.BigIntegerField()
    created_at = models.DateTimeField()
    ip = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'codes'


class Comment(models.Model, Model):
    commentid = models.IntegerField(primary_key=True)
    pid = models.BigIntegerField()
    cid = models.BigIntegerField()
    avatar = models.CharField(max_length=512, blank=True, null=True)
    uname = models.CharField(max_length=512, blank=True, null=True)
    created_at = models.CharField(max_length=128)
    content = models.TextField(blank=True, null=True)
    like_counts = models.IntegerField()
    reply = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'comments'


class Composer(models.Model, Model):
    cid = models.BigIntegerField(primary_key=True)
    banner = models.CharField(max_length=512)
    avatar = models.CharField(max_length=512)
    verified = models.IntegerField()
    name = models.CharField(max_length=128)
    intro = models.TextField(blank=True, null=True)
    like_counts = models.IntegerField()
    fans_counts = models.IntegerField()
    follow_counts = models.IntegerField()
    location = models.CharField(max_length=32, blank=True, null=True)
    career = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'composers'

    def get_posts(self, num=0):
        if num:
            cr_list = Copyright.objects.filter(cid=self.cid)[:num]
        else:
            cr_list = Copyright.objects.filter(cid=self.cid).all()
        posts = []
        for cr in cr_list:
            post = Post.get(pid=cr.pid)
            # print(dir(cr))
            post.roles = cr.roles
            posts.append(post)
        return posts


class Copyright(models.Model, Model):
    pcid = models.CharField(primary_key=True, max_length=32)
    pid = models.BigIntegerField()
    cid = models.BigIntegerField()
    roles = models.CharField(max_length=32)

    class Meta:
        managed = False
        db_table = 'copyrights'


class Post(models.Model, Model):
    pid = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=256)
    thumbnail = models.CharField(max_length=512, blank=True, null=True)
    preview = models.CharField(max_length=512, blank=True, null=True)
    video = models.CharField(max_length=512, blank=True, null=True)
    video_format = models.CharField(max_length=32, blank=True, null=True)
    duration = models.IntegerField()
    category = models.CharField(max_length=512)
    created_at = models.CharField(max_length=128)
    description = models.TextField(blank=True, null=True)
    play_counts = models.IntegerField()
    like_counts = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'posts'

    def get_composers(self):
        cr_list = Copyright.objects.filter(pid=self.pid).all()
        composers = []
        for cr in cr_list:
            composer = Composer.get(cid=cr.cid)
            composer.roles = cr.roles
            composers.append(composer)
            # print('composers', composers)
        # print('composers"111111111"', composers)
        return composers

    @property
    def backgroud(self):
        return '%s@960w_540h_50-30bl_1e_1c' % self.raw_image

    @property
    def raw_image(self):
        if self.preview:
            return self.preview.split('@')[0]
        return ''
