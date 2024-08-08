
@login_required(login_url='login_user')
def like_post(request, pk):
    username = request.user.username
    post = get_object_or_404(PostModel, pk=pk)
    like_check = LikePost.objects.filter(username=username, postID=pk).first()

    if like_check is None:
        new_like = LikePost.objects.create(username=username, postID=pk)
        new_like.save()
        post.num_of_likes += 1
        post.save()
        liked = True
    else:
        like_check.delete()
        post.num_of_likes -= 1
        post.save()
        liked = False

    return JsonResponse({'new_like_count': post.num_of_likes, 'liked': liked})

