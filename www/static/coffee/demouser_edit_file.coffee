root = exports ? this
root.Hs or= {}
Hs = root.Hs

$ ->
    CDN_PREFIX = "http://tasterest-cdn.xialiwei.com"

    file_lists = []
    current_dom_file_src = null
    current_dom_file_save = null
    current_dom_file_type = null
    current_dom_file_poster = null
    current_dom_file_name = null
    current_dom_file_size = null
    current_dom_sections = null
    current_dom_loading_area = null
    current_dom_list_area = null

    if window.File and window.FileList and window.FileReader and window.Blob and window.Worker
        handleFileSelect1 = (evt) ->
            img_add = $(this).attr("id")=="demouser_file_add_upload" ? true : false
            _room_id = BLOCK_ID
            _room_id = USER_ID
            content_type = "HWEBFILE//"
            evt.stopPropagation()
            evt.preventDefault()

            files = null
            if evt.target.files
                files = evt.target.files
            else
                files = evt.dataTransfer.files

            file_lists.push(files)
            file_index = 0
            startingByte = 0
            endingByte = 0

            console.log "demouser edit file coffee"
            console.log BLOCK_ID

            uploadFile = (file) ->
                if file == undefined
                    return
                if file.type == undefined
                    return
                type = if file.type then file.type else 'n/a'
                console.log type
                
                # if not (type.split("/")[0] in ["file"])
                # # if not (type in ["image/jpeg","image/jpg","image/webp","image/png","image/gif","image/bmp"])
                #     file_index += 1
                #     alert "文件格式不支持"
                #     return
                reader = new FileReader()
                tempfile = null
                startingByte = 0
                console.log("正在上传第一个文件")

                loading_flag = uuid2(6,null)
                current_dom_loading_area.append """
                    <div id="loading_#{loading_flag}" class="loading_flag" contenteditable="false"></div>
                """
                $("#loading_#{loading_flag}").animate
                        "width":"25%"
                    ,1000

                xhrProvider = () ->
                    xhr = jQuery.ajaxSettings.xhr()
                    if xhr.upload
                        xhr.upload.addEventListener('progress', updateProgress, false)
                    return xhr

                updateProgress = (evt) ->
                    #console.log startingByte, file.size, evt.loaded, evt.total
                    console.log("Uploading file #{file_index+1} of #{files.length} at #{(startingByte + (endingByte-startingByte)*evt.loaded/evt.total)/file.size*100}%")

                uploadNextFile = () ->
                    console.log("正在要上传下一个文件")
                    file_index += 1
                    if file_index < files.length
                        uploadFile(files[file_index])
                        console.log("===")
                        console.log(file_index)
                        console.log("===|||")
                    else
                        file_lists.shift()
                        if file_lists.length > 1
                            file_index = 0
                            files = file_lists[0]
                            uploadFile(files[file_index])
                            console.log("===+++")
                            console.log(file_index)
                            console.log("===|||")
                        else
                            console.log("===>>>")
                            obj = document.getElementById('demouser_file_add_upload')
                            obj.outerHTML = obj.outerHTML

                reader.onload = (evt) ->
                    content = evt.target.result.slice evt.target.result.indexOf("base64,")+7
                    bin = atob content

                    worker = new Worker "/static/js/md5.js"
                    worker.onmessage = (event) ->
                        md5 = event.data
                        # console.log "md5", md5, file

                        Qiniu_UploadUrl_https = "https://up-cn-east-2.qiniup.com"
                        if window.location.protocol == "https:"
                            Qiniu_UploadUrl = Qiniu_UploadUrl_https
                        else
                            Qiniu_UploadUrl = "http://up-cn-east-2.qiniup.com"

                        worker_aim_url = "/api/file/demouser/check"
                        $.post worker_aim_url,
                            "block_id": _room_id
                            "md5": md5
                        , (data) ->
                            if files.length == 1
                                console.log("正在上传1个文件")
                                if data["exists"]

                                    result_url = "#{CDN_PREFIX}/#{BLOCK_ID}_demouser_#{md5}"
                                    $("#loading_#{loading_flag}").animate
                                            "width":"100%"
                                        ,500 ,()->
                                            $("#loading_#{loading_flag}").remove()
                                            current_dom_list_area.append """
                                            <div class="order_create_imgs_item">
                                                <img class="order_create_imgs_item_img" src="#{result_url}">
                                            </div>
                                            """
                                    obj = document.getElementById('demouser_file_add_upload')
                                    obj.outerHTML = obj.outerHTML
                                    return
                            else
                                if file_index+1 == files.length
                                    console.log("正在上传最后一个文件")
                                    if data["exists"]
                                        result_url = "#{CDN_PREFIX}/#{BLOCK_ID}_demouser_#{md5}"
                                        $("#loading_#{loading_flag}").animate
                                                "width":"100%"
                                            ,500 ,()->
                                                $("#loading_#{loading_flag}").remove()
                                                current_dom_list_area.append """
                                                <div class="order_create_imgs_item">
                                                    <img class="order_create_imgs_item_img" src="#{result_url}">
                                                </div>
                                                """

                                        obj = document.getElementById('demouser_file_add_upload')
                                        obj.outerHTML = obj.outerHTML
                                        # current_dom_sections.append """
                                        # <div class="section"><img src="#{result_url}"></div>
                                        # """
                                        # update_dom_content_img(current_dom_sections)
                                        return
                                        # content = content_type+md5
                                        # if Hs.image_add_type?
                                        #     if Hs.image_add_type == "image_add_list"
                                        #         Hs.image_add_list.push content
                                        #         Hs.image_add_list_action(content)
                                        #         obj = document.getElementById('img_add_upload')
                                        #         obj.outerHTML = obj.outerHTML
                                        #         return
                                        # return $.ajax
                                        #     url: '/api/comment/submit',
                                        #     type: 'POST',
                                        #     dataType: 'json',
                                        #     data: 
                                        #         "app": WX_APP,
                                        #         "aim_id": _room_id,
                                        #         "content": content
                                        #     success: (data) ->
                                        #         console.log(data)
                                        #         obj = document.getElementById('img_add_upload')
                                        #         obj.outerHTML = obj.outerHTML
                                        #     error: (error) ->
                                        #         console.log(error)
                                else
                                    console.log("正在上传"+(file_index+1)+"/"+files.length+"个视频")
                                    if data["exists"]
                                        result_url = "#{CDN_PREFIX}/#{BLOCK_ID}_demouser_#{md5}"
                                        if file_index == 0
                                            $("#loading_#{loading_flag}").animate
                                                    "width":"100%"
                                                ,500 ,()->
                                                    $("#loading_#{loading_flag}").remove()
                                                    current_dom_list_area.append """
                                                    <div class="order_create_imgs_item">
                                                        <img class="order_create_imgs_item_img" src="#{result_url}">
                                                    </div>
                                                    """
                                        else
                                            current_dom_file_src.val(result_url)
                                            current_dom_file_poster.val(file.name)
                                            current_dom_file_name.val(file.name)
                                            current_dom_file_size.val(file.size)
                                            $("#loading_#{loading_flag}").animate
                                                    "width":"100%"
                                                ,500 ,()->
                                                    $("#loading_#{loading_flag}").remove()
                                                    current_dom_list_area.append """
                                                    <div class="order_create_imgs_item">
                                                        <img class="order_create_imgs_item_img" src="#{result_url}">
                                                    </div>
                                                    """
                                        return uploadNextFile()
                            upload_token = data["token"]

                            Qiniu_upload = (f, token, key) ->
                                xhr = new XMLHttpRequest()
                                xhr.open('POST', Qiniu_UploadUrl, true)
                                formData = new FormData()
                                if (key != null and key != undefined)
                                    formData.append('key', key)
                                formData.append('token', token)
                                formData.append('file', f)
                                xhr.upload.addEventListener "progress", (evt) ->
                                    if (evt.lengthComputable)
                                        nowDate = new Date().getTime()
                                        taking = nowDate - startDate
                                        x = (evt.loaded) / 1024
                                        y = taking / 1000
                                        uploadSpeed = (x / y)
                                        if (uploadSpeed > 1024)
                                            formatSpeed = (uploadSpeed / 1024).toFixed(2) + "Mb\/s"
                                        else
                                            formatSpeed = uploadSpeed.toFixed(2) + "Kb\/s"

                                        percentComplete = Math.round(evt.loaded * 100 / evt.total)
                                        console.log(percentComplete, ",", formatSpeed)
                                        $("#loading_#{loading_flag}").css
                                            "width":"#{25+percentComplete*0.75}%"
                                , false

                                xhr.onreadystatechange = (response) ->
                                    if (xhr.readyState == 4 and xhr.status == 200 and xhr.responseText != "")
                                        blkRet = JSON.parse(xhr.responseText)
                                        $.post "/api/file/demouser/add",
                                                "aim_id": _room_id
                                                "md5": md5
                                            , () ->
                                                result_url = "#{CDN_PREFIX}/#{BLOCK_ID}_demouser_#{md5}"
                                                $("#loading_#{loading_flag}").animate
                                                        "width":"100%"
                                                    ,500 ,()->
                                                        $("#loading_#{loading_flag}").remove()
                                                        current_dom_list_area.append """
                                                        <div class="order_create_imgs_item">
                                                            <img class="order_create_imgs_item_img" src="#{result_url}">
                                                        </div>
                                                        """
                                                uploadNextFile()

                                startDate = new Date().getTime()
                                xhr.send formData

                            Qiniu_upload(file, upload_token, _room_id+"_demouser_"+md5)

                    worker.postMessage bin

                reader.readAsDataURL file
            if file_lists.length >= 1
                uploadFile files[file_index]
        $("body").on "change", "#demouser_file_add_upload", handleFileSelect1

        $("body").on "click",".order_create_imgs_add",(evt)->
            dom_file_add = $(this)
            $("#demouser_file_add_upload").click()
            current_dom_loading_area = $(".order_create_imgs_loading")
            current_dom_list_area = $(".order_create_imgs_list")










