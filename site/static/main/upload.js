
// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
	var cookies = document.cookie.split(';');
	for (var i = 0; i < cookies.length; i++) {
	    var cookie = jQuery.trim(cookies[i]);
	    // Does this cookie string begin with the name we want?
	    if (cookie.substring(0, name.length + 1) === (name + '=')) {
		cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
		break;
	    }
	}
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

$("#file-input").fileinput({
    theme: 'explorer-fas',
    // showPreview: false, 
    uploadUrl: 'upload',
    maxFileSize: 2048,
    maxFilesNum: 5,
    allowedFileTypes: ['image'],
    allowedFileExtensions: ['jpg', 'png', 'gif','ico','webp'],
    showUpload: false,
    showRemove: false,
    showUploadedThumbs: true,
    showUploadProgress: false,
    browseIcon: "",
    browseLabel: "Upload",
    showCaption: false,
    browseOnZoneClick: true,
    overwriteInitial:false,
    minFileCount:1,
    maxFileCount:5,
    uploadAsync: false,
    uploadExtraData: uploadExtraOption,
    ajaxSettings: {headers: {"X-CSRFToken": csrftoken}}
}).on("filebatchselected", function(event,files){
    
    $("#file-input").fileinput("upload");
    console.log('File batch uploading...');
    
}).on('filebatchuploadsuccess', function(event, data) {
    var form = data.form, files = data.files, extra = data.extra,
	response = data.response, reader = data.reader;
    console.log('File batch upload success');
});

function uploadExtraOption(previewId, index)
{
    var ret={};
    op_type = $("#imageOperation").val();

    
    switch (op_type) {
        case "Compress":
	return {
	    img_op :  'compress',
	    compress_level: $( "input[name=compress-level]:checked" ).val(),
	    colorIndex : $("#enableColorIndex").prop("checked")
	};
	break;
	
	case "Resize":
	return {
	    img_op :  'resize',
	    width: $("#resizeWidth").val(),
	    height: $("#resizeHeight").val(),
	    ignoreAspectRatio : $("#resizeIgnoreAspectRatio").prop("checked")
	};
	break;
	
	case "Convert":
	return {
	    img_op :  'convert',
	    img_type: $("select#convertType option:selected").val(),
	    keepMaxInfo : $("#resizeIgnoreAspectRatio").prop("checked")
	};
	break;
	
	case "Transparent":
	return {
	    img_op :  'transparent',
	    transparentColor: $("#transparentColor").val(),
	    colorFuzz: $("#colorFuzz").val()
	};
	break;
	
	case "Watermark":
	return {
	    img_op :  'watermark',
	    watermarkText: $("#watermarkText").val(),
	    opacity:  $("#watermarkOpacity").val()
	};
	break;
	
	case "Animate":
	return {
	    img_op :  'animate',
	    delay :  $("#timeDelay").val()
	};
	break;
	default:
	ret = { img_op:'compress', compress_level:'default', depth:8};
	}
    
    return ret;
}

$("#compress button").click(function(){

    // alert($.fn.fileinput);
    
    // $("form.imag-op") 
    // add compress image operation
    
});

