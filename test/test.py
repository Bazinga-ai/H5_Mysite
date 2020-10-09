from qa_program.models import Question

pre_kind = 'K'
pre_id = 1336

for i in range(1337, 3060):
    a = Question.objects.get(id=i)
    # print('ID: ' + a.id)
    if a.kind == pre_kind:
        a.no = a.id - pre_id
    else:
        pre_kind = a.kind
        pre_id = a.id - 1
        a.no = a.id - pre_id
    a.save()