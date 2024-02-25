import copy


def get_file_name(request):
    doc = request.FILES.get("doc")
    doc_copy = copy.copy(doc)
    return {"file_name": doc_copy}


def user_permission_is_in_group(request):
    user_is_in_group = request.user.groups.filter(name='update_bace').exists()
    return {'user_is_in_group': user_is_in_group}
