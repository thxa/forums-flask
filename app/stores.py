import itertools


class BaseStore:
    def __init__(self, data_provider, last_id):
        self._data_provider = data_provider
        self._last_id = last_id

    def get_all(self):
        return self._data_provider

    def add(self, item_instance):
        item_instance.id = self._last_id
        self._data_provider.append(item_instance)
        self._last_id += 1

    def get_by_id(self, _id):
        all_item = self.get_all()
        result = None
        for item in all_item:
            if item.id == _id:
                result = item
                break
        return result

    def update(self, instance):
        all_itam = self.get_all()
        instance_id = instance.id
        for index, e in enumerate(all_itam):
            if e.id == instance_id:
                all_itam[index] = instance

    def delete(self, _id):
        scan = self.get_by_id(_id)
        self._data_provider.remove(scan)

    def entity_exists(self, instance):
        return instance in self.get_all()


class MemberStore(BaseStore):
    members = []
    last_id = 1

    def __init__(self):
        super().__init__(MemberStore.members, MemberStore.last_id)

    def get_by_name(self, member_name):
        all_members = self.get_all()
        # algorithm for searching by name
        return (member for member in all_members if member.name == member_name)

    def get_members_with_posts(self, all_posts):
        all_members = self.get_all()
        for member, post in itertools.product(all_members, all_posts):
            if post.member_id == member.id:
                member.posts.append(post)
        for member in all_members:
            yield member

    def get_top_two(self, all_posts):
        member_with_posts = list(self.get_members_with_posts(all_posts))
        member_with_posts.sort(key=lambda top: len(top.posts), reverse=True)
        yield member_with_posts[1]
        yield member_with_posts[2]


class PostStore(BaseStore):
    posts = []
    last_id = 1

    def __init__(self):
        super().__init__(PostStore.posts, PostStore.last_id)

    def get_posts_by_date(self):
        all_posts = self.get_all()
        all_posts.sort(key=lambda post: post.data, reverse=True)
        return (post for post in all_posts)
