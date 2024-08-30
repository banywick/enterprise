import redis


r = redis.StrictRedis(host="localhost", port=6379, db=0)


def get_file_name(request):
    file_name = r.get("file_name")
    if file_name:
        file_name = file_name.decode("utf8")
        return {"file_name": file_name}
    return {"file_name": file_name}


def user_permission_is_in_group(request):
    user_is_in_group_update = request.user.groups.filter(name="update_base").exists()
    user_is_in_group_inventory = request.user.groups.filter(name="inventory").exists()
    user_is_in_group_inventory_guest = request.user.groups.filter(name="inventory_guest").exists()
    return {"user_is_in_group_update": user_is_in_group_update,
            'user_is_in_group_inventory': user_is_in_group_inventory,
            'user_is_in_group_inventory_guest': user_is_in_group_inventory_guest}
