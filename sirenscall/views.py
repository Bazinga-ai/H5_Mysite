from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.template import loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.utils import DataError

from .models import Recorder
from .models import FileRadar
from django.utils import timezone
import string
import json
import re
import os
import hashlib

from django.core.files.uploadedfile import InMemoryUploadedFile

import mysite.settings as settings

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def index(request):
    template_name = 'sirenscall/index.html'
    template = loader.get_template(template_name)

    return render(request, template_name, context=None)

    # return HttpResponse("Siren's Call")

def radar(request):
    template_name = 'sirenscall/radar.html'
    template = loader.get_template(template_name)

    return render(request, template_name, context=None)


"""
recorder页面的初始化，陈列recorder信息
"""
def recorder_index(request):
    recorder_list = Recorder.objects.order_by('-pub_date')
    template_name = 'sirenscall/recorder_index.html'
    template = loader.get_template(template_name)

    paginator = Paginator(recorder_list, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    context = { 'contacts': contacts }

    # context = {
    #     'recorder_list': recorder_list,
    # }

    return HttpResponse(template.render({'contacts': contacts}, request))



"""
暂时用不上，学习时留下来的东西
"""
def recorder_detail(request, recorder_id):
    try:
        recorder = Recorder.objects.get(pk=recorder_id)
    except Recorder.DoesNotExist:
        raise Http404("Record %s does not exist." % recorder_id)
    return render(request, 'sirenscall/recorder_detail.html', {'recorder': recorder})



"""
按SUBMIT提交按钮后，进行表单验证和数据库存放
    status:
    1: SUCCESSFUL
    2: title or author invalid.(too long or short)
    3: Field[Text] is blank.
    4: password is too long or too short.
    5: password is invalid.
"""
def recorder_submit(request):
    title = request.POST['n_title']
    main_text = request.POST['n_main_text']
    author = request.POST['n_author']
    password = request.POST['n_password']
    pub_date = timezone.now()
    is_bold = False

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    print("[IP地址: %s]" % ip)

    if len(main_text) == 0:
        ret = {
            'status': 3,
            'data_error': '<br>Field [Text] is required.'
        }
        return HttpResponse(json.dumps(ret))
    else:
        if len(title) == 0:
            title = 'Untitled'

        if len(author) == 0:
            author = 'Unknown'
        
        if password == '0':
            pass
        else:
            if len(password) < 4 or len(password) > 20:
                ret = {
                    'status': 4,
                    'data_error': 'Field [Password] is required longer than 4<br> and shorter than 20.'
                }
                return HttpResponse(json.dumps(ret))
        
            result_password = re.compile(r"^[0-9a-zA-Z]\w{4,20}")
            if result_password.match(password):
                pass
            else:
                ret = {
                    'status': 5,
                    'data_error': '<br>Password is invalid.'
                }
                return HttpResponse(json.dumps(ret))
            
        
        try:
            print("[[[")
            print("标题: " + title)
            print(main_text)
            print("作者；" + author)
            print("发布日期：" + str(pub_date))
            print("密码：" + password)
            print("]]]")
            recorder = Recorder(title=title, main_text=main_text, pub_date=pub_date, is_bold=is_bold, author=author, ip=ip, password=password)
            recorder.save()
        
            print(request.get_full_path())
            ret = {
                'status': 1,
                'success': 'RECORD SUCCESSFUL.'
            }
            return HttpResponse(json.dumps(ret))
        
        except DataError:
            print("DATA ERROR")
            ret = {
                'status': 2,
                'data_error': 'Field is too long or invalid. <br> Field [Title] is required no longer than 64. <br> Field [Author] is required no longer than 32.',
            }
            
            return HttpResponse(json.dumps(ret))



"""
加密的信息按UNLOCK后的处理
    status:
    1: 成功
    2: 密码不正确
    3: 没有提交密码
"""
def recorder_pwd_check(request):
    password = request.POST['n_unlock']
    unlock_id = int(request.POST['unlock_id'])
    print("[请求解锁ID：%d    请求密码：%s]" % (unlock_id, password))

    try:
        recorder = Recorder.objects.get(id=unlock_id)
        if password == recorder.password:
            print("[Record ID: %d 解锁成功.]" % (unlock_id))
            ret = {
                'status': 1,
                'success': 'Record unlocked',
                'main_text': recorder.main_text,
            }
            return HttpResponse(json.dumps(ret))

        elif password != recorder.password:
            print("[Record ID: %d 解锁失败, 密码不正确.]" % (unlock_id))
            ret = {
                'status': 2,
                'data_error': 'Invalid Password.'
            }
            return HttpResponse(json.dumps(ret))
        
    except Recorder.DoesNotExist:
        raise Http404("Recorder does not exist.")



"""
测试页，在8月的时候拿来学习分页
"""
def testpage(request):
    prepare_list = Recorder.objects.order_by('-pub_date')
    template_name = 'sirenscall/test.html'
    template = loader.get_template(template_name)

    paginator = Paginator(prepare_list, 10)
    page = request.GET.get('page')
    contacts = paginator.get_page(page)

    # context = { 'prepare_list': prepare_list }

    return HttpResponse(template.render({'contacts': contacts}, request))


"""
测试页bug表单
"""
def test_form(request):
    print("?")
    temp_str = request.POST['d_test_str']
    print(type(temp_str))
    print(temp_str)

    return HttpResponse(".1.1.")


"""
测试bug表单2
"""
def submit_test(request):
    print("START: test_submit")
    temp_str = request.POST['d_test_str']
    print(type(temp_str))
    print(temp_str)

    return HttpResponse("SSSS")




"""
文件上传
    status:
        1: 成功
        2: 文件没选择
        3: 浮点数错误
        4: front status代码错误
        5: 密码过长
        6:
"""
def file_upload(request):
    
    password = request.POST.get('password')
    front_status = request.POST.get('front_status')
    front_real_size = request.POST.get('front_real_size')


    file_obj = request.FILES.get('file_obj')
    if str(file_obj) == 'None':
        msg = {
                'status': 2,
                'msg': 'Submit failed! You have not selected a file.',
            }
        return HttpResponse(json.dumps(msg))

    print("front_status: " + front_status)
    print("front_real_size: " + front_real_size)


    if front_real_size.split(' ')[1] == 'MB':
        print(front_real_size.split(' ')[0])
        if float(front_real_size.split(' ')[0]) > 20:
            print("float error")
            msg = {
                'status': 3,
                'msg': 'Submit failed! Float error.'
            }
            return HttpResponse(json.dumps(msg))

    if int(front_status) != 1:
        print("front_status != 1")
        msg = {
            'status': 4,
            'msg': 'Submit failed! Front status error.'
        }
        return HttpResponse(json.dumps(msg))

    upload_date = timezone.now()
    file_name = file_obj.name
    file_size = file_obj.size
    
    file_type = file_obj.name.split('.')[-1]
    file_type = file_type.lower()

    #取IP
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')

    try:
        latest_id = FileRadar.objects.order_by('-id')[0].id
        latest_id = str(latest_id + 1)
        
        code = hashlib.md5()
        combined_str = latest_id + password
        code.update(combined_str.encode('utf-8'))
        temp_str = code.hexdigest()
        code.update(temp_str.encode('utf-8'))

    

        base_dir = str(settings.BASE_DIR) + '\\sirenscall\\savefile\\' + latest_id + '_' + file_name + '\\' + code.hexdigest()
        os.makedirs(base_dir)
        path_real = os.path.join(base_dir + '\\{0}'.format(file_obj.name))
        f = open(path_real, 'wb+')

        # chunks将对应的文件数据转换成若干片段, 分段写入,
        #可以有效提高文件的写入速度, 适用于2.5M以上的文件
        for chunk in file_obj.chunks():
            f.write(chunk)
        f.close()
        # 根据路径打开指定的文件(以二进制读写方式打开)
    
    except Exception:
        print("ERROR")
        ret = {
            'status': -1,
            'msg': 'Error.'
        }

    print('------Radar 文件上传------')
    print('[文件名: ' + file_name + ']')
    print('[上传日期: ' + upload_date.__str__() + ']')
    print('[文件大小: ' + str(file_size) +']')
    print('[文件类型: ' + file_type +']')
    path_str = str(path_real)
    print('[保存路径: ' + path_str +']')

    try:
        fileRadar = FileRadar(file_name=file_name, upload_date=upload_date,ip=ip, password=password, file_type=file_type, size=file_size, path=path_str)

        fileRadar.crc = code.hexdigest()

        fileRadar.save()
    except DataError:
        msg = {
            'status': 5,
            'msg': 'Submit failed! Password is too long.'
        }
        return HttpResponse(json.dumps(msg))
    

    print('[文件ID: ' + str(fileRadar.id) + ']')

    ret = {
        'status': 1,
        'msg': 'Uploaded Successful.<br> ID: ' + str(fileRadar.id),
        'id': fileRadar.id,
    }

    return HttpResponse(json.dumps(ret))


"""
文件下载
    status:
    1: 成功
    2: ID不存在
    3: 密码错误
    4: 文件不存在
"""
def file_download_check(request):
    file_id = request.POST.get('id');
    password = request.POST.get('password');

    if not file_id.isdigit():
        ret = {
            'status': 2,
            'msg': 'ERROR: Invalid ID.',
        }
        return HttpResponse(json.dumps(ret))

    if int(file_id) <= 0:
        ret = {
            'status': 2,
            'msg': 'ERROR: Invalid ID.',
        }
        return HttpResponse(json.dumps(ret))

    try:
        fileRadar = FileRadar.objects.get(pk=file_id)
    except FileRadar.DoesNotExist:
        print('[请求ID ' + file_id + ' 不存在.]')
        ret = {
            'status': 2,
            'msg': 'ERROR: Invalid ID.',
        }
        return HttpResponse(json.dumps(ret))
    
    if fileRadar.password == password:
        print('[匹配到ID为 ' + file_id + ' 密码为 ' + password + ' 的文件.]')
        path = fileRadar.path
        print('[文件路径: ' + path + ']')

        if not os.path.isfile(path):
            ret = {
                'status': 4,
                'msg': 'ERROR: Missing file.'
            }
            return HttpResponse(json.dumps(ret))


        ret = {
            'status': 1,
            'msg': 'OK. Preparing to download file...',
            # 'path': path,
            'name': fileRadar.file_name,
        }
        return HttpResponse(json.dumps(ret))

    else:
        print('请求ID ' + file_id + ' 的密码错误.')
        ret = {
            'status': 3,
            'msg': 'ERROR: Invalid Password.',
        }
        return HttpResponse(json.dumps(ret))

    print(file_id)
    print(password)
    return HttpResponse()


def file_download(request, file_id, password):
    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    try:
        print('[开始下载...]')
        
        code = hashlib.md5()
        combined_str = file_id + password
        code.update(combined_str.encode('utf-8'))
        temp_str = code.hexdigest()
        code.update(temp_str.encode('utf-8'))
        final_str = code.hexdigest()

        fileRadar = FileRadar.objects.get(id=int(file_id))
        fileRadar.download_times += 1
        fileRadar.save()
        name = fileRadar.file_name
        # 设置响应头
        # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
        base_path = str(settings.BASE_DIR) + '\\sirenscall\\savefile\\' + file_id + '_' + name + '\\' + final_str + '\\' + name
        response = StreamingHttpResponse(file_iterator(base_path))
        # 以流的形式下载文件,这样可以实现任意格式的文件下载
        response['Content-Type'] = 'application/octet-stream'
        # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
        response['Content-Disposition'] = 'attachment; filename=%s' % name.encode('utf8').decode('ISO-8859-1')

    except:
       return HttpResponse("Sorry but Not Found the File")

    return response





def blank(request):
    return HttpResponse("?")