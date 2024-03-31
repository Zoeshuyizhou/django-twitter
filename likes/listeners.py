def incr_likes_count(sender, instance, created, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F

    if not created:
        return

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        # TODO HOMEWORK 给 Comment 使用类似的方法进行 likes_count 的统计
        return

    # 不可以使用
    # tweet = instance.content_object
    # tweet.likes_count += 1
    # tweet.save() 的方式
    # 因此这个操作不是原子操作，必须使用 update 语句才是原子操作
    # 如果在我 tweet.likes_count += 1 之后，tweet.save() 之前，有另外一个人也+=1 这个就错了
    # 明星发帖的时候错误率会更高 因为同一时间超多人点赞
    tweet = instance.content_object
    Tweet.objects.filter(id=tweet.id).update(likes_count=F('likes_count') + 1)
    # SQL Query: Update Likes_count = Likes_count+1 from tweets_table where id = <instance.object_id>


def decr_likes_count(sender, instance, **kwargs):
    from tweets.models import Tweet
    from django.db.models import F

    model_class = instance.content_type.model_class()
    if model_class != Tweet:
        # TODO HOMEWORK 给 Comment 使用类似的方法进行 likes_count 的统计
        return

    # handle tweet likes cancel
    tweet = instance.content_object
    Tweet.objects.filter(id=tweet.id).update(likes_count=F('likes_count') - 1)
